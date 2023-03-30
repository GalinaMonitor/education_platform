# BASE
FROM python:3.11-slim as python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


# BUILDER
FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y curl git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=1.3.0
RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION

# Install main dependencies
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./

RUN poetry install --only main

# PRODUCTION
FROM python-base as production

# Copying venv into image
COPY --from=builder-base $VENV_PATH $VENV_PATH
WORKDIR /backend
COPY . .

CMD ["uvicorn", "main:app", "--reload", "--port", "8000", "--host", "0.0.0.0"]
