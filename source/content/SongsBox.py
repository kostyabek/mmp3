import tkinter as tk
from tkinter import filedialog
import random


class SongsBox:
    def __init__(self, gui):
        self.gui = gui
        self.songMetadata = None
        self.playbackControls = None

        self.songsListSize = 0

        self.currentSongIndex = 0
        self.songsFullPaths = ()
        self.currentSongFullPath = ""

        self.__bind_songs_box_event()
        self.__give_commands_to_buttons()

    def __bind_songs_box_event(self):
        self.gui.songsList.bind("<ButtonRelease-1>", self.__play_selected_song)

    def __play_selected_song(self, e):
        self.playbackControls.execute_preparation_actions_before_playing()
        self.currentSongIndex = e.widget.curselection()[0]
        self.__get_current_song_full_path()
        self.playbackControls.play_selected_song()

    def __get_current_song_full_path(self):
        for path in self.songsFullPaths:
            if path.find(self.gui.songsList.get(self.currentSongIndex)) != -1:
                self.currentSongFullPath = path
                break

    def __give_commands_to_buttons(self):
        self.gui.btn_add_songs.config(command=self.__add_songs)
        self.gui.btn_clear_songs_list.config(command=self.clear_songs_list)
        self.gui.btn_shuffle.config(command=self.shuffle_songs)

    def __add_songs(self):
        songs_new = filedialog.askopenfilenames(filetypes=((".mp3", "*.mp3"),))
        if len(songs_new) > 0:
            for song in songs_new:
                if song in self.songsFullPaths:
                    songs_new_list = list(songs_new)
                    songs_new_list.remove(song)
                    songs_new = tuple(songs_new_list)

            self.songsFullPaths += songs_new
            songs_name_only = [name[name.rfind("/") + 1:-4] for name in songs_new]
            self.gui.songsList.insert(tk.END, *songs_name_only)
            self.songsListSize += len(songs_new)

    def clear_songs_list(self):
        self.gui.songsList.delete(0, tk.END)
        self.songsFullPaths = ()
        self.songsListSize = 0
        self.currentSongIndex = 0

        self.songMetadata.clear_song_metadata()

        self.playbackControls.clear_playback()
        self.gui.place_play_button()

    def shuffle_songs(self):
        songs_full_paths_list = list(self.songsFullPaths)

        random.shuffle(songs_full_paths_list)

        if self.playbackControls.isSongLoaded:
            songs_full_paths_list.remove(self.currentSongFullPath)
            songs_full_paths_list.insert(0, self.currentSongFullPath)
            self.currentSongIndex = 0

        self.songsFullPaths = tuple(songs_full_paths_list)

        songs_names_list = [name[name.rfind("/") + 1:-4] for name in songs_full_paths_list]

        self.gui.songsList.delete(0, tk.END)
        self.gui.songsList.insert(tk.END, *songs_names_list)

        self.playbackControls.select_current_index()

    def check_if_song_is_borderline(self):
        if self.currentSongIndex == 0 and self.songsListSize == 1:
            return -1
        if self.currentSongIndex == 0 and self.songsListSize > 1:
            return 0
        if self.currentSongIndex + 1 == self.songsListSize:
            return 1

    def get_playback_controls_reference(self, playback_controls_object):
        self.playbackControls = playback_controls_object

    def get_song_metadata_reference(self, song_metadata_object):
        self.songMetadata = song_metadata_object
