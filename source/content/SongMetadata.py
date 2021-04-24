import stagger as stg
import mutagen.mp3 as mtg
from PIL import Image, ImageTk
import io
import time


class SongMetadata:
    def __init__(self, gui):
        self.gui = gui
        self.songsBox = None

        self.songTag = None
        self.songFullTitle = ""
        self.songTitle = ""
        self.songRawPlaytime = 0
        self.songFormattedPlaytime = None
        self.songRawLength = 0
        self.songFormattedLength = None

        self.coverRawImage = None

        self.songNameCycleFlag = None
        self.wasSliderUsed = False

    def read_song_metadata(self, song_full_path):
        self.cancel_all_cycles()

        try:
            self.songTag = stg.read_tag(song_full_path)
        except stg.errors.NoTagError:
            self.songTitle = song_full_path[song_full_path.rfind("/") + 1:-4]
            self.songFullTitle = self.__build_song_full_title("", self.songTitle)
        else:
            self.songTitle = self.songTag.title
            self.songFullTitle = self.__build_song_full_title(self.songTag.artist, self.songTitle)

        self.gui.songNameLabel.configure(text=self.songFullTitle)

        if len(self.songFullTitle) > 27:
            self.__cycle_spin_song_full_title()

        self.__get_song_cover_image()
        self.get_song_length()

    def stop_song_title_cycle(self):
        if self.songNameCycleFlag is not None:
            self.gui.master.after_cancel(self.songNameCycleFlag)

    def __build_song_full_title(self, artist, name):
        if len(artist) == 0:
            return f"{name}  "
        return f"{artist} - {name}  "

    def __cycle_spin_song_full_title(self):
        self.songFullTitle = self.songFullTitle[-1] + self.songFullTitle[:-1]

        self.gui.songNameLabel.configure(text=self.songFullTitle)

        self.songNameCycleFlag = self.gui.master.after(1000, self.__cycle_spin_song_full_title)

    def __get_song_cover_image(self):
        if not self.__check_if_tag_has_image():
            self.gui.coverLabel.configure(image=self.gui.coverImagePlaceholder)
            return

        byte_data = self.songTag[stg.id3.APIC][0].data
        image_io = io.BytesIO(byte_data)
        image_file = Image.open(image_io)
        image_file = image_file.resize((150, 150), Image.ANTIALIAS)
        self.coverRawImage = ImageTk.PhotoImage(image_file)
        self.gui.coverLabel.configure(image=self.coverRawImage)

    def __check_if_tag_has_image(self):
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
        self.gui.songTimeLabel.configure(text=self.songFormattedPlaytime + "/" + self.songFormattedLength)

    def update_playtime_on_slide(self, playtime_from_slider):
        self.songRawPlaytime = playtime_from_slider
        self.raw_playtime_to_formatted(self.songRawPlaytime)

        self.update_song_playtime_label()

    def clear_song_metadata(self):
        self.gui.coverLabel.configure(image=self.gui.coverImagePlaceholder)
        self.gui.songNameLabel.configure(text="N/A")
        self.gui.songTimeLabel.configure(text="X:XX/X:XX")
        self.songFullTitle = ""
        self.songTag = None
        self.coverRawImage = None
        self.songFormattedPlaytime = None
        self.songFormattedLength = None
        self.songRawLength = 0

        self.set_playtime_to_zero()

        self.stop_song_title_cycle()

    def set_playtime_to_zero(self):
        self.songRawPlaytime = 0

    def get_songs_box_reference(self, songs_box_object):
        self.songsBox = songs_box_object

    def cancel_all_cycles(self):
        if self.songNameCycleFlag is not None:
            self.gui.master.after_cancel(self.songNameCycleFlag)

    def get_title_from_tag(self, path):
        try:
            song_tag = stg.read_tag(path)
        except stg.errors.NoTagError:
            song_title = path[path.rfind("/") + 1:-4]
        else:
            song_title = song_tag.title

        return song_title
