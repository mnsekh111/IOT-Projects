import smbus
import math
import time
import os, json
import ibmiotf.application
import uuid

prev_gx = 0
prev_gy = 0
prev_gz = 0

prev_ax = 0
prev_ay = 0
prev_az = 0

sum_gx = 0
sum_gy = 0
sum_gz = 0

sum_ax = 0
sum_ay = 0
sum_az = 0
count = 0
# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

current_class = 1


def read_byte(adr):
    return bus.read_byte_data(address, adr)


def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr + 1)
    val = (high << 8) + low
    return val


def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val


def dist(a, b):
    return math.sqrt((a * a) + (b * b))


def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)


def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)


def threshold_check(ax, ay, az, gx, gy, gz):
    if (abs(prev_ax) - abs(ax)) >= 0.2:
        ax_delta = True
    else:
        ax_delta = False

    if (abs(prev_ay) - abs(ay)) >= 0.2:
        ay_delta = True
    else:
        ay_delta = False

    if (abs(prev_az) - abs(az)) >= 0.2:
        az_delta = True
    else:
        az_delta = False

    if (abs(prev_gx) - abs(gx)) >= 4:
        gx_delta = True
    else:
        gx_delta = False

    if (abs(prev_gy) - abs(gy)) >= 4:
        gy_delta = True
    else:
        gy_delta = False

    if (abs(prev_gz) - abs(gz)) >= 4:
        gz_delta = True
    else:
        gz_delta = False

    return ax_delta or ay_delta or az_delta or gx_delta or gy_delta or gz_delta


def on_message(cmd):
    global current_class
    payload = json.loads(json.loads(cmd.payload))
    if payload["open"] == "1":
        current_class = 1
    if payload["close"] == "1":
        current_class = -1


bus = smbus.SMBus(1)  # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68  # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

client = None

try:
    options = ibmiotf.application.ParseConfigFile("/home/pi/device.cfg")
    client = ibmiotf.application.Client(options)
    client.connect()
    client.deviceEventCallback = on_message
    client.subscribeToDeviceEvents(event="class")
    while True:
        gx = read_word_2c(0x43)
        gy = read_word_2c(0x45)
        gz = read_word_2c(0x47)

        gx_scaled = round(gx / 131.0, 4)
        gy_scaled = round(gy / 131.0, 4)
        gz_scaled = round(gz / 131.0, 4)

        ax = read_word_2c(0x3b)
        ay = read_word_2c(0x3d)
        az = read_word_2c(0x3f)

        ax_scaled = round(ax / 16384.0, 4)
        ay_scaled = round(ay / 16384.0, 4)
        az_scaled = round(az / 16384.0, 4)

        if threshold_check(ax_scaled, ay_scaled, az_scaled, gx_scaled, gy_scaled, gz_scaled):
            global sum_ax, sum_ay, sum_az, sum_gx, sum_gy, sum_gz, count
            sum_ax += ax_scaled
            sum_ay += ay_scaled
            sum_az += az_scaled
            sum_gx += gx_scaled
            sum_gy += gy_scaled
            sum_gz += gz_scaled
            count += 1
        else:
            if count > 3:
                svm_train_data = "1:" + str(round(sum_ax / count,4)) + " 2:" + str(round(sum_ay / count,4)) + " 3:" + str(round(sum_az / count,4)) + " 4:" + str(round(sum_gx / count,4)) + " 5:" + str(round(sum_gy / count,4)) + " 6:" + str(round(sum_gz / count,4))
                #svm_train_data = str(current_class) + " 1:" + str(round(sum_ax / count,4)) + " 2:" + str(round(sum_ay / count,4)) + " 3:" + str(round(sum_az / count,4)) + " 4:" + str(round(sum_gx / count,4)) + " 5:" + str(round(sum_gy / count,4)) + " 6:" + str(round(sum_gz / count,4))
                print svm_train_data
                count = 0
                sum_ax = 0
                sum_ay = 0
                sum_az = 0
                sum_gx = 0
                sum_gy = 0
                sum_gz = 0
                client.publishEvent("RasPi", "b827ebaf79e5", "SensorData", "json", svm_train_data)
		current_class *= -1

        prev_ax = ax_scaled
        prev_ay = ay_scaled
        prev_az = az_scaled
        prev_gx = gx_scaled
        prev_gy = gy_scaled
        prev_gz = gz_scaled

        time.sleep(0.1)

except ibmiotf.ConnectionException  as e:
    print e
