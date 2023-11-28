import serial
import struct

ser = serial.Serial('COM5', 115200, timeout=1)

def readSerial():
    # Read data from the serial port
    data = ser.read(8)  

    # Unpack the binary data into a float
    value = struct.unpack('d', data)[0]
    print(f'Received value: {value}')

    return value

def writeSerial(value):
    value += 5
    print("The value sent is", value)

    # bytes = value.to_bytes(4, byteorder='little')
    bytes = struct.pack('d', value)
    ser.write(bytes)

def testSerial():
    b0 = b'\x00'
    b1 = b'\x00'
    b2 = b'\x01'

    packet = [b0,b1,b2]
    ser.write(b''.join(packet))

# value = readSerial()
# writeSerial(value)