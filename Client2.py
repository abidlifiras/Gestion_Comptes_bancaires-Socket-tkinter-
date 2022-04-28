from cgitb import text
import socket
from threading import Thread
import time 
from tkinter import *

buf = 1024
PORT = 5050
format = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "172.18.0.153" #"192.168.56.1"
ADDR = (SERVER, PORT)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #le type du socket : SOCK_STREAM pour le protocole TCP



#client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client_socket.connect(ADDR)
#---------------------------------------------------------
def receive():
    failed = False
    while True:
        try :
            msg = client_socket.recv(buf).decode(format) 
            if msg==DISCONNECT_MESSAGE :
                msg_list.insert(END," OUPS LE SERVEUR NE REPONDS PAS !!!")
                time.sleep(2)
                exitscene()
            if msg=="AUREVOIR" :
                msg_list.insert(END, msg)
                time.sleep(3)
                exitscene()
            else : 
                msg_list.insert(END, msg)
        except :
            if (failed == False) :
                msg_list.insert(END," ----- Veuillez patienter svp :) ----- ")
            failed = True
            
            

#--------------------------------------------------------------
def send(event=None):  
    msg = my_msg.get()
    my_msg.set("")  
    client_socket.send(bytes(msg, format))
#-----------------------------------------------------------------
def exitscene(event=None):
    client_socket.send(bytes(DISCONNECT_MESSAGE, format))
    scene.destroy()
#--------------------------------------------------------------------
scene=Tk()
scene.title("Application Transaction")
messages_frame = Frame(scene)
my_msg = StringVar()
scrollbar =Scrollbar(messages_frame)
msg_list =Listbox(messages_frame, height=30, width=100, yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
msg_list.pack()
messages_frame.pack()
entry_field =Entry(scene, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button =Button(scene, text="repondre")
send_button.bind("<ButtonRelease-1>", send)
send_button.pack()
exit_button = Button (scene, text = "Quitter")
exit_button.bind("<ButtonRelease-1>", exitscene)
exit_button.pack()
#------------------------------------------------------------------------------------
def auth(event=None) :
    ref=entry_field1.get()
    if not ref :
        view.title("INVALDE REFERENCE")
        return None

    client_socket.send(bytes(str(ref),format))
    test=client_socket.recv(buf).decode(format)
    if int(test)==1 :
        view.title("Redirection vers menu")
        time.sleep(3)
        receive_thread = Thread(target=receive)
        receive_thread.start()
        view.destroy()
        scene.mainloop()
    else :
        view.title("Veuillez creer un compte")
        time.sleep(3)
        receive_thread = Thread(target=receive)
        receive_thread.start()
        view.destroy()
        scene.mainloop()


#--------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------

try:
    client_socket.connect(ADDR)
    test = True
except :
    print("the server is offline")
    test = False
if test :
    view=Tk()
    view.title("Authentification")
    view.geometry("400x300")
    ch1=client_socket.recv(buf).decode(format)
    ch=Label(view,text=ch1)
    ch.pack()
    entry_field1=Entry(view, textvariable="")
    entry_field1.bind("<Return>", auth)
    entry_field1.pack()
    send_button =Button(view, text="repondre")
    send_button.bind("<ButtonRelease-1>", auth)
    send_button.pack()
    view.mainloop()










