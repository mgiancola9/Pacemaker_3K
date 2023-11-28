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
    
    #function that determines if the parameter is a part of the required mode 
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
        b5 = struct.pack('B', self.parameter(user,'REACT'))
        b6 = struct.pack('B', self.parameter(user,'RESPF')) #response factor RF in simulink

        b7 = struct.pack('d', self.parameter(user,'W_THRESH')) #const 0.5
        b8 = struct.pack('d', self.parameter(user,'J_THRESH')) #const 1.75
        b9 = struct.pack('d', self.parameter(user,'R_Thresh')) #const 3
        #recovery time 
        b10 = struct.pack('B', self.parameter(user,'RECOVT'))
        #W_MSR
        b11 = struct.pack('B', self.parameter(user,'MSR'))
        #J_MSR
        b12 = struct.pack('B', self.parameter(user,'MSR'))
        #R_MSR
        b13 = struct.pack('B', self.parameter(user,'MSR'))
        #W_Hys
        b14 = struct.pack('B', self.parameter(user,'HYST'))
        #J_Hys
        b15 = struct.pack('B', self.parameter(user,'HYST'))
        #R_Hys
        b16 = struct.pack('B', self.parameter(user,'HYST'))
        #ATRIUM
        b17 = struct.pack('f', self.parameter(user,'AA')) #Atrial amp
        b18 = struct.pack('B', self.parameter(user,'APW')) #Atrial pulse width
        b19 = struct.pack('H', self.parameter(user,'ARP')) #Atrial refractory period
        b20 = struct.pack('B', self.parameter(user,'AS')) #Atrial sensitivity
        #VENTRICLE
        b21 = struct.pack('f', self.parameter(user,'VA')) #Ventricular amp
        b22 = struct.pack('B', self.parameter(user,'VPW')) #Ventricular pulse width
        b23 = struct.pack('H', self.parameter(user,'VRP'))  #Ventricular refractory period
        b24 = struct.pack('B', self.parameter(user,'VS')) #Ventricular sensitivity

        #sum all of the values that were packed
        sum = user['MODE'] + user['LRL'] + user['URL'] + self.parameter(user,'REACT') + self.parameter(user,'RESPF') + self.parameter(user,'W_THRESH') + self.parameter(user,'J_THRESH') + self.parameter(user,'R_Thresh') + self.parameter(user,'RECOVT') + self.parameter(user,'MSR') + self.parameter(user,'MSR') + self.parameter(user,'MSR') + self.parameter(user,'HYST') + self.parameter(user,'HYST') + self.parameter(user,'HYST') + self.parameter(user,'AA') + self.parameter(user,'APW') + self.parameter(user,'ARP') + self.parameter(user,'AS') + self.parameter(user,'VA') + self.parameter(user,'VPW') + self.parameter(user,'VRP') + self.parameter(user,'VS')
        
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
    
    #write a function that reads the data from the pacemaker and unpacks it to the variables corresponding to the dictrionary keys as above
    def sumPacemakerData(self, data, sum):

        data = struct.unpack("B", data[0:1])[0]
        LRL = struct.unpack("B", data[1:2])[0]
        URL = struct.unpack("B", data[2:3])[0]
        REACT = struct.unpack("B", data[3:4])[0]
        RESPF = struct.unpack("B", data[4:5])[0]
        W_THRESH = struct.unpack("d", data[5:13])[0]
        J_THRESH = struct.unpack("d", data[13:21])[0]
        R_THRESH = struct.unpack("d", data[21:29])[0]
        RECOVT = struct.unpack("B", data[29:30])[0]
        W_MSR = struct.unpack("B", data[30:31])[0]
        J_MSR = struct.unpack("B", data[31:32])[0]
        R_MSR = struct.unpack("B", data[32:33])[0]
        W_HYST = struct.unpack("B", data[33:34])[0]
        J_HYST = struct.unpack("B", data[34:35])[0]
        R_HYST = struct.unpack("B", data[35:36])[0]
        AA = struct.unpack("f", data[36:40])[0]
        APW = struct.unpack("B", data[40:41])[0]
        ARP = struct.unpack("H", data[41:43])[0]
        AS = struct.unpack("B", data[43:44])[0]
        VA = struct.unpack("f", data[44:48])[0]
        VPW = struct.unpack("B", data[48:49])[0]
        VRP = struct.unpack("H", data[49:51])[0]
        VS = struct.unpack("B", data[51:52])[0]

        sum = data + LRL + URL + REACT + RESPF + W_THRESH + J_THRESH + R_THRESH + RECOVT + W_MSR + J_MSR + R_MSR + W_HYST + J_HYST + R_HYST + AA + APW + ARP + AS + VA + VPW + VRP + VS

        return sum
    
    def writeToPacemaker(self, user):
        # Pack values and establish serial connection
        packet = self.packParameters(user)
        COM = self.deviceIdentifier(needCom=True)

        ser = serial.Serial(COM,115200)
        ser.write(b''.join(packet))
        print('Data has been written: ', packet)

        # Recieve values from pacemaker and check if it was transmitted correctly
