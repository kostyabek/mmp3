import pygame
import atexit
import source.content.GUI as GUI
import source.content.SongMetadata as SongMetadata
import source.content.PlaybackControls as PlaybackControls
import source.content.SongsBox as SongsBox
import source.content.About as About


class Program:
    def __init__(self, master):
        atexit.register(self.__prepare_to_exit)
        pygame.init()
        self.gui = GUI.GUI(master)

        self.songsBox = SongsBox.SongsBox(self.gui)
        self.currentSongMetadata = SongMetadata.SongMetadata(self.gui)
        self.playbackControls = PlaybackControls.PlaybackControls(self.gui)

        self.songsBox.get_playback_controls_reference(self.playbackControls)
        self.songsBox.get_song_metadata_reference(self.currentSongMetadata)

        self.currentSongMetadata.get_songs_box_reference(self.songsBox)

        self.playbackControls.get_songs_box_reference(self.songsBox)
        self.playbackControls.get_song_metadata_reference(self.currentSongMetadata)

        self.gui.btn_show_about.config(command=lambda: self.__show_about(master))

    def __show_about(self, master):
        self.about = About.About(master, bg=self.gui.backgroundColor)

    def __prepare_to_exit(self):
        self.currentSongMetadata.cancel_all_cycles()
        self.playbackControls.cancel_all_cycles()
