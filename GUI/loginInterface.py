import tkinter as tk
from tkinter import messagebox
from pacemakerInterface import PacemakerInterface

# Class for all the login and register pages
class LoginInterface:
    def __init__(self, app, box, userStorage):
        # Sets up frame to put all components on
        self.box = box

        # Variables to use for text font
        self.titleFont = ('Helvatical bold', 14)
        self.subtextFont = ('Helvatical bold', 12, "bold")

        # Defines an instance of the user storage and starts GUI with starting page
        self.app = app
        self.userStorage = userStorage
        self.pacemakerInterface = PacemakerInterface(app, app.box, self, userStorage)
        self.startPage()

    # Start page
    def startPage(self):
        startPage = self.app.redirectPage()

        title = tk.Label(startPage, text="Welcome to the PULSEMASTER Interface", font=self.titleFont, bg="lightblue", height=2)
        title.pack(fill=tk.BOTH)

        description = tk.Label(startPage, text="Login or register a new patient below.", font=self.subtextFont, height=4)
        description.pack()

        loginButton = tk.Button(startPage, text="Login", font=self.subtextFont, command=self.loginPage, padx=50, pady=3)
        loginButton.pack(pady=(0, 20))

        registerButton = tk.Button(startPage, text="Register", font=self.subtextFont, command=self.registerPage, padx=40, pady=3)
        registerButton.pack()

    # Login page
    def loginPage(self):
        def authenticateUser():
            username = self.usernameEntry.get()
            password = self.passwordEntry.get()

            # Check for empty fields
            if username == "" or password == "":
                messagebox.showwarning("Login Error", "Username and/or password cannot be empty!", parent=self.box)
                return
            
            elif " " in username or " " in password:
                messagebox.showwarning("Registration Error", "Username and/or Password cannot have spaces!", parent=self.box)
                return

            # Check if the user exists and the password is correct
            userFound, passwordFound, user = self.userStorage.searchUser(username,password)

            if userFound and passwordFound:
                self.pacemakerInterface.homePage(user,True)

            elif userFound and not passwordFound:
                messagebox.showwarning("Login Error", "Incorrect password for the username provided.", parent=self.box)

            elif not userFound:
                messagebox.showwarning("Login Error", "Username does not exist. Please register first.", parent=self.box)

        loginPage = self.app.redirectPage()

        title = tk.Label(loginPage, text="Login to Existing Patient", font=self.titleFont, bg="sienna1", height=2)
        title.pack(fill=tk.BOTH)

        usernameTitle = tk.Label(loginPage, text="Username", font=self.subtextFont)
        usernameTitle.pack(fill=tk.BOTH, pady=(20, 0))
        self.usernameEntry = tk.Entry(loginPage)
        self.usernameEntry.pack()

        passwordTitle = tk.Label(loginPage, text="Password", font=self.subtextFont)
        passwordTitle.pack(fill=tk.BOTH, pady=(20, 0))
        self.passwordEntry = tk.Entry(loginPage, show="*")
        self.passwordEntry.pack(pady=(0, 20))

        loginButton = tk.Button(loginPage, text="Login", font=self.subtextFont, command=authenticateUser, padx=40, pady=3)
        loginButton.pack()

        backButton = tk.Button(loginPage, text="Back", font=self.subtextFont, command=self.startPage, padx=40, pady=3)
        backButton.pack(side="bottom", anchor="sw", padx=5, pady=5)

    # Register page
    def registerPage(self):
        registerPage = self.app.redirectPage()

        title = tk.Label(registerPage, text="Register New Patient", font=self.titleFont, bg="lightgreen", height=2)
        title.pack(fill=tk.BOTH)

        usernameTitle = tk.Label(registerPage, text="Username", font=self.subtextFont)
        usernameTitle.pack(fill=tk.BOTH, pady=(20, 0))
        usernameEntry = tk.Entry(registerPage)
        usernameEntry.pack()

        passwordTitle = tk.Label(registerPage, text="Password", font=self.subtextFont)
        passwordTitle.pack(fill=tk.BOTH, pady=(20, 0))
        passwordEntry = tk.Entry(registerPage, show="*")
        passwordEntry.pack(pady=(0, 20))

        # Registers the user when clicked
        def registerUser():
            username = usernameEntry.get()
            password = passwordEntry.get()

            # Check for good username
            if username == "":
                messagebox.showwarning("Registration Error", "Username cannot be empty!", parent=self.box)
                return

            # Check for good password
            elif password == "":
                messagebox.showwarning("Registration Error", "Password cannot be empty!", parent=self.box)
                return
            
            # Check for spaces in username
            elif " " in username or " " in password:
                messagebox.showwarning("Registration Error", "Username and/or Password cannot have spaces!", parent=self.box)
                return

            # Check if there are already 10 users registered
            elif self.userStorage.numUsers() == 10:
                messagebox.showwarning("Registration Error", "The maximum number of users has been reached, which is 10. Consider deleting an existing user before attempting to register a new user.", parent=self.box)
                return

            # Check if username already exists
            usernameExists = self.userStorage.userExists(username)
            if usernameExists:
                messagebox.showwarning("Registration Error", "Another user already has this username!", parent=self.box)
                return

            # Log new user in
            newUser = self.userStorage.addNewUser(username,password)
            self.pacemakerInterface.homePage(newUser,True)
            # messagebox.showinfo("Registration Successful", username + " has been registered!", parent=self.box)

        registerButton = tk.Button(registerPage, text="Register", font=self.subtextFont, command=registerUser, padx=40, pady=3)
        registerButton.pack()

        existingUsersButton = tk.Button(registerPage, text="Existing Users", font=self.subtextFont, command=self.existingUsersPage, padx=17, pady=3)
        existingUsersButton.pack(pady=(20, 0))

        backButton = tk.Button(registerPage, text="Back", font=self.subtextFont, command=self.startPage, padx=40, pady=3)
        backButton.pack(side="bottom", anchor="sw", padx=5, pady=5)

    # Existing users page
    def existingUsersPage(self):
        existingUsers = self.app.redirectPage()

        title = tk.Label(existingUsers, text="Existing Users", font=self.titleFont, bg="mediumpurple", height=2)
        title.pack(fill=tk.BOTH)

        description = tk.Label(existingUsers, text=f"Current Users: {self.userStorage.numUsers()}/10. Click on a user to delete.", font=self.subtextFont)
        description.pack(pady=20)

        # Prompts user to delete the chosen user
        def deleteUser(username):
            result = messagebox.askquestion("Delete User", f"Are you sure you want to delete user {username}?")
            if result == "yes":
                self.userStorage.deleteUser(username)
                self.existingUsersPage()
                messagebox.showinfo("Deletion Successful", username + " has been deleted!", parent=self.box)

        buttonsContainer = tk.Frame(existingUsers)
        buttonsContainer.pack(fill=tk.Y)
        row_num = 0
        col_num = 0

        # Creates a button for each user
        usernames = self.userStorage.listUsers()
        for username in usernames:
            userButton = tk.Button(buttonsContainer, text=username, font=self.subtextFont, command=lambda name=username: deleteUser(name), width=12, pady=3)
            userButton.grid(row=row_num, column=col_num, padx=10, pady=5)

            # Alternate between columns, and move down rows
            col_num = 1 - col_num
            if col_num == 0:
                row_num += 1

        backButton = tk.Button(existingUsers, text="Back", font=self.subtextFont, command=self.registerPage, padx=40, pady=3)
        backButton.pack(side="bottom", anchor="sw", padx=5, pady=5)