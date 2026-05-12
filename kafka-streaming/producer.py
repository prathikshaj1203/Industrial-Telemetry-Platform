from kafka import KafkaProducer
import json
import time
import sys
import os

sys.path.append(os.path.abspath("../telemetry-simulator"))

from machine import Machine


producer = KafkaProducer(

    bootstrap_servers='localhost:9092',

    value_serializer=lambda v: json.dumps(v).encode('utf-8')

)


machines = [

    Machine("WLD_101", "Robotic Welding Arm"),
    Machine("CNV_202", "Conveyor Belt System"),
    Machine("CNC_303", "CNC Machining Unit"),
    Machine("HYD_404", "Hydraulic Press"),
    Machine("PNT_505", "Paint Booth Ventilation")

]


while True:

    for machine in machines:

        telemetry = machine.generate_telemetry()

        producer.send(
            "machine-telemetry",
            telemetry
        )

        print(f"Sent: {telemetry}")

    time.sleep(3)