FROM python:3.10-alpine AS builder

WORKDIR /app

RUN apk add --no-cache gcc musl-dev postgresql-dev libpq

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.10-alpine

WORKDIR /app

COPY --from=builder /root/.cache /root/.cache

COPY . .

CMD ["gunicorn", "task_manager.wsgi:application", "--bind", "0.0.0.0:10000"]