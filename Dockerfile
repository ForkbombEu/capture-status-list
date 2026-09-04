# syntax=docker/dockerfile:1

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Non-root runtime user. The app lazily generates keys/private.pem and
# keys/public.pem at first signing, so keys/ must be writable by this user.
RUN groupadd --gid 10001 app \
    && useradd --uid 10001 --gid app --home-dir /app --no-create-home app \
    && mkdir -p /app/keys \
    && chown -R app:app /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY *.py ./
COPY .puria/design ./.puria/design

USER app

# Persist the ES256 test key across restarts; the JWT kid is static, so a
# regenerated key would invalidate cached verifier/JWKS state.
VOLUME ["/app/keys"]

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/status/1', timeout=3)"

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]