"""Country-aware signing key and certificate configuration.

The module only describes and reads signing material supplied by the operator.  It
never generates, copies, or otherwise modifies key files.  A country-specific
pair takes precedence over the legacy ``private.pem``/``certificate.der`` pair
in the configured key directory.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path


_DEFAULT_KEY_DIR = "keys"
_COUNTRY_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*\Z")
_REFERENCE_FILENAMES = {
    "FC": ("PID-DS-0001_UT.pem", "PID-DS-0001_UT_cert.der"),
    "PT": ("PID-DS-0001_PT.pem", "PID-DS-0001_PT_cert.der"),
    "EE": ("PID-DS-0001_EE.pem", "PID-DS-0001_EE_cert.der"),
    "CZ": ("PID-DS-0001_CZ.pem", "PID-DS-0001_CZ_cert.der"),
    "NL": ("PID-DS-0001_NL.pem", "PID-DS-0001_NL_cert.der"),
    "LU": ("PID-DS-0001_LU.pem", "PID-DS-0001_LU_cert.der"),
    "EU": ("PID-DS-0001_EU.pem", "PID-DS-0001_EU_cert.der"),
    "AV": ("AgeVerificationDS-001.pem", "AgeVerificationDS-001_cert.der"),
    "AV2": ("AgeVerificationDS-001.pem", "AgeVerificationDS-001_cert.der"),
}


def _validate_country(country: str) -> str:
    """Validate a country identifier before using it in a filesystem path."""

    if not isinstance(country, str):
        raise TypeError("country must be a string")
    if not country or not _COUNTRY_RE.fullmatch(country):
        raise ValueError("country must be a safe path component")
    return country


def country_kid(country: str) -> str:
    """Return the stable key identifier used for a country's status lists."""

    return f"{_validate_country(country)}-status-list"


# Descriptive aliases keep the country-to-kid operation discoverable to callers.
kid_for_country = country_kid
country_to_kid = country_kid


def _key_dir() -> Path:
    configured = os.environ.get("EUDI_KEY_DIR")
    return Path(configured or _DEFAULT_KEY_DIR).expanduser()


def _existing_or_primary(primary: Path, legacy: Path) -> Path:
    if primary.is_file():
        return primary
    if legacy.is_file():
        return legacy
    # Retain the country-specific path in the configuration when no material
    # exists yet; loading it then gives the caller the normal FileNotFoundError.
    return primary


@dataclass(frozen=True)
class CountryKeyMaterial:
    """Filesystem-backed signing material for one country.

    ``private_key_path`` points to a PEM encoded private key.  The certificate
    path is optional because JWT signing does not require a certificate, while
    CWT/COSE callers may use the DER bytes when one is configured.
    """

    country: str
    private_key_path: Path
    certificate_path: Path | None
    kid: str

    def __post_init__(self) -> None:
        _validate_country(self.country)

    def load_private_pem(self) -> str:
        """Read and return the private key PEM text without changing the file."""

        return Path(self.private_key_path).read_text(encoding="ascii")

    def load_certificate_der(self) -> bytes | None:
        """Read the optional DER certificate, returning ``None`` when absent."""

        if self.certificate_path is None:
            return None
        return Path(self.certificate_path).read_bytes()

    @property
    def private_pem(self) -> str:
        """Convenience access to :meth:`load_private_pem`."""
        return self.load_private_pem()

    @property
    def certificate_der(self) -> bytes | None:
        """Convenience access to :meth:`load_certificate_der`."""
        return self.load_certificate_der()


def material_for(country: str) -> CountryKeyMaterial:
    """Resolve operator-supplied country signing material from ``EUDI_KEY_DIR``.

    Supports both the local ``<country>.key.pem`` convention and the filename
    layout used by the European reference service. Missing certificates remain
    valid for local JWT/CWT debugging; no key files are generated or copied.
    """
    country = _validate_country(country)
    key_dir = _key_dir()
    reference_key, reference_cert = _REFERENCE_FILENAMES.get(country, (None, None))
    key_candidates = [
        key_dir / f"{country}.key.pem",
        key_dir / reference_key if reference_key else key_dir / "__missing__",
        key_dir / "private.pem",
    ]
    private_path = next(
        (path for path in key_candidates if path.is_file()), key_candidates[0]
    )
    certificate_candidates = [
        key_dir / f"{country}.cert.der",
        key_dir / reference_cert if reference_cert else key_dir / "__missing__",
        key_dir / "certificate.der",
    ]
    certificate_path = next(
        (path for path in certificate_candidates if path.is_file()), None
    )
    return CountryKeyMaterial(
        country=country,
        private_key_path=private_path,
        certificate_path=certificate_path,
        kid=country_kid(country),
    )


__all__ = [
    "CountryKeyMaterial",
    "country_kid",
    "country_to_kid",
    "kid_for_country",
    "material_for",
]
