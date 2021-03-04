import tkinter as tk
from source.content import program


def main():
    # Defining our root window
    root = tk.Tk()
    root.title("MMP3 - Mini MP3 Player")
    # root.iconbitmap("")
    root.geometry("480x640")
    root.resizable(False, False)
    root.config(bg="#2B2B2B")

    window = program.Program(root)

    root.mainloop()


main()
