# Mock EUDI Token Status List

Minimal local Token Status List (TSL) server for EUDI Wallet Functional
Conformance Assessment experiments.

The standards-critical endpoint is `GET /status/1`. It returns a signed JWT
Status List Token with a `status_list` claim containing `bits` and `lst`, where
`lst` is the zlib-compressed status byte array encoded as base64url without
padding.

The issuer, credential registry, debug endpoint, reset endpoint, and verifier
endpoint are simplified test infrastructure. They are not EUDI issuance,
presentation, trust-list, PKI, authentication, authorization, or wallet
protocol implementations.

Passing the included tests does not constitute EUDI certification or formal
conformance. Formal conformance requires testing against the applicable EUDI
requirements, versions, profiles, and official test specifications.

## Standards

Implemented status-list format:

- IETF Token Status List, `draft-ietf-oauth-status-list-21`:
  https://datatracker.ietf.org/doc/draft-ietf-oauth-status-list/
- Commission Implementing Regulation (EU) 2024/2977, as amended by Commission
  Implementing Regulation (EU) 2026/1731, for the EUDI use case expectation that
  Token Status Lists are used for wallet instance attestation and key
  attestation revocation:
  https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32026R1731
- JSON Web Token (JWT), RFC 7519:
  https://www.rfc-editor.org/rfc/rfc7519
- JSON Web Signature (JWS), RFC 7515:
  https://www.rfc-editor.org/rfc/rfc7515

This mock uses `bits = 1`:

- `0x00`: `VALID`
- `0x01`: `REVOKED`, corresponding to the TSL `INVALID` status value

The status list contains 10,000 entries by default. All entries start as
`VALID`.

## Run

```sh
pip install -r requirements.txt
uvicorn app:app --reload
```

The app generates a local ES256 test signing key on first use:

```text
keys/private.pem
keys/public.pem
```

These files are local test material and are ignored by git.

## Test

```sh
pytest
```

Repository policy validation is available through mise:

```sh
mise run lint
mise run test
mise run pytest
mise run build
```

## Architecture

```text
Test Issuer
|
| credential + status reference
v
Test Wallet
|
| credential presentation
v
Test Verifier
|
| GET Status List
v
Mock Status List Server
```

## Status Flow

```text
ISSUED
|
v
VALID
|
| revoke
v
REVOKED
```

## Status-List Flow

```text
Credential
|
| idx = 42
v
Status List Token
|
| decode index 42
v
status = REVOKED
```

## API

Create a test credential:

```sh
curl -X POST http://localhost:8000/credentials \
  -H 'content-type: application/json' \
  -d '{"credential_id":"cred-001"}'
```

Response:

```json
{
  "credential_id": "cred-001",
  "idx": 42,
  "status_list_uri": "http://localhost:8000/status/1",
  "referenced_token_status": {
    "status_list": {
      "idx": 42,
      "uri": "http://localhost:8000/status/1"
    }
  }
}
```

Retrieve the real standards-based Status List Token:

```sh
curl -H 'accept: application/statuslist+jwt' http://localhost:8000/status/1
```

Revoke a credential:

```sh
curl -X POST http://localhost:8000/credentials/cred-001/revoke
```

Verify a credential through the test verifier:

```sh
curl -X POST http://localhost:8000/verify/cred-001
```

Read a raw status value through the debug-only endpoint:

```sh
curl http://localhost:8000/debug/status/42
```

Reset all in-memory test state:

```sh
curl -X POST http://localhost:8000/reset
```

## Privacy Notes

The status-list token only carries indexed status values. It does not include
names, email addresses, dates of birth, credential holder IDs, or credential
IDs.

This mock does not by itself prove unlinkability. Unlinkability requires
analysis of the complete protocol and deployment architecture, including index
assignment, list partitioning, issuer behavior, verifier behavior, network
observability, and operational policy.
