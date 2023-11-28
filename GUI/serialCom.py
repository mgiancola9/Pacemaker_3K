from tkinter import messagebox
import serial
import serial.tools.list_ports
import struct

# Class for all serial communication functionalities
class SerialCom:
    def __init__(self, box, pacemakerInterface):
        # Sets up frame to put all components on
        self.box = box

        # Sets up reference of the pacemakerInterface class
        self.pacemakerInterface = pacemakerInterface

        # Holds if the device was connected or disconnect in the previous state
        self.deviceStatus = "Disconnected"

        # Holds if a user is currently logged in
        self.loggedIn = True

        # Holds a reference to the device status display to modify
        self.deviceStatusDisplay = None

    # Constantly displays status of device
    def displayDeviceStatus(self, initial=False):
        # Do not check device if user is not logged in
        if not self.loggedIn:
            return
        
        deviceConnected, deviceID = self.deviceIdentifier()
        
        # If device has just been connected, set device status true and inform the user
        if deviceConnected and self.deviceStatus == "Disconnected":
            self.deviceStatus = "Connected"

            if self.newDevice():    # If this is a new device, notify the user!
                messagebox.showinfo("Pacemaker Connected", "NEW Pacemaker device has been connected!", parent=self.box)
            elif not initial:       # If this is not the initial login, notify the user!
                messagebox.showinfo("Pacemaker Connected", "Pacemaker device has been connected!", parent=self.box)

        # If device has just been disconnected, set device status false and inform the user
        elif not deviceConnected and self.deviceStatus == "Connected":
            self.deviceStatus = "Disconnected"
            if not initial:
                messagebox.showinfo("Pacemaker Disconnected", "Pacemaker device has been disconnected!", parent=self.box)

        # Finally, displays current status on home page
        deviceLabelExists = self.deviceStatusDisplay.winfo_exists()
        if deviceLabelExists:
            self.deviceStatusDisplay.config(text=f"Device Status: {self.deviceStatus}", fg='green' if self.deviceStatus == 'Connected' else 'red')

        self.box.after(1000, self.displayDeviceStatus)

    # Constantly checks whether device is connected or disconnected
    def deviceIdentifier(self, needCom=False):
        # Checks each available port and sees if pacemaker device is one of them
        pacemakerName = "JLink CDC UART Port"
        ports = serial.tools.list_ports.comports()

        for port, desc, hwid in sorted(ports):
            if pacemakerName in desc and needCom:
                return port
            elif pacemakerName in desc:
                return True, str(hwid)

        return False, ""
    
    # Detect if the device has ever been used by the user before
    def newDevice(self):
        deviceStatus, deviceID = self.deviceIdentifier()
        if deviceID in self.pacemakerInterface.currentUser['Devices']:
            return False
        
        # If the current device is not in the list, add it to history of used devices
        self.pacemakerInterface.currentUser['Devices'].append(deviceID)
        return True
    
    def parameter(self, user, parameter):
        if parameter in user:
            return user[parameter]
        else:
            return 0
    
    # Pack all needed parameter and return
    def packParameters(self, user):
        packet = []

        b0 = b'\x00'                            # Parity bit
        b1 = b'\x00'                            # Serial mode. 0 for run mode, 1 for egram mode
        b2 = struct.pack('B', user['MODE'])
        b3 = struct.pack('B', user['LRL'])
        b4 = struct.pack('B', user['URL'])
        b5 = struct.pack('B', self.parameter(user,'MSR'))


        # Bits that still have to be fixed
        b6 = struct.pack('f', user['A_AMPLITUDE'])
        b7 = struct.pack('f', user['V_AMPLITUDE'])
        b8 = struct.pack('B', user['A_WIDTH'])
        b9 = struct.pack('B', user['V_WIDTH'])
        b10 = struct.pack('f', user['A_SENSITIVITY'])
        b11 = struct.pack('f', user['V_SENSITIVITY'])
        b12 = struct.pack('H', user['VRP'])
        b13 = struct.pack('H', user['ARP'])
        b14 = struct.pack('B', user['ACTIV'])
        b15 = struct.pack('B', user['REACT_TIME'])
        b16 = struct.pack('B', user['RESPONSE_FAC'])
        b17 = struct.pack('B', user['RECOVERY_TIME'])
        
        packet.append(b0)
        packet.append(b1)
        packet.append(b2)
        packet.append(b3)
        packet.append(b4)
        packet.append(b5)
        packet.append(b6)
        packet.append(b7)
        packet.append(b8)
        packet.append(b9)
        packet.append(b10)
        packet.append(b11)
        packet.append(b12)
        packet.append(b13)
        packet.append(b14)
        packet.append(b15)
        packet.append(b16)
        packet.append(b17)

        return packet
    
    def writeToPacemaker(self, user):
        # Pack values and establish serial connection
        packet = self.packParameters(user)
        COM = self.deviceIdentifier(needCom=True)

        ser = serial.Serial(COM,115200)
        ser.write(b''.join(packet))
        print('Data has been written: ', packet)

        # Recieve values from pacemaker and check if it was transmitted correctly
