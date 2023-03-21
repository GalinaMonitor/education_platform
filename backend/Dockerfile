FROM python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN apt-get update \
    && apt-get install --no-install-recommends -y curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /backend
COPY ./requirements.txt ./
RUN pip install -r ./requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--reload", "--port", "8000", "--host", "0.0.0.0"]
