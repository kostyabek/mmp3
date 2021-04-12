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

        self.isSongRemovingMode = False

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
        self.gui.btn_enter_song_removing_mode.config(command=self.enter_song_removing_mode)
        self.gui.btn_remove_selected_songs.config(command=self.__remove_selected_songs)
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

    # def remove_all_songs(self):
    #     self.gui.songsList.delete(0, tk.END)
    #     self.gui.place_play_button()
    #
    #     self.songsFullPaths = ()
    #     self.songsListSize = 0
    #     self.currentSongIndex = 0
    #
    #     self.songMetadata.clear_song_metadata()
    #
    #     self.playbackControls.clear_playback()

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

        self.select_current_index()

    def check_if_song_is_borderline(self):
        # NEEDS REFACTORING
        if self.currentSongIndex == 0 and self.songsListSize == 1:
            return -1
        if self.currentSongIndex == 0 and self.songsListSize > 1:
            return 0
        if self.currentSongIndex + 1 == self.songsListSize:
            return 1

    def enter_song_removing_mode(self):
        if not self.isSongRemovingMode:
            self.isSongRemovingMode = True
            self.gui.songsList.config(selectmode=tk.EXTENDED)
            self.gui.songsList.unbind("<ButtonRelease-1>")

            self.gui.btn_enter_song_removing_mode.config(bg="#6E6E6E")
            self.gui.btn_remove_selected_songs.config(state=tk.NORMAL)
        else:
            self.isSongRemovingMode = False
            self.gui.songsList.config(selectmode=tk.BROWSE)
            self.__bind_songs_box_event()

            self.gui.btn_enter_song_removing_mode.config(bg="#3C3F41")
            self.gui.btn_remove_selected_songs.config(state=tk.DISABLED)

    def __remove_selected_songs(self):
        selected_songs_indices = self.gui.songsList.curselection()
        selected_songs_titles = []

        songs_full_paths_list = list(self.songsFullPaths)
        all_songs_titles = list(self.gui.songsList.get(0, tk.END))

        for i in selected_songs_indices:
            selected_songs_titles.append(self.gui.songsList.get(i))

        for song_title in selected_songs_titles:
            for song_full_path in songs_full_paths_list:
                if song_title in song_full_path:
                    songs_full_paths_list.remove(song_full_path)
                    if self.currentSongFullPath.find(song_title) != -1:
                        self.reset_player_state()

        self.songsFullPaths = tuple(songs_full_paths_list)
        self.songsListSize = len(self.songsFullPaths)

        for song_title in selected_songs_titles:
            all_songs_titles.remove(song_title)

        self.gui.songsList.delete(0, tk.END)
        self.gui.songsList.insert(tk.END, *all_songs_titles)
        self.select_current_index()

    def select_current_index(self):
        self.gui.songsList.selection_clear(0, tk.END)
        self.gui.songsList.activate(self.currentSongIndex)
        self.gui.songsList.selection_set(self.currentSongIndex)

    def reset_player_state(self):
        self.gui.place_play_button()

        self.currentSongIndex = 0

        self.songMetadata.clear_song_metadata()

        self.playbackControls.clear_playback()

    def get_playback_controls_reference(self, playback_controls_object):
        self.playbackControls = playback_controls_object

    def get_song_metadata_reference(self, song_metadata_object):
        self.songMetadata = song_metadata_object
