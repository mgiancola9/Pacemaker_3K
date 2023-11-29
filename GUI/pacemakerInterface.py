import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from runInterface import RunInterface
from serialCom import SerialCom

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
        self.serialCom = SerialCom(box, self)
        self.runInterface = RunInterface(app,box,self,self.serialCom)

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

        # Device status section, given as reference to serialCom so it can modify the value
        self.serialCom.deviceStatusDisplay = tk.Label(homePage, text=f"Device Status: {self.serialCom.deviceStatus}", font=self.subtextFont, fg='green' if self.serialCom.deviceStatus == 'Connected' else 'red')
        self.serialCom.deviceStatusDisplay.pack(pady=(30, 0))
        deviceDescription = tk.Label(homePage, text="Connect or disconnect the device from the USB port.", font=self.subtextFont)
        deviceDescription.pack(pady=(10, 10))

        # Egram section
        runDescription = tk.Label(homePage, text="Activate pacemaker for a specified mode.", font=self.subtextFont)
        runDescription.pack(pady=(20, 10))
        runButton = tk.Button(homePage, text="Run pacemaker", font=self.subtextFont, command=lambda currentUser=self.currentUser: self.runInterface.runPage(currentUser), width=15, pady=3)
        runButton.pack()

        # Logout section
        def logout():
            self.serialCom.loggedIn = False
            self.loginInterface.startPage()

        logoutButton = tk.Button(homePage, text="Logout", font=self.subtextFont, command=logout, padx=40, pady=3)
        logoutButton.pack(side="bottom", anchor="se", padx=5, pady=5)

        # Starts detecting if device has been connected or not
        if newLogin:
            self.serialCom.loggedIn = True
            self.serialCom.displayDeviceStatus(initial=True)

    # Pacing mode pages
    def settingsPage(self, mode):
        settingsPage = self.app.redirectPage()

        # Copies values of the current mode, to be modified then saved
        modeValues = self.currentUser[mode].copy()

        # Title for the page
        title = tk.Label(settingsPage, text=f"Pacemaker Settings - {mode}", font=self.titleFont, bg="mediumpurple", height=2)
        title.pack(fill=tk.BOTH)

        # Functions for slider changes
        def LRLChange(value):
            value = float(value)
            if 30 <= value < 50:
                roundedValue = round(value / 5) * 5
            elif 50 <= value < 90:
                roundedValue = round(value)
            elif 90 <= value <= 175:
                roundedValue = round(value / 5) * 5

            if mode == "AOOR" or mode == "AAIR" or mode == "VOOR" or mode == "VVIR":
                MSRAddition = roundedValue - modeValues["LRL"]
                modeValues["W_MSR"] += MSRAddition 
                modeValues["J_MSR"] += MSRAddition
                modeValues["R_MSR"] += MSRAddition
            modeValues["LRL"] = roundedValue
            lrlLabel.config(text=f"LRL: {roundedValue} ppm")

        # VPW and APW update when the slider changes
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
        def VAAmpChange(value, VorA):
            value = float(value)
            if 0 <= value <= 5 :
                roundedValue = round(round(value / 0.1) * 0.1, 1)

            modeValues[VorA] = roundedValue
            if VorA == "AA":
                aaLabel.config(text=f"AA: {roundedValue} V")
            elif VorA == "VA":
                vaLabel.config(text=f"VA: {roundedValue} V")

        # Return the current mode to be put for the initial label
        def initialHYSTTHRESHChange(HYST, THRESH, word=False):
            if HYST == [0.75, 1.75, 2.75] and THRESH == [1.0, 2.0, 3.0]:
                return "V-Low" if word else 0.75
            elif HYST == [0.85, 1.85, 2.85] and THRESH == [1.1, 2.1, 3.1]:
                return "Low" if word else 1
            elif HYST == [0.95, 1.95, 2.95] and THRESH == [1.2, 2.2, 3.2]:
                return "Med-Low" if word else 1.75
            elif HYST == [1.05, 2.05, 3.05] and THRESH == [1.3, 2.3, 3.3]:
                return "Med" if word else 2
            elif HYST == [1.15, 2.15, 3.15] and THRESH == [1.4, 2.4, 3.4]:
                return "Med-High" if word else 2.75
            elif HYST == [1.25, 2.25, 3.25] and THRESH == [1.5, 2.5, 3.5]:
                return "High" if word else 3
            elif HYST == [1.35, 2.35, 3.35] and THRESH == [1.6, 2.6, 3.6]:
                return "V-High" if word else 3.75

        # Updates Thresh for slider
        def HYSTTHRESHChange(value):
            value = float(value)
            if 0.75 <= value < 1:
                HYSTValue = [0.75, 1.75, 2.75]
                THRESHValue = [1.0, 2.0, 3.0]
                mode = "V-Low"
            elif 1 <= value < 1.5:
                HYSTValue = [0.85, 1.85, 2.85]
                THRESHValue = [1.1, 2.1, 3.1]
                mode = "Low"
            elif 1.5 <= value < 2:
                HYSTValue = [0.95, 1.95, 2.95]
                THRESHValue = [1.2, 2.2, 3.2]
                mode = "Med-Low"
            elif 2 <= value < 2.5:
                HYSTValue = [1.05, 2.05, 3.05]
                THRESHValue = [1.3, 2.3, 3.3]
                mode = "Med"
            elif 2.5 <= value < 3:
                HYSTValue = [1.15, 2.15, 3.15]
                THRESHValue = [1.4, 2.4, 3.4]
                mode = "Med-High"
            elif 3 <= value < 3.5:
                HYSTValue = [1.25, 2.25, 3.25]
                THRESHValue = [1.5, 2.5, 3.5]
                mode = "High"
            elif value >= 3.5:
                HYSTValue = [1.35, 2.35, 3.35]
                THRESHValue = [1.6, 2.6, 3.6]
                mode = "V-High"
            
            modeValues["W_HYST"], modeValues["J_HYST"], modeValues["R_HYST"] = HYSTValue
            modeValues["W_THRESH"], modeValues["J_THRESH"], modeValues["R_THRESH"] = THRESHValue
            hystThreshLabel.config(text=f"HYST/THRESH: {mode} V")

        # Return the current mode to be put for the initial label
        def initialMSRChange(value, word=False):
            LRL = modeValues["LRL"]
            if value == [LRL + 2, LRL + 20, LRL + 40]:
                return "V-Low" if word else 0.75
            elif value == [LRL + 4, LRL + 22, LRL + 42]:
                return "Low" if word else 1
            elif value == [LRL + 6, LRL + 24, LRL + 44]:
                return "Med-Low" if word else 1.75
            elif value == [LRL + 8, LRL + 26, LRL + 46]:
                return "Med" if word else 2
            elif value == [LRL + 10, LRL + 28, LRL + 48]:
                return "Med-High" if word else 2.75
            elif value == [LRL + 12, LRL + 30, LRL + 50]:
                return "High" if word else 3
            elif value == [LRL + 14, LRL + 32, LRL + 52]:
                return "V-High" if word else 3.75

        # Updates MSR for slider
        def MSRChange(value):
            value = float(value)
            LRL = modeValues["LRL"]
            if 0.75 <= value < 1:
                roundedValue = [LRL + 2, LRL + 20, LRL + 40]
                mode = "V-Low"
            elif 1 <= value < 1.5:
                roundedValue = [LRL + 4, LRL + 22, LRL + 42]
                mode = "Low"
            elif 1.5 <= value < 2:
                roundedValue = [LRL + 6, LRL + 24, LRL + 44]
                mode = "Med-Low"
            elif 2 <= value < 2.5:
                roundedValue = [LRL + 8, LRL + 26, LRL + 46]
                mode = "Med"
            elif 2.5 <= value < 3:
                roundedValue = [LRL + 10, LRL + 28, LRL + 48]
                mode = "Med-High"
            elif 3 <= value < 3.5:
                roundedValue = [LRL + 12, LRL + 30, LRL + 50]
                mode = "High"
            elif value >= 3.5:
                roundedValue = [LRL + 14, LRL + 32, LRL + 52]
                mode = "V-High"
            
            modeValues["W_MSR"], modeValues["J_MSR"], modeValues["R_MSR"] = roundedValue
            msrLabel.config(text=f"MSR: {mode} ppm")

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
        lrlSlider = ttk.Scale(slidersContainer, from_=30, to=175, length=200, orient="horizontal", value=modeValues["LRL"], command=lambda value: LRLChange(value))
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
            # rate smoothing slider
            rsLabel = tk.Label(slidersContainer, text=f"RS: {modeValues['RS']} %")
            rsLabel.grid(row=row, column=col, pady=(8, 0))
            rsSlider = ttk.Scale(slidersContainer, from_=0, to=25, length=200, orient="horizontal", value=modeValues["RS"], command=lambda value: generalChange(value, 3, "RS", "%"))
            rsSlider.grid(row=row+1, column=col, padx=20)
            updateRowCol()

        #exclusive for AAIR, VVIR, AOOR, VOOR
        if mode == "VOOR" or mode == "AOOR" or mode == "VVIR" or mode == "AAIR":
            msrLabel = tk.Label(slidersContainer, text=f"MSR: {initialMSRChange([modeValues['W_MSR'], modeValues['J_MSR'], modeValues['R_MSR']], word=True)} ppm")
            msrLabel.grid(row=row, column=col, pady=(8, 0))
            msrSlider = ttk.Scale(slidersContainer, from_=0.75, to=3.75, length=200, orient="horizontal", value=initialMSRChange([modeValues['W_MSR'], modeValues['J_MSR'], modeValues['R_MSR']]), command=lambda value: MSRChange(value))
            msrSlider.grid(row=row+1, column=col, padx=20)
            updateRowCol()

            # Calls THRESHChange initially to receive string on what the current value is, instead of an int
            hystThreshLabel = tk.Label(slidersContainer, text=f"HYST/THRESH: {initialHYSTTHRESHChange([modeValues['W_HYST'], modeValues['J_HYST'], modeValues['R_HYST']], [modeValues['W_THRESH'], modeValues['J_THRESH'], modeValues['R_THRESH']], word=True)} V")
            hystThreshLabel.grid(row=row, column=col, pady=(8, 0))
            hystThreshSlider = ttk.Scale(slidersContainer, from_=0.75, to=3.75, length=200, orient="horizontal", value=initialHYSTTHRESHChange([modeValues['W_HYST'], modeValues['J_HYST'], modeValues['R_HYST']], [modeValues['W_THRESH'], modeValues['J_THRESH'], modeValues['R_THRESH']]), command=lambda value: HYSTTHRESHChange(value))
            hystThreshSlider.grid(row=row+1, column=col, padx=20)
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