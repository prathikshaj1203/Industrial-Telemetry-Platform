def validate_telemetry(data):

    required_fields = [

        "machine_id",
        "machine_type",
        "state",
        "temperature",
        "vibration",
        "pressure",
        "rpm",
        "power_usage",
        "timestamp"

    ]

    for field in required_fields:

        if field not in data:
            return False, f"Missing field: {field}"

    if data["temperature"] < 0 or data["temperature"] > 150:
        return False, "Invalid temperature"

    if data["vibration"] < 0 or data["vibration"] > 5:
        return False, "Invalid vibration"

    if data["rpm"] < 0 or data["rpm"] > 10000:
        return False, "Invalid RPM"

    if data["state"] not in ["NORMAL", "WARNING", "CRITICAL"]:
        return False, "Invalid machine state"

    return True, "Valid telemetry"