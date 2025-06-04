FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

WORKDIR /app/

ENV PYTHONPATH=/app

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["fastapi", "run", "--workers", "4", "app/main.py"]