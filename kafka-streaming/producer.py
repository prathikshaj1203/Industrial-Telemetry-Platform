from kafka import KafkaProducer
import json
import time
import sys
import os
from dotenv import load_dotenv

load_dotenv()

sys.path.append(
    os.path.abspath("../telemetry-simulator")
)

from machine import Machine

# ==========================================
# MACHINE CONFIGURATIONS
# ==========================================
machine_templates = [

    {
        "prefix": "WLD",
        "count": 3,
        "machine_type": "Robotic Welding Arm",
        "machine_category": "Welding",
        "temp_range": (65, 105),
        "vibration_range": (0.2, 0.9),
        "pressure_range": (35, 60),
        "rpm_range": (1000, 1600),
        "power_range": (450, 750)
    },

    {
        "prefix": "CNC",
        "count": 3,
        "machine_type": "CNC Machining Unit",
        "machine_category": "CNC",
        "temp_range": (55, 95),
        "vibration_range": (0.3, 1.1),
        "pressure_range": (25, 45),
        "rpm_range": (1400, 2600),
        "power_range": (350, 750)
    },

    {
        "prefix": "CNV",
        "count": 3,
        "machine_type": "Conveyor Belt System",
        "machine_category": "Conveyor",
        "temp_range": (30, 75),
        "vibration_range": (0.1, 0.6),
        "pressure_range": (10, 25),
        "rpm_range": (700, 1300),
        "power_range": (200, 500)
    },

    {
        "prefix": "RBT",
        "count": 3,
        "machine_type": "Industrial Robotic Arm",
        "machine_category": "Robotics",
        "temp_range": (50, 90),
        "vibration_range": (0.2, 1.0),
        "pressure_range": (15, 30),
        "rpm_range": (1200, 3000),
        "power_range": (400, 800)
    },

    {
        "prefix": "PRS",
        "count": 2,
        "machine_type": "Industrial Press Machine",
        "machine_category": "PressMachine",
        "temp_range": (60, 110),
        "vibration_range": (0.2, 1.2),
        "pressure_range": (80, 200),
        "rpm_range": (200, 800),
        "power_range": (500, 1000)
    },

    {
        "prefix": "ASM",
        "count": 2,
        "machine_type": "Assembly Line Station",
        "machine_category": "Assembly",
        "temp_range": (35, 70),
        "vibration_range": (0.1, 0.6),
        "pressure_range": (10, 30),
        "rpm_range": (300, 1000),
        "power_range": (200, 600)
    },

    {
        "prefix": "PKG",
        "count": 2,
        "machine_type": "Packaging Conveyor",
        "machine_category": "Packaging",
        "temp_range": (30, 65),
        "vibration_range": (0.1, 0.5),
        "pressure_range": (5, 20),
        "rpm_range": (200, 700),
        "power_range": (150, 400)
    },

    {
        "prefix": "HVAC",
        "count": 2,
        "machine_type": "Industrial HVAC System",
        "machine_category": "HVAC",
        "temp_range": (18, 45),
        "vibration_range": (0.1, 0.5),
        "pressure_range": (15, 40),
        "rpm_range": (500, 1800),
        "power_range": (300, 900)
    },

    {
        "prefix": "CLG",
        "count": 2,
        "machine_type": "Cooling Pump System",
        "machine_category": "Cooling",
        "temp_range": (10, 35),
        "vibration_range": (0.1, 0.6),
        "pressure_range": (20, 80),
        "rpm_range": (700, 2200),
        "power_range": (250, 750)
    },

    {
        "prefix": "BTRY",
        "count": 2,
        "machine_type": "Industrial Battery Backup",
        "machine_category": "PowerSystems",
        "temp_range": (20, 60),
        "vibration_range": (0.0, 0.2),
        "pressure_range": (1, 10),
        "rpm_range": (0, 100),
        "power_range": (500, 1500)
    },

    {
        "prefix": "QLT",
        "count": 1,
        "machine_type": "AI Quality Inspection Robot",
        "machine_category": "QualityInspection",
        "temp_range": (30, 70),
        "vibration_range": (0.1, 0.4),
        "pressure_range": (5, 20),
        "rpm_range": (300, 1200),
        "power_range": (150, 500)
    }

]



# ==========================================
# KAFKA PRODUCER
# ==========================================

producer = KafkaProducer(

    bootstrap_servers='localhost:9092',

    value_serializer=lambda value: json.dumps(
        value
    ).encode('utf-8')

)

# ==========================================
# CREATE MACHINE OBJECTS
# ==========================================

machines = []

for template in machine_templates:

    for i in range(1, template["count"] + 1):

        machine = Machine(

            f"{template['prefix']}_{100 + i}",

            template["machine_type"],

            template["machine_category"],

            template["temp_range"],

            template["vibration_range"],

            template["pressure_range"],

            template["rpm_range"],

            template["power_range"]

        )

        machines.append(machine)

# ==========================================
# PRODUCER LOOP
# ==========================================

print("\nProducer Started...\n")

while True:

    for machine in machines:

        telemetry = machine.generate_telemetry()

        producer.send(

            "machine-telemetry",

            telemetry

        )

        print(
            f"Sent -> {telemetry}"
        )

    time.sleep(3)