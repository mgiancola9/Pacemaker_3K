import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class PacemakerInterface:
    # Defines all initial values/protocols for the pages
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

    # Clears the current page, and redirects to the new one
    def redirectPage(self):
        # Goes through each active frame and deletes components in frame before deleting itself
        for frame in self.box.winfo_children():
            for widget in frame.winfo_children():
                widget.destroy()
            frame.destroy()

        # Creates new frame for the current page
        newPage = tk.Frame(self.box)
        newPage.pack(fill=tk.BOTH, expand=True)
        return newPage

    # Home page when user is logged in
    def homePage(self, currentUser = None):
        homePage = self.redirectPage()
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

        egramButton = tk.Button(homePage, text="egram", font=self.subtextFont, command=self.egramPage, width=12, pady=3)
        egramButton.pack()

        # Logout section
        logoutButton = tk.Button(homePage, text="Logout", font=self.subtextFont, command=self.loginInterface.startPage, padx=40, pady=3)
        logoutButton.pack(side="bottom", anchor="se", padx=5, pady=5)

    # Pacing mode pages
    def settingsPage(self, mode):
        settingsPage = self.redirectPage()

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
        def VAPWChange(value, VorA):
            value = float(value)
            if value <= 0.1:
                roundedValue = 0.05
            elif value <= 1.9:  # extra round to keep out fp rounding errors
                roundedValue = round(round(value / 0.1) * 0.1, 1)

            modeValues[VorA] = roundedValue
            if VorA == "APW":
                apwLabel.config(text=f"APW: {roundedValue} ms")
            elif VorA == "VPW":
                vpwLabel.config(text=f"VPW: {roundedValue} ms")

        # AS and VS update when the slider changes
        def AVSensChange(value, VorA):
            value = float(value)
            if 0.25 <= value <= 0.375:
                roundedValue = 0.25
            elif value <= 0.625:
                roundedValue = 0.5
            elif value <= 0.875:
                roundedValue = 0.75
            elif value <= 1:
                roundedValue = 1.0
            elif value <= 10:
                roundedValue = round(value / 0.5) * 0.5

            modeValues[VorA] = roundedValue
            if VorA == "AS":
                asLabel.config(text=f"AS: {roundedValue} mV")
            elif VorA == "VS":
                vsLabel.config(text=f"VS: {roundedValue} mV")

        # AA and VA update when the slider changes
        def VAAmpChange(value, VorA):
            value = float(value)
            if value < 0.5:
                roundedValue = 0
            elif value < 3.2:
                roundedValue = round(round(value / 0.1) * 0.1, 1)
            elif value < 3.35:
                roundedValue = 3.2
            elif value < 3.5:
                roundedValue = 3.5
            elif value <= 7:
                roundedValue = round(value / 0.5, 1) * 0.5

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

        # LRL slider for all modes
        lrlLabel = tk.Label(settingsPage, text=f"LRL: {modeValues['LRL']} ppm")
        lrlLabel.pack(pady=(8, 0))

        lrlSlider = ttk.Scale(settingsPage, from_=30, to=175, length=200, orient="horizontal", value=modeValues["LRL"],
                             command=lambda value: LRLHChange(value, "LRL"))
        lrlSlider.pack()

        # URL slider for all modes
        urlLabel = tk.Label(settingsPage, text=f"URL: {modeValues['URL']} ppm")
        urlLabel.pack(pady=(8, 0))

        urlSlider = ttk.Scale(settingsPage, from_=50, to=175, length=200, orient="horizontal", value=modeValues["URL"],
                              command=lambda value: generalChange(value, 5, "URL", "ppm"))
        urlSlider.pack()

        # Sliders for AOO and AAI
        if mode == "AOO" or mode == "AAI":
            aaLabel = tk.Label(settingsPage, text=f"AA: {modeValues['AA']} V")
            aaLabel.pack(pady=(8, 0))

            aaSlider = ttk.Scale(settingsPage, from_=0, to=7, length=200, orient="horizontal", value=modeValues["AA"],
                                 command=lambda value: VAAmpChange(value, "AA"))
            aaSlider.pack()

            apwLabel = tk.Label(settingsPage, text=f"APW: {modeValues['APW']} ms")
            apwLabel.pack(pady=(8, 0))

            apwSlider = ttk.Scale(settingsPage, from_=0.05, to=1.9, length=200, orient="horizontal",
                                  value=modeValues["APW"], command=lambda value: VAPWChange(value, "APW"))
            apwSlider.pack()

        # Sliders for VOO and VII
        elif mode == "VOO" or mode == "VVI":
            vaLabel = tk.Label(settingsPage, text=f"VA: {modeValues['VA']} V")
            vaLabel.pack(pady=(8, 0))

            vaSlider = ttk.Scale(settingsPage, from_=0, to=7, length=200, orient="horizontal", value=modeValues["VA"],
                                 command=lambda value: VAAmpChange(value, "VA"))
            vaSlider.pack()

            vpwLabel = tk.Label(settingsPage, text=f"VPW: {modeValues['VPW']} ms")
            vpwLabel.pack(pady=(8, 0))

            vpwSlider = ttk.Scale(settingsPage, from_=0.05, to=1.9, length=200, orient="horizontal",
                                  value=modeValues["VPW"], command=lambda value: VAPWChange(value, "VPW"))
            vpwSlider.pack()

        # Sliders only for AAI
        if mode == "AAI":
            arpLabel = tk.Label(settingsPage, text=f"ARP: {modeValues['ARP']} ms")
            arpLabel.pack(pady=(8, 0))

            arpSlider = ttk.Scale(settingsPage, from_=150, to=500, length=200, orient="horizontal",
                                  value=modeValues["ARP"], command=lambda value: generalChange(value, 10, "ARP", "ms"))
            arpSlider.pack()

            asLabel = tk.Label(settingsPage, text=f"AS: {modeValues['AS']} mV")
            asLabel.pack(pady=(8, 0))

            asSlider = ttk.Scale(settingsPage, from_=0.25, to=10, length=200, orient="horizontal",
                                 value=modeValues["AS"], command=lambda value: AVSensChange(value, "AS"))
            asSlider.pack()

            pvarpLabel = tk.Label(settingsPage, text=f"PVARP: {modeValues['PVARP']} ms")
            pvarpLabel.pack(pady=(8, 0))

            pvarpSlider = ttk.Scale(settingsPage, from_=150, to=500, length=200, orient="horizontal",
                                   value=modeValues["PVARP"], command=lambda value: generalChange(value, 10, "PVARP", "ms"))
            pvarpSlider.pack()

        # Sliders only for VVI
        elif mode == "VVI":
            vrpLabel = tk.Label(settingsPage, text=f"VRP: {modeValues['VRP']} ms")
            vrpLabel.pack(pady=(8, 0))

            vrpSlider = ttk.Scale(settingsPage, from_=150, to=500, length=200, orient="horizontal",
                                  value=modeValues["VRP"], command=lambda value: generalChange(value, 10, "VRP", "ms"))
            vrpSlider.pack()

            vsLabel = tk.Label(settingsPage, text=f"VS: {modeValues['VS']} mV")
            vsLabel.pack(pady=(8, 0))

            vsSlider = ttk.Scale(settingsPage, from_=0.25, to=10, length=200, orient="horizontal",
                                 value=modeValues["VS"], command=lambda value: AVSensChange(value, "VS"))
            vsSlider.pack()

        # shared VVI and AAI slider
        if mode == "VVI" or mode == "AAI":
            # #hysterisis slider
            # hystLabel = tk.Label(settingsPage, text=f"HYST: {modeValues['HYST']} ppm")
            # hystLabel.pack(pady=(10,0))

            # hystSlider = ttk.Scale(settingsPage, from_=0, to=175, length=200, orient="horizontal", value=modeValues["HYST"], command=lambda value:LRLHChange(value, "HYST"))
            # hystSlider.pack()

            # rate smoothing slider
            rsLabel = tk.Label(settingsPage, text=f"RS: {modeValues['RS']} %")
            rsLabel.pack(pady=(10, 0))

            rsSlider = ttk.Scale(settingsPage, from_=0, to=25, length=200, orient="horizontal", value=modeValues["RS"],
                                 command=lambda value: generalChange(value, 3, "RS", "%"))
            rsSlider.pack()

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

    # Page to display egram graph
    def egramPage(self):
        egramPage = self.redirectPage()

        # Create the egram graph (add code here to create the graph)

        backButton = tk.Button(egramPage, text="Back", font=self.subtextFont, command=self.homePage, padx=40, pady=3)
        backButton.pack(side="bottom", anchor="sw", padx=5, pady=5)