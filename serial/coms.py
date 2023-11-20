import serial.tools.list_ports

def list_available_ports():
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("No COM ports found")
    else:
        print("Available COM ports:")
        for port, desc, hwid in sorted(ports):
            print(f"{port}: {desc} [{hwid}]")

# Call the function to list available COM ports
list_available_ports()