import tkinter as tk
from tkinter import filedialog
import source.content.GUI as GUI
import random


class SongsBox:
    def __init__(self, gui):
        self.gui = gui
        self.songMetadata = None
        self.playbackControls = None

        self.songsListSize = 0

        self.currentSongIndex = -1
        self.songsFullPaths = []
        self.currentSongFullPath = ""

        self.isSongRemovingMode = False

        self.query = tk.StringVar()

        self.__bind_songs_box_event()
        self.__bind_search_field_event()
        self.__give_commands_to_widgets()

    def __bind_songs_box_event(self):
        self.gui.songsList.bind("<ButtonRelease-1>", self.__play_selected_song)

    def __play_selected_song(self, e):
        self.playbackControls.execute_preparation_actions_before_playing()

        selected_song_name = self.gui.songsList.get(e.widget.curselection()[0])
        for path in self.songsFullPaths:
            if selected_song_name in path:
                self.currentSongIndex = self.songsFullPaths.index(path)
                self.currentSongFullPath = path

        self.playbackControls.play_selected_song()

        self.update_song_qty_label()

    def __bind_search_field_event(self):
        self.gui.field_search.bind("<KeyRelease>", lambda event: self.__search_songs_from_entry(event))

    def __search_songs_from_entry(self, e):
        items_list = self.get_song_names_from_paths(self.songsFullPaths)
        self.gui.songsList.delete(0, tk.END)

        query_result = [item for item in items_list if self.query.get() in item]

        self.gui.songsList.insert(tk.END, *query_result)

        if len(self.query.get()) == 0:
            for item in items_list:
                if self.songMetadata.songTitle in item:
                    self.gui.songsList.activate(items_list.index(item))
                    self.gui.songsList.selection_set(items_list.index(item))

    def __get_current_song_full_path(self):
        for path in self.songsFullPaths:
            if path.find(self.gui.songsList.get(self.currentSongIndex)) != -1:
                self.currentSongFullPath = path
                break

    def __give_commands_to_widgets(self):
        self.gui.btn_add_songs.config(command=self.__add_songs)
        self.gui.btn_song_removing_mode_switch.config(command=self.song_removing_mode_switch)
        self.gui.btn_remove_selected_songs.config(command=self.__remove_selected_songs)
        self.gui.btn_shuffle.config(command=self.shuffle_songs)

        self.gui.field_search.config(textvariable=self.query)

    def __add_songs(self):
        songs_new = filedialog.askopenfilenames(filetypes=((".mp3", "*.mp3"),))
        if len(songs_new) > 0:
            for song in songs_new:
                if song in self.songsFullPaths or song[-3:] != "mp3":
                    songs_new_list = list(songs_new)
                    songs_new_list.remove(song)
                    songs_new = tuple(songs_new_list)

            self.songsFullPaths += songs_new
            songs_name_only = self.get_song_names_from_paths(songs_new)
            self.gui.songsList.insert(tk.END, *songs_name_only)
            self.songsListSize += len(songs_new)

        self.update_song_qty_label()

    def get_song_names_from_paths(self, songs_list):
        songs_name_only = [name[name.rfind("/") + 1:-4] for name in songs_list]
        return songs_name_only

    def update_song_qty_label(self):
        if len(self.gui.songsList.curselection()) == 0 and self.currentSongIndex == -1 or self.songsListSize == 0:
            self.gui.songsQtyLabel.config(text=f"{str(self.songsListSize)} song(s)")
        else:
            self.gui.songsQtyLabel.config(text=f"{str(self.currentSongIndex+1)} of {str(self.songsListSize)} song(s)")

    def shuffle_songs(self):
        songs_full_paths_list = list(self.songsFullPaths)

        random.shuffle(songs_full_paths_list)

        if self.playbackControls.isSongLoaded:
            songs_full_paths_list.remove(self.currentSongFullPath)
            songs_full_paths_list.insert(0, self.currentSongFullPath)
            self.currentSongIndex = 0

        self.songsFullPaths = songs_full_paths_list

        songs_names_list = [name[name.rfind("/") + 1:-4] for name in songs_full_paths_list]

        self.gui.songsList.delete(0, tk.END)
        self.gui.songsList.insert(tk.END, *songs_names_list)

        self.select_current_index()
        self.update_song_qty_label()

    def check_if_song_is_borderline(self):
        if self.currentSongIndex == 0 and self.songsListSize == 1:
            return -1
        if self.currentSongIndex == 0 and self.songsListSize > 1:
            return 0
        if self.currentSongIndex + 1 == self.songsListSize:
            return 1

    def song_removing_mode_switch(self):
        if not self.isSongRemovingMode:
            self.isSongRemovingMode = True
            self.gui.songsList.config(selectmode=tk.EXTENDED)
            self.gui.songsList.unbind("<ButtonRelease-1>")

            self.gui.btn_song_removing_mode_switch.config(bg="#6E6E6E")
            self.gui.btn_remove_selected_songs.config(state=tk.NORMAL)
        else:
            self.isSongRemovingMode = False
            self.gui.songsList.config(selectmode=tk.BROWSE)
            self.__bind_songs_box_event()

            self.gui.btn_song_removing_mode_switch.config(bg=GUI.GUI.backgroundColor)
            self.gui.btn_remove_selected_songs.config(state=tk.DISABLED)

            self.select_current_index()

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

        if self.songsListSize == 0:
            self.currentSongIndex = -1

        for song_title in selected_songs_titles:
            all_songs_titles.remove(song_title)

        self.gui.songsList.delete(0, tk.END)
        self.gui.songsList.insert(tk.END, *all_songs_titles)

        if self.playbackControls.isSongLoaded:
            self.__find_song_by_name()
        if self.currentSongIndex != -1:
            self.select_current_index()

        self.update_song_qty_label()

    def __find_song_by_name(self):
        for item in self.gui.songsList.get(0, tk.END):
            if self.songMetadata.songTitle in item:
                self.currentSongIndex = self.gui.songsList.get(0, tk.END).index(item)

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
