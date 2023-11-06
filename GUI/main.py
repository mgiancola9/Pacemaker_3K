from app import App
from userStorage import UserStorage
from loginInterface import LoginInterface

# Main function
if __name__ == "__main__":
    userStorage = UserStorage()
    app = App(userStorage)
    loginInterface = LoginInterface(app, app.box, userStorage)

    app.run()