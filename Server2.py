
from datetime import time
from optparse import Values
import os
import random
from secrets import choice
import socket 
import threading
from time import sleep
from tkinter import *
from tkinter.ttk import Treeview
buf=1024
format="utf8"
PORT = 5050
ref_compte=[]
SERVER =  "172.18.0.153" #socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)
#---------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------   
class gerer_client(threading.Thread):
        testconn=True
        lock=threading.Lock()
        def __init__(self,conn,details):
            threading.Thread.__init__(self)
            self.conn=conn
            self.details=details
        def exist(self,ch):
            for i in ref_compte :
                if str(ch)==i :
                    return True
            return False
#---------------------------------------------------------------------------------------
        def creer_compte(self,ref):
            ref_compte.append(ref)
            ch=ref
            self.conn.send(bytes('**** Veuillez entrer vos coordonnées **** \n "Valeur du votre compte"' ,format))
            val=self.receive()
            ch=ch+' '+val+' '
            self.conn.send(bytes("Etat du votre compte \n 1/ Negative \t 2/ Positive",format))
            msg=self.receive()
            if (int(msg)==1):
                ch=ch+'NEGATIVE'+' '
                ch=ch+str(random.randint(int(val),int(val)+300))
            if (int(msg)==2) :
                ch=ch+'POSITIVE'+' '
                ch=ch+str(random.randint(0,int(val)))
            self.conn.send(bytes(ch,format))
            compte= open("comptes.txt",'a+')
            compte.write(ch+"\n")
            compte.close()
