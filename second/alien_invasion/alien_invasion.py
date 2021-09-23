import sys
import pygame
from time import sleep
from random import *
from setting import Setting
from ship import Ship
from game_stats import GameStats
from Bullet import Bullet
from Alien import Alien
from Button import Button
from scoreboard import Scoreboard
class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.setting = Setting()
        self.screen = pygame.display.set_mode((self.setting.screen_width,self.setting.screen_height),pygame.RESIZABLE)
        pygame.display.set_caption(self.setting.caption)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.create_aliens()
        self.flag = 1
        self.stats = GameStats(self)
        self.play_button = Button(self,"Play")
        self.sb = Scoreboard(self)

    def create_aliens(self):
        alien = Alien(self)
        alien_width = alien.rect.width
        number_now = randint(1,8)
        screen_width_now = self.setting.screen_width - alien_width
        a = []
        num = randint(0,20)
        while num < screen_width_now:
            a.append(num)
            num += int(alien_width + 10)
        for i in range(0,number_now):
            alien = Alien(self)
            alien.rect.x = choice(a)
            self.aliens.add(alien)

    def fire(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def keydown(self,key):
        if key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif key == pygame.K_UP:
            self.ship.moving_up = True
        elif key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif key == pygame.K_q:
            sys.exit()
        elif key == pygame.K_SPACE:
            self.fire()

    def keyup(self,key):
        if key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif key == pygame.K_UP:
            self.ship.moving_up = False
        elif key == pygame.K_DOWN:
            self.ship.moving_down = False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                try:
                    self.keydown(event.key)
                except AttributeError:
                    self.create_aliens()
            elif event.type == pygame.KEYUP:
                self.keyup(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_play_button(mouse_pos)

    def check_play_button(self,mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self.stats.game_active = True
            self.stats.reset_stats()
            self.aliens.empty()
            self.bullets.empty()
            self.create_aliens()
            self.ship.center_ship()
            self.flag = 1
            pygame.mouse.set_visible(False)
            self.sb.prep_score()
            self.sb.high_score()
            self.sb.prep_ship()

    def ship_hit(self):
        if self.stats.ships >1:
            self.stats.ships -= 1
            self.aliens.empty()
            self.bullets.empty()
            self.ship.center_ship()
            self.flag = 1
            pygame.time.set_timer(pygame.KEYDOWN, 0)
            self.create_aliens()
            self.sb.prep_ship()
            sleep(2)
        else:
            self.stats.game_active = False
            if self.stats.score > self.stats.high_score:
                self.stats.high_score = self.stats.score
            pygame.time.set_timer(pygame.KEYDOWN, 0)
            pygame.mouse.set_visible(True)

    def update_screen(self):
        self.screen.fill(self.setting.bg_color)
        self.ship.blitme()
        for b in self.bullets.sprites():
            b.draw_bullet()
        self.aliens.draw(self.screen)
        if not self.stats.game_active:
            self.play_button.draw_button()
        self.sb.show_score()
        pygame.display.flip()

    def update_bullet(self):
        self.bullets.update()
        for b in self.bullets.copy():
            if b.rect.bottom <= 0:
                self.bullets.remove(b)
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if collisions:
            self.stats.score += self.setting.alien_points
            self.sb.prep_score()

    def aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self.ship_hit()
                break

    def update_alien(self):
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self.ship_hit()
        self.aliens_bottom()

    def run_game(self):
        while True:
            self.events()
            if self.stats.game_active:
                self.ship.update()
                self.update_bullet()
                if self.flag:
                    self.flag = 0
                    pygame.time.set_timer(pygame.KEYDOWN, 1500)
                self.update_alien()
            self.update_screen()
