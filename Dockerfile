# Dockerfile

FROM python:3.7-slim

WORKDIR /app

# Set the timezone
RUN echo "Asia/Kolkata" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata

# Install gcc, python3-dev, and sqlite3
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev sqlite3 && \
    rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./rpi_metrics_collector.py" ]
