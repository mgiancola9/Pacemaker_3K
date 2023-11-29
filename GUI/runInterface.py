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
            
            # Create a Figure with two subplots
            fig = Figure(figsize=(10, 4), dpi=100, facecolor='#D3D3D3')
            fig.subplots_adjust(wspace=0.4)

            # Set plots
            ax_atrial = fig.add_subplot(131, aspect='equal')
            ax_ventricular = fig.add_subplot(132, aspect='equal')
            ax_both = fig.add_subplot(133, aspect='equal')

            # Set labels for the x and y axes and titles
            ax_atrial.set_xlabel('Time (ms)')
            ax_atrial.set_ylabel('Voltage (mV)')
            ax_ventricular.set_xlabel('Time (ms)')
            ax_ventricular.set_ylabel('Voltage (mV)')
            ax_both.set_xlabel('Time (ms)')
            ax_both.set_ylabel('Voltage (mV)')
            ax_atrial.set_title('Atrial Plot')
            ax_ventricular.set_title('Ventricular Plot')
            ax_both.set_title('Both Plots')

            # Create a canvas to display the Figure
            canvas = FigureCanvasTkAgg(fig, runPage)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

                        
                        # Initialize data
            # time_window = 10  # seconds
            # update_interval = 100  # milliseconds

            # # Function to generate sample ECG data
            # def generate_ecg_data():
            #     t = (datetime.now() - start_time).total_seconds()
            #     atrial_data = np.sin(2 * np.pi * t / 2)  # Replace with your atrial ECG data function
            #     ventricular_data = 0.5 * np.sin(2 * np.pi * t / 2)  # Replace with your ventricular ECG data function
            #     return atrial_data, ventricular_data

            # # Function to update the plot
            # def update(frame):
            #     atrial_data, ventricular_data = generate_ecg_data()
                
            #     # Calculate the time difference between now and when the data point was received
            #     current_time = datetime.now()
            #     time_difference = (current_time - start_time).total_seconds()
                
            #     time_data.append(time_difference)  # Use time difference as x-axis value
            #     atrial_data_buffer.append(atrial_data)
            #     ventricular_data_buffer.append(ventricular_data)

            #     # Update the plot data
            #     line_atrial.set_data(time_data, atrial_data_buffer)
            #     line_ventricular.set_data(time_data, ventricular_data_buffer)

            #     # Adjust the x-axis limits after 10 seconds
            #     if time_difference > time_window:
            #         ax.set_xlim(time_difference - time_window, time_difference)

            #     # Update x-axis ticks with increasing time values
            #     plt.xticks(np.arange(max(0, time_difference - time_window), time_difference + 1, 1))

            #     # Update y-axis limits based on incoming data
            #     y_min = min(min(atrial_data_buffer), min(ventricular_data_buffer))
            #     y_max = max(max(atrial_data_buffer), max(ventricular_data_buffer))
            #     ax.set_ylim(y_min - 0.2, y_max + 0.2)

            #     # Explicitly update the plot
            #     plt.draw()
            #     plt.pause(0.01)  # Adjust the pause duration as needed

            #     return line_atrial, line_ventricular

            # # Set up the figure and axes
            # fig, ax = plt.subplots()
            # ax.set_xlabel('Time (s)')
            # ax.set_ylabel('Amplitude')
            # ax.set_title('Real-time ECG Data')

            # # Initialize plot data
            # start_time = datetime.now()
            # time_data = []
            # atrial_data_buffer = []
            # ventricular_data_buffer = []

            # # Initialize the plot with empty data
            # line_atrial, = ax.plot([], [], label='Atrial ECG', color='blue')
            # line_ventricular, = ax.plot([], [], label='Ventricular ECG', color='red')

            # ax.legend()
            # ax.grid(True)

            # # Set up the animation
            # animation = FuncAnimation(fig, update, blit=False, interval=update_interval)

            # plt.show()


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