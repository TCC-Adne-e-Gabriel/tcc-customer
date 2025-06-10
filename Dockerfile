FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN addgroup --gid 1001 --system app && \
    adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group app

USER app

WORKDIR /app/

ENV PYTHONPATH=/app

COPY app/ ./app/
COPY scripts/ ./scripts/
COPY .env .env

CMD ["fastapi", "run", "--workers", "4", "app/main.py"]