import pygame.mixer


class Sound:

    def __init__(self, path: str):
        self.path = path
        self.sound = pygame.mixer.Sound(path)

    def play(self):
        pygame.mixer.Sound.play(self.sound)
