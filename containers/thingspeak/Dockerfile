FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ../src ./src
COPY ../.env .env

ENV PYTHONPATH=/app

CMD ["python", "src/ingestion/mqtt_broker/thingspeak/data_ingestion.py"]

EXPOSE 1883


