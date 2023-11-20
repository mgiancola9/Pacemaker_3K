import serial
import struct

ser = serial.Serial('COM5', 115200, timeout=1)

try:
    # Read data from the serial port
    data = ser.read(4)  
    print("Data extracted: ", data)

    # Unpack the binary data into a float
    value = struct.unpack('f', data)[0]
    print(f'Received value: {value}')

finally:
    # Close the serial connection
    ser.close()

    