from tkinter import messagebox
import serial
import serial.tools.list_ports

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

        #
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
    def deviceIdentifier(self):
        # Checks each available port and sees if pacemaker device is one of them
        pacemakerName = "JLink CDC UART Port"
        ports = serial.tools.list_ports.comports()

        for port, desc, hwid in sorted(ports):
            if pacemakerName in desc:
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