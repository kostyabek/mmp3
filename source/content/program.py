import tkinter as tk
import pygame
import source.content.SongMetadata as SongMetadata
import source.content.PlaybackControls as PlaybackControls
import source.content.SongsBox as SongsBox


class Program:
    def __init__(self, master):
        pygame.init()

        # Defining top frame
        self.topFrame = tk.Frame(master, background="red")
        self.topFrame.grid(row=0, column=0, sticky="nswe")

        # Defining right side of top frame
        self.rightSideFrame = tk.Frame(self.topFrame, background="yellow")
        self.rightSideFrame.grid(row=0, column=1, sticky="nswe")

        # Defining bottom frame
        self.bottomFrame = tk.Frame(master, background="blue")
        self.bottomFrame.grid(row=1, column=0, sticky="nswe")

        self.songsBox = SongsBox.SongsBox(self.bottomFrame)
        self.currentSongMetadata = SongMetadata.SongMetadata(self.topFrame, self.rightSideFrame, self.songsBox)
        self.songsBox.get_song_metadata_reference(self.currentSongMetadata)
        self.playbackControls = PlaybackControls.PlaybackControls(self.rightSideFrame, self.songsBox, self.currentSongMetadata)
        self.songsBox.get_song_playback_controls_reference(self.playbackControls)

        # Stretching by columns
        master.grid_columnconfigure(0, weight=1)
        self.topFrame.grid_columnconfigure(1, weight=1)

        # Stretching by rows
        master.grid_rowconfigure(1, weight=1)
