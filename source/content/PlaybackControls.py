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
        self.isMuted = False

        self.isSongEndedFlag = None
        self.sliderPlaybackUpdateFlag = None
        self.buttonStateChangerFlag = None

        self.savedNewSongPosition = -1
        self.previousVolume = 100

        self.__bind_playback_slider_event()
        self.__bind_sound_slider_event()
        self.__give_commands_to_controls()

        self.__cycle_button_state_changer()

    def __bind_playback_slider_event(self):
        self.gui.slider_song.bind("<ButtonRelease-1>", lambda event: self.__set_song_from_new_position(e=event,
                                                                                                       new_position=self.gui.slider_song.get()))

    def __bind_sound_slider_event(self):
        self.gui.slider_volume.bind("<ButtonRelease-1>", lambda event: self.__set_previous_volume(e=event,
                                                                                                  previous_volume=self.gui.slider_volume.get()))

    def __set_previous_volume(self, e, previous_volume):
        self.previousVolume = previous_volume

    def __set_song_from_new_position(self, e, new_position):
        self.stop_slider_update_cycle()
        self.songMetadata.wasSliderUsed = True
        self.songMetadata.song_playtime_counter(playtime_from_slider=new_position)
        self.__cycle_update_slider_position()
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
        self.gui.slider_song.config(command=self.change_song_position_on_slide)
        self.gui.slider_volume.config(command=self.__set_volume)
        self.gui.btn_volume.config(command=self.__mute_switch)

    def prev_song(self):
        if self.songsBox.songsListSize > 1 and self.songsBox.currentSongIndex > 0:
            prev_song = list(self.songsBox.songsFullPaths)[self.songsBox.currentSongIndex - 1]

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

                    self.gui.songsList.selection_clear(0, tk.END)
                    if len(self.songsBox.query.get()) == 0:
                        self.songsBox.select_current_index()

                    self.songsBox.update_song_qty_label()

                    pygame.mixer.music.play(loops=0)

    def execute_preparation_actions_before_playing(self):
        self.stop_slider_update_cycle()

        self.update_slider_bound()
        self.songMetadata.set_playtime_to_zero()
        self.reset_slider_position()

    def update_slider_bound(self):
        self.gui.slider_song.config(to=self.songMetadata.songRawLength)

    def reset_slider_position(self):
        self.gui.slider_song.config(value=0)

    def __cycle_update_slider_position(self):
        if not self.isSongPaused:
            self.songMetadata.song_playtime_counter()
            self.gui.slider_song.config(value=self.songMetadata.songRawPlaytime)

        self.sliderPlaybackUpdateFlag = self.gui.master.after(250, self.__cycle_update_slider_position)

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
        self.__change_pause_button_to_play()

        self.gui.master.after(50, self.__cycle_wait_for_song_to_end)

        if self.sliderPlaybackUpdateFlag is None:
            self.__cycle_update_slider_position()

        if self.check_if_song_position_changed_while_paused():
            pygame.mixer.music.play(loops=0, start=self.savedNewSongPosition)
            self.savedNewSongPosition = -1
            return

        pygame.mixer.music.unpause()

    def __change_pause_button_to_play(self):
        self.gui.btn_play.grid_remove()
        self.gui.btn_pause.grid()

    def __cycle_wait_for_song_to_end(self):
        for event in pygame.event.get():
            if event.type == self.SONG_END:
                self.__check_if_song_is_last()
                self.__autoplay_next_song()
                self.stop_wait_for_song_to_end_cycle()
        self.isSongEndedFlag = self.gui.master.after(50, self.__cycle_wait_for_song_to_end)

    def __check_if_song_is_last(self):
        if self.songsBox.currentSongIndex == self.songsBox.songsListSize - 1:
            self.stop_slider_update_cycle()
            self.stop_wait_for_song_to_end_cycle()

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
            self.songMetadata.set_playtime_to_zero()

            self.gui.songsList.selection_clear(0, tk.END)
            if len(self.songsBox.query.get()) == 0:
                self.songsBox.select_current_index()

            self.songsBox.update_song_qty_label()

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
            self.stop_slider_update_cycle()
            pygame.mixer.music.pause()

            self.gui.btn_pause.grid_remove()
            self.gui.btn_play.grid()

    def next_song(self):
        if self.songsBox.songsListSize > 1 and self.songsBox.currentSongIndex < self.songsBox.songsListSize - 1:
            next_song = list(self.songsBox.songsFullPaths)[self.songsBox.currentSongIndex + 1]

            self.isSongPaused = False

            self.songsBox.currentSongIndex += 1

            self.__load_new_song(next_song)
            self.isSongLoaded = True
            self.gui.place_pause_button()

            self.execute_preparation_actions_before_playing()

            self.__cycle_update_slider_position()

            self.gui.songsList.selection_clear(0, tk.END)
            if len(self.songsBox.query.get()) == 0:
                self.songsBox.select_current_index()

            self.songsBox.update_song_qty_label()
            pygame.mixer.music.play(loops=0)

    def __load_new_song(self, song):
        self.songsBox.currentSongFullPath = song

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

    def change_song_position_on_slide(self, x):
        self.stop_slider_update_cycle()
        self.songMetadata.wasSliderUsed = True
        self.songMetadata.update_playtime_on_slide(self.gui.slider_song.get())

    def __set_volume(self, x):
        new_volume = self.gui.slider_volume.get()
        new_volume_int = int(new_volume)
        self.gui.volumeLabel.config(text=str(new_volume_int))

        self.__change_volume_icon_on_value(new_volume_int)

        new_volume_converted = new_volume / 100
        pygame.mixer.music.set_volume(new_volume_converted)

    def __change_volume_icon_on_value(self, volume):
        if volume > 40:
            self.isMuted = False
            self.gui.btn_volume.config(image=self.gui.img_volume_loud)
            self.gui.btn_volume.bind("<Enter>",
                                     lambda event, image=self.gui.img_volume_loud_hover: self.gui.on_enter(e=event,
                                                                                                           image=image))
            self.gui.btn_volume.bind("<Leave>",
                                     lambda event, image=self.gui.img_volume_loud: self.gui.on_leave(e=event,
                                                                                                     image=image))
        elif 40 > volume > 0:
            self.isMuted = False
            self.gui.btn_volume.config(image=self.gui.img_volume_quiet)
            self.gui.btn_volume.bind("<Enter>",
                                     lambda event, image=self.gui.img_volume_quiet_hover: self.gui.on_enter(e=event,
                                                                                                            image=image))
            self.gui.btn_volume.bind("<Leave>",
                                     lambda event, image=self.gui.img_volume_quiet: self.gui.on_leave(e=event,
                                                                                                      image=image))
        elif volume == 0:
            self.isMuted = True
            self.gui.btn_volume.config(image=self.gui.img_volume_muted)
            self.gui.btn_volume.bind("<Enter>",
                                     lambda event, image=self.gui.img_volume_muted_hover: self.gui.on_enter(e=event,
                                                                                                            image=image))
            self.gui.btn_volume.bind("<Leave>",
                                     lambda event, image=self.gui.img_volume_muted: self.gui.on_leave(e=event,
                                                                                                      image=image))

    def __mute_switch(self):
        if self.isMuted:
            self.isMuted = False
            self.gui.slider_volume.set(self.previousVolume)
            self.__change_volume_icon_on_value(self.previousVolume)
        else:
            self.isMuted = True
            self.gui.slider_volume.set(0)
            self.__change_volume_icon_on_value(0)

    def __cycle_button_state_changer(self):
        if self.isSongLoaded:
            self.gui.btn_play.config(state=tk.NORMAL)
            self.gui.btn_shuffle.config(state=tk.NORMAL)
            self.gui.btn_repeat.config(state=tk.NORMAL)
            self.gui.slider_song.config(state=tk.NORMAL)

            if self.songsBox.check_if_song_is_borderline() == -1:
                self.gui.btn_next.config(state=tk.DISABLED)
                self.gui.btn_prev.config(state=tk.DISABLED)

            elif self.songsBox.check_if_song_is_borderline() == 0:
                self.gui.btn_prev.config(state=tk.DISABLED)
                self.gui.btn_next.config(state=tk.NORMAL)

            elif self.songsBox.check_if_song_is_borderline() == 1:
                self.gui.btn_prev.config(state=tk.NORMAL)
                self.gui.btn_next.config(state=tk.DISABLED)
            else:
                self.gui.btn_prev.config(state=tk.NORMAL)
                self.gui.btn_next.config(state=tk.NORMAL)
        else:
            self.__disable_all_controls()

        self.buttonStateChangerFlag = self.gui.master.after(250, self.__cycle_button_state_changer)

    def __disable_all_controls(self):
        self.gui.btn_prev.config(state=tk.DISABLED)
        self.gui.btn_play.config(state=tk.DISABLED)
        self.gui.btn_next.config(state=tk.DISABLED)
        self.gui.btn_shuffle.config(state=tk.DISABLED)
        self.gui.btn_repeat.config(state=tk.DISABLED)
        self.gui.slider_song.config(state=tk.DISABLED)

    def play_selected_song(self):
        self.gui.btn_play.config(state=tk.NORMAL)

        self.__cycle_wait_for_song_to_end()

        self.isSongPaused = False
        self.__change_play_button_to_pause()

        pygame.mixer.music.load(self.songsBox.currentSongFullPath)
        self.isSongLoaded = True
        self.songMetadata.read_song_metadata(self.songsBox.currentSongFullPath)

        self.update_slider_bound()
        self.__cycle_update_slider_position()

        pygame.mixer.music.play(loops=0)

    def clear_playback(self):
        pygame.mixer.music.unload()
        self.isSongLoaded = False

        if self.isSongOnRepeat:
            self.repeat_switch()

        self.reset_slider_position()

        self.stop_slider_update_cycle()
        self.stop_wait_for_song_to_end_cycle()

    def stop_slider_update_cycle(self):
        if self.sliderPlaybackUpdateFlag:
            self.gui.master.after_cancel(self.sliderPlaybackUpdateFlag)
            self.sliderPlaybackUpdateFlag = None

    def stop_wait_for_song_to_end_cycle(self):
        if self.isSongEndedFlag:
            self.gui.master.after_cancel(self.isSongEndedFlag)

    def __song_path_to_name(self, song_path):
        return song_path[song_path.rfind("/") + 1:]

    def get_songs_box_reference(self, songs_box_object):
        self.songsBox = songs_box_object

    def get_song_metadata_reference(self, song_metadata_object):
        self.songMetadata = song_metadata_object

    def cancel_all_cycles(self):
        if self.sliderPlaybackUpdateFlag is not None:
            self.gui.master.after_cancel(self.sliderPlaybackUpdateFlag)
            self.sliderPlaybackUpdateFlag = None
        if self.isSongEndedFlag is not None:
            self.gui.master.after_cancel(self.isSongEndedFlag)
            self.isSongEndedFlag = None
        if self.buttonStateChangerFlag is not None:
            self.gui.master.after_cancel(self.buttonStateChangerFlag)
            self.buttonStateChangerFlag = None
