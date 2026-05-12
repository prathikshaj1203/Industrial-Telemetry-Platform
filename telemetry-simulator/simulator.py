import time
from machine import Machine
import json

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

        print(json.dumps(telemetry, indent=4))

    print("-" * 80)

    time.sleep(3)