#-----------------------------------------------------------------------------------------
        def gerer_compte(self,ref):
            retour=1
            while retour==1 :
                self.lock.acquire()
                self.conn.send(bytes("1/Retrait \n 2/Ajout \n 3/recevoir une facture",format))
                choix=int(self.receive())
                compte=open("comptes.txt",'r')
                historique=open("historiques.txt",'a+')
                lines=compte.readlines()
                compte.close()
                compte=open("comptes.txt",'w')
                while(choix not in range(1,4)) :
                    self.conn.send(bytes("choix erroné ! \n",format))
                    self.conn.send(bytes("1/Retrait \n 2/Ajout \n 3/recevoir une facture",format))
                    choix=int(self.receive())

                if (choix==1):
                    for line in lines :
                            parcour=line.split(" ")
                            if (parcour[0]==ref) :#compte eli 7achti byh
                                self.conn.send(bytes("tapez le montant",format))
                                mont=int(self.receive())
                                if (parcour[2].upper()=="NEGATIVE"):
                                    if((int(parcour[1])+mont)>int(parcour[3])) :#hedha fi negative w ye7chemch
                                        self.conn.send(bytes("impossible de depasser la seuil",format))
                                        his=parcour[0]+' '
                                        his=his+parcour[1]+' '+parcour[2]
                                        his=his+' '+parcour[3]+' '+'retrait'+' '+str(mont)+' '+'echec'
                                        historique.write(his+'\n')
                                        compte.write(line)
                                    if(mont+int(parcour[1]))<int(parcour[3]) :#hedha hyetou lkol fi negative
                                        self.conn.send(bytes("TRANSACTION EFFECTUE AVEC SUCCES",format))
                                        parcour[1]=str(int(parcour[1])-mont)
                                        tarif=(mont*2)/100
                                        fac=parcour[0]+' '+str(tarif)
                                        facture=open("factures.txt","a+")
                                        facture.write(fac +"\n")
                                        facture.close()
                                        his=parcour[0]+' '
                                        his=his+parcour[1]+' '+parcour[2]+' '+parcour[3]
                                        fin=his+' '+'retrait'+' '+str(mont)+' '+'succes'
                                        historique.write(fin+'\n')
                                        compte.write(his)

                                if (parcour[2].upper()=="POSITIVE"):
                                    if(mont>(int(parcour[1])+(int(parcour[1])))):#hedha fi positive w fibelou denya msayba
                                        self.conn.send(bytes("impossible de depasser la seuil",format))
                                        his=parcour[0]+' '
                                        his=his+parcour[1]+' '+parcour[2]
                                        his=his+' '+parcour[3]+' '+'retrait'+' '+str(mont)+' '+'echec'
                                        historique.write(his+'\n')
                                        compte.write(line)
                                    if(mont<int(parcour[1])):#hedha fehem 9adrou
                                        self.conn.send(bytes("TRANSACTION EFFECTUE AVEC SUCCES",format))
                                        parcour[1]=str(int(parcour[1])-mont)
                                        his=parcour[0]+' '
                                        his=his+parcour[1]+' '+parcour[2]+' '+parcour[3]
                                        fin=his+' '+'retrait'+' '+str(mont)+' '+'succes'
                                        historique.write(fin+'\n')
                                        compte.write(his)
                                    if(mont in range(int(parcour[1]),int(parcour[3])+int(parcour[1]))):#hedha allah ghaleb ta7et byh
                                        self.conn.send(bytes("TRANSACTION EFFECTUE AVEC SUCCES",format))
                                        parcour[1]=str(mont-int(parcour[1]))
                                        tarif=(mont*2)/100
                                        fac=parcour[0]+' '+str(tarif)
                                        facture=open("factures.txt","a+")
                                        facture.write(fac +"\n")
                                        facture.close()
                                        parcour[2]="NEGATIVE"
                                        his=parcour[0]+' '
                                        his=his+parcour[1]+' '+parcour[2]+' '+parcour[3]
                                        fin=his+' '+'retrait'+' '+str(mont)+' '+'succes'
                                        historique.write(fin+'\n')
                                        compte.write(his)




                            else :
                                compte.write(line)
                if(choix==2):
                    for line in lines :
                        parcour=line.split(" ")
                        if (parcour[0]==ref) :#compte eli 7achti byh
                            self.conn.send(bytes("tapez le montant",format))
                            mont=int(self.receive()) 
                            if (parcour[2].upper()=="NEGATIVE"):
                                    if(int(parcour[1])>mont):#7awel tastati3
                                        self.conn.send(bytes("TRANSACTION EFFECTUE AVEC SUCCES",format))
                                        parcour[1]=str(int(parcour[1])-mont)
                                        his=parcour[0]+' '
                                        his=his+parcour[1]+' '+parcour[2]+' '+parcour[3]
                                        fin=his+' '+'ajout'+' '+str(mont)+' '+'succes'
                                        historique.write(fin+'\n')
                                        compte.write(his)
                                    else : #heya ti7 w ena ntala3ha 
                                        self.conn.send(bytes("TRANSACTION EFFECTUE AVEC SUCCES",format))
                                        parcour[1]=str(mont-int(parcour[1])) 
                                        parcour[2]="POSITIVE"  
                                        his=parcour[0]+' '
                                        his=his+parcour[1]+' '+parcour[2]+' '+parcour[3]
                                        fin=his+' '+'ajout'+' '+str(mont)+' '+'succes'
                                        historique.write(fin+'\n')
                                        compte.write(his)                             

                            else :#hedha 7ala maah
                                self.conn.send(bytes("TRANSACTION EFFECTUE AVEC SUCCES",format))
                                parcour[1]=str(int(parcour[1])+mont)
                                his=parcour[0]+' '
                                his=his+parcour[1]+' '+parcour[2]+' '+parcour[3]
                                fin=his+' '+'ajout'+' '+str(mont)+' '+'succes'
                                historique.write(fin+'\n')
                                compte.write(his) 




                        else :                 
                            compte.write(line)
                    
                if (choix==3):
                    self.lock.release()
                    if (exist_facture(ref)==False) :
                        self.conn.send(bytes("vous n'avez pas de facture à payer",format))
                    else :
                        fac=open("factures.txt","r")
                        lines=fac.readlines()
                        fac.close()
                        somme=0.0
                        for line in lines :
                            parcour=line.split(' ')
                            if (parcour[0]==ref) :
                                somme+=float(parcour[1][0]+parcour[1][1]+parcour[1][2])
                        self.conn.send(bytes("**** Votre facture **** ",format))
                        self.conn.send(bytes(str(somme)+" dt , Merci de la payer \n",format))

                self.conn.send(bytes("voulez vous retournez au menu principale ! \n 1/oui \t 2/non",format))
                retour=int(self.receive())
                self.lock.release()
                if(retour==2):
                    self.conn.send(bytes("AUREVOIR",format))
                    self.receive()












#-------------------------------------------------------------------------------------------
            
        def receive(self):
            ch=self.conn.recv(buf).decode(format)
            if ch==DISCONNECT_MESSAGE :
                ch1=Label(scene,text=f"[!DISCONNECT] {self.details} deconnected.")
                ch1.pack()
                scene.update()
            else :
                return ch

        def run(self):
            ch=Label(scene,text=f"[NEW CONNECTION] {self.details} connected.")
            ch.pack()
            scene.update()

            self.conn.send(bytes(" Bienvenue veuillez tapez la reference de votre compte ",format))
            ch=self.receive()
            print(ref_compte)
            
            if(exist(ch)==False):
                self.conn.send(bytes("0",format))
                self.creer_compte(ch)
                self.gerer_compte(ch)
            else :
                self.conn.send(bytes("1",format))
                self.gerer_compte(ch)
#--------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------
def exist(ch):
    for i in ref_compte :
        if str(ch)==i :
             return True
    return False
#----------------------------------------------------------
def voir_compte ( ):
    view=Toplevel(scene)
    view.title("voir les comptes")
    ch=Label(view,text="**** BONJOUR ****")
    ch.pack()
    tableview=Treeview(view,columns=(1,2,3,4),heigh=14, show ="headings")
    tableview.heading(1,text="Reference du compte")
    tableview.heading(2,text="Valeur du compte")
    tableview.heading(3,text="Etat du compte")
    tableview.heading(4,text="Plafond du compte")
    compte=open("comptes.txt",'r')
    lines=compte.readlines()
    compte.close()
    if(lines == []):
        ch1=Label(view,text=" !! OUPS ...  ")
        ch1.pack()

    else : 
        for line in lines :
         parcour=line.split(' ')
         tableview.insert('',END,values=parcour)


        tableview.pack()

