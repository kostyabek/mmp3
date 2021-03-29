import tkinter as tk
import stagger as stg
import mutagen.mp3 as mtg
from PIL import Image, ImageTk
import io
import time


class SongMetadata:
    def __init__(self, top_frame, right_side_frame, songs_box):
        self.songsBox = songs_box
        self.songTag = None
        self.songFullTitle = ""
        self.songRawPlaytime = 0
        self.songFormattedPlaytime = None
        self.songRawLength = 0
        self.songFormattedLength = None

        self.coverImagePlaceholder = self.__prepare_cover_image_placeholder()
        self.coverRawImage = None
        self.coverLabel = tk.Label(top_frame, bd=0, image=self.coverImagePlaceholder)
        self.__place_song_cover_image()

        self.songInfoFrame = tk.Frame(right_side_frame, background="green")
        self.songNameLabel = tk.Label(self.songInfoFrame, width=25, text="N/A", font="Ubuntu 14", anchor="w")
        self.songTimeLabel = tk.Label(self.songInfoFrame, text="X:XX/X:XX", font="Ubuntu 10")
        self.__place_song_info()

        self.songNameCycleFlag = 0
        self.songTimeDataFlag = 0
        self.wasLongTitle = False
        self.wasSliderUsed = False

    def __prepare_cover_image_placeholder(self):
        cover_raw_image = Image.open("../img/cover placeholder.png")
        cover_raw_image = cover_raw_image.resize((150, 150), Image.ANTIALIAS)
        return ImageTk.PhotoImage(cover_raw_image)

    def __place_song_cover_image(self):
        self.coverLabel.grid(row=0, column=0, padx=5, pady=5)

    def __place_song_info(self):
        self.songInfoFrame.grid(row=0, column=0, pady=(20, 15), sticky="w")

        self.songNameLabel.grid(row=0, column=0)
        self.songTimeLabel.grid(row=1, column=0, sticky="w")

    def read_song_metadata(self, song_full_path):
        if self.wasLongTitle:
            self.songNameLabel.after_cancel(self.songNameCycleFlag)

        self.songTag = stg.read_tag(song_full_path)
        self.songFullTitle = self.__build_song_full_title()
        self.songNameLabel.configure(text=self.songFullTitle)

        self.__start_song_title_cycler()

        self.__get_song_cover_image()
        self.get_song_length()

    def __build_song_full_title(self):
        if len(self.songTag.artist) == 0 or len(self.songTag.title) == 0:
            return self.songsBox.songsList.get(tk.ACTIVE)
        return self.songTag.artist + " - " + self.songTag.title + "  "

    def __start_song_title_cycler(self):
        if len(self.songFullTitle) > 35:
            self.wasLongTitle = True
            self.songNameCycleFlag = self.songNameLabel.after(1000, self.__cycle_song_full_title)

    def __cycle_song_full_title(self):
        if len(self.songFullTitle) > 35:
            self.songFullTitle = self.songFullTitle[-1] + self.songFullTitle[:-1]

            self.songNameLabel.configure(text=self.songFullTitle)

            self.songNameCycleFlag = self.songNameLabel.after(1000, self.__cycle_song_full_title)

    def __get_song_cover_image(self):
        if not self.__check_if_song_has_image():
            self.coverLabel.configure(image=self.coverImagePlaceholder)
            return

        byte_data = self.songTag[stg.id3.APIC][0].data
        image_io = io.BytesIO(byte_data)
        image_file = Image.open(image_io)
        image_file = image_file.resize((150, 150), Image.ANTIALIAS)
        self.coverRawImage = ImageTk.PhotoImage(image_file)
        self.coverLabel.configure(image=self.coverRawImage)

    def __check_if_song_has_image(self):
        if len(self.songTag.picture) == 0:
            return False
        return True

    def get_song_length(self):
        song_mutagen = mtg.MP3(self.songsBox.currentSongFullPath)
        self.songRawLength = song_mutagen.info.length
        if self.songRawLength > 3600:
            self.songFormattedLength = time.strftime("%H:%M:%S", time.gmtime(self.songRawLength))
            return
        self.songFormattedLength = time.strftime("%M:%S", time.gmtime(self.songRawLength))

    def song_playtime_counter(self, playtime_from_slider=0):
        if self.wasSliderUsed:
            self.songRawPlaytime = playtime_from_slider
            self.wasSliderUsed = False
        else:
            self.songRawPlaytime += 0.25

        self.raw_playtime_to_formatted(self.songRawPlaytime)

        self.update_song_playtime_label()

    def raw_playtime_to_formatted(self, playtime):
        if self.songRawLength > 3600:
            self.songFormattedPlaytime = time.strftime("%H:%M:%S", time.gmtime(playtime))
        else:
            self.songFormattedPlaytime = time.strftime("%M:%S", time.gmtime(playtime))

    def update_song_playtime_label(self):
        self.songTimeLabel.configure(text=self.songFormattedPlaytime + "/" + self.songFormattedLength)

    def update_playtime_on_slide(self, playtime_from_slider):
        self.songRawPlaytime = playtime_from_slider
        self.raw_playtime_to_formatted(self.songRawPlaytime)

        self.update_song_playtime_label()

    def clear_song_metadata(self):
        self.coverLabel.configure(image=self.coverImagePlaceholder)
        self.songNameLabel.configure(text="N/A")
        self.songTimeLabel.configure(text="X:XX/X:XX")
        self.songFullTitle = ""
        self.songTag = None
        self.coverRawImage = None
        self.songFormattedPlaytime = None
        self.songFormattedLength = None
        self.reset_playtime()
        self.songRawLength = 0

    def reset_playtime(self):
        self.songRawPlaytime = 0
