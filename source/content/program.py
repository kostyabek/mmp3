import tkinter as tk
import pygame
import source.content.CurrentSongInfo as CurrentSongInfo
import source.content.PlaybackControls as PlaybackControls
import source.content.Playlist as Playlist


class Program:
    def __init__(self, master):
        pygame.mixer.init()

        # Defining top frame
        self.topFrame = tk.Frame(master, background="red")
        self.topFrame.grid(row=0, column=0, sticky="nswe")

        # Defining right side of top frame
        self.rightSideFrame = tk.Frame(self.topFrame, background="yellow")
        self.rightSideFrame.grid(row=0, column=1, sticky="nswe")

        # Defining bottom frame
        self.bottomFrame = tk.Frame(master, background="blue")
        self.bottomFrame.grid(row=1, column=0, sticky="nswe")

        self.currentSongInfo = CurrentSongInfo.CurrentSongInfo(self.topFrame, self.rightSideFrame)
        self.playlist = Playlist.Playlist(self.bottomFrame)
        self.playbackControls = PlaybackControls.PlaybackControls(self.rightSideFrame, self.playlist)

        # Stretching by columns
        master.grid_columnconfigure(0, weight=1)
        self.topFrame.grid_columnconfigure(1, weight=1)

        # Stretching by rows
        master.grid_rowconfigure(1, weight=1)
