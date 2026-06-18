# Pinned image for this legacy stack (Python 3.8 EOL, Werkzeug <=2.0.3).
# A Dockerfile fully decouples the build from nixpacks' moving defaults, which
# break this app whenever Railway bumps its builder.
FROM python:3.8.20-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN pip install pipenv

WORKDIR /app

# Copy lockfiles first so dependency layers cache across code changes.
# --deploy refuses to build if Pipfile.lock is out of sync with the Pipfile.
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --system

COPY . .

# Railway injects $PORT at runtime; fall back to 8000 to match prior behavior.
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT:-8000}"]
