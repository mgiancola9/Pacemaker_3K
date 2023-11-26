import json

# Class for all the user storage
class UserStorage:
    def __init__(self):
        # Defining constants for pacing modes based on nominal values
        self.LRL_VALUE = 60
        self.URL_VALUE = 120
        self.AA_VALUE = 5 #was 3.5
        self.APW_VALUE = 1 #was 0.4 (updated)
        self.VA_VALUE = 5
        self.VPW_VALUE = 1 #was 0.4 
        self.VRP_VALUE = 320
        self.ARP_VALUE = 250
        self.AS_VALUE = 0.75
        self.VS_VALUE = 2.5
        self.PVARP_VALUE = 250
        self.HYST_VALUE = 60
        self.RATESM_VALUE = 0

        #ass 2 additions:
        self.MSR_VALUE = 120
        self.ACTIV_VALUE = 2
        self.REACT_VALUE = 30
        self.RESPF_VALUE = 8
        self.RECOVT_VALUE = 5

        # Reads current storage
        self.userData = None
        self.openStorage()

    # Defines all initial values/protocols for the pages
    def openStorage(self):
        try:
            with open("./userData.json", "r") as file:
                self.userData = json.load(file)
        except FileNotFoundError:
            self.userData = []

    # Saves new user data to json after interface is closed
    def saveUserData(self):
        with open('./userData.json', 'w') as file:
            json.dump(self.userData, file)

    # Searches if the user exists with the username and password
    def searchUser(self, username, password):
        userFound, passwordFound, currentUser = False, False, None
        for user in self.userData:
            if user["username"] == username:
                userFound = True
                if user["password"] == password:
                    passwordFound = True
                    currentUser = user
                    break
                else:
                    passwordFound = False
                    break

        return userFound, passwordFound, currentUser
    
    # Searches if the username already exists
    def userExists(self, username):
        for user in self.userData:
            if user["username"] == username:
                return True
            
        return False
    
    # Returns the number of registered users
    def numUsers(self):
        return len(self.userData)
    
    # Adds a new user to the user storage
    def addNewUser(self, username, password):
        newUser = {
                    "username": username,
                    "password": password,
                    "AOO": {"LRL": self.LRL_VALUE, "URL": self.URL_VALUE, "AA": self.AA_VALUE, "APW": self.APW_VALUE},
                    "VOO": {"LRL": self.LRL_VALUE, "URL": self.URL_VALUE, "VA": self.VA_VALUE, "VPW": self.VPW_VALUE},
                    "AAI": {"LRL": self.LRL_VALUE, "URL": self.URL_VALUE, "AA": self.AA_VALUE, "APW": self.APW_VALUE, "AS": self.AS_VALUE, "ARP": self.ARP_VALUE, "PVARP": self.PVARP_VALUE, "HYST": self.HYST_VALUE, "RS": self.RATESM_VALUE},
                    "VVI": {"LRL": self.LRL_VALUE, "URL": self.URL_VALUE, "VA": self.VA_VALUE, "VPW": self.VPW_VALUE, "VS": self.VS_VALUE, "VRP": self.VRP_VALUE, "HYST": self.HYST_VALUE, "RS": self.RATESM_VALUE},
                    "AOOR": {"LRL": self.LRL_VALUE, "URL": self.URL_VALUE, "AA": self.AA_VALUE, "APW": self.APW_VALUE, "MSR": self.MSR_VALUE, "ACTIV": self.ACTIV_VALUE, "REACT": self.REACT_VALUE, "RESPF": self.RESPF_VALUE, "RECOVT": self.RECOVT_VALUE},
                    "VOOR": {"LRL": self.LRL_VALUE, "URL": self.URL_VALUE, "VA": self.VA_VALUE, "VPW": self.VPW_VALUE, "MSR": self.MSR_VALUE, "ACTIV": self.ACTIV_VALUE, "REACT": self.REACT_VALUE, "RESPF": self.RESPF_VALUE, "RECOVT": self.RECOVT_VALUE},
                    "AAIR": {"LRL": self.LRL_VALUE, "URL": self.URL_VALUE, "AA": self.AA_VALUE, "APW": self.APW_VALUE, "AS": self.AS_VALUE, "ARP": self.ARP_VALUE, "PVARP": self.PVARP_VALUE, "HYST": self.HYST_VALUE, "RS": self.RATESM_VALUE, "MSR": self.MSR_VALUE, "ACTIV": self.ACTIV_VALUE, "REACT": self.REACT_VALUE, "RESPF": self.RESPF_VALUE, "RECOVT": self.RECOVT_VALUE},
                    "VVIR": {"LRL": self.LRL_VALUE, "URL": self.URL_VALUE, "VA": self.VA_VALUE, "VPW": self.VPW_VALUE, "VS": self.VS_VALUE, "VRP": self.VRP_VALUE, "HYST": self.HYST_VALUE, "RS": self.RATESM_VALUE, "MSR": self.MSR_VALUE, "ACTIV": self.ACTIV_VALUE, "REACT": self.REACT_VALUE, "RESPF": self.RESPF_VALUE, "RECOVT": self.RECOVT_VALUE},
                    "lastDeviceUsed": None,
                    "Devices": []
                }

        # Adds new user to storage and returns the new user
        self.userData.append(newUser)
        return newUser 
    
    # Deletes user from storage
    def deleteUser(self, username):
        for user in self.userData:
            if user["username"] == username:
                self.userData.remove(user)
                break

    # Provides all users in an array
    def listUsers(self):
        users = []
        for user in self.userData:
            users.append(user["username"])

        return users
    
    # modifies user data as the user sent in 
    def modifyUserData(self, username, mode, modeValues):
        for user in self.userData:
            if user["username"] == username:
                user[mode] = modeValues
                return