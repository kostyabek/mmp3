import tkinter as tk
import source.content.GUI as GUI
from source.content import program


def main():
    master = tk.Tk()
    master.title("MMP3 - Mini MP3 Player")
    # root.iconbitmap("")
    master.geometry("480x640")
    master.resizable(False, False)
    master.config(bg=GUI.GUI.backgroundColor)

    window = program.Program(master)

    master.mainloop()


main()
