# Dockerfile

FROM python:3.7-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Add the sysfs path as a volume
VOLUME /sys/class/thermal/thermal_zone0/temp

# Add the rpi_metrics directory as a volume
VOLUME /rpi_metrics

CMD [ "python", "./rpi_metrics_collector.py" ]
