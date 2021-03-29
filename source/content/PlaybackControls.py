import tkinter as tk
import random
import pygame
import tkinter.ttk as ttk


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

        self.isSongEndedFlag = None
        self.sliderUpdateFlag = None

        self.savedNewSongPosition = -1

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
                                  state=tk.DISABLED,
                                  command=self.resume_pause_playback)
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
                                     command=self.songsBox.shuffle_songs)
        self.btn_repeat = tk.Button(self.controlsFrame,
                                    image=self.img_repeat,
                                    bg="#2B2B2B",
                                    activebackground="#2B2B2B",
                                    borderwidth=0,
                                    command=self.repeat_switch)
        # self.scaleStyle = ttk.Style()
        # self.__configure_scale_style()
        self.slider_song = ttk.Scale(right_side_frame,
                                     length=300,
                                     # style='songSlider.Horizontal.TScale',
                                     from_=0,
                                     to=100,
                                     orient=tk.HORIZONTAL,
                                     value=0,
                                     state=tk.DISABLED,
                                     command=self.change_song_position)

        self.__bind_events_to_controls()
        self.__place_frame()
        self.__place_controls()

    def __configure_scale_style(self):
        self.scaleStyle.configure("songSlider.Horizontal.TScale", background='#FFDB00')

    def __bind_events_to_controls(self):
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

        self.slider_song.bind("<ButtonRelease-1>", lambda event: self.__set_song_from_new_position(e=event, new_position=self.slider_song.get()))

    def __on_enter(self, e, image):
        e.widget['image'] = image

    def __on_leave(self, e, image):
        e.widget['image'] = image

    def __set_song_from_new_position(self, e, new_position):
        self.slider_song.config(state=tk.NORMAL)
        self.songMetadata.wasSliderUsed = True
        self.songMetadata.song_playtime_counter(playtime_from_slider=new_position)
        if self.isSongPaused:
            self.savedNewSongPosition = new_position
            return
        else:
            pygame.mixer.music.play(loops=0, start=new_position)

    def __place_frame(self):
        self.controlsFrame.grid(row=1, column=0, sticky="w")

    def __place_controls(self):
        self.btn_prev.grid(row=0, column=0, padx=(0, 15))

        # Remembering pause button's position
        self.btn_pause.grid(row=0, column=1)
        self.btn_pause.grid_remove()

        self.btn_play.grid(row=0, column=1)
        self.btn_next.grid(row=0, column=2, padx=(15, 0))
        self.btn_shuffle.grid(row=0, column=3, ipadx="2px", padx=("20px", 0))
        self.btn_repeat.grid(row=0, column=4, ipadx="2px")

        self.slider_song.grid(row=2, column=0, padx=2, pady=(15, 0), sticky="we")

    def execute_preparation_actions_before_playing(self):
        if self.sliderUpdateFlag:
            self.slider_song.after_cancel(self.sliderUpdateFlag)

        self.update_slider_bound()
        self.songMetadata.reset_playtime()
        self.reset_slider_position()

    def resume_pause_playback(self):
        if self.__check_if_song_is_paused():
            return

        self.__change_play_button_to_pause()

    def play_selected_song(self):
        self.btn_play.config(state=tk.NORMAL)

        self.__wait_for_song_to_end()

        self.__change_play_button_to_pause()

        pygame.mixer.music.load(self.songsBox.currentSongFullPath)
        self.isSongLoaded = True
        self.songMetadata.read_song_metadata(self.songsBox.currentSongFullPath)

        self.slider_song.config(state=tk.NORMAL)

        self.update_slider_bound()
        self.update_slider_position()
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

        self.controlsFrame.after(50, self.__wait_for_song_to_end)

        self.update_slider_position()

        if self.check_if_song_position_changed_while_paused():
            pygame.mixer.music.play(loops=0, start=self.savedNewSongPosition)
            self.savedNewSongPosition = -1
            return

        pygame.mixer.music.unpause()

    def check_if_song_position_changed_while_paused(self):
        if self.savedNewSongPosition != -1:
            return True
        return False

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
                self.select_current_index()
                self.controlsFrame.after_cancel(self.isSongEndedFlag)
        self.isSongEndedFlag = self.controlsFrame.after(50, self.__wait_for_song_to_end)

    def __autoplay_next_song(self):
        if self.isSongOnRepeat:
            self.execute_preparation_actions_before_playing()
            pygame.mixer.music.load(self.songsBox.currentSongFullPath)
            pygame.mixer.music.play(loops=0)
            return

        if self.songsBox.songsListSize > 1 and self.songsBox.currentSongIndex < self.songsBox.songsListSize - 1:
            next_song = self.songsBox.songsFullPath[self.songsBox.currentSongIndex + 1]
            self.songsBox.currentSongFullPath = next_song
            self.songMetadata.read_song_metadata(next_song)
            self.songsBox.currentSongIndex += 1
            self.reset_slider_position()
            self.update_slider_bound()
            self.songMetadata.reset_playtime()
            pygame.mixer.music.load(next_song)
            pygame.mixer.music.play(loops=0)

    def select_current_index(self):
        self.songsBox.songsList.selection_clear(0, tk.END)
        self.songsBox.songsList.activate(self.songsBox.currentSongIndex)
        self.songsBox.songsList.selection_set(self.songsBox.currentSongIndex)

    def pause_song(self):
        if pygame.mixer.music.get_busy():
            self.isSongPaused = True
            self.slider_song.after_cancel(self.sliderUpdateFlag)
            pygame.mixer.music.pause()

            self.btn_pause.grid_remove()
            self.btn_play.grid()

    def next_song(self):
        if len(self.songsBox.currentSongFullPath) > 0:
            if self.songsBox.songsListSize > 1 and self.songsBox.currentSongIndex < self.songsBox.songsListSize - 1:
                next_song = self.songsBox.songsList.get(self.songsBox.currentSongIndex + 1)

                for path in self.songsBox.songsFullPath:
                    if path.find(next_song) != -1:
                        self.isSongPaused = False

                        next_song = path
                        self.songsBox.currentSongIndex += 1

                        self.__load_new_song(next_song)
                        self.isSongLoaded = True
                        self.place_pause_button()

                        self.execute_preparation_actions_before_playing()
                        self.update_slider_position()

    def prev_song(self):
        if self.songsBox.songsListSize > 1 and self.songsBox.currentSongIndex > 0:
            prev_song = self.songsBox.songsList.get(self.songsBox.currentSongIndex - 1)

            for path in self.songsBox.songsFullPath:
                if path.find(prev_song) != -1:
                    self.isSongPaused = False

                    prev_song = path
                    self.songsBox.currentSongIndex -= 1

                    self.__load_new_song(prev_song)
                    self.isSongLoaded = True
                    self.place_pause_button()

                    self.execute_preparation_actions_before_playing()
                    self.update_slider_position()

    def place_pause_button(self):
        self.btn_play.grid_remove()

        self.btn_pause.grid()

    def place_play_button(self):
        self.btn_pause.grid_remove()

        self.btn_play.grid()

    def __load_new_song(self, song):
        self.songsBox.currentSongFullPath = song

        self.select_current_index()

        self.songMetadata.read_song_metadata(self.songsBox.currentSongFullPath)

        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

    def clear_playback(self):
        # pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        self.isSongLoaded = False

        self.songMetadata.clear_song_metadata()

        self.reset_slider_position()
        self.slider_song.config(state=tk.DISABLED)

    def shuffle_songs(self):
        songs_full_paths_list = list(self.songsBox.songsFullPath)

        random.shuffle(songs_full_paths_list)

        if self.isSongLoaded:
            songs_full_paths_list.remove(self.songsBox.currentSongFullPath)
            songs_full_paths_list.insert(0, self.songsBox.currentSongFullPath)
            self.songsBox.currentSongIndex = 0

        self.songsBox.songsFullPath = tuple(songs_full_paths_list)

        songs_names_list = [name[name.rfind("/") + 1:-4] for name in songs_full_paths_list]

        self.songsBox.songsList.delete(0, tk.END)
        self.songsBox.songsList.insert(tk.END, *songs_names_list)

        self.select_current_index()

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

    def change_song_position(self, x):
        self.songMetadata.wasSliderUsed = True
        self.songMetadata.update_playtime_on_slide(self.slider_song.get())
        self.slider_song.config(state=tk.ACTIVE)

    def update_slider_position(self):
        if not self.isSongPaused and str(self.slider_song.cget("state")) == "normal":
            self.songMetadata.song_playtime_counter()
            self.slider_song.config(value=self.songMetadata.songRawPlaytime)

        self.sliderUpdateFlag = self.slider_song.after(250, self.update_slider_position)

    def reset_slider_position(self):
        self.slider_song.config(value=0)

    def update_slider_bound(self):
        self.slider_song.config(to=self.songMetadata.songRawLength)

    def __song_path_to_name(self, song_path):
        return song_path[song_path.rfind("/") + 1:]
