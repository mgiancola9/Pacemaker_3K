import tkinter as tk

# Sets up GUI and size
box = tk.Tk()
box.title("Pacemaker GUI")
box.geometry("500x500")
box.minsize(400, 300)

# Variables to use for text font
titleFont = ('Helvatical bold',14)
subtextFont = ('Helvatical bold',12)

# Clears the current page, and redirects to the new one
currentPage = None
def redirectPage(newPage):
    global currentPage
    if currentPage:
        currentPage.pack_forget()

    currentPage = newPage
    newPage.pack(fill=tk.BOTH)

# Start page
def startPage():
    startPage = tk.Frame(box)
    redirectPage(startPage)

    title = tk.Label(startPage, text="Welcome to the PULSEMASTER Interface", font=titleFont, bg="lightblue", height=2)
    title.pack(fill=tk.BOTH)

    description = tk.Label(startPage, text="Login or register a new patient below.", font=subtextFont, height=4)
    description.pack(fill=tk.BOTH)

    loginButton = tk.Button(startPage, text ="Login", font=subtextFont,command=loginPage, padx=50, pady=3)
    loginButton.pack(expand=True)  

    space = tk.Label(startPage, text="", height=1)
    space.pack()

    registerButton = tk.Button(startPage, text ="Register", font=subtextFont, padx=40, pady=3)
    registerButton.pack(side="top", expand=True)  

# Login page
def loginPage():
    loginPage = tk.Frame(box)
    redirectPage(loginPage)

    title = tk.Label(loginPage, text="Yuh", font=titleFont, bg="lightblue", height=2)
    title.pack(fill=tk.BOTH)


# Start GUI with start page
startPage()
box.mainloop()