FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

COPY src ./src

CMD ["python", "src/ingestion/mqtt_bridge/thingspeak/data_ingestion.py"]
