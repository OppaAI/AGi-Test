# test_gnss.py
import serial
import time
from micropyGPS import MicropyGPS

# --- Settings ---
PORT = "/dev/ttyTHS1"   # change if needed
BAUD = 9600             # typical GNSS baudrate
TIMEZONE = 0            # UTC offset, set if you want local time

# --- Init GNSS parser ---
gps = MicropyGPS(TIMEZONE, 'dd')  # 'dd' = decimal degrees format

# --- Open UART port ---
ser = serial.Serial(PORT, BAUD, timeout=1)
print(f"Listening on {PORT} at {BAUD} baud...")

while True:
    sentence = ser.readline().decode('ascii', errors='replace').strip()
    if sentence.startswith("$"):   # valid NMEA
        for c in sentence:
            gps.update(c)

        # Print data if fix available
        if gps.valid:
            print(f"Lat: {gps.latitude[0]:.6f}, Lon: {gps.longitude[0]:.6f}")
            print(f"UTC Time: {gps.utc}")
            print(f"Date: {gps.date_string('long')}")
            print(f"Speed: {gps.speed_string('kph')}")
            print("-" * 40)
    else:
        print("No valid NMEA sentence...")
    time.sleep(1)
