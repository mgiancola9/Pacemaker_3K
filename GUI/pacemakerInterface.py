import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from egramInterface import EgramInterface
import serial
import serial.tools.list_ports



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

        # Calls polling function to detect whether pacemaker is connected, for every second.
        self.deviceStatus = "Disconnected"
        self.loggedIn = True
        self.deviceStatusDisplay = None


    #########SERIAL CODE START ###################################################################################################################
    
    # Constantly displays status of device
    def displayDeviceStatus(self, initial=False):
        # Do not check device if user is not logged in
        if not self.loggedIn:
            return
        deviceConnected = self.detectDeviceStatus()
        
        # If device has just been connected, set device status true and inform the user
        if deviceConnected and self.deviceStatus == "Disconnected":
            self.deviceStatus = "Connected"
            if not initial:             # If this is the initial login, do not notify the user!

                if self.newDevice():    # If this is a new device, notify the user!
                    messagebox.showinfo("Pacemaker Connected", "NEW Pacemaker device has been connected!", parent=self.box)
                else:
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
    def detectDeviceStatus(self):
        # Checks each available port and sees if pacemaker device is one of them
        pacemakerName = "JLink CDC UART Port"
        ports = serial.tools.list_ports.comports()

        for port, desc, hwid in sorted(ports):
            if pacemakerName in desc:
                return True

        return False
    
    def deviceidentifier(self):
        # Checks each available port and sees if pacemaker device is one of them and then returns the hwid code
        pacemakerName = "JLink CDC UART Port"
        ports = serial.tools.list_ports.comports()

        for port, desc, hwid in sorted(ports):
            if pacemakerName in desc:
                return str(hwid)
            else: 
                print ("error with device name")

        return ""
    
    def newDevice(self):
        device_name = self.deviceidentifier()
        if device_name in self.currentUser['Devices']:
            return False
        
        #if it isn't in the list, add it
        self.currentUser['Devices'].append(device_name)
        return True

    #########SERIAL CODE END ###################################################################################################################

    # Home page when user is logged in. Takes currentUser parameter to communicate between loginInterface class
    def homePage(self, currentUser = None, newLogin=False):
        homePage = self.app.redirectPage()
        if newLogin:
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

        AOORButton = tk.Button(buttonsContainer, text="AOOR", font=self.subtextFont, width=12, pady=3, command=lambda: self.settingsPage("AOOR"))
        AOORButton.grid(row=2, column=0, padx=10, pady=5)

        AAIRButton = tk.Button(buttonsContainer, text="AAIR", font=self.subtextFont, width=12, pady=3, command=lambda: self.settingsPage("AAIR"))
        AAIRButton.grid(row=2, column=1, padx=10, pady=5)

        VOORButton = tk.Button(buttonsContainer, text="VOOR", font=self.subtextFont, width=12, pady=3, command=lambda: self.settingsPage("VOOR"))
        VOORButton.grid(row=3, column=0, padx=10, pady=5)

        VVIRButton = tk.Button(buttonsContainer, text="VVIR", font=self.subtextFont, width=12, pady=3, command=lambda: self.settingsPage("VVIR"))
        VVIRButton.grid(row=3, column=1, padx=10, pady=5)

        # Device status section
        self.deviceStatusDisplay = tk.Label(homePage, text=f"Device Status: {self.deviceStatus}", font=self.subtextFont, fg='green' if self.deviceStatus == 'Connected' else 'red')
        self.deviceStatusDisplay.pack(pady=(30, 0))
        deviceDescription = tk.Label(homePage, text="Connect or disconnect the device from the USB port.", font=self.subtextFont)
        deviceDescription.pack(pady=(10, 10))

        # Egram section
        egramDescription = tk.Label(homePage, text="Develop egram data.", font=self.subtextFont)
        egramDescription.pack(pady=(20, 10))
        egramButton = tk.Button(homePage, text="egram", font=self.subtextFont, command=lambda currentUser=self.currentUser: self.egramInterface.egramPage(currentUser), width=12, pady=3)
        egramButton.pack()

        # Logout section
        def logout():
            self.loggedIn = False
            self.loginInterface.startPage()

        logoutButton = tk.Button(homePage, text="Logout", font=self.subtextFont, command=logout, padx=40, pady=3)
        logoutButton.pack(side="bottom", anchor="se", padx=5, pady=5)

        # Starts detecting if device has been connected or not
        if newLogin:
            self.loggedIn = True
            self.displayDeviceStatus(initial=True)

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
        # Updated for ass 2, now simple 0-5V interval with .1 increments
        def VAAmpChange(value, VorA):
            value = float(value)
            if 0 <= value <= 5 :
                roundedValue = round(round(value / 0.1) * 0.1, 1)

            modeValues[VorA] = roundedValue
            if VorA == "AA":
                aaLabel.config(text=f"AA: {roundedValue} V")
            elif VorA == "VA":
                vaLabel.config(text=f"VA: {roundedValue} V")

        # Updates ACTIV for slider. Also is used to initialize string for label, since it will be as int at first
        def ACTIVChange(value, Activ, initial=False):
            value = float(value)
            if 0.75 <= value < 1:
                roundedValue = 0.75
                mode = "V-Low"
            if 1 <= value < 1.5:
                roundedValue = 1
                mode = "Low"
            if 1.5 <= value < 2:
                roundedValue = 1.75
                mode = "Med-Low"
            if 2 <= value < 2.5:
                roundedValue = 2
                mode = "Med"
            if 2.5 <= value < 3:
                roundedValue = 2.75
                mode = "Med-High"
            if 3 <= value < 3.5:
                roundedValue = 3
                mode = "High"
            if value >= 3.5:
                roundedValue = 3.75
                mode = "V-High"

            # If this is the initial call of this method for the label, return the mode to be labelled
            if initial:
                return mode
            
            # Else, modify the slider and relabel the label as usual
            modeValues[Activ] = roundedValue
            activLabel.config(text=f"ACTIV: {mode} V")

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
            elif type == "MSR":
                msrLabel.config(text=f"MSR: {roundedValue} {unit}")
            elif type == "REACT":
                reactLabel.config(text=f"REACT: {roundedValue} {unit}")
            elif type == "RESPF":
                respfLabel.config(text=f"RESPF: {roundedValue} {unit}")
            elif type == "RECOVT":
                recovtLabel.config(text=f"RECOVT: {roundedValue} {unit}")

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
        if mode == "AOO" or mode == "AAI" or mode == "AOOR" or mode == "AAIR":
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
        if mode == "VOO" or mode == "VVI" or mode == "VOOR" or mode == "VVIR":
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
        if mode == "AAI" or mode == "AAIR":
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
        elif mode == "VVI" or mode == "VVIR":
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
        if mode == "VVI" or mode == "AAI" or mode == "VVIR" or mode == "AAIR":
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

        #exclusive for AAIR, VVIR, AOOR, VOOR
        if mode == "VOOR" or mode == "AOOR" or mode == "VVIR" or mode == "AAIR":
            msrLabel = tk.Label(slidersContainer, text=f"MSR: {modeValues['MSR']} ppm")
            msrLabel.grid(row=row, column=col, pady=(8, 0))
            msrSlider = ttk.Scale(slidersContainer, from_=50, to=175, length=200, orient="horizontal", value=modeValues["MSR"], command=lambda value: generalChange(value, 5, "MSR", "ppm"))
            msrSlider.grid(row=row+1, column=col, padx=20)
            updateRowCol()

            # Calls ACTIVChange initially to receive string on what the current value is, instead of an int
            activLabel = tk.Label(slidersContainer, text=f"ACTIV: {ACTIVChange(modeValues['ACTIV'], 'ACTIV', True)} V")
            activLabel.grid(row=row, column=col, pady=(8, 0))
            activSlider = ttk.Scale(slidersContainer, from_=0.75, to=3.75, length=200, orient="horizontal", value=modeValues["ACTIV"], command=lambda value: ACTIVChange(value, "ACTIV"))
            activSlider.grid(row=row+1, column=col, padx=20)
            updateRowCol()

            reactLabel = tk.Label(slidersContainer, text=f"REACT: {modeValues['REACT']} sec")
            reactLabel.grid(row=row, column=col, pady=(8, 0))
            reactSlider = ttk.Scale(slidersContainer, from_=10, to=50, length=200, orient="horizontal", value=modeValues["REACT"], command=lambda value: generalChange(value, 10, "REACT", "sec"))
            reactSlider.grid(row=row+1, column=col, padx=20)
            updateRowCol()

            respfLabel = tk.Label(slidersContainer, text=f"RESPF: {modeValues['RESPF']} ")
            respfLabel.grid(row=row, column=col, pady=(8, 0))
            respfSlider = ttk.Scale(slidersContainer, from_=1, to=16, length=200, orient="horizontal", value=modeValues["RESPF"], command=lambda value: generalChange(value, 1, "RESPF", "sec"))
            respfSlider.grid(row=row+1, column=col, padx=20)
            updateRowCol()

            recovtLabel = tk.Label(slidersContainer, text=f"RECOVT: {modeValues['RECOVT']} min")
            recovtLabel.grid(row=row, column=col, pady=(8, 0))
            recovtSlider = ttk.Scale(slidersContainer, from_=2, to=16, length=200, orient="horizontal", value=modeValues["RECOVT"], command=lambda value: generalChange(value, 1, "RECOVT", "min"))
            recovtSlider.grid(row=row+1, column=col, padx=20)
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