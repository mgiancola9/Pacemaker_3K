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
    
    # Function that determines if the parameter is a part of the required mode 
    def parameter(self, user, parameter):
        if parameter in user:
            return user[parameter]
        else:
            return 0
    
    # Special function to force URL to be a specific value based on its difference with URL
    def regulateURL(self, user, mode):
        if mode == "AOO" or mode == "AAI" or mode == "VOO" or mode == "VVI" and (user['URL'] <= user['LRL']):
            return user['LRL'] + 10
        elif mode == "AOOR" or mode == "AAIR" or mode == "VOOR" or mode == "VVIR" and (user['URL'] - user['LRL']) < 60:
            return user['R_MSR']
        else:
            return user['URL']
    
    # Pack all needed parameter and return
    def packParameters(self, user, mode, egram=False):
        packet = []

        b0 = b'\x00'                                            # Parity bit
        b1 = b'\x01' if egram else b'\x00'                      # Serial mode. 0 for run mode, 1 for egram mode
        b2 = struct.pack('B', user['MODE'])                     # Mode being used
        b3 = struct.pack('H', user['LRL'])                      # Lower rate limit
        b4 = struct.pack('H', self.regulateURL(user, mode))     # Upper rate limit
        b5 = struct.pack('H', self.parameter(user,'REACT'))     # Reaction time
        b6 = struct.pack('H', self.parameter(user,'RESPF'))     # Response factor RF in simulink
        b7 = struct.pack('d', self.parameter(user,'W_THRESH'))  # Walk threshold
        b8 = struct.pack('d', self.parameter(user,'J_THRESH'))  # Jog threshold
        b9 = struct.pack('d', self.parameter(user,'R_THRESH'))  # Run threshold
        b10 = struct.pack('H', self.parameter(user,'RECOVT'))   # Recovery time
        b11 = struct.pack('H', self.parameter(user,'W_MSR'))    # Walk max sensing rate
        b12 = struct.pack('H', self.parameter(user,'J_MSR'))    # Jog max sensing rate
        b13 = struct.pack('H', self.parameter(user,'R_MSR'))    # Run max sensing rate
        b14 = struct.pack('d', self.parameter(user,'J_HYST'))   # Walk hysterisis
        b15 = struct.pack('d', self.parameter(user,'R_HYST'))   # Jog hysterisis
        b16 = struct.pack('d', self.parameter(user,'W_HYST'))   # Run hysterisis
        b17 = struct.pack('f', self.parameter(user,'AA'))       # Atrial amp
        b18 = struct.pack('H', self.parameter(user,'APW'))      # Atrial pulse width
        b19 = struct.pack('H', self.parameter(user,'ARP'))      # Atrial refractory period
        b20 = struct.pack('f', self.parameter(user,'AS'))       # Atrial sensitivity
        b21 = struct.pack('f', self.parameter(user,'VA'))       # Ventricular amp
        b22 = struct.pack('H', self.parameter(user,'VPW'))      # Ventricular pulse width
        b23 = struct.pack('H', self.parameter(user,'VRP'))      # Ventricular refractory period
        b24 = struct.pack('f', self.parameter(user,'VS'))       # Ventricular sensitivity

        # Sum all of the values that were packed
        sum = user['MODE'] + user['LRL'] + self.regulateURL(user, mode) + self.parameter(user,'REACT') + self.parameter(user,'RESPF') + self.parameter(user,'W_THRESH') + self.parameter(user,'J_THRESH') + self.parameter(user,'R_THRESH') + self.parameter(user,'RECOVT') + self.parameter(user,'J_MSR') + self.parameter(user,'R_MSR') + self.parameter(user,'W_MSR') + self.parameter(user,'J_HYST') + self.parameter(user,'R_HYST') + self.parameter(user,'W_HYST') + self.parameter(user,'AA') + self.parameter(user,'APW') + self.parameter(user,'ARP') + self.parameter(user,'AS') + self.parameter(user,'VA') + self.parameter(user,'VPW') + self.parameter(user,'VRP') + self.parameter(user,'VS')

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
        packet.append(b18)
        packet.append(b19)
        packet.append(b20)
        packet.append(b21)
        packet.append(b22)
        packet.append(b23)
        packet.append(b24)

        return packet, sum
    
    # Sum all of the values written to the pacemaker and received back
    def readPacemakerData(self, ser, egram=False):

        MODE = struct.unpack("B", ser.read(1))[0]
        LRL = struct.unpack("H", ser.read(2))[0]
        URL = struct.unpack("H", ser.read(2))[0]
        REACT = struct.unpack("H", ser.read(2))[0]
        RESPF = struct.unpack("H", ser.read(2))[0]
        W_THRESH = struct.unpack("d", ser.read(8))[0]
        J_THRESH = struct.unpack("d", ser.read(8))[0]
        R_THRESH = struct.unpack("d", ser.read(8))[0]
        RECOVT = struct.unpack("H", ser.read(2))[0]
        W_MSR = struct.unpack("H", ser.read(2))[0]
        J_MSR = struct.unpack("H", ser.read(2))[0]
        R_MSR = struct.unpack("H", ser.read(2))[0]
        W_HYST = struct.unpack("d", ser.read(8))[0]
        J_HYST = struct.unpack("d", ser.read(8))[0]
        R_HYST = struct.unpack("d", ser.read(8))[0]
        AA = struct.unpack("f", ser.read(4))[0]
        APW = struct.unpack("H", ser.read(2))[0]
        ARP = struct.unpack("H", ser.read(2))[0]
        AS = struct.unpack("f", ser.read(4))[0]
        VA = struct.unpack("f", ser.read(4))[0]
        VPW = struct.unpack("H", ser.read(2))[0]
        VRP = struct.unpack("H", ser.read(2))[0]
        VS = struct.unpack("f", ser.read(4))[0]
        ATR_SIGNAL = struct.unpack("d", ser.read(8))[0]
        VENT_SIGNAL = struct.unpack("d", ser.read(8))[0]

        if egram:
            return [ATR_SIGNAL, VENT_SIGNAL]
        else:
            sum = MODE + LRL + URL + REACT + RESPF + W_THRESH + J_THRESH + R_THRESH + RECOVT + W_MSR + J_MSR + R_MSR + W_HYST + J_HYST + R_HYST + AA + APW + ARP + AS + VA + VPW + VRP + VS
            return sum
    
    def writeToPacemaker(self, user, mode):
        # Pack values
        packet, writeSum = self.packParameters(user, mode)
        COM = self.deviceIdentifier(needCom=True)

        # Establish serial connection and write to board
        ser = serial.Serial(COM, 115200)
        ser.write(b''.join(packet))
        print('Data has been written: ', packet)

        # Recieve values from board and check if it was transmitted correctly
        readSum = self.readPacemakerData(ser)

        # Notify user whether the data has been written successfully or not
        if readSum == writeSum:
            messagebox.showinfo("Run Successful", f"{mode} is now running on the pacemaker.", parent=self.box)
        else:
            messagebox.showinfo("Error Write", "There was an error writing the parameters to the pacemaker.", parent=self.box) 

    def receiveEgramData(self, user, mode):
        # Pack values
        packet, sum = self.packParameters(user, mode, egram=True)
        COM = self.deviceIdentifier(needCom=True)

        # Establish serial connection and write to board
        ser = serial.Serial(COM, 115200)
        ser.write(b''.join(packet))
        data = self.readPacemakerData(ser, egram=True)
        # ser.close()
        
        return data



