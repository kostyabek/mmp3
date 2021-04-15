import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk


class GUI:
    backgroundColor = "#2B2B2B"
    songsListBackgroundColor = "#3C3F41"
    foregroundColor = "#BBBBBB"
    foregroundActiveColor = "#F0F0F0"

    def __init__(self, master):
        self.master = master

        # Defining top frame
        self.topFrame = tk.Frame(master, background=GUI.backgroundColor) # red
        self.topFrame.grid(row=0, column=0, sticky="nswe")

        # Defining right side of the top frame
        self.rightSideFrame = tk.Frame(self.topFrame, background=GUI.backgroundColor) # yellow
        self.rightSideFrame.grid(row=0, column=1, sticky="nswe")

        # Defining controls frame
        self.controlsFrame = tk.Frame(self.rightSideFrame, background=GUI.backgroundColor) # no color
        self.controlsFrame.grid(row=1, column=0, sticky="w")

        # Defining bottom frame
        self.songsListFrame = tk.Frame(master, background=GUI.backgroundColor) # blue
        self.songsListFrame.grid(row=1, column=0, sticky="nswe")

        # Defining bottom buttons frame
        self.bottomButtonsFrame = tk.Frame(master, background=GUI.backgroundColor)
        self.bottomButtonsFrame.grid(row=2, column=0, sticky="nswe")


        # Stretching by columns
        master.grid_columnconfigure(0, weight=1)
        self.topFrame.grid_columnconfigure(1, weight=1)

        # Stretching by rows
        master.grid_rowconfigure(1, weight=1)


        # Metadata
        self.coverImagePlaceholder = self.__prepare_cover_image_placeholder()

        self.coverLabel = tk.Label(self.topFrame, bd=0, image=self.coverImagePlaceholder)

        self.songInfoFrame = tk.Frame(self.rightSideFrame, background=GUI.backgroundColor) # green
        self.songNameLabel = tk.Label(self.songInfoFrame, width=25, bg=GUI.backgroundColor, fg=GUI.foregroundColor, text="N/A", font="Ubuntu 14", anchor="w")
        self.songTimeLabel = tk.Label(self.songInfoFrame, bg=GUI.backgroundColor, fg=GUI.foregroundColor, text="X:XX/X:XX", font="Ubuntu 10")

        self.songInfoFrame.grid(row=0, column=0, pady=(20, 15), sticky="w")
        self.songNameLabel.grid(row=0, column=0)
        self.songTimeLabel.grid(row=1, column=0, sticky="w")

        self.coverLabel.grid(row=0, column=0, padx=5, pady=5)


        # Controls
        self.img_prev = tk.PhotoImage(file="../img/icons/previous.png")
        self.img_prev_hover = tk.PhotoImage(file="../img/icons/previous(hover).png")
        self.img_play = tk.PhotoImage(file="../img/icons/play.png")
        self.img_play_hover = tk.PhotoImage(file="../img/icons/play(hover).png")

        self.img_pause = tk.PhotoImage(file="../img/icons/pause(big).png")
        self.img_pause_hover = tk.PhotoImage(file="../img/icons/pause(big hover).png")

        self.img_next = tk.PhotoImage(file="../img/icons/next.png")
        self.img_next_hover = tk.PhotoImage(file="../img/icons/next(hover).png")

        self.img_repeat = tk.PhotoImage(file="../img/icons/repeat.png")
        self.img_repeat_hover = tk.PhotoImage(file="../img/icons/repeat(hover).png")
        self.img_repeat_active = tk.PhotoImage(file="../img/icons/repeat(active).png")
        self.img_repeat_active_hover = tk.PhotoImage(file="../img/icons/repeat(active hover).png")

        self.btn_prev = tk.Button(self.controlsFrame,
                                  image=self.img_prev,
                                  bg=GUI.backgroundColor,
                                  activebackground=GUI.backgroundColor,
                                  borderwidth=0)
        self.btn_play = tk.Button(self.controlsFrame,
                                  image=self.img_play,
                                  bg=GUI.backgroundColor,
                                  activebackground=GUI.backgroundColor,
                                  borderwidth=0,
                                  state=tk.DISABLED)
        self.btn_pause = tk.Button(self.controlsFrame,
                                   image=self.img_pause,
                                   bg=GUI.backgroundColor,
                                   activebackground=GUI.backgroundColor,
                                   borderwidth=0)
        self.btn_next = tk.Button(self.controlsFrame,
                                  image=self.img_next,
                                  bg=GUI.backgroundColor,
                                  activebackground=GUI.backgroundColor,
                                  borderwidth=0)

        self.btn_repeat = tk.Button(self.controlsFrame,
                                    image=self.img_repeat,
                                    bg=GUI.backgroundColor,
                                    activebackground=GUI.backgroundColor,
                                    borderwidth=0)

        # Creating custom slider
        self.img_slider = tk.PhotoImage('self.img_slider', width=7, height=20, master=master)
        self.__create_img_from_pixels(self.img_slider, GUI.foregroundColor)

        self.img_slider_active = tk.PhotoImage('self.img_slider_active', width=7, height=20, master=master)
        self.__create_img_from_pixels(self.img_slider_active, GUI.foregroundActiveColor)

        self.style = ttk.Style(master)
        self.style.element_create('custom.Horizontal.Scale.slider', 'image', self.img_slider,
                                 ('active', self.img_slider_active))

        self.style.layout('custom.Horizontal.TScale',
                          [('Horizontal.Scale.trough',
                            {'expand': '1', 'sticky': 'we',
                             'children': [('Horizontal.Scale.track', {'sticky': 'we'}),
                                          ('custom.Horizontal.Scale.slider', {'side': 'left', 'sticky': ''})]})])

        self.style.configure('custom.Horizontal.TScale', background=GUI.backgroundColor)

        self.slider_song = ttk.Scale(self.rightSideFrame,
                                     length=300,
                                     style='custom.Horizontal.TScale',
                                     from_=0,
                                     to=100,
                                     orient=tk.HORIZONTAL,
                                     value=0,
                                     state=tk.DISABLED)

        self.btn_prev.bind("<Enter>", lambda event, image=self.img_prev_hover: self.on_enter(e=event, image=image))
        self.btn_prev.bind("<Leave>", lambda event, image=self.img_prev: self.on_leave(e=event, image=image))

        self.btn_play.bind("<Enter>", lambda event, image=self.img_play_hover: self.on_enter(e=event, image=image))
        self.btn_play.bind("<Leave>", lambda event, image=self.img_play: self.on_leave(e=event, image=image))

        self.btn_pause.bind("<Enter>", lambda event, image=self.img_pause_hover: self.on_enter(e=event, image=image))
        self.btn_pause.bind("<Leave>", lambda event, image=self.img_pause: self.on_leave(e=event, image=image))

        self.btn_next.bind("<Enter>", lambda event, image=self.img_next_hover: self.on_enter(e=event, image=image))
        self.btn_next.bind("<Leave>", lambda event, image=self.img_next: self.on_leave(e=event, image=image))

        self.btn_repeat.bind("<Enter>",
                             lambda event, image=self.img_repeat_hover: self.on_enter(e=event, image=image))
        self.btn_repeat.bind("<Leave>", lambda event, image=self.img_repeat: self.on_leave(e=event, image=image))

        self.btn_prev.grid(row=0, column=0, padx=(0, 15))

        # Remembering pause button's position
        self.btn_pause.grid(row=0, column=1)
        self.btn_pause.grid_remove()

        self.btn_play.grid(row=0, column=1)
        self.btn_next.grid(row=0, column=2, padx=(15, 0))

        self.btn_repeat.grid(row=0, column=4, ipadx="2px")

        self.slider_song.grid(row=2, column=0, padx=2, pady=(15, 0), sticky="we")


        # SongsBox
        self.songsListScrollbar = tk.Scrollbar(self.songsListFrame)
        self.songsListScrollbar.pack(side=tk.RIGHT,
                                     fill=tk.Y)
        self.songsList = tk.Listbox(self.songsListFrame,
                                    yscrollcommand=self.songsListScrollbar.set,
                                    bg=GUI.songsListBackgroundColor,
                                    fg=GUI.foregroundColor,
                                    selectbackground=GUI.backgroundColor)
        self.songsList.pack(fill="both", expand=True)
        self.songsListScrollbar.config(command=self.songsList.yview)

        self.img_add_songs = tk.PhotoImage(file="../img/icons/plus.png")
        self.img_add_songs_hover = tk.PhotoImage(file="../img/icons/plus(hover).png")
        self.img_enter_song_removing_mode = tk.PhotoImage(file="../img/icons/minus.png")
        self.img_enter_song_removing_mode_hover = tk.PhotoImage(file="../img/icons/minus(hover).png")
        self.img_remove_selected_songs = tk.PhotoImage(file="../img/icons/trashcan.png")
        self.img_remove_selected_songs_hover = tk.PhotoImage(file="../img/icons/trashcan(hover).png")
        self.img_shuffle = tk.PhotoImage(file="../img/icons/shuffle.png")
        self.img_shuffle_hover = tk.PhotoImage(file="../img/icons/shuffle(hover).png")

        self.btn_add_songs = tk.Button(self.bottomButtonsFrame,
                                       image=self.img_add_songs,
                                       bg=GUI.backgroundColor,
                                       activebackground=GUI.backgroundColor,
                                       relief=tk.GROOVE,
                                       bd=0)

        self.btn_enter_song_removing_mode = tk.Button(self.bottomButtonsFrame,
                                                      image=self.img_enter_song_removing_mode,
                                                      bg=GUI.backgroundColor,
                                                      activebackground=GUI.backgroundColor,
                                                      relief=tk.GROOVE,
                                                      bd=0)
        self.btn_remove_selected_songs = tk.Button(self.bottomButtonsFrame,
                                                   image=self.img_remove_selected_songs,
                                                   bg=GUI.backgroundColor,
                                                   activebackground=GUI.backgroundColor,
                                                   relief=tk.GROOVE,
                                                   state=tk.DISABLED,
                                                   bd=0)

        self.btn_shuffle = tk.Button(self.controlsFrame,
                                     image=self.img_shuffle,
                                     bg=GUI.backgroundColor,
                                     activebackground=GUI.backgroundColor,
                                     borderwidth=0)

        self.btn_add_songs.bind("<Enter>",
                                lambda event, image=self.img_add_songs_hover: self.on_enter(e=event, image=image))
        self.btn_add_songs.bind("<Leave>",
                                lambda event, image=self.img_add_songs: self.on_leave(e=event, image=image))

        self.btn_enter_song_removing_mode.bind("<Enter>",
                                       lambda event, image=self.img_enter_song_removing_mode_hover: self.on_enter(e=event,
                                                                                                          image=image))
        self.btn_enter_song_removing_mode.bind("<Leave>",
                                       lambda event, image=self.img_enter_song_removing_mode: self.on_leave(e=event,
                                                                                                    image=image))

        self.btn_remove_selected_songs.bind("<Enter>",
                                       lambda event, image=self.img_remove_selected_songs_hover: self.on_enter(e=event,
                                                                                                          image=image))

        self.btn_remove_selected_songs.bind("<Leave>",
                                               lambda event, image=self.img_remove_selected_songs: self.on_leave(
                                                   e=event,
                                                   image=image))

        self.btn_shuffle.bind("<Enter>",
                              lambda event, image=self.img_shuffle_hover: self.on_enter(e=event, image=image))
        self.btn_shuffle.bind("<Leave>", lambda event, image=self.img_shuffle: self.on_leave(e=event, image=image))

        self.btn_add_songs.pack(side=tk.LEFT, ipadx="5px", ipady="2px")
        self.btn_enter_song_removing_mode.pack(side=tk.LEFT, ipadx="5px", ipady="2px")
        self.btn_remove_selected_songs.pack(side=tk.LEFT, ipadx="5px", ipady="2px")
        self.btn_shuffle.grid(row=0, column=3, ipadx="2px", padx=("20px", 0))

        # About button
        self.img_about = tk.PhotoImage(file="../img/icons/about.png")
        self.img_about_hover = tk.PhotoImage(file="../img/icons/about(hover).png")

        self.btn_show_about = tk.Button(self.bottomButtonsFrame,
                                        image=self.img_about,
                                        bg=GUI.backgroundColor,
                                        activebackground=GUI.backgroundColor,
                                        relief=tk.GROOVE,
                                        bd=0)

        self.btn_show_about.bind("<Enter>",
                                 lambda event, image=self.img_about_hover: self.on_enter(e=event, image=image))
        self.btn_show_about.bind("<Leave>", lambda event, image=self.img_about: self.on_leave(e=event, image=image))
        self.btn_show_about.pack(side=tk.RIGHT, ipadx="1px", ipady="2px")

    def __prepare_cover_image_placeholder(self):
        cover_raw_image = Image.open("../img/cover placeholder.png")
        cover_raw_image = cover_raw_image.resize((150, 150), Image.ANTIALIAS)
        return ImageTk.PhotoImage(cover_raw_image)

    def on_enter(self, e, image):
        e.widget['image'] = image

    def on_leave(self, e, image):
        e.widget['image'] = image

    def place_pause_button(self):
        self.btn_play.grid_remove()

        self.btn_pause.grid()

    def place_play_button(self):
        self.btn_pause.grid_remove()

        self.btn_play.grid()

    def __create_img_from_pixels(self, img, color):
        pixel_line = "{" + " ".join(color for i in range(img.width())) + "}"
        pixels = " ".join(pixel_line for i in range(img.height()))
        img.put(pixels)
