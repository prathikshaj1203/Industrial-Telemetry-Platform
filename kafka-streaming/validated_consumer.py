from kafka import KafkaConsumer, KafkaProducer
import json
import psycopg2

from validator import validate_telemetry


connection = psycopg2.connect(

    host="127.0.0.1",
    database="telemetry_db",
    user="postgres",
    password="root1234"

)

cursor = connection.cursor()


consumer = KafkaConsumer(

    "machine-telemetry",

    bootstrap_servers='localhost:9092',

    auto_offset_reset='earliest',

    value_deserializer=lambda x: json.loads(x.decode('utf-8'))

)


dlq_producer = KafkaProducer(

    bootstrap_servers='localhost:9092',

    value_serializer=lambda v: json.dumps(v).encode('utf-8')

)


print("Validated consumer started...\n")


for message in consumer:

    telemetry = message.value

    is_valid, reason = validate_telemetry(telemetry)

    if is_valid:

        cursor.execute("""

        INSERT INTO machine_telemetry (

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

        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)

        """, (

            telemetry["machine_id"],
            telemetry["machine_type"],
            telemetry["state"],
            telemetry["temperature"],
            telemetry["vibration"],
            telemetry["pressure"],
            telemetry["rpm"],
            telemetry["power_usage"],
            telemetry["timestamp"]

        ))

        connection.commit()

        print(f"VALID telemetry stored: {telemetry}")

    else:

        dlq_event = {

            "error": reason,
            "bad_event": telemetry

        }

        dlq_producer.send(

            "machine-telemetry-dlq",
            dlq_event

        )

        print(f"INVALID telemetry sent to DLQ: {reason}")