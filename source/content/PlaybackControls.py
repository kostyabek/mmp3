import tkinter as tk
import pygame


class PlaybackControls:
    def __init__(self, gui):
        self.gui = gui
        self.songsBox = None
        self.songMetadata = None

        self.SONG_END = pygame.USEREVENT
        pygame.mixer.music.set_endevent(self.SONG_END)
        self.isSongPaused = False
        self.isSongOnRepeat = False
        self.isSongLoaded = False

        self.isSongEndedFlag = None
        self.sliderUpdateFlag = None

        self.savedNewSongPosition = -1

        self.__bind_slider_event()
        self.__give_commands_to_controls()

        self.__cycle_button_state_changer()

    def __bind_slider_event(self):
        self.gui.slider_song.bind("<ButtonRelease-1>", lambda event: self.__set_song_from_new_position(e=event, new_position=self.gui.slider_song.get()))

    def __set_song_from_new_position(self, e, new_position):
        self.gui.slider_song.config(state=tk.NORMAL)
        self.songMetadata.wasSliderUsed = True
        self.songMetadata.song_playtime_counter(playtime_from_slider=new_position)
        if self.isSongPaused:
            self.savedNewSongPosition = new_position
            return
        else:
            pygame.mixer.music.play(loops=0, start=new_position)

    def __give_commands_to_controls(self):
        self.gui.btn_prev.config(command=self.prev_song)
        self.gui.btn_play.config(command=self.resume_pause_playback)
        self.gui.btn_pause.config(command=self.pause_song)
        self.gui.btn_next.config(command=self.next_song)
        self.gui.btn_repeat.config(command=self.repeat_switch)
        self.gui.slider_song.config(command=self.change_song_position)

    def prev_song(self):
        if self.songsBox.songsListSize > 1 and self.songsBox.currentSongIndex > 0:
            prev_song = self.gui.songsList.get(self.songsBox.currentSongIndex - 1)

            for path in self.songsBox.songsFullPaths:
                if path.find(prev_song) != -1:
                    self.isSongPaused = False

                    prev_song = path
                    self.songsBox.currentSongIndex -= 1

                    self.__load_new_song(prev_song)
                    self.isSongLoaded = True
                    self.gui.place_pause_button()

                    self.execute_preparation_actions_before_playing()
                    self.__cycle_update_slider_position()

                    pygame.mixer.music.play(loops=0)

    def execute_preparation_actions_before_playing(self):
        if self.sliderUpdateFlag:
            self.gui.slider_song.after_cancel(self.sliderUpdateFlag)

        # self.songMetadata.clear_song_metadata()

        self.update_slider_bound()
        self.songMetadata.reset_playtime()
        self.reset_slider_position()

    def update_slider_bound(self):
        self.gui.slider_song.config(to=self.songMetadata.songRawLength)

    def reset_slider_position(self):
        self.gui.slider_song.config(value=0)

    def __cycle_update_slider_position(self):
        if not self.isSongPaused and str(self.gui.slider_song.cget("state")) == "normal":
            self.songMetadata.song_playtime_counter()
            self.gui.slider_song.config(value=self.songMetadata.songRawPlaytime)

        self.sliderUpdateFlag = self.gui.slider_song.after(250, self.__cycle_update_slider_position)

    def resume_pause_playback(self):
        if self.__check_if_song_is_paused():
            return

        self.__change_play_button_to_pause()

    def __check_if_song_is_paused(self):
        if not pygame.mixer.music.get_busy() and self.isSongPaused:
            self.__unpause()
            return True
        return False

    def __unpause(self):
        self.isSongPaused = False
        self.gui.btn_play.grid_remove()
        self.gui.btn_pause.grid()

        self.gui.controlsFrame.after(50, self.__cycle_wait_for_song_to_end)

        self.__cycle_update_slider_position()

        if self.check_if_song_position_changed_while_paused():
            pygame.mixer.music.play(loops=0, start=self.savedNewSongPosition)
            self.savedNewSongPosition = -1
            return

        pygame.mixer.music.unpause()

    def __cycle_wait_for_song_to_end(self):
        for event in pygame.event.get():
            if event.type == self.SONG_END:
                self.__autoplay_next_song()
                self.select_current_index()
                self.gui.controlsFrame.after_cancel(self.isSongEndedFlag)
        self.isSongEndedFlag = self.gui.controlsFrame.after(50, self.__cycle_wait_for_song_to_end)

    def select_current_index(self):
        self.gui.songsList.selection_clear(0, tk.END)
        self.gui.songsList.activate(self.songsBox.currentSongIndex)
        self.gui.songsList.selection_set(self.songsBox.currentSongIndex)

    def __autoplay_next_song(self):
        if self.isSongOnRepeat:
            self.execute_preparation_actions_before_playing()
            pygame.mixer.music.load(self.songsBox.currentSongFullPath)
            pygame.mixer.music.play(loops=0)
            self.__cycle_update_slider_position()
            return

        if self.songsBox.songsListSize > 1 and self.songsBox.currentSongIndex < self.songsBox.songsListSize - 1:
            self.songsBox.currentSongIndex += 1

            next_song = self.songsBox.songsFullPaths[self.songsBox.currentSongIndex]
            self.songsBox.currentSongFullPath = next_song
            self.songMetadata.read_song_metadata(next_song)

            self.reset_slider_position()
            self.update_slider_bound()
            self.songMetadata.reset_playtime()

            pygame.mixer.music.load(next_song)
            pygame.mixer.music.play(loops=0)

    def check_if_song_position_changed_while_paused(self):
        if self.savedNewSongPosition != -1:
            return True
        return False

    def __change_play_button_to_pause(self):
        if len(self.songsBox.songsFullPaths) > 0:
            self.gui.btn_play.grid_remove()
            self.gui.btn_pause.grid()

    def pause_song(self):
        if pygame.mixer.music.get_busy():
            self.isSongPaused = True
            self.gui.slider_song.after_cancel(self.sliderUpdateFlag)
            pygame.mixer.music.pause()

            self.gui.btn_pause.grid_remove()
            self.gui.btn_play.grid()

    def next_song(self):
        if self.songsBox.songsListSize > 1 and self.songsBox.currentSongIndex < self.songsBox.songsListSize - 1:
            next_song = self.gui.songsList.get(self.songsBox.currentSongIndex + 1)

            for path in self.songsBox.songsFullPaths:
                if path.find(next_song) != -1:
                    self.isSongPaused = False

                    next_song = path
                    self.songsBox.currentSongIndex += 1

                    self.__load_new_song(next_song)
                    self.isSongLoaded = True
                    self.gui.place_pause_button()

                    self.execute_preparation_actions_before_playing()

                    self.__cycle_update_slider_position()
                    pygame.mixer.music.play(loops=0)

    def __load_new_song(self, song):
        self.songsBox.currentSongFullPath = song

        self.select_current_index()

        self.songMetadata.read_song_metadata(self.songsBox.currentSongFullPath)

        pygame.mixer.music.load(song)

    def repeat_switch(self):
        if self.isSongOnRepeat:
            self.gui.btn_repeat.config(image=self.gui.img_repeat)
            self.isSongOnRepeat = False
            self.gui.btn_repeat.bind("<Enter>",
                                     lambda event, image=self.gui.img_repeat_hover: self.gui.on_enter(e=event,
                                                                                                      image=image))
            self.gui.btn_repeat.bind("<Leave>",
                                     lambda event, image=self.gui.img_repeat: self.gui.on_leave(e=event, image=image))
            return

        self.gui.btn_repeat.config(image=self.gui.img_repeat_active)
        self.gui.btn_repeat.bind("<Enter>",
                                 lambda event, image=self.gui.img_repeat_active_hover: self.gui.on_enter(e=event,
                                                                                                         image=image))
        self.gui.btn_repeat.bind("<Leave>", lambda event, image=self.gui.img_repeat_active: self.gui.on_leave(e=event,
                                                                                                              image=image))
        self.isSongOnRepeat = True

    def change_song_position(self, x):
        self.songMetadata.wasSliderUsed = True
        self.songMetadata.update_playtime_on_slide(self.gui.slider_song.get())
        self.gui.slider_song.config(state=tk.ACTIVE)

    def __cycle_button_state_changer(self):
        if self.isSongLoaded:
            if self.songsBox.check_if_song_is_borderline() == -1:
                self.gui.btn_next.config(state=tk.DISABLED)
                self.gui.btn_prev.config(state=tk.DISABLED)

            if self.songsBox.check_if_song_is_borderline() == 0:
                self.gui.btn_prev.config(state=tk.DISABLED)
            else:
                self.gui.btn_prev.config(state=tk.NORMAL)

            if self.songsBox.check_if_song_is_borderline() == 1:
                self.gui.btn_next.config(state=tk.DISABLED)
            else:
                self.gui.btn_next.config(state=tk.NORMAL)

            self.gui.btn_play.config(state=tk.NORMAL)
            self.gui.btn_shuffle.config(state=tk.NORMAL)
            self.gui.btn_repeat.config(state=tk.NORMAL)
            self.gui.slider_song.config(state=tk.NORMAL)
        else:
            self.__disable_all_controls()

        self.gui.controlsFrame.after(250, self.__cycle_button_state_changer)

    def __disable_all_controls(self):
        self.gui.btn_prev.config(state=tk.DISABLED)
        self.gui.btn_play.config(state=tk.DISABLED)
        self.gui.btn_next.config(state=tk.DISABLED)
        self.gui.btn_shuffle.config(state=tk.DISABLED)
        self.gui.btn_repeat.config(state=tk.DISABLED)
        self.gui.slider_song.config(state=tk.DISABLED)

    '''
    def __configure_scale_style(self):
        self.scaleStyle.configure("songSlider.Horizontal.TScale", background='#FFDB00')
    
    '''

    def play_selected_song(self):
        self.gui.btn_play.config(state=tk.NORMAL)

        self.__cycle_wait_for_song_to_end()

        self.__change_play_button_to_pause()

        pygame.mixer.music.load(self.songsBox.currentSongFullPath)
        self.isSongLoaded = True
        self.songMetadata.read_song_metadata(self.songsBox.currentSongFullPath)

        self.gui.slider_song.config(state=tk.NORMAL)

        self.update_slider_bound()
        self.__cycle_update_slider_position()
        pygame.mixer.music.play(loops=0)

    def clear_playback(self):
        pygame.mixer.music.unload()
        self.isSongLoaded = False
        if self.isSongOnRepeat:
            self.repeat_switch()

        self.reset_slider_position()

    def __song_path_to_name(self, song_path):
        return song_path[song_path.rfind("/") + 1:]

    def get_songs_box_reference(self, songs_box_object):
        self.songsBox = songs_box_object

    def get_song_metadata_reference(self, song_metadata_object):
        self.songMetadata = song_metadata_object
