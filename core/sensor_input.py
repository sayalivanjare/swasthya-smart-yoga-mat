import serial
import re

# -------------------------
# SERIAL CONNECTION
# -------------------------
try:
    ser = serial.Serial('COM3', 115200, timeout=1)
except:
    ser = None


# -------------------------
# SENSOR FUNCTION (ROBUST)
# -------------------------
def get_sensor_data():

    if ser is None:
        return []

    try:
        line = ser.readline().decode(errors='ignore').strip()

        # If empty line → ignore
        if not line:
            return []

        # Extract all numbers safely
        values = re.findall(r'\d+', line)

        values = [int(v) for v in values]

        # Ensure minimum consistency
        if len(values) < 6:
            return []

        return values

    except:
        return []