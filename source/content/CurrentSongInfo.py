import tkinter as tk


class CurrentSongInfo:
    def __init__(self, topFrame, rightSideFrame):
        self.cover = tk.Label(topFrame, width=18, height=8, bg="#BBBBBB", bd=0)
        self.__place_song_img()

        self.songInfoFrame = tk.Frame(rightSideFrame, background="green")
        self.songName = tk.Label(self.songInfoFrame, text="There has to be a song name", font="Tahoma 14")
        self.songLength = tk.Label(self.songInfoFrame, text="X:XX/X:XX", font="Tahoma 10")
        self.__place_song_info()

    def __place_song_img(self):
        # self.coverPlaceholder = PhotoImage(file="E:/PyCharm Projects/Images/img/cover placeholder.png")
        self.cover.grid(row=0, column=0, padx=25, pady=25)

    def __place_song_info(self):
        self.songInfoFrame.grid(row=0, column=0, pady=25, sticky="w")

        self.songName.grid(row=0, column=0)
        self.songLength.grid(row=1, column=0, sticky="w")