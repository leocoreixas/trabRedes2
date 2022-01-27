from tkinter import *
from functools import partial
import base64
import socket
import threading
import os
from _thread import *
import cv2
import pickle
import struct
import imutils
import tkinter as tk
from tkinter import messagebox
import client as _

def destroy(window, text, client, window2=None):
    window.destroy()
    #window2.destroy()
    if client.showMovie(text) == -1:
        messagebox.showerror("Error", "Não foi possível exibir o filme") #TODO: Pegar respota do servidor



def open(text, window, window2, client):

    btn = Button(window, text="Começar filme",command=lambda: destroy(window, text,client, window2))
    btn.place(x=280, y=190)

    return text

def validateLogin(username, type, tkWindow, var):
    print("username entered :", username.get())
    print("type entered :", type)
    print("var entered :", var.get())
    if var.get() == 0:
        messagebox.showerror("Error",'Selecione um Perfil')
        return
    if var.get() == 1:
        type = 'Usuário Básico'
    else:
        type = 'Usuário Premium'


    #global client
    client = _.Client(username.get(), var.get())
    tkWindow1 = Tk()
    tkWindow1.geometry('700x250')
    tkWindow1.title('Seleção do filme')
    text = Text(tkWindow1)
    text.insert(INSERT, type)
    nome = username.get()
    T = Text(tkWindow1, height=5, width=52)
    l = Label(tkWindow1, text=nome)
    l.config(font=("Courier", 14))
    l.pack()
    T.pack()

    T.insert(tk.END, type)

    if  var.get() == 1:
        btn = Button(tkWindow1, text="Começar filme", command=lambda: destroy(tkWindow1, "./videos/homem_aranha_360p.mp4", client, tkWindow))
        btn.place(x=260, y=130)
    elif var.get() == 2:
        valor = IntVar()

        btn = Button(tkWindow1, text="Homem Aranha 360p",command=lambda:open("./videos/homem_aranha_360p.mp4", tkWindow1, tkWindow, client))
        btn.place(x=60, y=170)
        btn = Button(tkWindow1, text="Homem Aranha 720p",command=lambda:open("./videos/homem_aranha_720p.mov", tkWindow1,tkWindow, client))
        btn.place(x=60, y=130)
        btn2 = Button(tkWindow1, text="Homem Aranha 1080p", command=lambda:open("./videos/homem_aranha_1080p.mov", tkWindow1,tkWindow, client))
        btn2.place(x=195, y=130)
        btn3 = Button(tkWindow1, text="Casa Gucci 720p", command=lambda:open("./videos/gucci_720p.mov", tkWindow1,tkWindow, client))
        btn3.place(x=335, y=130)
        btn4= Button(tkWindow1, text="Casa Gucci 1080p", command=lambda:open("./videos/gucci_1080p.mov", tkWindow1,tkWindow, client))
        btn4.place(x=450, y=130)

    return

# window
def initLogin():
    from login import validateLogin
    tkWindow = Tk()
    tkWindow.geometry('300x150')
    tkWindow.title('Cadastro de Usuário')

    var = IntVar()

    # username label and text entry box
    BasicoLabel = Radiobutton(tkWindow, text="Basico",variable=var, value=1).grid(row=2, column=0)
    Basico = StringVar()

    # username label and text entry box
    PremiumLabel = Radiobutton(tkWindow, text="Premium",variable=var, value=2).grid(row=2, column=1)
    Premium = StringVar()

    # username label and text entry box
    usernameLabel = Label(tkWindow, text="Nome").grid(row=0, column=0)
    username = StringVar()
    usernameEntry = Entry(tkWindow, textvariable=username).grid(row=0, column=1)

    # password label and password entry box
    typeLabel = Label(tkWindow, text="Senha").grid(row=1, column=0)
    type = StringVar()
    typeEntry = Entry(tkWindow, textvariable=type, show='*').grid(row=1, column=1)

    if var.get() == 1:
        type = 'Usuário Básico'
    else:
        type = 'Usuário Premium'
    validateLogin = partial(validateLogin, username, type, tkWindow, var)

    # login button
    loginButton = Button(tkWindow, text="Login", command=validateLogin).grid(row=4, column=0)

    tkWindow.mainloop()
    return


initLogin()