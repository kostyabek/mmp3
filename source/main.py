import tkinter as tk
from source.content import Program


def main():
    master = tk.Tk()
    window = Program.Program(master)

    master.mainloop()


main()
