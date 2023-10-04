import tkinter as tk

box = tk.Tk()
box.title("Pacemaker GUI")
box.geometry("500x500")
box.minsize(200, 200)

titleFont = ('Helvatical bold',14)
subtextFont = ('Helvatical bold',12)

def startPage():
    title = tk.Label(box, text="Hello, tkinter!", font=titleFont)
    title.pack()

    loginButton = tk.Button(box, text ="Login", font=subtextFont)
    loginButton.pack(side="top", expand=True)  

    registerButton = tk.Button(box, text ="Register", font=subtextFont)
    registerButton.pack(side="top", expand=True)  

startPage()
box.mainloop()