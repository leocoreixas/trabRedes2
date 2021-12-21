from tkinter import *
from functools import partial


def validateLogin(username, type):
    print("username entered :", username.get())
    print("type entered :", type.get())
    return


# window
def initLogin():
    from login import validateLogin
    tkWindow = Tk()
    tkWindow.geometry('300x150')
    tkWindow.title('Cadastro de Usuário')

    # username label and text entry box
    usernameLabel = Label(tkWindow, text="Nome").grid(row=0, column=0)
    username = StringVar()
    usernameEntry = Entry(tkWindow, textvariable=username).grid(row=0, column=1)

    # password label and password entry box
    typeLabel = Label(tkWindow, text="Senha").grid(row=1, column=0)
    type = StringVar()
    typeEntry = Entry(tkWindow, textvariable=type, show='*').grid(row=1, column=1)

    validateLogin = partial(validateLogin, username, type)

    # login button
    loginButton = Button(tkWindow, text="Login", command=validateLogin).grid(row=4, column=0)

    tkWindow.mainloop()
    return username.get(), type.get()