#--------------------------------------------------------------------
def chercher_facture(event=None):
    ref=my_msg.get()
    somme=0.0
    valeur=[]
    if (exist_facture(ref)==False):
        ch=Label(viewfac,text=" Pas de facture pour ce compte")
        ch.pack()
    else :
        tableview=Treeview(viewfac,columns=(1,2),heigh=14, show ="headings")
        tableview.heading(1,text="Reference du compte")
        tableview.heading(2,text="Montant à payer") 
        compte=open("factures.txt",'r')
        lines=compte.readlines()
        compte.close()
        for line in lines :
            parcour=line.split(' ')
            if (parcour[0]==ref) :
                somme+=float(parcour[1][0]+parcour[1][1]+parcour[1][2])
        valeur=[ref,str(somme)]
        tableview.insert('',END,values=valeur)
        tableview.pack()


    
#-----------------------------------------------------------------
def consulter_facture():
    global viewfac
    global my_msg
    viewfac=Toplevel(scene)
    viewfac.geometry("400x300")
    viewfac.title(" consulter facture ")
    ch=Label(viewfac,text="**** BONJOUR **** ")
    ch.pack()
    my_msg=StringVar()
    entry_field =Entry(viewfac, textvariable=my_msg)
    entry_field.pack()
    entry_field.bind("<Return>", chercher_facture)
    send_button =Button(viewfac, text="Chercher")
    send_button.bind("<ButtonRelease-1>", chercher_facture)
    send_button.pack()    
#-------------------------------------------------------------------------------------------------
def consulter_histrorique():
    view=Toplevel(scene)
    view.title("consulter l'historique")
    ch=Label(view,text="**** BONJOUR ****")
    ch.pack()
    tableview=Treeview(view,columns=(1,2,3,4,5,6,7),heigh=20, show ="headings")
    tableview.heading(1,text="Reference du compte")
    tableview.heading(2,text="Valeur apres transaction")
    tableview.heading(3,text="Etat apres transaction")
    tableview.heading(4,text="Plafond du compte")
    tableview.heading(5,text="operation")
    tableview.heading(6,text="valeur du montant")
    tableview.heading(7,text="echec/succes")
    compte=open("historiques.txt",'r')
    lines=compte.readlines()
    compte.close()
    for i in range(0,len(lines)-1,2) :
        parcour1=lines[i].split(" ")
        parcour2=lines[i+1].split(" ")
        parcour=parcour1+parcour2[1:4]
        tableview.insert('',END,values=parcour)



    tableview.pack()

#---------------------------------------------------------------------------------------------------
def quitter() :
        for conn in clientconnected :
            conn.send(bytes(DISCONNECT_MESSAGE,format))
        scene.destroy()

#-----------------------------------------------------------------------------------------------
def exist_facture(ch):
    ref_facture=[]
    compte=open("factures.txt","r")
    lines=compte.readlines()
    compte.close()
    for line in lines :
        ref=line.split(" ")
        ref_facture.append(ref[0])
    if( ch in ref_facture):
        return True
    else :
        return False
#---------------------------------------------------------------------------------------------------
def charger_ref_existant():
    compte=open("comptes.txt","r")
    lines=compte.readlines()
    compte.close()
    for line in lines :
        ref=line.split(" ")
        ref_compte.append(ref[0])
    

#---------------------------------------------------------------------------------------------------
def start():
    global conn
    global addr
    ch=Label(scene,text="[STARTING] server is starting...")
    ch1=Label(scene,text=f"[LISTENING] Server is listening on {SERVER}")
    charger_ref_existant()
    ch.pack()
    ch1.pack()
    scene.update()
    while True :
        server_socket.listen()
        conn, addr = server_socket.accept()
        clientconnected.append(conn)
        gerer_client(conn,addr).start()

clientconnected=[]
global scene 
scene=Tk()
scene.geometry("400x300")
scene.title("Application Transaction")
mainmenu=Menu(scene)
firstmenu=Menu(mainmenu)
firstmenu.add_command(label="le serveur est demarré ",command=threading.Thread(target=start).start())
firstmenu.add_separator()
firstmenu.add_command(label="voir les comptes",command=voir_compte)
firstmenu.add_command(label="consulter une facture",command=consulter_facture)
firstmenu.add_command(label="voir l'historique",command=consulter_histrorique)
firstmenu.add_separator()
firstmenu.add_command(label="Quitter",command=quitter)

mainmenu.add_cascade(label="gerer transactions",menu=firstmenu)
scene.config(menu=mainmenu)
scene.mainloop()




            
            
                



