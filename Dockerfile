FROM python:3.13-alpine AS builder

RUN apk add --no-cache \
    python3-dev \
    postgresql-dev \
    gcc \
    musl-dev

COPY requirements.txt .

RUN pip3 --no-cache-dir install -r requirements.txt


FROM python:3.13-alpine AS final

RUN apk add --no-cache libpq

WORKDIR /inventra-api

ENV FLASK_ENV=production

COPY --from=builder /usr/local/lib/python3.13 /usr/local/lib/python3.13
COPY --from=builder /usr/local/bin /usr/local/bin


COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini .

CMD ["python", "src/app.py"]