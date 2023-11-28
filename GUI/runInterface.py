import tkinter as tk
from tkinter import messagebox

class RunInterface:
    def __init__(self, app, box, pacemakerInterface, serialCom):
        # Sets up frame to put all components on
        self.box = box

        # Variable to hold the current user logged in
        self.currentUser = None

        # Variables to use for text font
        self.titleFont = ('Helvatical bold', 14)
        self.subtextFont = ('Helvatical bold', 12, "bold")

        # Defines instances of other classes
        self.app = app
        self.pacemakerInterface = pacemakerInterface
        self.serialCom = serialCom

    # Page to run pacemaker and display egram
    def runPage(self, currentUser):
        runPage = self.app.redirectPage()
        self.currentUser = currentUser

        title = tk.Label(runPage, text=f"Activate Pacemaker", font=self.titleFont, bg="spring green", height=2)
        title.pack(fill=tk.BOTH)

        # Top frame to select and run modes, and display egram
        runFrame = tk.Frame(runPage)
        runFrame.pack(side="top", fill="x", pady=(20,0), padx=(5,5))

        # Drop down menu to select menu to run
        modes = ["VOO", "VVI", "AOO", "AAI", "VVIR", "VOOR", "AAIR", "AOOR"]
        curMode = tk.StringVar(runFrame)
        curMode.set("Select a specified mode")
        
        selectMode = tk.OptionMenu(runFrame, curMode, *modes)
        selectMode.config(width=20) 
        selectMode.pack(side="left", padx=5, pady=5)

        # Activate the egram graphs
        def runEgram():
            # Do not run if pacemaker is not connected
            if self.serialCom.deviceStatus == "Disconnected":
                messagebox.showinfo("Run Unsuccessful", "Pacemaker must be connected before displaying Egram.", parent=self.box)
                return

        egramButton = tk.Button(runFrame, text="Activate Egram", command=runEgram, font=self.subtextFont, padx=20, pady=3)
        egramButton.pack(side="right", padx=5, pady=5)

        # Run the pacemaker
        def runPacemaker():
            mode = curMode.get()

            # Do not run if pacemaker is not connected
            if self.serialCom.deviceStatus == "Disconnected":
                messagebox.showinfo("Run Unsuccessful", "Pacemaker must be connected before running.", parent=self.box)
                return
            # Do not run if a mode has not been selected
            elif mode == "Select a specified mode":
                messagebox.showinfo("Run Unsuccessful", "Select a mode before running the pacemaker.", parent=self.box)
                return
            
            # Write programmable parameters to the board
            self.serialCom.writeToPacemaker(self.currentUser[mode], mode)

        runButton = tk.Button(runFrame, text="Run mode", command=runPacemaker, font=self.subtextFont, padx=40, pady=3)
        runButton.pack(side="bottom", padx=5, pady=5)

        # Back button
        backButton = tk.Button(runPage, text="Back", font=self.subtextFont, command=self.pacemakerInterface.homePage, padx=40, pady=3)
        backButton.pack(side="bottom", anchor="sw", padx=5, pady=5)