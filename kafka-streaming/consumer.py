from kafka import KafkaConsumer
import json


consumer = KafkaConsumer(

    "machine-telemetry",

    bootstrap_servers='localhost:9092',

    auto_offset_reset='earliest',

    value_deserializer=lambda x: json.loads(x.decode('utf-8'))

)


print("Listening for telemetry events...\n")


for message in consumer:

    telemetry = message.value

    print(telemetry)