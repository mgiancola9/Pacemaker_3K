import tkinter

box = tkinter.Tk()
box.title("Pacemaker GUI")
box.geometry("500x500")

def startPage():
    button = tkinter.Button(box, text ="Click")
    button.pack(side="top", expand=True)   

startPage()
box.mainloop()