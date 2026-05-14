from kafka import KafkaConsumer, KafkaProducer
import json
import psycopg2
import os
from dotenv import load_dotenv
import os
load_dotenv()
print(os.getenv("DB_PASSWORD"))
# -------------------------------
# PostgreSQL Connection
# -------------------------------
connection = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

cursor = connection.cursor()

# -------------------------------
# Create Table if Not Exists
# -------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS telemetry_data (

    id SERIAL PRIMARY KEY,

    machine_id VARCHAR(50),

    machine_type VARCHAR(100),

    state VARCHAR(20),

    temperature FLOAT,

    vibration FLOAT,

    pressure FLOAT,

    rpm INT,

    power_usage FLOAT,

    timestamp TIMESTAMP

)
""")

connection.commit()

# -------------------------------
# Kafka Consumer
# -------------------------------

consumer = KafkaConsumer(

    "machine-telemetry",

    bootstrap_servers='127.0.0.1:9092',

    auto_offset_reset='earliest',

    value_deserializer=lambda x: json.loads(x.decode('utf-8'))

)

# -------------------------------
# DLQ Producer
# -------------------------------

dlq_producer = KafkaProducer(

    bootstrap_servers='localhost:9092',

    value_serializer=lambda x: json.dumps(x).encode('utf-8')

)

# -------------------------------
# Data Lake Path
# -------------------------------

RAW_DATA_PATH = "../data-lake/raw"

os.makedirs(RAW_DATA_PATH, exist_ok=True)

# -------------------------------
# Validation Function
# -------------------------------

VALID_STATES = ["NORMAL", "WARNING", "CRITICAL"]

def validate_telemetry(data):

    if data["state"] not in VALID_STATES:
        return False, "Invalid machine state"

    if data["temperature"] < 0 or data["temperature"] > 150:
        return False, "Invalid temperature value"

    if data["vibration"] < 0:
        return False, "Invalid vibration value"

    return True, "Valid telemetry"

# -------------------------------
# Consumer Loop
# -------------------------------

print("Listening for telemetry events...\n")

for message in consumer:

    data = message.value

    is_valid, reason = validate_telemetry(data)

    # ---------------------------
    # VALID TELEMETRY
    # ---------------------------

    if is_valid:

        cursor.execute("""

        INSERT INTO telemetry_data (

            machine_id,
            machine_type,
            state,
            temperature,
            vibration,
            pressure,
            rpm,
            power_usage,
            timestamp

        )

        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)

        """, (

            data["machine_id"],
            data["machine_type"],
            data["state"],
            data["temperature"],
            data["vibration"],
            data["pressure"],
            data["rpm"],
            data["power_usage"],
            data["timestamp"]

        ))

        connection.commit()

        # -----------------------
        # Save to Data Lake
        # -----------------------

        file_path = f"{RAW_DATA_PATH}/telemetry_log.json"

        with open(file_path, "a") as file:

            file.write(json.dumps(data) + "\n")

        print(f"VALID telemetry stored: {data}")

    # ---------------------------
    # INVALID TELEMETRY
    # ---------------------------

    else:

        dlq_data = {

            "error": reason,

            "bad_event": data

        }

        dlq_producer.send(
            "machine-telemetry-dlq",
            value=dlq_data
        )

        print(f"INVALID telemetry sent to DLQ: {reason}")