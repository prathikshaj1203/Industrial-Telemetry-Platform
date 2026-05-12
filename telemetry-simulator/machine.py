import random
from datetime import datetime
from states import *


class Machine:

    def __init__(self, machine_id, machine_type):

        self.machine_id = machine_id
        self.machine_type = machine_type
        self.state = NORMAL

    def change_state(self):

        probability = random.random()

        if self.state == NORMAL:

            if probability < 0.05:
                self.state = WARNING

        elif self.state == WARNING:

            if probability < 0.15:
                self.state = CRITICAL

            elif probability < 0.40:
                self.state = NORMAL

        elif self.state == CRITICAL:

            if probability < 0.30:
                self.state = MAINTENANCE

        elif self.state == MAINTENANCE:

            if probability < 0.80:
                self.state = NORMAL

    def generate_telemetry(self):

        self.change_state()

        # ROBOTIC WELDING ARM
        if self.machine_type == "Robotic Welding Arm":

            if self.state == NORMAL:

                temperature = random.uniform(70, 80)
                vibration = random.uniform(0.2, 0.4)
                pressure = random.uniform(40, 50)
                rpm = random.randint(1200, 1400)
                power_usage = random.randint(450, 500)

            elif self.state == WARNING:

                temperature = random.uniform(85, 95)
                vibration = random.uniform(0.5, 0.8)
                pressure = random.uniform(35, 40)
                rpm = random.randint(1000, 1200)
                power_usage = random.randint(500, 550)

            elif self.state == CRITICAL:

                temperature = random.uniform(100, 120)
                vibration = random.uniform(0.9, 1.3)
                pressure = random.uniform(20, 30)
                rpm = random.randint(800, 1000)
                power_usage = random.randint(550, 650)

        # CONVEYOR BELT SYSTEM
        elif self.machine_type == "Conveyor Belt System":

            if self.state == NORMAL:

                temperature = random.uniform(50, 65)
                vibration = random.uniform(0.1, 0.3)
                pressure = random.uniform(20, 30)
                rpm = random.randint(900, 1100)
                power_usage = random.randint(300, 400)

            elif self.state == WARNING:

                temperature = random.uniform(70, 85)
                vibration = random.uniform(0.4, 0.7)
                pressure = random.uniform(15, 20)
                rpm = random.randint(700, 900)
                power_usage = random.randint(400, 480)

            elif self.state == CRITICAL:

                temperature = random.uniform(90, 105)
                vibration = random.uniform(0.8, 1.2)
                pressure = random.uniform(10, 15)
                rpm = random.randint(500, 700)
                power_usage = random.randint(500, 600)

        # CNC MACHINING UNIT
        elif self.machine_type == "CNC Machining Unit":

            if self.state == NORMAL:

                temperature = random.uniform(65, 75)
                vibration = random.uniform(0.2, 0.5)
                pressure = random.uniform(30, 40)
                rpm = random.randint(1400, 1600)
                power_usage = random.randint(400, 500)

            elif self.state == WARNING:

                temperature = random.uniform(80, 90)
                vibration = random.uniform(0.5, 0.8)
                pressure = random.uniform(20, 30)
                rpm = random.randint(1200, 1400)
                power_usage = random.randint(500, 580)

            elif self.state == CRITICAL:

                temperature = random.uniform(95, 110)
                vibration = random.uniform(0.9, 1.4)
                pressure = random.uniform(10, 20)
                rpm = random.randint(900, 1200)
                power_usage = random.randint(600, 700)

        # HYDRAULIC PRESS
        elif self.machine_type == "Hydraulic Press":

            if self.state == NORMAL:

                temperature = random.uniform(60, 70)
                vibration = random.uniform(0.2, 0.4)
                pressure = random.uniform(80, 100)
                rpm = random.randint(600, 800)
                power_usage = random.randint(500, 600)

            elif self.state == WARNING:

                temperature = random.uniform(75, 90)
                vibration = random.uniform(0.5, 0.8)
                pressure = random.uniform(60, 80)
                rpm = random.randint(500, 650)
                power_usage = random.randint(650, 750)

            elif self.state == CRITICAL:

                temperature = random.uniform(95, 115)
                vibration = random.uniform(0.9, 1.4)
                pressure = random.uniform(40, 60)
                rpm = random.randint(300, 500)
                power_usage = random.randint(750, 900)

        # PAINT BOOTH VENTILATION
        elif self.machine_type == "Paint Booth Ventilation":

            if self.state == NORMAL:

                temperature = random.uniform(45, 60)
                vibration = random.uniform(0.1, 0.3)
                pressure = random.uniform(25, 35)
                rpm = random.randint(1000, 1200)
                power_usage = random.randint(250, 350)

            elif self.state == WARNING:

                temperature = random.uniform(65, 80)
                vibration = random.uniform(0.4, 0.7)
                pressure = random.uniform(15, 25)
                rpm = random.randint(800, 1000)
                power_usage = random.randint(350, 450)

            elif self.state == CRITICAL:

                temperature = random.uniform(85, 100)
                vibration = random.uniform(0.8, 1.1)
                pressure = random.uniform(5, 15)
                rpm = random.randint(600, 800)
                power_usage = random.randint(450, 550)

        # MAINTENANCE STATE
        if self.state == MAINTENANCE:

            temperature = random.uniform(30, 40)
            vibration = 0
            pressure = 0
            rpm = 0
            power_usage = random.randint(50, 100)

        # OFFLINE STATE
        elif self.state == OFFLINE:

            temperature = 0
            vibration = 0
            pressure = 0
            rpm = 0
            power_usage = 0

        telemetry = {

            "machine_id": self.machine_id,
            "machine_type": self.machine_type,
            "state": self.state,
            "temperature": round(temperature, 2),
            "vibration": round(vibration, 2),
            "pressure": round(pressure, 2),
            "rpm": rpm,
            "power_usage": power_usage,
            "timestamp": datetime.now().isoformat()

        }

        return telemetry