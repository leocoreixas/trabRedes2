import tkinter as tk


class Client:
    def __init__(self) -> None:
        self.user = ""
        self.password = ""
        self.type = ""

    def getUser(self):
        return self.user

    def getPassword(self):
        return self.password

    def getType(self):
        return self.type

    def setUser(self, text):
        self.user = text

    def setPassword(self, text):
        self.password = text

    def setType(self, text):
        self.type = text


class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.crialabel()
        self.user = self.entradadados()
        self.crialabel2()
        self.type = self.entradadados2()
        self.criarbotoes()

    def criarbotoes(self):
        self.btCriar = tk.Button(self)
        self.btCriar["text"] = "Botao1"
        self.btCriar.pack(side="top")
        print(self.user, self.type)

    def crialabel(self):
        self.label = tk.Label(self)
        self.label["text"] = "User"
        self.label.pack(side="top")

    def entradadados(self):
        self.edit = tk.Entry(self)
        self.edit.pack(side="top")
        return self.edit.get()

    def crialabel2(self):
        self.label = tk.Label(self)
        self.label["text"] = "Type"
        self.label.pack(side="top")

    def entradadados2(self):
        self.edit1 = tk.Entry(self)
        self.edit1.pack(side="top")
        return self.edit1.get()

    def setVal(self):
        self.user = self.edit.get()
        self.type = self.edit1.get()





