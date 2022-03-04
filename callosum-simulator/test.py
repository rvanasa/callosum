import serial
import time
import numpy as np

print(b'A' * 10)

arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

byte_grid = np.array([[
    [1, 2, 3],
    [4, 5, 6],
], [
    [7, 8, 9],
    [10, 11, 12],
]]).astype(np.uint8)

print(bytes(byte_grid))

while True:
    try:
        arduino.write(b'AAA')  # Alignment signal
        arduino.write(bytes(byte_grid))
        # arduino.flush()##

        # for byte in arduino.read():
        #     print(chr(byte), end='')  ###

        time.sleep(100)
    except Exception as err:
        # print(err)
        pass
