def change_song_position_on_slide(self, x):
    self.stop_slider_update_cycle()
    self.songMetadata.wasSliderUsed = True
    self.songMetadata.update_playtime_on_slide(self.gui.slider_song.get())