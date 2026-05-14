from kafka import KafkaProducer
import json
import time
import sys
import os
from dotenv import load_dotenv
import os
load_dotenv()

sys.path.append(os.path.abspath("../telemetry-simulator"))

from machine import Machine

MACHINES = [

    {
    "machine_id": "WLD_102",
    "machine_type": "Robotic Welding Arm",
    "machine_category": "Welding",
    "temp_range": (65, 105),
    "vibration_range": (0.2, 0.9),
    "pressure_range": (35, 60),
    "rpm_range": (1000, 1600),
    "power_range": (450, 750)
},

{
    "machine_id": "CNC_304",
    "machine_type": "CNC Machining Unit",
    "machine_category": "CNC",
    "temp_range": (55, 95),
    "vibration_range": (0.3, 1.1),
    "pressure_range": (25, 45),
    "rpm_range": (1400, 2600),
    "power_range": (350, 750)
},

{
    "machine_id": "CNV_203",
    "machine_type": "Conveyor Belt System",
    "machine_category": "Conveyor",
    "temp_range": (30, 75),
    "vibration_range": (0.1, 0.6),
    "pressure_range": (10, 25),
    "rpm_range": (700, 1300),
    "power_range": (200, 500)
},

{
    "machine_id": "RBT_701",
    "machine_type": "Industrial Robotic Arm",
    "machine_category": "Robotics",
    "temp_range": (50, 90),
    "vibration_range": (0.2, 1.0),
    "pressure_range": (15, 30),
    "rpm_range": (1200, 3000),
    "power_range": (400, 800)
},

{
    "machine_id": "PRS_601",
    "machine_type": "Industrial Press Machine",
    "machine_category": "PressMachine",
    "temp_range": (60, 110),
    "vibration_range": (0.2, 1.2),
    "pressure_range": (80, 200),
    "rpm_range": (200, 800),
    "power_range": (500, 1000)
},

{
    "machine_id": "ASM_801",
    "machine_type": "Assembly Line Station",
    "machine_category": "Assembly",
    "temp_range": (35, 70),
    "vibration_range": (0.1, 0.6),
    "pressure_range": (10, 30),
    "rpm_range": (300, 1000),
    "power_range": (200, 600)
},

{
    "machine_id": "PKG_901",
    "machine_type": "Packaging Conveyor",
    "machine_category": "Packaging",
    "temp_range": (30, 65),
    "vibration_range": (0.1, 0.5),
    "pressure_range": (5, 20),
    "rpm_range": (200, 700),
    "power_range": (150, 400)
}

]

producer = KafkaProducer(

    bootstrap_servers='localhost:9092',

    value_serializer=lambda v: json.dumps(v).encode('utf-8')

)
machines =[]

for config in MACHINES:

    machine = Machine(

        config["machine_id"],

        config["machine_type"],

        config["machine_category"],

        config["temp_range"],

        config["vibration_range"],

        config["pressure_range"],

        config["rpm_range"],

        config["power_range"]

    )

    machines.append(machine)


while True:

    for machine in machines:

        telemetry = machine.generate_telemetry()

        producer.send(
            "machine-telemetry",
            telemetry
        )

        print(f"Sent: {telemetry}")

    time.sleep(3)