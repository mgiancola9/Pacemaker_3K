import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from egramInterface import EgramInterface
import serial
import serial.tools.list_ports
import time

# Class for all pacemaker modifications
class PacemakerInterface:
    def __init__(self, app, box, loginInterface, userStorage):
        # Sets up frame to put all components on
        self.box = box

        # Variable to hold the current user logged in
        self.currentUser = None

        # Variables to use for text font
        self.titleFont = ('Helvatical bold', 14)
        self.subtextFont = ('Helvatical bold', 12, "bold")

        # Defines an instance for each module
        self.app = app
        self.loginInterface = loginInterface
        self.userStorage = userStorage
        self.egramInterface = EgramInterface(app,box,self)

        # Defines whether pacemaker device is connected or not
        self.device = False

        # self.deviceStatus()

    # Constantly checks whether device is connected or disconnected
    def deviceStatus(self):
        pacemakerName = "JLink CDC UART Port"

        while True:
            deviceConnected = False
            ports = serial.tools.list_ports.comports()

            for port, desc, hwid in sorted(ports):
                if pacemakerName in desc:
                    deviceConnected = True
                    break
            
            if deviceConnected and not self.device:
                print("Device connected.")
            elif not deviceConnected and self.device:
                print("Device disconnected.")

            time.sleep(1)

    # Home page when user is logged in. Takes currentUser parameter to communicate between loginInterface class
    def homePage(self, currentUser = None):
        homePage = self.app.redirectPage()
        if currentUser:
            self.currentUser = currentUser

        title = tk.Label(homePage, text=f"Welcome, {self.currentUser['username']}!", font=self.titleFont, bg="pink2", height=2)
        title.pack(fill=tk.BOTH)

        # Pulsing mode section
        modeDescription = tk.Label(homePage, text="Select a pacing mode.", font=self.subtextFont)
        modeDescription.pack(pady=20)

        buttonsContainer = tk.Frame(homePage)
        buttonsContainer.pack(fill=tk.Y)

        VOOButton = tk.Button(buttonsContainer, text="VOO", font=self.subtextFont, width=12, pady=3, command=lambda: self.settingsPage("VOO"))
        VOOButton.grid(row=0, column=0, padx=10, pady=5)

        VVIButton = tk.Button(buttonsContainer, text="VVI", font=self.subtextFont, width=12, pady=3, command=lambda: self.settingsPage("VVI"))
        VVIButton.grid(row=0, column=1, padx=10, pady=5)

        AOOButton = tk.Button(buttonsContainer, text="AOO", font=self.subtextFont, width=12, pady=3, command=lambda: self.settingsPage("AOO"))
        AOOButton.grid(row=1, column=0, padx=10, pady=5)

        AAIButton = tk.Button(buttonsContainer, text="AAI", font=self.subtextFont, width=12, pady=3, command=lambda: self.settingsPage("AAI"))
        AAIButton.grid(row=1, column=1, padx=10, pady=5)

        #Assignment 2 added modes:
        AOORButton = tk.Button(buttonsContainer, text="AOOR", font=self.subtextFont, width=12, pady=3, command=lambda: self.settingsPage("AOOR"))
        AOORButton.grid(row=2, column=0, padx=10, pady=5)

        AAIRButton = tk.Button(buttonsContainer, text="AAIR", font=self.subtextFont, width=12, pady=3, command=lambda: self.settingsPage("AAIR"))
        AAIRButton.grid(row=2, column=1, padx=10, pady=5)

        VOORButton = tk.Button(buttonsContainer, text="VOOR", font=self.subtextFont, width=12, pady=3, command=lambda: self.settingsPage("VOOR"))
        VOORButton.grid(row=3, column=0, padx=10, pady=5)

        VVIRButton = tk.Button(buttonsContainer, text="VVIR", font=self.subtextFont, width=12, pady=3, command=lambda: self.settingsPage("VVIR"))
        VVIRButton.grid(row=3, column=1, padx=10, pady=5)

        # Device detection section
        deviceDescription = tk.Label(homePage, text="Connect the device.", font=self.subtextFont)
        deviceDescription.pack(pady=(20, 10))

        # Switches between connecting and disconnecting the device
        def connectDevice():
            status = connectButton.cget("text")
            if status == "Connect":

                # Checks if a new device. If it is, asks the user if they want to connect it or not
                device = "device-a63145"
                if device != self.currentUser["lastDeviceUsed"]:
                    result = messagebox.askquestion("New Device", f"New device has been detected. Do you want to set it as your primary device?")
                    if result == "yes":
                        self.currentUser["lastDeviceUsed"] = device
                        status = "Disconnect"
                else:
                    status = "Disconnect"
            else:
                status = "Connect"

            connectButton.configure(text=status)

        connectButton = tk.Button(homePage, text="Connect", font=self.subtextFont, command=connectDevice, width=12, pady=3)
        connectButton.pack()

        # Egram section
        egramDescription = tk.Label(homePage, text="Develop egram data.", font=self.subtextFont)
        egramDescription.pack(pady=(20, 10))

        egramButton = tk.Button(homePage, text="egram", font=self.subtextFont, command=lambda currentUser=self.currentUser: self.egramInterface.egramPage(currentUser), width=12, pady=3)
        egramButton.pack()

        # Logout section
        logoutButton = tk.Button(homePage, text="Logout", font=self.subtextFont, command=self.loginInterface.startPage, padx=40, pady=3)
        logoutButton.pack(side="bottom", anchor="se", padx=5, pady=5)

    # Pacing mode pages
    def settingsPage(self, mode):
        settingsPage = self.app.redirectPage()

        # Copies values of the current mode, to be modified then saved
        modeValues = self.currentUser[mode].copy()

        # Title for the page
        title = tk.Label(settingsPage, text=f"Pacemaker Settings - {mode}", font=self.titleFont, bg="mediumpurple", height=2)
        title.pack(fill=tk.BOTH)

        # Functions for slider changes
        def LRLHChange(value, LorH):
            value = float(value)
            # if LorH == "HYST" and value < 30:
            #     roundedValue = 0
            if 30 <= value < 50:
                roundedValue = round(value / 5) * 5
            elif 50 <= value < 90:
                roundedValue = round(value)
            elif 90 <= value <= 175:
                roundedValue = round(value / 5) * 5

            modeValues[LorH] = roundedValue
            if LorH == "LRL":
                lrlLabel.config(text=f"LRL: {roundedValue} ppm")
            # elif LorH == "HYST":
            #     hystLabel.config(text=f"HYST: {roundedValue} ppm")

        # VPW and APW update when the slider changes
        # Updated for ass 2: program vals = 1-30ms old was (.1-1.9), incrememt by 1ms old was .1 (no 0.05 now), nominal = 1ms was 0.4
        def VAPWChange(value, VorA):
            value = float(value)
            if value <= 30:  # extra round to keep out fp rounding errors
                roundedValue = round(round(value / 1) * 1, 1)

            modeValues[VorA] = roundedValue
            if VorA == "APW":
                apwLabel.config(text=f"APW: {roundedValue} ms")
            elif VorA == "VPW":
                vpwLabel.config(text=f"VPW: {roundedValue} ms")

        # AS and VS update when the slider changes
        # Updated for ass 2, now simple 0-5V interval with .1 increments
        def AVSensChange(value, VorA):
            value = float(value)
            if 0 <= value <= 5:
                roundedValue = round(round(value / 0.1) * 0.1, 1)

            modeValues[VorA] = roundedValue
            if VorA == "AS":
                asLabel.config(text=f"AS: {roundedValue} V")
            elif VorA == "VS":
                vsLabel.config(text=f"VS: {roundedValue} V")

        # AA and VA update when the slider changes
        # Updated for ass 2, now simple 0-5V interval with .1 incrememnts
        def VAAmpChange(value, VorA):
            value = float(value)
            if 0 <= value <= 5 :
                roundedValue = round(round(value / 0.1) * 0.1, 1)

            modeValues[VorA] = roundedValue
            if VorA == "AA":
                aaLabel.config(text=f"AA: {roundedValue} V")
            elif VorA == "VA":
                vaLabel.config(text=f"VA: {roundedValue} V")

        # General function for when the slider changes
        def generalChange(value, increment, type, unit):
            value = float(value)
            roundedValue = round(value / increment) * increment
            modeValues[type] = roundedValue
            if type == "URL":
                urlLabel.config(text=f"URL: {roundedValue} {unit}")
            elif type == "ARP":
                arpLabel.config(text=f"ARP: {roundedValue} {unit}")
            elif type == "VRP":
                vrpLabel.config(text=f"VRP: {roundedValue} {unit}")
            elif type == "PVARP":
                pvarpLabel.config(text=f"PVARP: {roundedValue} {unit}")
            elif type == "RS":
                if roundedValue == 24:
                    roundedValue = 25
                    modeValues[type] = roundedValue
                rsLabel.config(text=f"RS: {roundedValue} {unit}")

        # Container to hold all sliders and titles
        slidersContainer = tk.Frame(settingsPage)
        slidersContainer.pack(fill=tk.Y)

        # Updates current row and column based on slider that was added.
        row = col = 0
        def updateRowCol():
            nonlocal row, col
            col = 1 - col
            if col == 0:
                row += 2  # Move by 2 rows since label and slider take two rows instead of 1


        # LRL slider for all modes
        lrlLabel = tk.Label(slidersContainer, text=f"LRL: {modeValues['LRL']} ppm")
        lrlLabel.grid(row=row, column=col, pady=(8, 0))
        lrlSlider = ttk.Scale(slidersContainer, from_=30, to=175, length=200, orient="horizontal", value=modeValues["LRL"], command=lambda value: LRLHChange(value, "LRL"))
        lrlSlider.grid(row=row+1, column=col, padx=20)
        updateRowCol()

        # URL slider for all modes
        urlLabel = tk.Label(slidersContainer, text=f"URL: {modeValues['URL']} ppm")
        urlLabel.grid(row=row, column=col, pady=(8, 0))
        urlSlider = ttk.Scale(slidersContainer, from_=50, to=175, length=200, orient="horizontal", value=modeValues["URL"], command=lambda value: generalChange(value, 5, "URL", "ppm"))
        urlSlider.grid(row=row+1, column=col, padx=20)
        updateRowCol()

        # Sliders for AOO and AAI
        if mode == "AOO" or mode == "AAI":
            aaLabel = tk.Label(slidersContainer, text=f"AA: {modeValues['AA']} V")
            aaLabel.grid(row=row, column=col, pady=(8, 0))
            aaSlider = ttk.Scale(slidersContainer, from_=0, to=5, length=200, orient="horizontal", value=modeValues["AA"], command=lambda value: VAAmpChange(value, "AA"))
            aaSlider.grid(row=row+1, column=col, padx=20)
            updateRowCol()

            apwLabel = tk.Label(slidersContainer, text=f"APW: {modeValues['APW']} ms")
            apwLabel.grid(row=row, column=col, pady=(8, 0))
            apwSlider = ttk.Scale(slidersContainer, from_=1, to=30, length=200, orient="horizontal", value=modeValues["APW"], command=lambda value: VAPWChange(value, "APW"))
            apwSlider.grid(row=row+1, column=col, padx=20)
            updateRowCol()

        # Sliders for VOO and VII
        if mode == "VOO" or mode == "VVI":
            vaLabel = tk.Label(slidersContainer, text=f"VA: {modeValues['VA']} V")
            vaLabel.grid(row=row, column=col, pady=(8, 0))
            vaSlider = ttk.Scale(slidersContainer, from_=0, to=5, length=200, orient="horizontal", value=modeValues["VA"], command=lambda value: VAAmpChange(value, "VA"))
            vaSlider.grid(row=row+1, column=col, padx=20)
            updateRowCol()

            vpwLabel = tk.Label(slidersContainer, text=f"VPW: {modeValues['VPW']} ms")
            vpwLabel.grid(row=row, column=col, pady=(8, 0))
            vpwSlider = ttk.Scale(slidersContainer, from_=1, to=30, length=200, orient="horizontal", value=modeValues["VPW"], command=lambda value: VAPWChange(value, "VPW"))
            vpwSlider.grid(row=row+1, column=col, padx=20)
            updateRowCol()

        # Sliders only for AAI
        if mode == "AAI":
            arpLabel = tk.Label(slidersContainer, text=f"ARP: {modeValues['ARP']} ms")
            arpLabel.grid(row=row, column=col, pady=(8, 0))
            arpSlider = ttk.Scale(slidersContainer, from_=150, to=500, length=200, orient="horizontal", value=modeValues["ARP"], command=lambda value: generalChange(value, 10, "ARP", "ms"))
            arpSlider.grid(row=row+1, column=col, padx=20)
            updateRowCol()

            asLabel = tk.Label(slidersContainer, text=f"AS: {modeValues['AS']} V")
            asLabel.grid(row=row, column=col, pady=(8, 0))
            asSlider = ttk.Scale(slidersContainer, from_=0, to=5, length=200, orient="horizontal", value=modeValues["AS"], command=lambda value: AVSensChange(value, "AS"))
            asSlider.grid(row=row+1, column=col, padx=20)
            updateRowCol()

            pvarpLabel = tk.Label(slidersContainer, text=f"PVARP: {modeValues['PVARP']} ms")
            pvarpLabel.grid(row=row, column=col, pady=(8, 0))
            pvarpSlider = ttk.Scale(slidersContainer, from_=150, to=500, length=200, orient="horizontal", value=modeValues["PVARP"], command=lambda value: generalChange(value, 10, "PVARP", "ms"))
            pvarpSlider.grid(row=row+1, column=col, padx=20)
            updateRowCol()

        # Sliders only for VVI
        elif mode == "VVI":
            vrpLabel = tk.Label(slidersContainer, text=f"VRP: {modeValues['VRP']} ms")
            vrpLabel.grid(row=row, column=col, pady=(8, 0))
            vrpSlider = ttk.Scale(slidersContainer, from_=150, to=500, length=200, orient="horizontal", value=modeValues["VRP"], command=lambda value: generalChange(value, 10, "VRP", "ms"))
            vrpSlider.grid(row=row+1, column=col, padx=20)
            updateRowCol()

            vsLabel = tk.Label(slidersContainer, text=f"VS: {modeValues['VS']} V")
            vsLabel.grid(row=row, column=col, pady=(8, 0))
            vsSlider = ttk.Scale(slidersContainer, from_=0, to=5, length=200, orient="horizontal", value=modeValues["VS"], command=lambda value: AVSensChange(value, "VS"))
            vsSlider.grid(row=row+1, column=col, padx=20)
            updateRowCol()

        # shared VVI and AAI slider
        if mode == "VVI" or mode == "AAI":
            # #hysterisis slider
            # hystLabel = tk.Label(settingsPage, text=f"HYST: {modeValues['HYST']} ppm")
            # hystLabel.pack(pady=(10,0))

            # hystSlider = ttk.Scale(settingsPage, from_=0, to=175, length=200, orient="horizontal", value=modeValues["HYST"], command=lambda value:LRLHChange(value, "HYST"))
            # hystSlider.pack()

            # rate smoothing slider
            rsLabel = tk.Label(slidersContainer, text=f"RS: {modeValues['RS']} %")
            rsLabel.grid(row=row, column=col, pady=(8, 0))
            rsSlider = ttk.Scale(slidersContainer, from_=0, to=25, length=200, orient="horizontal", value=modeValues["RS"], command=lambda value: generalChange(value, 3, "RS", "%"))
            rsSlider.grid(row=row+1, column=col, padx=20)
            updateRowCol()

        # Bottom buttons to save and go back
        buttonFrame = tk.Frame(settingsPage)
        buttonFrame.pack(side="bottom", fill="x")

        # Copies modified data to the storage and the current user
        def saveData():
            self.userStorage.modifyUserData(self.currentUser["username"], mode, modeValues)
            self.currentUser[mode] = modeValues
            messagebox.showinfo("Save Successful", "Settings have been saved!", parent=self.box)

        # Save, Back, and Flash to Pacemaker buttons
        saveButton = tk.Button(buttonFrame, text="Save", font=self.subtextFont, padx=40, pady=3, command=saveData)
        saveButton.pack(side="right", padx=5, pady=5)

        backButton = tk.Button(buttonFrame, text="Back", font=self.subtextFont, padx=40, pady=3, command=self.homePage)
        backButton.pack(side="left", padx=5, pady=5)

        # Code for flashing to the Pacemaker
        def flashCode():
            messagebox.showinfo("Settings Flash Successful", "Settings have been flashed to the Pacemaker!", parent=self.box)

        flashButton = tk.Button(buttonFrame, text="Flash to Pacemaker", font=self.subtextFont, command=flashCode, padx=40, pady=3)
        flashButton.pack(side="bottom", padx=5, pady=5)