from kafka import KafkaConsumer
import json
import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()
connection = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

cursor = connection.cursor()


cursor.execute("""

CREATE TABLE IF NOT EXISTS machine_telemetry (

    id SERIAL PRIMARY KEY,

    machine_id VARCHAR(50),
    machine_type VARCHAR(100),
    machine_category VARCHAR(50),
    state VARCHAR(50),

    temperature FLOAT,
    vibration FLOAT,
    pressure FLOAT,

    rpm INT,
    power_usage INT,

    timestamp TIMESTAMP

)

""")

# Add machine_category column if it doesn't exist
try:
    cursor.execute("ALTER TABLE machine_telemetry ADD COLUMN IF NOT EXISTS machine_category VARCHAR(50)")
    connection.commit()
except Exception as e:
    print(f"Column might already exist: {e}")

connection.commit()


consumer = KafkaConsumer(

    "machine-telemetry",

    bootstrap_servers='localhost:9092',

    auto_offset_reset='earliest',

    value_deserializer=lambda x: json.loads(x.decode('utf-8'))

)


print("Storing telemetry into PostgreSQL...\n")


for message in consumer:

    telemetry = message.value

    cursor.execute("""

    INSERT INTO machine_telemetry (

        machine_id,
        machine_type,
        machine_category,
        state,
        temperature,
        vibration,
        pressure,
        rpm,
        power_usage,
        timestamp

    )

    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

    """, (

        telemetry["machine_id"],
        telemetry["machine_type"],
        telemetry.get("machine_category", None),
        telemetry["state"],
        telemetry["temperature"],
        telemetry["vibration"],
        telemetry["pressure"],
        telemetry["rpm"],
        telemetry["power_usage"],
        telemetry["timestamp"]

    ))

    connection.commit()

    print(f"Stored: {telemetry}")