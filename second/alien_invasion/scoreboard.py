import pygame.font
from pygame.sprite import Group
from ship import Ship
class Scoreboard:
    def __init__(self,ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.setting = ai_game.setting
        self.stats = ai_game.stats
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,48)
        self.prep_score()
        self.high_score()
        self.prep_ship()
    def prep_score(self):
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str,True,self.text_color,self.setting.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    def high_score(self):
        high_s = str(self.stats.high_score)
        self.high_score_image = self.font.render(high_s, True, self.text_color, self.setting.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top
    def prep_ship(self):
        self.shipss = Group()
        for n in range(self.stats.ships):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + n * ship.rect.width
            ship.rect.y = 10
            self.shipss.add(ship)
    def show_score(self):
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.shipss.draw(self.screen)