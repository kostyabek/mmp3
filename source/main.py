import tkinter as tk
from source.content import program


def main():
    # Defining our root window
    master = tk.Tk()
    master.title("MMP3 - Mini MP3 Player")
    # root.iconbitmap("")
    master.geometry("480x640")
    master.resizable(False, False)
    master.config(bg="#2B2B2B")

    window = program.Program(master)

    master.mainloop()


main()
