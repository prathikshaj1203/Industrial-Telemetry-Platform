import random
from datetime import datetime


class Machine:

    def __init__(

        self,

        machine_id,
        machine_type,
        machine_category,

        temp_range,
        vibration_range,
        pressure_range,
        rpm_range,
        power_range

    ):

        self.machine_id = machine_id
        self.machine_type = machine_type
        self.machine_category = machine_category

        self.temp_range = temp_range
        self.vibration_range = vibration_range
        self.pressure_range = pressure_range
        self.rpm_range = rpm_range
        self.power_range = power_range

    def generate_telemetry(self):

        temperature = round(
            random.uniform(*self.temp_range),
            2
        )

        vibration = round(
            random.uniform(*self.vibration_range),
            2
        )

        pressure = round(
            random.uniform(*self.pressure_range),
            2
        )

        rpm = random.randint(*self.rpm_range)

        power_usage = round(
            random.uniform(*self.power_range),
            2
        )

        # ==================================
        # MACHINE STATE LOGIC
        # ==================================

        if (
            temperature > self.temp_range[1] * 0.9
            or vibration > self.vibration_range[1] * 0.9
        ):

            state = "WARNING"

        else:

            state = "NORMAL"

        telemetry = {

            "machine_id": self.machine_id,

            "machine_type": self.machine_type,

            "machine_category": self.machine_category,

            "state": state,

            "temperature": temperature,

            "vibration": vibration,

            "pressure": pressure,

            "rpm": rpm,

            "power_usage": power_usage,

            "timestamp": datetime.now().isoformat()

        }

        return telemetry