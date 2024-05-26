# Dockerfile

FROM python:3.7-slim

WORKDIR /app

# Install gcc and python3-dev
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Add the rpi_metrics directory as a volume
VOLUME /rpi_metrics

CMD [ "python", "./rpi_metrics_collector.py" ]
