import tkinter as tk

# Class to initialize the interface
class App:
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