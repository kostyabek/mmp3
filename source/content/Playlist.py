import tkinter as tk
from tkinter import filedialog


class Playlist:
    songsFullPath = ()

    def __init__(self, bottomFrame):
        self.songsList = tk.Listbox(bottomFrame, bg="#3C3F41", fg="#BBBBBB", selectbackground="#2B2B2B")

        self.img_add_songs = tk.PhotoImage(file="E:/PyCharm Projects/Images/img/icons/plus.png")
        self.img_remove_songs = tk.PhotoImage(file="E:/PyCharm Projects/Images/img/icons/minus.png")

        self.btn_add_songs = tk.Button(bottomFrame,
                                       image=self.img_add_songs,
                                       bg="#3C3F41",
                                       fg="#BBBBBB",
                                       relief=tk.GROOVE,
                                       bd=0,
                                       command=self.add_songs)

        self.btn_clear_songs_list = tk.Button(bottomFrame,
                                              image=self.img_remove_songs,
                                              bg="#3C3F41",
                                              fg="#BBBBBB",
                                              relief=tk.GROOVE,
                                              bd=0,
                                              command=self.clear_songs_list)

        self.btn_enter_song_removing_mode = tk.Button(bottomFrame,
                                                      text="Remove chosen songs",
                                                      width=20,
                                                      bg="#3C3F41",
                                                      fg="#BBBBBB",
                                                      relief=tk.GROOVE,
                                                      bd=0,
                                                      command=self.enter_song_removing_mode)

        self.btn_remove_chosen_songs = tk.Button(bottomFrame,
                                                 text="Remove chosen songs",
                                                 width=20,
                                                 bg="#3C3F41",
                                                 fg="#BBBBBB",
                                                 relief=tk.GROOVE,
                                                 bd=0,
                                                 command=self.remove_chosen_songs)

        self.songsListSize = 0

        self.place_playlist()
        self.place_buttons()

        self.removingSongs = False

    def place_playlist(self):
        self.songsList.pack(fill="both", expand=True)

    def place_buttons(self):
        self.btn_add_songs.pack(side=tk.LEFT, ipadx="5px", ipady="2px")
        self.btn_clear_songs_list.pack(side=tk.LEFT, ipadx="5px", ipady="2px")
        # self.btn_enter_song_removing_mode.pack(side=tk.LEFT, ipadx="5px")

    def add_songs(self):
        songsNew = filedialog.askopenfilenames(filetypes=((".mp3", "*.mp3"),))
        if len(songsNew) > 0:
            for song in songsNew:
                if song in self.songsFullPath:
                    songsNewList = list(songsNew)
                    songsNewList.remove(song)
                    songsNew = tuple(songsNewList)

            Playlist.songsFullPath += songsNew
            songsNameOnly = [name[name.rfind("/") + 1:] for name in songsNew]
            self.songsList.insert(tk.END, *songsNameOnly)
            self.songsListSize += len(songsNew)

    def clear_songs_list(self):
        self.songsList.delete(0, tk.END)
        Playlist.songsFullPath = ()

    def enter_song_removing_mode(self):
        # self.removingSongs = True
        # self.btn_enter_song_removing_mode.config(bg="#C62626", text="Remove!")
        self.songsList.config(selectmode=tk.EXTENDED)

    def remove_chosen_songs(self):
        pass
