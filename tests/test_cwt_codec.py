import pytest
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
    decode_dss_signature,
    encode_dss_signature,
)

from cwt_codec import (
    STATUS_LIST_CWT_MEDIA_TYPE,
    _CborTag,
    _decode_cbor,
    _encode_cbor,
    decode_cwt,
    encode_cwt,
)


PAYLOAD = {2: "https://issuer.example/status/1", 6: 0, 65533: {"bits": 1, "lst": b"x"}}


def _key_pair() -> tuple[ec.EllipticCurvePrivateKey, str, str]:
    key = ec.generate_private_key(ec.SECP256R1())
    private_pem = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ).decode()
    public_pem = key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode()
    return key, private_pem, public_pem


def _bstr(value: bytes) -> bytes:
    length = len(value)
    if length < 24:
        return bytes([0x40 | length]) + value
    if length < 0x100:
        return bytes([0x58, length]) + value
    return bytes([0x59]) + length.to_bytes(2, "big") + value


def _rfc9052_sig_structure(protected: bytes, payload: bytes) -> bytes:
    # array(4), tstr "Signature1", bstr protected, bstr h'' (external_aad), bstr payload
    return b"\x84\x6aSignature1" + _bstr(protected) + b"\x40" + _bstr(payload)


def test_signature_verifies_as_rfc9052_cose_sign1() -> None:
    key, private_pem, _ = _key_pair()

    token = _decode_cbor(
        encode_cwt(PAYLOAD, private_pem, STATUS_LIST_CWT_MEDIA_TYPE, kid="EU-status-list")
    )

    assert token.number == 18
    protected, unprotected, payload, signature = token.value
    assert unprotected == {4: b"EU-status-list"}
    assert len(signature) == 64
    key.public_key().verify(
        encode_dss_signature(
            int.from_bytes(signature[:32], "big"), int.from_bytes(signature[32:], "big")
        ),
        _rfc9052_sig_structure(protected, payload),
        ec.ECDSA(hashes.SHA256()),
    )


def test_decode_rejects_signature_over_bare_protected_and_payload() -> None:
    key, _, public_pem = _key_pair()
    protected = _encode_cbor({1: -7, 16: STATUS_LIST_CWT_MEDIA_TYPE})
    payload = _encode_cbor(PAYLOAD)
    r, s = decode_dss_signature(key.sign(protected + payload, ec.ECDSA(hashes.SHA256())))
    token = _encode_cbor(
        _CborTag(18, [protected, {}, payload, r.to_bytes(32, "big") + s.to_bytes(32, "big")])
    )

    with pytest.raises(ValueError):
        decode_cwt(token, public_pem)
