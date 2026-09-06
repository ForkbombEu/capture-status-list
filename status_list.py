from __future__ import annotations

import base64
import hashlib
import hmac
import math
import time
import zlib
from typing import Iterable

import jwt


DEFAULT_BITS = 1
DEFAULT_STATUS_LIST_SIZE = 10_000
STATUS_VALID = 0x00
STATUS_INVALID = 0x01


TOKEN_TTL_SECONDS = 43_200
ALLOWED_BITS = {1, 2, 4, 8}


class IndexScatter:
    """Keyed format-preserving permutation over ``[0, size)``.

    Credentials are allocated in issuance order (a monotonic cursor) but the
    index they publish is ``permute(cursor)``: observers correlating issuance
    time and order learn nothing about index proximity, and revoking one index
    reveals nothing about its neighbours. Mirrors the Feistel scatter used by
    the German national wallet backend, sized for arbitrary domains via
    cycle-walking (they require >= 2**20 via FPE; we do not).
    """

    ROUNDS = 4

    def __init__(self, size: int, seed: bytes) -> None:
        if size < 1:
            raise ValueError(f"size must be positive: {size}")
        self.size = size
        self.seed = seed
        self._bits = max((size - 1).bit_length(), 1)
        self._left = self._bits // 2
        self._right = self._bits - self._left

    def permute(self, cursor: int) -> int:
        if not 0 <= cursor < self.size:
            raise InvalidStatusListIndex(cursor, self.size)
        value = self._feistel(cursor)
        while value >= self.size:
            value = self._feistel(value)
        return value

    def _feistel(self, value: int) -> int:
        # Alternating unbalanced Feistel. Each round swaps the half widths, so
        # an even round count restores the original split; every round is
        # invertible because the round function reads only the new left half.
        left_width = self._left
        right_width = self._right
        left = (value >> right_width) & ((1 << left_width) - 1)
        right = value & ((1 << right_width) - 1)
        for rnd in range(self.ROUNDS):
            f = self._round(rnd, right) & ((1 << left_width) - 1)
            left, right = right, left ^ f
            left_width, right_width = right_width, left_width
        return (left << right_width) | right

    def _round(self, rnd: int, value: int) -> int:
        message = rnd.to_bytes(1, "big") + value.to_bytes(8, "big")
        digest = hmac.new(self.seed, message, hashlib.sha256).digest()
        return int.from_bytes(digest[:8], "big")


class InvalidStatusListIndex(ValueError):
    def __init__(self, idx: int, size: int) -> None:
        super().__init__(f"status-list index {idx} is outside 0..{size - 1}")
        self.idx = idx
        self.size = size


def status_label(value: int) -> str:
    if value == STATUS_VALID:
        return "VALID"
    if value == STATUS_INVALID:
        return "REVOKED"
    return f"UNKNOWN({value})"


def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def base64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode((value + padding).encode("ascii"))


def pack_status_values(values: Iterable[int], bits: int = DEFAULT_BITS) -> bytes:
    _validate_bits(bits)
    statuses = list(values)
    max_value = (1 << bits) - 1
    byte_count = math.ceil(len(statuses) * bits / 8)
    packed = bytearray(byte_count)

    for idx, value in enumerate(statuses):
        if value < 0 or value > max_value:
            raise ValueError(f"status value {value} exceeds {bits}-bit capacity")
        bit_offset = (idx * bits) % 8
        byte_offset = (idx * bits) // 8
        packed[byte_offset] |= value << bit_offset

    return bytes(packed)


def read_packed_status(packed: bytes, idx: int, bits: int = DEFAULT_BITS) -> int:
    _validate_bits(bits)
    size = len(packed) * 8 // bits
    if idx < 0 or idx >= size:
        raise InvalidStatusListIndex(idx, size)

    bit_offset = (idx * bits) % 8
    byte_offset = (idx * bits) // 8
    mask = (1 << bits) - 1
    return (packed[byte_offset] >> bit_offset) & mask


def unpack_status_values(
    packed: bytes,
    bits: int = DEFAULT_BITS,
    size: int | None = None,
) -> list[int]:
    _validate_bits(bits)
    capacity = len(packed) * 8 // bits
    result_size = capacity if size is None else size
    if result_size < 0 or result_size > capacity:
        raise InvalidStatusListIndex(result_size, capacity + 1)
    return [read_packed_status(packed, idx, bits) for idx in range(result_size)]


def encode_status_list(values: Iterable[int], bits: int = DEFAULT_BITS) -> str:
    packed = pack_status_values(values, bits)
    compressed = zlib.compress(packed, level=9)
    return base64url_encode(compressed)


def decode_status_list(
    encoded: str,
    bits: int = DEFAULT_BITS,
    size: int | None = None,
) -> list[int]:
    packed = zlib.decompress(base64url_decode(encoded))
    return unpack_status_values(packed, bits=bits, size=size)


def read_encoded_status(encoded: str, idx: int, bits: int = DEFAULT_BITS) -> int:
    packed = zlib.decompress(base64url_decode(encoded))
    return read_packed_status(packed, idx, bits=bits)


def generate_status_list(
    values: Iterable[int],
    bits: int = DEFAULT_BITS,
    aggregation_uri: str | None = None,
) -> dict[str, int | str]:
    status_list: dict[str, int | str] = {
        "bits": bits,
        "lst": encode_status_list(values, bits=bits),
    }
    if aggregation_uri is not None:
        status_list["aggregation_uri"] = aggregation_uri
    return status_list


def generate_status_list_token(
    values: Iterable[int],
    *,
    private_key_pem: str,
    issuer: str,
    subject: str,
    kid: str,
    bits: int = DEFAULT_BITS,
    ttl: int = TOKEN_TTL_SECONDS,
) -> str:
    now = int(time.time())
    payload = {
        "iss": issuer,
        "sub": subject,
        "iat": now,
        "exp": now + ttl,
        "ttl": ttl,
        "status_list": generate_status_list(values, bits=bits),
    }
    headers = {
        "alg": "ES256",
        "kid": kid,
        "typ": "statuslist+jwt",
    }
    return jwt.encode(payload, private_key_pem, algorithm="ES256", headers=headers)


def _validate_bits(bits: int) -> None:
    if bits not in ALLOWED_BITS:
        allowed = ", ".join(str(value) for value in sorted(ALLOWED_BITS))
        raise ValueError(f"bits must be one of {allowed}: {bits}")
