import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

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

        # Create a Figure with two subplots
        self.fig = Figure(figsize=(10, 4), dpi=100, facecolor='#D3D3D3')
        self.fig.subplots_adjust(wspace=0.4)

        # Set plots
        self.ax_atrial = self.fig.add_subplot(131)
        self.ax_ventricular = self.fig.add_subplot(132)
        self.ax_both = self.fig.add_subplot(133)

        # Set labels for the x and y axes and titles
        self.ax_atrial.set_xlabel('Time (ms)')
        self.ax_atrial.set_ylabel('Voltage (mV)')
        self.ax_ventricular.set_xlabel('Time (ms)')
        self.ax_ventricular.set_ylabel('Voltage (mV)')
        self.ax_both.set_xlabel('Time (ms)')
        self.ax_both.set_ylabel('Voltage (mV)')
        self.ax_atrial.set_title('Atrial')
        self.ax_ventricular.set_title('Ventricular')
        self.ax_both.set_title('Atrial/Ventricular')

        self.stopGraph = False
        self.graphOn = False
        self.egramData = {'Atrial': [], 'Ventricular': []}  # Placeholder for Egram data
        self.timer_interval = 1750  # Time interval in millisecond
        self.canvas = None

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

        # Create a canvas to display the Figure
        self.canvas = FigureCanvasTkAgg(self.fig, runPage)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Activate the egram graphs
        def runEgram(run=False):
            mode = curMode.get()

            # Do not run if pacemaker is not connected
            if self.serialCom.deviceStatus == "Disconnected":
                messagebox.showinfo("Run Unsuccessful", "Pacemaker must be connected before displaying Egram.", parent=self.box)
                return
            # Set default mode since egram does not care about mode
            elif mode == "Select a specified mode":
                mode = "VOO"

            # Waits for all serial com to finish up before running
            if not run:
                self.box.attributes("-disabled", True)
                self.box.after(4000, lambda: runEgram(run=True))
                return
            else:
                self.box.attributes("-disabled", False)
            
            # Change egram button
            egramButton.config(text="Stop Egram", command=stopEgram)
            
            # Clear canvis before drawing and data
            self.ax_atrial.clear()
            self.ax_ventricular.clear()
            self.ax_both.clear()
            self.egramData = {'Atrial': [], 'Ventricular': []}
            
            # Start graphing
            startTime = datetime.now()
            self.graphOn = True
            updateEgramData(mode, startTime)

        def updateEgramData(mode, startTime):
            # Fetch Egram data from the pacemaker using send_parameters method
            egramData = self.serialCom.receiveEgramData(self.currentUser[mode],mode)

            if not self.stopGraph:
                # Calculate the elapsed time
                elapsed_time = datetime.now() - startTime

                # Update data
                self.egramData['Atrial'].append((elapsed_time, egramData[0]))
                self.egramData['Ventricular'].append((elapsed_time, egramData[1]))

                # Update graphs
                updateSubplot(self.ax_atrial, self.egramData['Atrial'], 'Atrial')
                updateSubplot(self.ax_ventricular, self.egramData['Ventricular'], 'Ventricular')
                updateSubplot(self.ax_both, self.egramData['Atrial'], 'Atrial/Ventricular')
                updateSubplot(self.ax_both, self.egramData['Ventricular'], 'Atrial/Ventricular', clear=False)

                # Schedule the next update after the specified time interval
                self.box.after(self.timer_interval, updateEgramData, mode, startTime)

            self.stopGraph = False

        def updateSubplot(axis, new_data, plot_title, clear=True):
            # Clear the axis
            if clear:
                axis.clear()

            # Extract timestamps and data
            timestamps, voltage_data = zip(*new_data)

            # Calculate the elapsed time in seconds for each data point
            elapsed_times = [(timestamp - timestamps[0]).total_seconds() for timestamp in timestamps]

            # Plot the data
            if plot_title == "Atrial":
                axis.plot(elapsed_times, voltage_data, 'r-')
            elif plot_title == "Ventricular":
                axis.plot(elapsed_times, voltage_data, 'b-')
            elif plot_title == "Atrial/Ventricular" and clear:
                axis.plot(elapsed_times, voltage_data, 'r-')
            elif plot_title == "Atrial/Ventricular" and not clear:
                axis.plot(elapsed_times, voltage_data, 'b-')
            axis.set_title(plot_title)

            # Set x-axis limits dynamically based on elapsed time
            max_elapsed_time = max(elapsed_times)
            min_elapsed_time = max(0, max_elapsed_time - 30)  # Keep a time frame of 50 seconds
            axis.set_xlim(min_elapsed_time, max_elapsed_time)

            # Redraw the canvas
            self.canvas.draw()

        # Stops egram when button clicked
        def stopEgram(back=False):
            egramButton.config(text="Activate Egram", command=runEgram)
            self.stopGraph = True
            self.graphOn = False
            if back:
                self.pacemakerInterface.homePage()

        egramButton = tk.Button(runFrame, text="Activate Egram", command=runEgram, font=self.subtextFont, padx=20, pady=3)
        egramButton.pack(side="right", padx=5, pady=5)

        # Run the pacemaker
        def runPacemaker(run=False):
            mode = curMode.get()

            # Do not run if pacemaker is not connected
            if self.serialCom.deviceStatus == "Disconnected":
                messagebox.showinfo("Run Unsuccessful", "Pacemaker must be connected before running.", parent=self.box)
                return
            # Do not run if a mode has not been selected
            elif mode == "Select a specified mode":
                messagebox.showinfo("Run Unsuccessful", "Select a mode before running the pacemaker.", parent=self.box)
                return
            
            # Waits for all serial com to finish up before running
            if self.graphOn:
                stopEgram()
            if not run:
                self.box.attributes("-disabled", True)
                self.box.after(4000, lambda: runPacemaker(run=True))
                return
            else:
                self.box.attributes("-disabled", False)
            
            # Write programmable parameters to the board
            self.serialCom.writeToPacemaker(self.currentUser[mode], mode)

        runButton = tk.Button(runFrame, text="Run mode", command=runPacemaker, font=self.subtextFont, padx=40, pady=3)
        runButton.pack(side="bottom", padx=5, pady=5)

        # Back button
        backButton = tk.Button(runPage, text="Back", font=self.subtextFont, command=lambda: stopEgram(back=True), padx=40, pady=3)
        backButton.pack(side="bottom", anchor="sw", padx=5, pady=5)