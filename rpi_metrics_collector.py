# rpi_metrics_collector.py

import os
import sqlite3
import psutil
import socket
from time import sleep

# Create a new SQLite database (or connect to an existing one)
# in the rpi_metrics directory
db_path = '/rpi_metrics/metrics.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Create a table for your metrics
c.execute('''
    CREATE TABLE IF NOT EXISTS rpi_metrics (
        timestamp TEXT,
        hostname TEXT,
        cpu_usage REAL,
        memory_usage REAL,
        temperature REAL
    )
''')

while True:
    # Collect metrics
    timestamp = datetime.datetime.now()
    hostname = socket.gethostname()
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent

    # Read temperature from sysfs
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
        temp_milli = int(f.read())
    temperature = temp_milli / 1000.0

    # Store metrics in the database
    c.execute('''
        INSERT INTO rpi_metrics VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, hostname, cpu_usage, memory_usage, temperature))

    # Commit the changes and sleep for a while before collecting the next set of metrics
    conn.commit()
    sleep(60)
