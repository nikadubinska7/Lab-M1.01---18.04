"""
HomeGuard Security System Simulator
Author: Nika Dubinska
Description: A smart home monitoring system that processes sensor readings
             and triggers alerts for security, safety, and comfort issues.
"""

import random
from datetime import datetime

# System configuration
HOME_MODES = ["HOME", "AWAY", "SLEEP"]
ALERT_SEVERITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

# Current system state
current_mode = "AWAY"

def create_sensor(sensor_id, location, sensor_type, threshold=None):
    """
    Creates a sensor data structure.

    Parameters:
    - sensor_id: Unique identifier for the sensor
    - location: Where the sensor is located
    - sensor_type: Type of sensor ("motion", "temperature", "door", "smoke")
    - threshold: Optional threshold value for the sensor

    Returns:
    - A dictionary representing the sensor
    """
    sensor = {
        "id": sensor_id,
        "location": location,
        "type": sensor_type,
        "threshold": threshold,
        "current_value": None
    }
    return sensor


def create_alert(severity, message, sensor_id, timestamp):
    """
    Creates an alert data structure.

    Parameters:
    - severity: Alert severity level
    - message: Description of the alert
    - sensor_id: ID of the sensor that triggered the alert
    - timestamp: When the alert was triggered

    Returns:
    - A dictionary representing the alert
    """
    alert = {
        "severity": severity,
        "message": message,
        "sensor_id": sensor_id,
        "timestamp": timestamp
    }
    return alert

def is_abnormal_reading(sensor, reading_value):
    """
    Checks if a sensor reading is abnormal based on sensor type and thresholds.

    Parameters:
    - sensor: Sensor dictionary
    - reading_value: The current reading from the sensor

    Returns:
    - True if the reading is abnormal, False otherwise
    """
    sensor_type = sensor["type"]

    if sensor_type == "temperature":
        if reading_value < 35 or reading_value > 95:
            return True
        else:
            return False

    elif sensor_type == "motion":
        if reading_value is True:
            return True
        else:
            return False

    elif sensor_type == "door":
        if reading_value == "OPEN":
            return True
        else:
            return False

    elif sensor_type == "smoke":
        if reading_value == "DETECTED":
            return True
        else:
            return False

    return False


def should_trigger_security_alert(sensor, reading_value, system_mode):
    """
    Determines if a security alert should be triggered.

    Parameters:
    - sensor: Sensor dictionary
    - reading_value: The current reading from the sensor
    - system_mode: Current system mode (HOME, AWAY, SLEEP)

    Returns:
    - True if a security alert should be triggered, False otherwise
    """
    sensor_type = sensor["type"]

    if system_mode == "AWAY":
        if sensor_type == "motion" and reading_value is True:
            return True
        elif sensor_type == "door" and reading_value == "OPEN":
            return True

    return False


def generate_reading(sensor):
    """
    Generates a realistic reading for a sensor.

    Parameters:
    - sensor: Sensor dictionary

    Returns:
    - A realistic reading value based on sensor type
    """
    sensor_type = sensor["type"]

    if sensor_type == "temperature":
        return random.randint(30, 100)
    elif sensor_type == "motion":
        return random.choice([True, False])
    elif sensor_type == "door":
        return random.choice(["OPEN", "CLOSED"])
    elif sensor_type == "smoke":
        return random.choice(["CLEAR", "DETECTED"])

    return None


def process_reading(sensor, reading_value, system_mode):
    """
    Processes a sensor reading and determines if alerts are needed.

    Parameters:
    - sensor: Sensor dictionary
    - reading_value: The reading from the sensor
    - system_mode: Current system mode

    Returns:
    - A list of alerts (empty if no alerts needed)
    """
    alerts = []
    timestamp = datetime.now().strftime("%H:%M:%S")

    sensor_id = sensor["id"]
    location = sensor["location"]
    sensor_type = sensor["type"]

    # 1. Security alerts
    if should_trigger_security_alert(sensor, reading_value, system_mode):
        if sensor_type == "motion":
            alerts.append(
                create_alert(
                    "HIGH",
                    f"SECURITY: Motion detected in {location} while in {system_mode} mode!",
                    sensor_id,
                    timestamp
                )
            )
        elif sensor_type == "door":
            alerts.append(
                create_alert(
                    "HIGH",
                    f"SECURITY: {location} opened while in {system_mode} mode!",
                    sensor_id,
                    timestamp
                )
            )

    # 2. Safety alerts
    if sensor_type == "temperature":
        if reading_value < 35:
            alerts.append(
                create_alert(
                    "CRITICAL",
                    f"SAFETY: {location} temperature is too low at {reading_value}°F! Frozen pipe risk.",
                    sensor_id,
                    timestamp
                )
            )
        elif reading_value > 95:
            alerts.append(
                create_alert(
                    "CRITICAL",
                    f"SAFETY: {location} temperature is too high at {reading_value}°F! Equipment failure risk.",
                    sensor_id,
                    timestamp
                )
            )

    elif sensor_type == "smoke":
        if reading_value == "DETECTED":
            alerts.append(
                create_alert(
                    "CRITICAL",
                    f"SAFETY: Smoke detected in {location}! Fire risk.",
                    sensor_id,
                    timestamp
                )
            )

    # 3. Comfort notifications (only in HOME mode)
    if system_mode == "HOME" and sensor_type == "temperature":
        if reading_value < 65 or reading_value > 75:
            alerts.append(
                create_alert(
                    "LOW",
                    f"COMFORT: {location} temperature is {reading_value}°F, outside the comfort range.",
                    sensor_id,
                    timestamp
                )
            )

    return alerts


# Initialize sensors for the Peterson home
sensors = [
    create_sensor("MOTION_001", "Living Room", "motion"),
    create_sensor("TEMP_001", "Kitchen", "temperature", threshold=35),
    create_sensor("DOOR_001", "Front Door", "door"),
    create_sensor("SMOKE_001", "Bedroom", "smoke")
]

# Test print statements
print(f"Initialized {len(sensors)} sensors")
for sensor in sensors:
    print(f"  - {sensor['id']}: {sensor['location']} ({sensor['type']})")


    # Test temperature check
test_sensor = create_sensor("TEMP_TEST", "Test Room", "temperature", threshold=35)
print(f"34°F is abnormal: {is_abnormal_reading(test_sensor, 34)}")
print(f"68°F is abnormal: {is_abnormal_reading(test_sensor, 68)}")

# Test security alert
motion_sensor = create_sensor("MOTION_TEST", "Test Room", "motion")
print(f"Motion in AWAY mode triggers alert: {should_trigger_security_alert(motion_sensor, True, 'AWAY')}")
print(f"Motion in HOME mode triggers alert: {should_trigger_security_alert(motion_sensor, True, 'HOME')}")