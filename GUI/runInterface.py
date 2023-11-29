import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime, timedelta
import numpy as np
from tkinter import *

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
        self.ax_atrial = self.fig.add_subplot(131, aspect='equal')
        self.ax_ventricular = self.fig.add_subplot(132, aspect='equal')
        self.ax_both = self.fig.add_subplot(133, aspect='equal')

        # Set labels for the x and y axes and titles
        self.ax_atrial.set_xlabel('Time (ms)')
        self.ax_atrial.set_ylabel('Voltage (mV)')
        self.ax_ventricular.set_xlabel('Time (ms)')
        self.ax_ventricular.set_ylabel('Voltage (mV)')
        self.ax_both.set_xlabel('Time (ms)')
        self.ax_both.set_ylabel('Voltage (mV)')
        self.ax_atrial.set_title('Atrial Plot')
        self.ax_ventricular.set_title('Ventricular Plot')
        self.ax_both.set_title('Both Plots')

        self.stopGraph = False
        self.egramData = {'Atrial': [], 'Ventricular': []}  # Placeholder for Egram data
        self.timer_interval = 75  # Time interval in millisecond
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
        def runEgram():
            mode = curMode.get()

            # Do not run if pacemaker is not connected
            if self.serialCom.deviceStatus == "Disconnected":
                messagebox.showinfo("Run Unsuccessful", "Pacemaker must be connected before displaying Egram.", parent=self.box)
                return
            # Do not run if a mode has not been selected
            elif mode == "Select a specified mode":
                messagebox.showinfo("Run Unsuccessful", "Select a mode before running the pacemaker.", parent=self.box)
                return
            
            startTime = datetime.now()
            updateEgramData(mode, startTime)

        def updateEgramData(mode, startTime):
            # Fetch Egram data from the pacemaker using send_parameters method
            egramData = self.serialCom.receiveEgramData(self.currentUser[mode],mode)

            if not self.stopGraph:
                # Calculate the elapsed time
                elapsed_time = datetime.now() - startTime

                # Update atrial graph
                self.egramData['Atrial'].append((elapsed_time, egramData[0]))
                updateSubplot(self.ax_atrial, self.egramData['Atrial'], 'Atrial')

                # Update ventricular graph
                self.egramData['Ventricular'].append((elapsed_time, egramData[1]))
                updateSubplot(self.ax_ventricular, self.egramData['Ventricular'], 'Ventricular')

                # Update both graph
                self.egramData['Atrial'].append((elapsed_time, egramData[0]))
                self.egramData['Ventricular'].append((elapsed_time, egramData[1]))
                updateSubplot(self.ax_atrial, self.egramData['Atrial'], 'Atrial')
                updateSubplot(self.ax_ventricular, self.egramData['Ventricular'], 'Ventricular')

                # Schedule the next update after the specified time interval
                self.box.after(self.timer_interval, updateEgramData, mode, startTime)

        def updateSubplot(axis, new_data, plot_title):
            # Clear the axis
            axis.clear()

            # Extract timestamps and data
            timestamps, voltage_data = zip(*new_data)

            # Calculate the elapsed time in seconds for each data point
            elapsed_times = [(timestamp - timestamps[0]).total_seconds() for timestamp in timestamps]

            # Plot the data
            axis.plot(elapsed_times, voltage_data, 'b-')
            axis.set_title(plot_title)

            # Set x-axis limits dynamically based on elapsed time
            max_elapsed_time = max(elapsed_times)
            min_elapsed_time = max(0, max_elapsed_time - 15)  # Keep a time frame of 50 seconds
            axis.set_xlim(min_elapsed_time, max_elapsed_time)

            # Redraw the canvas
            self.canvas.draw()

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