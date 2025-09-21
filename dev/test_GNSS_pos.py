# test_gnss_full_address.py
import serial
import time
import requests
from micropyGPS import MicropyGPS

# --- Settings ---
PORT = "/dev/ttyTHS1"    # your UART port
BAUD = 9600              # typical GNSS baudrate
TIMEZONE = 0             # UTC offset

# --- Init GNSS parser ---
gps = MicropyGPS(TIMEZONE, 'dd')

# --- Open UART port ---
ser = serial.Serial(PORT, BAUD, timeout=1)
print(f"Listening on {PORT} at {BAUD} baud...")

def reverse_geocode(lat, lon):
    """Get full address from lat/lon using OpenStreetMap Nominatim with fallback info"""
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1"
        resp = requests.get(url, headers={"User-Agent": "Jetson-GNSS-Tester"}, timeout=5)
        data = resp.json()
        addr = data.get('address', {})

        city = addr.get('city', addr.get('town', addr.get('village', addr.get('county', 'Unknown'))))
        country = addr.get('country', 'Unknown')
        street = addr.get('road', 'Unknown')
        number = addr.get('house_number', 'Unknown')

        # Fallback: if house_number is missing, try nearby features
        if number == "Unknown":
            # neighborhood or suburb
            number = addr.get('neighbourhood', addr.get('suburb', 'Unknown'))

        # Extra fallback: if street missing, try pedestrian or footway
        if street == "Unknown":
            street = addr.get('pedestrian', addr.get('footway', street))

        return city, country, street, number
    except Exception as e:
        return "Error", "Error", "Error", "Error"

while True:
    line = ser.readline().decode('ascii', errors='replace').strip()
    if line:
        print("RAW:", line)  # show raw NMEA
        for c in line:
            gps.update(c)

        # Only print when we have a valid lat/lon
        if gps.latitude and gps.longitude and gps.valid:
            # Apply N/S and E/W
            lat = gps.latitude[0] * (1 if gps.latitude[1] == 'N' else -1)
            lon = gps.longitude[0] * (1 if gps.longitude[1] == 'E' else -1)
            print(f"Parsed Lat/Lon: {lat:.6f}, {lon:.6f}")

            # UTC time
            utc_tuple = gps.timestamp  # (hours, minutes, seconds)
            print(f"UTC Time: {utc_tuple[0]:02}:{utc_tuple[1]:02}:{utc_tuple[2]:02}")

            # Date
            date_tuple = gps.date  # (day, month, year)
            year = date_tuple[2]
            if year < 2000:
                year += 2000
            print(f"Date: {date_tuple[0]:02}/{date_tuple[1]:02}/{year:04}")

            # Speed
            print(f"Speed: {gps.speed_string('kph')} kph")

            # Reverse geocode
            city, country, street, number = reverse_geocode(lat, lon)
            print(f"Address: {number} {street}, {city}, {country}")
            print("-" * 60)

            time.sleep(1)
