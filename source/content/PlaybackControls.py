import tkinter as tk
import random
import pygame


class PlaybackControls:
    def __init__(self, right_side_frame, songs_box, song_metadata):
        self.controlsFrame = tk.Frame(right_side_frame)

        self.songsBox = songs_box
        self.songMetadata = song_metadata

        self.SONG_END = pygame.USEREVENT
        pygame.mixer.music.set_endevent(self.SONG_END)
        self.isSongPaused = False
        self.isSongOnRepeat = False
        self.isSongLoaded = False

        self.img_prev = tk.PhotoImage(file="../img/icons/previous.png")
        self.img_prev_hover = tk.PhotoImage(file="../img/icons/previous(hover).png")
        self.img_play = tk.PhotoImage(file="../img/icons/play.png")
        self.img_play_hover = tk.PhotoImage(file="../img/icons/play(hover).png")

        self.img_pause = tk.PhotoImage(file="../img/icons/pause(big).png")
        self.img_pause_hover = tk.PhotoImage(file="../img/icons/pause(big hover).png")

        self.img_next = tk.PhotoImage(file="../img/icons/next.png")
        self.img_next_hover = tk.PhotoImage(file="../img/icons/next(hover).png")
        self.img_shuffle = tk.PhotoImage(file="../img/icons/shuffle.png")
        self.img_shuffle_hover = tk.PhotoImage(file="../img/icons/shuffle(hover).png")
        self.img_repeat = tk.PhotoImage(file="../img/icons/repeat.png")
        self.img_repeat_hover = tk.PhotoImage(file="../img/icons/repeat(hover).png")
        self.img_repeat_active = tk.PhotoImage(file="../img/icons/repeat(active).png")
        self.img_repeat_active_hover = tk.PhotoImage(file="../img/icons/repeat(active hover).png")

        self.btn_prev = tk.Button(self.controlsFrame,
                                  image=self.img_prev,
                                  bg="#2B2B2B",
                                  activebackground="#2B2B2B",
                                  borderwidth=0,
                                  command=self.prev_song)
        self.btn_play = tk.Button(self.controlsFrame,
                                  image=self.img_play,
                                  bg="#2B2B2B",
                                  activebackground="#2B2B2B",
                                  borderwidth=0,
                                  command=self.play_song)
        self.btn_pause = tk.Button(self.controlsFrame,
                                   image=self.img_pause,
                                   bg="#2B2B2B",
                                   activebackground="#2B2B2B",
                                   borderwidth=0,
                                   command=self.pause_song)
        self.btn_next = tk.Button(self.controlsFrame,
                                  image=self.img_next,
                                  bg="#2B2B2B",
                                  activebackground="#2B2B2B",
                                  borderwidth=0,
                                  command=self.next_song)
        self.btn_shuffle = tk.Button(self.controlsFrame,
                                     image=self.img_shuffle,
                                     bg="#2B2B2B",
                                     activebackground="#2B2B2B",
                                     borderwidth=0,
                                     command=self.shuffle_songs)
        self.btn_repeat = tk.Button(self.controlsFrame,
                                    image=self.img_repeat,
                                    bg="#2B2B2B",
                                    activebackground="#2B2B2B",
                                    borderwidth=0,
                                    command=self.repeat_switch)

        self.__bind_events_to_buttons()
        self.__place_frame()
        self.__place_buttons()

    def __bind_events_to_buttons(self):
        self.btn_prev.bind("<Enter>", lambda event, image=self.img_prev_hover: self.__on_enter(e=event, image=image))
        self.btn_prev.bind("<Leave>", lambda event, image=self.img_prev: self.__on_leave(e=event, image=image))

        self.btn_play.bind("<Enter>", lambda event, image=self.img_play_hover: self.__on_enter(e=event, image=image))
        self.btn_play.bind("<Leave>", lambda event, image=self.img_play: self.__on_leave(e=event, image=image))

        self.btn_pause.bind("<Enter>", lambda event, image=self.img_pause_hover: self.__on_enter(e=event, image=image))
        self.btn_pause.bind("<Leave>", lambda event, image=self.img_pause: self.__on_leave(e=event, image=image))

        self.btn_next.bind("<Enter>", lambda event, image=self.img_next_hover: self.__on_enter(e=event, image=image))
        self.btn_next.bind("<Leave>", lambda event, image=self.img_next: self.__on_leave(e=event, image=image))

        self.btn_shuffle.bind("<Enter>", lambda event, image=self.img_shuffle_hover: self.__on_enter(e=event, image=image))
        self.btn_shuffle.bind("<Leave>", lambda event, image=self.img_shuffle: self.__on_leave(e=event, image=image))

        self.btn_repeat.bind("<Enter>", lambda event, image=self.img_repeat_hover: self.__on_enter(e=event, image=image))
        self.btn_repeat.bind("<Leave>", lambda event, image=self.img_repeat: self.__on_leave(e=event, image=image))

    def __on_enter(self, e, image):
        e.widget['image'] = image

    def __on_leave(self, e, image):
        e.widget['image'] = image

    def __place_frame(self):
        self.controlsFrame.grid(row=1, column=0, sticky="w")

    def __place_buttons(self):
        self.btn_prev.grid(row=0, column=0, padx=(0, 15))

        # Remembering pause button's position
        self.btn_pause.grid(row=0, column=2)
        self.btn_pause.grid_remove()

        self.btn_play.grid(row=0, column=2)
        self.btn_next.grid(row=0, column=4, padx=(15, 0))
        self.btn_shuffle.grid(row=0, column=5, ipadx="2px", padx=("20px", 0))
        self.btn_repeat.grid(row=0, column=6, ipadx="2px")

    def play_song(self):
        self.controlsFrame.after(50, self.__wait_for_song_to_end)

        if self.__check_if_song_is_paused():
            return

        self.__change_play_button_to_pause()

        self.__get_current_song_full_path()

        pygame.mixer.music.load(self.songsBox.currentSongFullPath)
        self.isSongLoaded = True
        self.songMetadata.read_song_metadata(self.songsBox.currentSongFullPath)
        pygame.mixer.music.play(loops=0)

    def __check_if_song_is_paused(self):
        if not pygame.mixer.music.get_busy() and self.isSongPaused:
            self.__unpause()
            return True
        return False

    def __unpause(self):
        self.isSongPaused = False
        self.btn_play.grid_remove()
        self.btn_pause.grid()
        pygame.mixer.music.unpause()

    def __change_play_button_to_pause(self):
        if len(self.songsBox.songsFullPath) > 0:
            self.btn_play.grid_remove()
            self.btn_pause.grid()

    def __get_current_song_full_path(self):
        for path in self.songsBox.songsFullPath:
            if path.find(self.songsBox.songsList.get(tk.ACTIVE)) != -1:
                self.songsBox.currentSongFullPath = path
                break

    def __wait_for_song_to_end(self):
        for event in pygame.event.get():
            if event.type == self.SONG_END:
                self.__autoplay_next_song()
                self.__select_current_index()
        self.controlsFrame.after(50, self.__wait_for_song_to_end)

    def __autoplay_next_song(self):
        if self.isSongOnRepeat:
            pygame.mixer.music.load(self.songsBox.currentSongFullPath)
            pygame.mixer.music.play(loops=0)
            return

        if self.songsBox.songsListSize > 1 and self.songsBox.currentSongIndex < self.songsBox.songsListSize - 1:
            next_song = self.songsBox.songsFullPath[self.songsBox.currentSongIndex + 1]
            self.songMetadata.read_song_metadata(next_song)
            self.songsBox.currentSongFullPath = next_song
            self.songsBox.currentSongIndex += 1
            pygame.mixer.music.load(next_song)
            pygame.mixer.music.play(loops=0)

    def __select_current_index(self):
        self.songsBox.songsList.selection_clear(0, tk.END)
        self.songsBox.songsList.activate(self.songsBox.currentSongIndex)
        self.songsBox.songsList.selection_set(self.songsBox.currentSongIndex)

    def pause_song(self):
        if pygame.mixer.music.get_busy():
            self.isSongPaused = True
            pygame.mixer.music.pause()

            self.btn_pause.grid_remove()
            self.btn_play.grid()

    def next_song(self):
        if self.songsBox.songsListSize > 1 and self.songsBox.currentSongIndex < self.songsBox.songsListSize - 1:
            next_song = self.songsBox.songsList.get(self.songsBox.currentSongIndex + 1)

            for path in self.songsBox.songsFullPath:
                if path.find(next_song) != -1:
                    next_song = path
                    self.songsBox.currentSongIndex += 1

                    self.__load_new_song(next_song)
                    self.isSongLoaded = True
                    self.place_pause_button()

    def prev_song(self):
        if self.songsBox.songsListSize > 1 and self.songsBox.currentSongIndex > 0:
            prev_song = self.songsBox.songsList.get(self.songsBox.currentSongIndex - 1)

            for path in self.songsBox.songsFullPath:
                if path.find(prev_song) != -1:
                    prev_song = path
                    self.songsBox.currentSongIndex -= 1

                    self.__load_new_song(prev_song)
                    self.isSongLoaded = True
                    self.place_pause_button()

    def place_pause_button(self):
        self.btn_play.grid_remove()

        self.btn_pause.grid()

    def place_play_button(self):
        self.btn_pause.grid_remove()

        self.btn_play.grid()

    def __load_new_song(self, song):
        self.songsBox.currentSongFullPath = song

        self.__select_current_index()

        self.songMetadata.read_song_metadata(self.songsBox.currentSongFullPath)

        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

    def clear_playback(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        self.songMetadata.clear_song_metadata()

    def shuffle_songs(self):
        songs_full_paths_list = list(self.songsBox.songsFullPath)

        random.shuffle(songs_full_paths_list)

        if self.isSongLoaded:
            songs_full_paths_list.remove(self.songsBox.currentSongFullPath)
            songs_full_paths_list.insert(0, self.songsBox.currentSongFullPath)
            self.songsBox.currentSongIndex = 0

        songs_names_list = [name[name.rfind("/") + 1:-4] for name in songs_full_paths_list]

        self.songsBox.songsList.delete(0, tk.END)
        self.songsBox.songsList.insert(tk.END, *songs_names_list)
        self.__select_current_index()

    def repeat_switch(self):
        if self.isSongLoaded:
            if self.isSongOnRepeat:
                self.btn_repeat.config(image=self.img_repeat)
                self.isSongOnRepeat = False
                self.btn_repeat.bind("<Enter>", lambda event, image=self.img_repeat_hover: self.__on_enter(e=event, image=image))
                self.btn_repeat.bind("<Leave>", lambda event, image=self.img_repeat: self.__on_leave(e=event, image=image))
                return

            self.btn_repeat.config(image=self.img_repeat_active)
            self.btn_repeat.bind("<Enter>", lambda event, image=self.img_repeat_active_hover: self.__on_enter(e=event, image=image))
            self.btn_repeat.bind("<Leave>", lambda event, image=self.img_repeat_active: self.__on_leave(e=event, image=image))
            self.isSongOnRepeat = True

    def __song_path_to_name(self, song_path):
        return song_path[song_path.rfind("/") + 1:]
