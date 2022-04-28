from time import sleep
from tkinter import *

from matplotlib.pyplot import text
def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)

#-------------------------------------------------------------
def send(event=None):
    global entry_field1
    global view
    rep=entry_field.get()
    if(int(rep) not in range(1,3)):
        scene.title("CHOIX INVALIDE !!!")
        scene.update()
        return None
    
    elif (int(rep)==2):
        scene.destroy()
        sleep(2)
        execfile("C:/Users/FIRAS/Desktop/PSR/client2.py")
    else :
        view=Toplevel(scene)
        view.title("Authentification")
        ch=Label(view,text="**** TAPEZ MOT DE PASSE SERVEUR ****")
        ch.pack()
        entry_field1=Entry(view, show="*" ,text="")
        entry_field1.bind("<Return>", auth)
        entry_field1.pack()
        send_button =Button(view, text="repondre")
        send_button.bind("<ButtonRelease-1>", auth)
        send_button.pack()

#---------------------------------------------------------------------------
def auth(event=None) :
    rep=entry_field1.get()
    if rep.upper()!="ROOT" :
        view.destroy()
        scene.title("MOT PASSE INVALIDE !!!")
        return None
    else :
        view.destroy()
        scene.title("CONNEXION ...")
        sleep(2)
        scene.destroy()
        execfile("C:/Users/FIRAS/Desktop/PSR/server2.py")




scene=Tk()
scene.geometry("400x300")
scene.title("Application Transaction")
ch=Label(scene,text="Se connecter en tant que : ")
ch.pack()
ch1=Label(scene,text="1/Serveur \n 2/Client")
ch1.pack()
entry_field =Entry(scene, textvariable="")
entry_field.bind("<Return>", send)
entry_field.pack()
send_button =Button(scene, text="repondre")
send_button.bind("<ButtonRelease-1>", send)
send_button.pack()
scene.mainloop()