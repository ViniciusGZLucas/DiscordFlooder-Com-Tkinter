from tkinter import *
from functools import partial
import tkinter
import time
import urllib
import json
from urllib.request import Request
from threading import Thread

#Variables
App = None
#Variavel que recebe valores de um arquivo de texto (Obrigatorio o arquivo existir)
Tokens = open("Tokens.txt").readlines()
#----------------
BL = None
NL = None
LL = None
LL2 = None
NL2 = None
#-----------------

#Cria o GUI
def Application():
    global App
    App = Tk(screenName="DiscordFunctions")
    App.title("DiscordFunctions")
    App.geometry("500x500")
#-------------

#Cria um Button no GUI
def AddButton(App,Tittle,Command,*Args):
    if Command != None and Args != None:
        Button = tkinter.Button(App,text=Tittle,command=partial(Command,Args))
    elif Command !=None:
        Button = tkinter.Button(App, text=Tittle,command=Command)
    else:
        Button = tkinter.Button(App, text=Tittle)
    Button.pack()
    return Button
#------------------------

#Cria um Textbox no GUI
def AddTextBox(App,txtvariable):
    Entry = tkinter.Entry(App,textvariable=txtvariable)
    Entry.pack()
    return Entry
#-----------------------

#Cria um Label No GUI
def AddLabel(App,Text):
    Label = tkinter.Label(App)
    Label["text"] = Text
    Label.pack()
    return Label
#---------------------

#Cria um CheckBox no GUI
def AddCheckBox(App,Name,Var,Command,*Arg):
    CheckBox = tkinter.Checkbutton(App,text=Name,variable=Var,command=partial(Command,Arg))
    CheckBox.pack()
    return CheckBox
#-----------------------

StartStop = False

#Chamada apenas para para o flood dos bots setando False na variavel
def StopFlood(*Args):
    global StartStop
    StartStop = False
#---------------------------------------------------------------------

#Entra no servidor do discord caso os bots nao estejam
def Joiner(InviteLink,Token):
    try:
        urllib.request.urlopen(Request("https://discordapp.com/api/v8/invites/{}".format(InviteLink),data="".encode("utf-8"),headers={"authorization":str(Token).replace("\n",""),"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"}))
    except:
        pass
#--------------------------------------------------------

#Cria um processo para cada token funcionar independentemente
def StartFlood(*Args):
    global StartStop
    StartStop = True
    Process = []
    for Token in Tokens:
        Joiner(Entry3.get(),Token)
        Process.append(Thread(target=MandarDiscMsg,args=(Token.replace("\n",""),Args[0],)))
    for x in range(len(Process)):
        Process[x].start()
#-----------------------------------------------------------------

#Manda a mensagem no chat do discord
def MandarDiscMsg(Token,*Args):
    global StartStop
    Channel,Msg = Args[0]
    Browser = Request("https://discordapp.com/api/v6/channels/{}/messages".format(Channel.get()),data=json.dumps({"content":Msg.get()}).encode("utf-8"),headers={"authorization":Token,"content-type":"application/json","user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"})
    while StartStop:
        try:
            urllib.request.urlopen(Browser)
            time.sleep(0.5)
        except:
            pass
#--------------------------------------

#Dependencia da Função (Reacter)
def Reagir(*args):
    global Tokens
    for Token in Tokens:
        try:
            urllib.request.urlopen(Request("https://discord.com/api/v8/channels/{}/messages/{}/reactions/{}/%40me".format(args[0][0].get(), args[0][1].get(), str(args[0][2].get().encode()).replace("b'\\x","%").replace("\\x","%").replace("'","")),data="".encode("utf-8"), headers={"authorization": Token.replace("\n",""), "content-type": "application/json","user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"},method="PUT"))
        except:
            pass
#------------------------------------

#Função Que Cria uma reação na mensagem desejada
def Reacter(*args):
    global NL,BL,LL,NL2,LL2,Entry5,Entry2,Entry4
    if(args[0][1].get()==1):
        LL = AddLabel(args[0][0],"Message ID")
        NL = AddTextBox(args[0][0],Entry4)
        LL2 = AddLabel(args[0][0],"Emoji(https://pt.piliapp.com/emoji/list/)")
        NL2 = AddTextBox(args[0][0],Entry5)
        BL = AddButton(args[0][0],"Reagir",Reagir,Entry2,NL,NL2)
    else:
        Label.destroy(self=LL)
        Button.destroy(self=BL)
        Text.destroy(self=NL)
        Label.destroy(self=LL2)
        Text.destroy(self=NL2)
#-----------------------------------------------------

def Quit(*args):
    exit()

Application()

Test = IntVar()

#Tkinter Strings
Entry1 = tkinter.StringVar(App)
Entry2 = tkinter.StringVar(App)
Entry3 = tkinter.StringVar(App)
Entry4 = tkinter.StringVar(App)
Entry5 = tkinter.StringVar(App)
#-----------------------

#Tkinter Items Add
AddLabel(App,"Servidor para os Bots Entrarem")
AddTextBox(App,Entry3)
AddLabel(App,"Mensagem para Enviar")
AddTextBox(App,Entry1)
AddLabel(App,"Chat para Floodar")
AddTextBox(App,Entry2)
AddButton(App,"Mandar",StartFlood,Entry2,Entry1)
AddButton(App,"Stop",StopFlood)
AddButton(App,"Quit",Quit,App)
AddCheckBox(App,"Reagir",Test,Reacter,App,Test,Entry2,Entry4,Entry5)
#-------------------------

#Application Run
App.mainloop()
#---------------
