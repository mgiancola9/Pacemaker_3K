import tkinter as tk

# Sets up GUI and size
box = tk.Tk()
box.title("Pacemaker GUI")
box.geometry("500x500")
box.minsize(400, 300)

# Variables to use for text font
titleFont = ('Helvatical bold', 14)
subtextFont = ('Helvatical bold', 12, "bold")

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

    loginButton = tk.Button(startPage, text ="Login", font=subtextFont, command=loginPage, padx=50, pady=3)
    loginButton.pack(expand=True, pady=(0,20))  

    registerButton = tk.Button(startPage, text ="Register", font=subtextFont, command=registerPage, padx=40, pady=3)
    registerButton.pack(side="top", expand=True)  

# Login page
def loginPage():
    loginPage = tk.Frame(box)
    loginPage.pack(fill=tk.BOTH, expand=True)
    redirectPage(loginPage)

    title = tk.Label(loginPage, text="Login to Existing Patient", font=titleFont, bg="sienna1", height=2)
    title.pack(fill=tk.BOTH)

    backButton = tk.Button(loginPage, text ="Back", font=subtextFont, command=startPage, padx=40, pady=3)
    backButton.pack(side="bottom", anchor="sw", padx=5, pady=5)

# Register page
def registerPage():
    registerPage = tk.Frame(box)
    registerPage.pack(fill=tk.BOTH, expand=True)
    redirectPage(registerPage)

    title = tk.Label(registerPage, text="Register New Patient", font=titleFont, bg="lightgreen", height=2)
    title.pack(fill=tk.BOTH)

    usernameTitle = tk.Label(registerPage, text="Username", font=subtextFont)
    usernameTitle.pack(fill=tk.BOTH, pady=(20,0))
    usernameEntry = tk.Entry(registerPage)
    usernameEntry.pack()

    passwordTitle = tk.Label(registerPage, text="Password", font=subtextFont)
    passwordTitle.pack(fill=tk.BOTH, pady=(20,0))
    passwordEntry = tk.Entry(registerPage)
    passwordEntry.pack()

    backButton = tk.Button(registerPage, text ="Back", font=subtextFont, command=startPage, padx=40, pady=3)
    backButton.pack(side="bottom", anchor="sw", padx=5, pady=5)


# Start GUI with start page
startPage()
box.mainloop()