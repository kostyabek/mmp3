import pygame
import source.content.GUI as GUI
import source.content.SongMetadata as SongMetadata
import source.content.PlaybackControls as PlaybackControls
import source.content.SongsBox as SongsBox


class Program:
    def __init__(self, master):
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
