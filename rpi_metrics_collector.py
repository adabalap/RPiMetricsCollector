import os
import mysql.connector
import psutil
from time import sleep
import datetime

# Get environment variables
db_host = os.getenv('DB_HOST', 'localhost')
db_user = os.getenv('DB_USER', 'root')
db_password = os.getenv('DB_PASSWORD', '')
db_name = os.getenv('DB_NAME', 'rpi_metrics')

# Create a new MariaDB connection
conn = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)
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
    hostname = os.getenv('HOSTNAME', 'unknown')
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent

    # Read temperature from sysfs
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
        temp_milli = int(f.read())
    temperature = temp_milli / 1000.0

    # Store metrics in the database
    c.execute('''
        INSERT INTO rpi_metrics VALUES (%s, %s, %s, %s, %s)
    ''', (timestamp, hostname, cpu_usage, memory_usage, temperature))

    # Commit the changes and sleep for a while before collecting the next set of metrics
    conn.commit()
    sleep(300)
