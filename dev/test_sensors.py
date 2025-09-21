import time
import smbus2

ADDR = 0x53

# Registers
LTR390_MAIN_CTRL = 0x00
LTR390_MEAS_RATE = 0x04
LTR390_GAIN = 0x05
LTR390_PART_ID = 0x06
LTR390_MAIN_STATUS = 0x07
LTR390_ALSDATA = 0x0D
LTR390_UVSDATA = 0x10

# Default settings
GAIN_DEFAULT = 0x01       # Gain 3x
MEAS_RATE_DEFAULT = 0x02  # 100ms

# Measurement enable flags
LTR390_ALS_EN = 0x02
LTR390_UVS_EN = 0x10

class LTR390:
    def __init__(self, address=ADDR, bus=7):
        self.address = address
        time.sleep(0.1)  # let I2C bus stabilize
        self.i2c = smbus2.SMBus(bus)

        # Power on
        self.write_byte(LTR390_MAIN_CTRL, 0x01)
        time.sleep(0.05)

        # Set gain and measurement rate
        self.write_byte(LTR390_GAIN, GAIN_DEFAULT)
        self.write_byte(LTR390_MEAS_RATE, MEAS_RATE_DEFAULT)
        time.sleep(0.05)

        # Enable ALS and UV measurement
        self.write_byte(LTR390_MAIN_CTRL, LTR390_ALS_EN | LTR390_UVS_EN)
        time.sleep(0.1)

        # Check sensor ID
        self.ID = self.read_byte(LTR390_PART_ID)
        if self.ID != 0xB2:
            print(f"Read ID error! Got {hex(self.ID)}, check hardware...")
            raise Exception("Sensor not found")
        print(f"LTR390 detected, ID: {hex(self.ID)}")

    def read_byte(self, reg):
        for _ in range(10):
            try:
                return self.i2c.read_byte_data(self.address, reg)
            except (BlockingIOError, OSError):
                time.sleep(0.01)
        raise Exception(f"Failed to read register {hex(reg)}")

    def write_byte(self, reg, value):
        for _ in range(10):
            try:
                self.i2c.write_byte_data(self.address, reg, value)
                return
            except (BlockingIOError, OSError):
                time.sleep(0.01)
        raise Exception(f"Failed to write {hex(value)} to register {hex(reg)}")

    def data_ready(self):
        try:
            status = self.read_byte(LTR390_MAIN_STATUS)
            return (status & 0x08) != 0  # ALS data ready bit
        except Exception:
            return False

    def read_als(self):
        try:
            data = self.i2c.read_i2c_block_data(self.address, LTR390_ALSDATA, 3)
            return data[0] | (data[1] << 8) | (data[2] << 16)
        except OSError:
            return None

    def read_uv(self):
        try:
            data = self.i2c.read_i2c_block_data(self.address, LTR390_UVSDATA, 3)
            return data[0] | (data[1] << 8) | (data[2] << 16)
        except OSError:
            return None


# --- Main loop ---
# --- Main loop ---
if __name__ == "__main__":
    sensor = LTR390()
    
    # Wait for the first valid measurement
    print("Waiting for sensor data...")
    while not sensor.data_ready():
        time.sleep(0.1)
    
    print("Sensor data ready! Starting readings...")

    try:
        while True:
            als = sensor.read_als()
            uv = sensor.read_uv()

            if als is not None and uv is not None:
                print(f"ALS: {als}, UV: {uv}")
            else:
                print("Failed to read sensor data, retrying...")

            # Sleep according to measurement rate
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("Exiting...")

