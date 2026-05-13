from kafka import KafkaConsumer
import json
from dotenv import load_dotenv
import os
load_dotenv()
consumer = KafkaConsumer(

    "machine-telemetry-dlq",

    bootstrap_servers='localhost:9092',

    auto_offset_reset='earliest',

    value_deserializer=lambda x: json.loads(x.decode('utf-8'))

)


print("Listening to DLQ...\n")


for message in consumer:

    print("DLQ EVENT:")
    print(message.value)
    print("-" * 50)