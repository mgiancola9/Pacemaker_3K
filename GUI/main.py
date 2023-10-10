import tkinter as tk
from tkinter import messagebox
import json

# Loads currently saved user data
try:
    with open("./GUI/userData.json", "r") as file:
        userData = json.load(file)
except FileNotFoundError:
    userData = []

# Variable to hold the current user logged in
currentUser = None

# Saves new user data to json after interface is closed
def saveUserData():
    with open('./GUI/userData.json', 'w') as file:
        json.dump(userData, file)
    box.destroy()

# Sets up GUI and size
box = tk.Tk()
box.title("Pacemaker GUI")
box.geometry("500x500")
box.minsize(500, 500)

# Variables to use for text font
titleFont = ('Helvatical bold', 14)
subtextFont = ('Helvatical bold', 12, "bold")

# Clears the current page, and redirects to the new one
def redirectPage():
    # Goes through each active frame and deletes components in frame before deleting itself
    for frame in box.winfo_children():
        for widget in frame.winfo_children():
            widget.destroy()
        frame.destroy()

    # Creates new frame for the current page
    newPage = tk.Frame(box)
    newPage.pack(fill=tk.BOTH, expand=True)
    return newPage

# Start page
def startPage():
    startPage = redirectPage()

    title = tk.Label(startPage, text="Welcome to the PULSEMASTER Interface", font=titleFont, bg="lightblue", height=2)
    title.pack(fill=tk.BOTH)

    description = tk.Label(startPage, text="Login or register a new patient below.", font=subtextFont, height=4)
    description.pack()

    loginButton = tk.Button(startPage, text ="Login", font=subtextFont, command=loginPage, padx=50, pady=3)
    loginButton.pack(pady=(0,20))  

    registerButton = tk.Button(startPage, text ="Register", font=subtextFont, command=registerPage, padx=40, pady=3)
    registerButton.pack()  

# Login page
def loginPage():
    def authenticateUser():
        username = usernameEntry.get()
        password = passwordEntry.get()

        # Check for empty fields
        if username == "" or password == "":
            messagebox.showwarning("Login Error", "Username and password cannot be empty!", parent=box)
            return

        # Check if the user exists and the password is correct
        user_found = False
        for user in userData:
            if user["username"] == username:
                user_found = True
                if user["password"] == password:
                    global currentUser
                    currentUser = user
                    homePage()
                    return
                else:
                    messagebox.showwarning("Login Error", "Incorrect password for the username provided.", parent=box)
                    return

        if not user_found:
            messagebox.showwarning("Login Error", "Username does not exist. Please register first.", parent=box)

    loginPage = redirectPage()

    title = tk.Label(loginPage, text="Login to Existing Patient", font=titleFont, bg="sienna1", height=2)
    title.pack(fill=tk.BOTH)

    usernameTitle = tk.Label(loginPage, text="Username", font=subtextFont)
    usernameTitle.pack(fill=tk.BOTH, pady=(20, 0))
    usernameEntry = tk.Entry(loginPage)
    usernameEntry.pack()

    passwordTitle = tk.Label(loginPage, text="Password", font=subtextFont)
    passwordTitle.pack(fill=tk.BOTH, pady=(20, 0))
    passwordEntry = tk.Entry(loginPage, show="*")
    passwordEntry.pack(pady=(0, 20))

    loginButton = tk.Button(loginPage, text="Login", font=subtextFont, command=authenticateUser, padx=40, pady=3)
    loginButton.pack()

    backButton = tk.Button(loginPage, text="Back", font=subtextFont, command=startPage, padx=40, pady=3)
    backButton.pack(side="bottom", anchor="sw", padx=5, pady=5)

# Register page
def registerPage():
    registerPage = redirectPage()

    title = tk.Label(registerPage, text="Register New Patient", font=titleFont, bg="lightgreen", height=2)
    title.pack(fill=tk.BOTH)

    usernameTitle = tk.Label(registerPage, text="Username", font=subtextFont)
    usernameTitle.pack(fill=tk.BOTH, pady=(20,0))
    usernameEntry = tk.Entry(registerPage)
    usernameEntry.pack()

    passwordTitle = tk.Label(registerPage, text="Password", font=subtextFont)
    passwordTitle.pack(fill=tk.BOTH, pady=(20,0))
    passwordEntry = tk.Entry(registerPage, show="*")
    passwordEntry.pack(pady=(0,20))

    # Registers the user when clicked
    def registerUser():
        username = usernameEntry.get()
        password = passwordEntry.get()

        # Check for good username
        if username == "":
            messagebox.showwarning("Registration Error", "Username cannot be empty!", parent=box)
            return

        # Check for good password
        elif password == "":
            messagebox.showwarning("Registration Error", "Password cannot be empty!", parent=box)
            return
        
        # Check if there are already 10 users registered
        elif len(userData) == 10:
            messagebox.showwarning("Registration Error", "The max amount of users has been reached, which is 10. Consider deleting an existing user before attempting to register a new user.", parent=box)
            return
        
        # Check if username already exists
        for pastUsers in userData:
            if pastUsers["username"] == username:
                messagebox.showwarning("Registration Error", "Another user already has this username!", parent=box)
                return
        
        # Add new user if all checks have passed
        newUser = {"username": username, "password": password}
        messagebox.showinfo("Registration Successful", username + " has been registered!", parent=box)
        userData.append(newUser)

    registerButton = tk.Button(registerPage, text ="Register", font=subtextFont, command=registerUser, padx=40, pady=3)
    registerButton.pack() 

    existingUsersButton = tk.Button(registerPage, text ="Existing Users", font=subtextFont, command=existingUsersPage, padx=17, pady=3)
    existingUsersButton.pack(pady=(20,0)) 

    backButton = tk.Button(registerPage, text ="Back", font=subtextFont, command=startPage, padx=40, pady=3)
    backButton.pack(side="bottom", anchor="sw", padx=5, pady=5)

