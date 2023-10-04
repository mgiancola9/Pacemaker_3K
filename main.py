import tkinter as tk

box = tk.Tk()
box.title("Pacemaker GUI")
box.geometry("500x500")
box.minsize(400, 300)

titleFont = ('Helvatical bold',14)
subtextFont = ('Helvatical bold',12)

def startPage():
    title = tk.Label(box, text="Welcome to the PULSEMASTER Interface", font=titleFont, bg="yellow", height=2)
    title.pack(fill=tk.BOTH)

    loginButton = tk.Button(box, text ="Login", font=subtextFont)
    loginButton.pack(expand=True)  

    registerButton = tk.Button(box, text ="Register", font=subtextFont)
    registerButton.pack(side="top", expand=True)  

startPage()
box.mainloop()