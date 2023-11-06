import tkinter as tk
# from tkinter import messagebox
# from tkinter import ttk

class EgramInterface:
    def __init__(self, app, box, pacemakerInterface):
        # Sets up frame to put all components on
        self.box = box

        # Variable to hold the current user logged in
        self.currentUser = None

        # Variables to use for text font
        self.titleFont = ('Helvatical bold', 14)
        self.subtextFont = ('Helvatical bold', 12, "bold")

        # Defines an instance of the user storage and starts GUI with starting page
        self.app = app
        self.pacemakerInterface = pacemakerInterface

    # Page to display egram graph, passed with currentUser to communicate with the pacemakerInterface class
    def egramPage(self, currentUser):
        egramPage = self.app.redirectPage()
        self.currentUser = currentUser

        # Create the egram graph (add code here to create the graph)

        backButton = tk.Button(egramPage, text="Back", font=self.subtextFont, command=self.pacemakerInterface.homePage, padx=40, pady=3)
        backButton.pack(side="bottom", anchor="sw", padx=5, pady=5)