import tkinter as tk
import random
import pygame


class PlaybackControls:
    def __init__(self, rightSideFrame, playlist):
        self.controlsFrame = tk.Frame(rightSideFrame)

        self.playlist = playlist

        # Getting button images
        self.img_prev = tk.PhotoImage(file="E:/PyCharm Projects/Images/img/icons/previous.png")
        self.img_stop = tk.PhotoImage(file="E:/PyCharm Projects/Images/img/icons/stop.png")
        self.img_play = tk.PhotoImage(file="E:/PyCharm Projects/Images/img/icons/play.png")
        self.img_pause = tk.PhotoImage(file="E:/PyCharm Projects/Images/img/icons/pause.png")
        self.img_pause_active = tk.PhotoImage(file="E:/PyCharm Projects/Images/img/icons/pause(active).png")
        self.img_next = tk.PhotoImage(file="E:/PyCharm Projects/Images/img/icons/next.png")
        self.img_shuffle = tk.PhotoImage(file="E:/PyCharm Projects/Images/img/icons/shuffle.png")
        self.img_repeat = tk.PhotoImage(file="E:/PyCharm Projects/Images/img/icons/repeat.png")

        # Creating buttons
        self.btn_prev = tk.Button(self.controlsFrame,
                                  image=self.img_prev,
                                  bg="#2B2B2B",
                                  activebackground="#2B2B2B",
                                  borderwidth=0,
                                  command=self.prev_song)
        self.btn_stop = tk.Button(self.controlsFrame,
                                  image=self.img_stop,
                                  bg="#2B2B2B",
                                  activebackground="#2B2B2B",
                                  borderwidth=0,
                                  command=self.stop_song)
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
                                    borderwidth=0)

        # Utility controls variables
        self.isPaused = False
        self.currentSongIndex = -1

        self.__place_frame()
        self.__place_buttons()

    def __place_frame(self):
        # Frame for controls
        self.controlsFrame.grid(row=1, column=0, sticky="w")

    def __place_buttons(self):
        # Placing buttons
        self.btn_prev.grid(row=0, column=0, ipadx="7px")
        self.btn_stop.grid(row=0, column=1, ipadx="7px")
        self.btn_play.grid(row=0, column=2, ipadx="7px")
        self.btn_pause.grid(row=0, column=3, ipadx="7px")
        self.btn_next.grid(row=0, column=4, ipadx="7px")
        self.btn_shuffle.grid(row=0, column=5, ipadx="2px", padx=("20px", 0))
        self.btn_repeat.grid(row=0, column=6, ipadx="2px")

    def play_song(self):
        if not pygame.mixer.music.get_busy() and self.isPaused:
            pygame.mixer.music.unpause()
            self.isPaused = False
            self.btn_pause.config(image=self.img_pause)
            return

        if len(self.playlist.songsFullPath) > 0:
            # Getting song's full path
            for path in self.playlist.songsFullPath:
                if path.find(self.playlist.songsList.get(tk.ACTIVE)) != -1:
                    self.songCurrent = path
                    break

            # Loading the song into the mixer
            pygame.mixer.music.load(self.songCurrent)

            # Queuing the next song
            self.currentSongIndex = self.playlist.curselection()[0]
            self.__queue_song()

            # Playing the song
            pygame.mixer.music.play(loops=0)

    def __queue_song(self):
        if self.playlistSize > 1 and self.currentSongIndex < self.playlistSize - 1:
            self.songNext = self.songsFullPath[self.playlist.curselection()[0] + 1]
            pygame.mixer.music.queue(self.songNext)

    def stop_song(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        self.isPaused = False
        self.btn_pause.configure(image=self.img_pause)

    def pause_song(self):
        if pygame.mixer.music.get_busy():
            self.isPaused = True
            pygame.mixer.music.pause()
            self.btn_pause.config(image=self.img_pause_active)

    def next_song(self):
        if self.playlist.songsListSize > 1 and self.currentSongIndex < self.playlistSize - 1:
            nextSong = self.playlist.get(self.currentSongIndex + 1)
            for path in self.songsFullPath:
                if path.find(nextSong) != -1:
                    nextSong = path
                    self.currentSongIndex += 1
                    self.playlist.selection_clear(0, tk.END)
                    self.playlist.activate(self.currentSongIndex)
                    self.playlist.selection_set(self.currentSongIndex)
                    pygame.mixer.music.load(nextSong)
                    pygame.mixer.music.play(loops=0)
                    print(self.currentSongIndex)

    def prev_song(self):
        if self.playlistSize > 1 and self.currentSongIndex > 0:
            prevSong = self.playlist.get(self.currentSongIndex - 1)
            for path in self.songsFullPath:
                if path.find(prevSong) != -1:
                    prevSong = path
                    self.currentSongIndex -= 1
                    self.playlist.selection_clear(0, tk.END)
                    self.playlist.activate(self.currentSongIndex)
                    self.playlist.selection_set(self.currentSongIndex)
                    pygame.mixer.music.load(prevSong)
                    pygame.mixer.music.play(loops=0)

    # COMPLETE THIS FUCKING METHOD
    def shuffle_songs(self):
        songsList = list(self.playlist.get(0, tk.END))
        random.shuffle(songsList)
        print(self.songCurrent)
        if pygame.mixer.music.get_busy():
            songsList.remove(self.songCurrent[self.songCurrenturrent.rfind("/") + 1:])
            print(self.songCurrent[self.songCurrenturrent.rfind("/") + 1:])
            songsList.insert(0, self.songCurrent[self.songCurrenturrent.rfind("/") + 1:])

        self.playlist.delete(0, tk.END)
        self.playlist.insert(tk.END, *songsList)