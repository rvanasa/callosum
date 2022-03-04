import serial
import time

serial_port = 'COM5'


def _setup():
    try:
        return serial.Serial(port=serial_port, baudrate=57600, timeout=.001)
    except Exception as err:
        print(err)


arduino = _setup()


def is_open():
    return arduino is not None


def send_data(data):
    if not is_open():
        return

    try:
        start = time.perf_counter()
        arduino.write(data)
        # arduino.write(byte_sequence)
        # print(byte_sequence[:2])

        print(time.perf_counter() - start)

        for byte in arduino.readall():  ##
            print(chr(byte), end='')
    except serial.SerialTimeoutException:
        print('Write timeout')
    except Exception as err:
        print(err)
