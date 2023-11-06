import tkinter as tk

class App:
    # Defines all initial values/protocols for the pages
    def __init__(self, userStorage):
        # Sets up GUI frame and size
        self.box = tk.Tk()
        self.box.title("Pacemaker GUI")
        self.box.geometry("600x600")
        self.box.minsize(600, 600)

        # Initializes user storage to the instance of it passed in
        self.userStorage = userStorage

    # Saves current user data and deletes the interface
    def deleteBox(self):
        self.userStorage.saveUserData()
        self.box.destroy()

    # Function to start the GUI
    def run(self):
        self.box.protocol("WM_DELETE_WINDOW", self.deleteBox)
        self.box.mainloop()