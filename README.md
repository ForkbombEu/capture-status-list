# Mock EUDI Token Status List

Minimal local Token Status List (TSL) server for EUDI Wallet Functional
Conformance Assessment experiments.

The standards-critical legacy endpoint is `GET /status/1`. The EU-compatible
registry API is `POST /token_status_list/take`: it allocates paired lists for
each country × doctype and returns UUID-based `token_status_list` and
`identifier_list` URIs. Both resources negotiate JWT and CBOR/COSE CWT.

Status-list bytes use the `status_list` claim containing `bits` and `lst`,
where `lst` is the zlib-compressed status byte array encoded as base64url
without padding in JWT form (raw compressed bytes in CWT form).

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
mise run serve
```

`serve` depends on `setup`, which creates `.venv/` with `uv` and installs
`requirements.txt` into it. Every Python task (`serve`, `pytest`, `seed`) runs
from that virtualenv, so nothing is installed into the global interpreter.
Without mise:

```sh
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn app:app --reload
```

Open the console at `http://localhost:8000/` and the branded API documentation
at `http://localhost:8000/docs`.

Seed demo UI data after the server is running:

```sh
mise run seed
```

The default seed creates a mixed debugger fixture: multiple countries and
doctypes, active and expired pools, revoked and non-revoked credentials, and a
mix of verified and not-yet-verified rows. Use `mise run seed -- --simple` for
the original single-pool fixture.
The app reads operator-supplied country signing material without generating or
copying secrets. Set `EUDI_KEY_DIR` to the mounted key directory; it accepts
`<country>.key.pem` / `<country>.cert.der`, the European reference filenames
(`PID-DS-0001_<country>.pem` and matching `_cert.der`, plus the AV filenames),
or the local fallback `private.pem` / `certificate.der`. The certificate is
emitted in JWT `x5c` and CWT COSE header label 33, and the verifier resolves
the signing key from `x5c`, so operator material needs no JWKS registration.

Without `EUDI_KEY_DIR`, local test mode generates a test key and a matching
self-signed certificate on first use:

```text
keys/private.pem
keys/certificate.der
```

The self-signed certificate makes every country list self-describing (`x5c`),
so the console verifier works out of the box. These files are local test
material and are ignored by git.

## Deploy (Docker)

```sh
mise run docker:build
mise run docker:run
```

`docker:run` serves the app on `http://localhost:8000` and mounts a named
volume for `keys/`, so the generated ES256 test key survives container
restarts. Run without the volume for ephemeral local testing:

```sh
docker run --rm -p 8000:8000 capture-status-list
```

When the service is behind a TLS-terminating reverse proxy, set
`STATUS_LIST_PUBLIC_URL` to its public origin. The value is used in returned
status-list references and signed token claims, so it must be the externally
reachable HTTPS URL without a path:

```sh
docker run --rm -p 8000:8000 \
  -e STATUS_LIST_PUBLIC_URL=https://status.example.com \
  capture-status-list
```

`mise` is a host development tool and is intentionally not installed in the
minimal Python runtime image. When seeding from the host while the container
is running, use:

```sh
mise run seed -- --base-url http://localhost:8000
```

When running the command inside the container shell, use Python directly:

```sh
python /app/seed.py --base-url http://127.0.0.1:8000
```

The command seeds the rich multi-country fixture. Add `--simple` for the
legacy single-pool fixture.

## Design

The user interface follows the Credimi Extras brand. `.puria/design/DESIGN.md`
is the design source; `brand/` holds the runtime copies of the canonical
assets, installed unchanged from the `credimi-extras-template` repository:

```text
brand/style.css                            brand stylesheet, loaded first
brand/fonts/InterVariable.ttf              brand sans      (SIL OFL 1.1)
brand/fonts/SourceCodeProVariable.ttf      brand monospace (SIL OFL 1.1)
brand/logos/credimi_logo.svg               mark, dark — also /favicon.svg
brand/logos/credimi_logo_negative.svg      mark, negative
brand/logos/credimi_logo-transp.svg        wordmark, dark
brand/logos/credimi_logo-transp_white.svg  wordmark, white
```

The whole directory is served at `/brand`, so `fonts/` stays a sibling of
`style.css` and the self-hosted `@font-face` rules resolve. No fonts are
fetched from a third party. The application stylesheet lives in `ui.py` and
loads after `brand/style.css`; it declares only what the brand foundation does
not provide. The four logos are frozen: `tests/test_brand.py` checks the
runtime copies against the SHA-256 digests pinned in `.puria/design/DESIGN.md`
§1.

Every HTML page, the API documentation included, carries the same chrome: the
Credimi Extras top strip, the topbar wordmark, the deep-indigo footer with the
ForkBomb sub-bar, and the Credimi Extras bottom strip.

## Test

```sh
mise run pytest
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
POST /token_status_list/take
|
| country × doctype + expiry_date
v
Paired UUID list references
|
| Accept: JWT or CWT/CBOR
v
Status value: VALID or REVOKED
```

## API

EU-compatible paired-list API:

```sh
curl -X POST http://localhost:8000/token_status_list/take \
  -H 'X-Api-Key: test' \
  --data-urlencode country=EU \
  --data-urlencode doctype=org.iso.18013.5.1.mDL \
  --data-urlencode expiry_date=2099-12-31
```

The response contains one `status_list` reference and one paired
`identifier_list` reference. Fetch either URI with `Accept:
application/statuslist+jwt` or `application/statuslist+cwt` (and the matching
`identifierlist` media types). Revoke through the reference-compatible API:

```sh
curl -X POST http://localhost:8000/token_status_list/set \
  -H 'X-Api-Key: test' \
  --data-urlencode uri='<status-list-uri>' \
  --data-urlencode idx=123 \
  --data-urlencode status=1
```

`GET /token_status_list/get` and `GET /identifier_list/get` expose raw indexed
values for debugging. `GET /debug/status-lists` lists all allocated pools for
the console.

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

Decode the current Status List Token — header, payload, the inflated `lst`
and the signing JWKS — through the debug-only endpoint the console uses. The
`lst` field carries the compressed and inflated byte counts plus a readable
window of the inflated entries, one hex digit per entry (`0` valid, `1`
revoked at `bits = 1`):

```sh
curl http://localhost:8000/debug/status-list
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
