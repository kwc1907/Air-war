import pygame
from pygame.sprite import Sprite
class Alien(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.y = float(self.rect.y)
        self.setting = ai_game.setting

    def update(self):
        self.y += self.setting.alien_speed
        self.rect.y = self.y