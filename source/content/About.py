import tkinter as tk
import webbrowser
import source.content.GUI as GUI


class About(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.geometry("300x400")
        self.title("About")
        # self.iconbitmap("")
        self.resizable(False, False)
        self.madeBy = tk.Label(self, text="Made by\nKonstantin Biektin", bg=GUI.GUI.backgroundColor, fg=GUI.GUI.foregroundColor)
        self.madeBy.pack()
        # self.btn_github = tk.Button(self, image=)


        self.grab_set()
