import tkinter as tk
from tkinter import filedialog
import random


class SongsBox:
    songsFullPath = ()

    def __init__(self, bottom_frame):
        self.songMetadata = None
        self.playbackControls = None

        self.songsList = tk.Listbox(bottom_frame, bg="#3C3F41", fg="#BBBBBB", selectbackground="#2B2B2B")

        self.img_add_songs = tk.PhotoImage(file="../img/icons/plus.png")
        self.img_add_songs_hover = tk.PhotoImage(file="../img/icons/plus(hover).png")
        self.img_clear_songs_list = tk.PhotoImage(file="../img/icons/minus.png")
        self.img_clear_songs_list_hover = tk.PhotoImage(file="../img/icons/minus(hover).png")

        self.btn_add_songs = tk.Button(bottom_frame,
                                       image=self.img_add_songs,
                                       bg="#3C3F41",
                                       fg="#BBBBBB",
                                       relief=tk.GROOVE,
                                       bd=0,
                                       command=self.__add_songs)

        self.btn_clear_songs_list = tk.Button(bottom_frame,
                                              image=self.img_clear_songs_list,
                                              bg="#3C3F41",
                                              fg="#BBBBBB",
                                              relief=tk.GROOVE,
                                              bd=0,
                                              command=self.clear_songs_list)

        self.btn_enter_song_removing_mode = tk.Button(bottom_frame,
                                                      text="Remove chosen songs",
                                                      width=20,
                                                      bg="#3C3F41",
                                                      fg="#BBBBBB",
                                                      relief=tk.GROOVE,
                                                      bd=0,
                                                      command=self.enter_song_removing_mode)

        self.btn_remove_chosen_songs = tk.Button(bottom_frame,
                                                 text="Remove chosen songs",
                                                 width=20,
                                                 bg="#3C3F41",
                                                 fg="#BBBBBB",
                                                 relief=tk.GROOVE,
                                                 bd=0,
                                                 command=self.remove_chosen_songs)

        self.songsListSize = 0

        self.__bind_events_to_songs_list()
        self.__place_playlist()
        self.__bind_events_to_buttons()
        self.__place_buttons()

        self.removingSongs = False
        self.currentSongIndex = 0
        self.currentSongFullPath = ""

    def __place_playlist(self):
        self.songsList.pack(fill="both", expand=True)

    def __bind_events_to_buttons(self):
        self.btn_add_songs.bind("<Enter>",
                                lambda event, image=self.img_add_songs_hover: self.__on_enter(e=event, image=image))
        self.btn_add_songs.bind("<Leave>",
                                lambda event, image=self.img_add_songs: self.__on_leave(e=event, image=image))

        self.btn_clear_songs_list.bind("<Enter>",
                                       lambda event, image=self.img_clear_songs_list_hover: self.__on_enter(e=event, image=image))
        self.btn_clear_songs_list.bind("<Leave>",
                                       lambda event, image=self.img_clear_songs_list: self.__on_leave(e=event, image=image))

    def __on_enter(self, e, image):
        e.widget['image'] = image

    def __on_leave(self, e, image):
        e.widget['image'] = image

    def __bind_events_to_songs_list(self):
        self.songsList.bind("<ButtonRelease-1>", self.__play_selected_song)

    def __play_selected_song(self, e):
        self.playbackControls.execute_preparation_actions_before_playing()

        self.currentSongIndex = e.widget.curselection()[0]
        self.__get_current_song_full_path()
        self.playbackControls.play_selected_song()

    def __get_current_song_full_path(self):
        for path in SongsBox.songsFullPath:
            if path.find(self.songsList.get(self.currentSongIndex)) != -1:
                self.currentSongFullPath = path
                print(self.currentSongFullPath)
                break

    def __place_buttons(self):
        self.btn_add_songs.pack(side=tk.LEFT, ipadx="5px", ipady="2px")
        self.btn_clear_songs_list.pack(side=tk.LEFT, ipadx="5px", ipady="2px")
        # self.btn_enter_song_removing_mode.pack(side=tk.LEFT, ipadx="5px")

    def __add_songs(self):
        songs_new = filedialog.askopenfilenames(filetypes=((".mp3", "*.mp3"),))
        if len(songs_new) > 0:
            for song in songs_new:
                if song in SongsBox.songsFullPath:
                    songs_new_list = list(songs_new)
                    songs_new_list.remove(song)
                    songs_new = tuple(songs_new_list)

            SongsBox.songsFullPath += songs_new
            songs_name_only = [name[name.rfind("/") + 1:-4] for name in songs_new]
            self.songsList.insert(tk.END, *songs_name_only)
            self.songsListSize += len(songs_new)
            # self.songsList.activate(0)
            # self.songsList.selection_set(0)

    def clear_songs_list(self):
        self.songsList.delete(0, tk.END)
        SongsBox.songsFullPath = ()

        self.songMetadata.clear_song_metadata()

        self.playbackControls.clear_playback()
        self.playbackControls.place_play_button()

    def shuffle_songs(self):
        songs_full_paths_list = list(SongsBox.songsFullPath)

        random.shuffle(songs_full_paths_list)

        if self.playbackControls.isSongLoaded:
            songs_full_paths_list.remove(self.currentSongFullPath)
            songs_full_paths_list.insert(0, self.currentSongFullPath)
            self.currentSongIndex = 0

        self.songsFullPath = tuple(songs_full_paths_list)

        songs_names_list = [name[name.rfind("/") + 1:-4] for name in songs_full_paths_list]

        self.songsList.delete(0, tk.END)
        self.songsList.insert(tk.END, *songs_names_list)

        self.playbackControls.select_current_index()

    def enter_song_removing_mode(self):
        # self.removingSongs = True
        # self.btn_enter_song_removing_mode.config(bg="#C62626", text="Remove!")
        self.songsList.config(selectmode=tk.EXTENDED)

    def remove_chosen_songs(self):
        pass

    def get_song_metadata_reference(self, song_metadata):
        self.songMetadata = song_metadata

    def get_song_playback_controls_reference(self, playback_controls):
        self.playbackControls = playback_controls


