import pygame
import os
from src.sound import Sound
from src.theme import Theme


class Config:

    def __init__(self):
        self.themes = []
        self._add_themes()
        self.idx = 0
        self.theme = self.themes[self.idx]
        # font
        self.move_sound = Sound(path=os.path.join('assets/sounds/move.wav'))
        self.capture_sound = Sound(path=os.path.join('assets/sounds/capture.wav'))

    def change_theme(self):
        self.idx += 1
        self.idx %= len(self.themes)
        self.theme = self.themes[self.idx]

    def _add_themes(self):
        green = Theme(light_bg=(234, 235, 200), dark_bg=(119, 154, 88),
                      light_trace=(244, 247, 116), dark_trace=(172, 195, 51),
                      light_moves='#C86464', dark_moves='#C84646', hover=(180, 180, 180))
        brown = Theme(light_bg=(235, 209, 166), dark_bg=(165, 117, 80),
                      light_trace=(245, 234, 100), dark_trace=(209, 185, 59),
                      light_moves='#C86464', dark_moves='#C84646', hover=(180, 180, 180))
        blue = Theme(light_bg=(229, 228, 200), dark_bg=(60, 95, 135),
                     light_trace=(123, 187, 227), dark_trace=(43, 119, 191),
                     light_moves='#C86464', dark_moves='#C84646', hover=(180, 180, 180))
        grey = Theme(light_bg=(120, 119, 118), dark_bg=(86, 85, 84),
                     light_trace=(99, 126, 143), dark_trace=(82, 102, 128),
                     light_moves='#C86464', dark_moves='#C84646', hover=(180, 180, 180))

        self.themes = [grey, brown, blue, green]