# Existing users page
def existingUsersPage():
    existingUsers = redirectPage()

    title = tk.Label(existingUsers, text="Existing Users", font=titleFont, bg="mediumpurple", height=2)
    title.pack(fill=tk.BOTH)

    description = tk.Label(existingUsers, text=f"Current Users: {len(userData)}/10. Click on a user to delete.", font=subtextFont)
    description.pack(pady=20)

    # Prompts user to delete user chosen
    def deleteUser(username):
        for user in userData:
            if user["username"] == username:
                userData.remove(user)
                break

        result = messagebox.askquestion("Delete User", f"Are you sure you want to delete user {username}?")
        if result == "yes":
            existingUsersPage()
            messagebox.showinfo("Deletion Successful", username + " has been deleted!", parent=box)

    buttonsContainer = tk.Frame(existingUsers)
    buttonsContainer.pack(fill=tk.Y)
    row_num = 0  
    col_num = 0  
    
    # Goes through userData and creates a button for each user
    for user in userData:
        userButton = tk.Button(buttonsContainer, text=user["username"], font=subtextFont, command=lambda name=user["username"]: deleteUser(name), width=12, pady=3)
        userButton.grid(row=row_num, column=col_num, padx=10, pady=5)

        # Alternate between columns, and move down rows
        col_num = 1 - col_num
        if col_num == 0:
            row_num += 1

    backButton = tk.Button(existingUsers, text ="Back", font=subtextFont, command=registerPage, padx=40, pady=3)
    backButton.pack(side="bottom", anchor="sw", padx=5, pady=5)

# Home page when user is logged in
def homePage():
    homePage = redirectPage()

    username = currentUser["username"]

    title = tk.Label(homePage, text=f"Welcome, {username}!", font=titleFont, bg="pink2", height=2)
    title.pack(fill=tk.BOTH)

    # Pulsing mode section
    modeDescription = tk.Label(homePage, text="Select a pacing mode.", font=subtextFont)
    modeDescription.pack(pady=20)

    buttonsContainer = tk.Frame(homePage)
    buttonsContainer.pack(fill=tk.Y)

    VOOButton = tk.Button(buttonsContainer, text="VOO", font=subtextFont, width=12, pady=3)
    VOOButton.grid(row=0, column=0, padx=10, pady=5)
    
    VVIButton = tk.Button(buttonsContainer, text="VVI", font=subtextFont, width=12, pady=3)
    VVIButton.grid(row=0, column=1, padx=10, pady=5)
    
    AOOButton = tk.Button(buttonsContainer, text="AOO", font=subtextFont, width=12, pady=3)
    AOOButton.grid(row=1, column=0, padx=10, pady=5)
    
    AAIButton = tk.Button(buttonsContainer, text="AAI", font=subtextFont, width=12, pady=3)
    AAIButton.grid(row=1, column=1, padx=10, pady=5)

    # Device detection section
    deviceDescription = tk.Label(homePage, text="Connect the device.", font=subtextFont)
    deviceDescription.pack(pady=20)

    # Switches between connecting and disconnecting the device
    def connectDevice():
        status = connectButton.cget("text")
        if status == "Connect":
            status = "Disconnect"
        else:
            status = "Connect"

        connectButton.configure(text=status)

    connectButton = tk.Button(homePage, text="Connect", font=subtextFont, command=connectDevice, width=12, pady=3)
    connectButton.pack()

    # logout section
    logoutButton = tk.Button(homePage, text ="Logout", font=subtextFont, command=startPage, padx=40, pady=3)
    logoutButton.pack(side="bottom", anchor="se", padx=5, pady=5)


# Start GUI with start page
startPage()
box.protocol("WM_DELETE_WINDOW", saveUserData)
box.mainloop()