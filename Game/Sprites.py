#Классы спрайтов для игры
import pygame
from Config import *

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames_r[0]
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) #позиция
        self.vel = vec(0,0) #скорость
        self.acc = vec(0,0) #ускорение

        def update(self):
            self.animate()
            self.acc = vec(0, PLAYER_GRAV)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.acc.x = -PLAYER_ACC
            if keys[pygame.K_d]:
                self.acc.x = PLAYER_ACC

            self.acc.x += self.vel.x * PLAYER_FRICTION
            self.vel += self.acc
            if abs(self.vel.x) < 0.5:
                self.vel.x = 0

            # Horizontal movement
            self.pos.x += self.vel.x + 0.5 * self.acc.x
            self.rect.midbottom = self.pos
            hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
            for hit in hits:
                if self.vel.x > 0:
                    self.pos.x = hit.rect.left - self.rect.width / 2
                elif self.vel.x < 0:
                    self.pos.x = hit.rect.right + self.rect.width / 2
                self.vel.x = 0
                self.rect.midbottom = self.pos

            # Vertical movement
            self.pos.y += self.vel.y + 0.5 * self.acc.y
            self.rect.midbottom = self.pos
            hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
            self.grounded = False
            for hit in hits:
                if self.vel.y > 0:
                    self.pos.y = hit.rect.top
                    self.vel.y = 0
                    self.jumping = False
                    self.grounded = True
                elif self.vel.y < 0:
                    self.pos.y = hit.rect.bottom + self.rect.height
                    self.vel.y = 0
                self.rect.midbottom = self.pos

    def load_images(self):
        self.walk_frames_l = [self.game.spritesheet_player.get_image(32, 38, 112, 96),
                              self.game.spritesheet_player.get_image(192, 40, 119, 79),
                              self.game.spritesheet_player.get_image(348, 20, 106, 90),
                              self.game.spritesheet_player.get_image(504, 14, 100, 102),
                              self.game.spritesheet_player.get_image(638, 28, 88, 100)]
        for frame in self.walk_frames_l:
            frame.set_colorkey((0,0,0))
        self.walk_frames_r = []
        for frame in self.walk_frames_l:
            self.walk_frames_r.append(pygame.transform.flip(frame, True, False))
            frame.set_colorkey((0, 0, 0))
        self.standing_frames_l = [self.game.spritesheet_player.get_image(758, 37, 90, 92)]
        for frame in self.standing_frames_l:
            frame.set_colorkey((0,0,0))
        self.standing_frames_r = []
        for frame in self.standing_frames_l:
            self.standing_frames_r.append(pygame.transform.flip(frame, True, False))
            frame.set_colorkey((0, 0, 0))
        self.jumping_frames_l = [self.game.spritesheet_player.get_image(192, 40, 119, 79),
                               self.game.spritesheet_player.get_image(638, 28, 88, 100)]
        for frame in self.jumping_frames_l:
            frame.set_colorkey((0,0,0))
        self.jumping_frames_r = []
        for frame in self.jumping_frames_l:
            self.jumping_frames_r.append(pygame.transform.flip(frame, True, False))
            frame.set_colorkey((0, 0, 0))

    def jump(self):
        #Прыжок только когда есть платформа под лапками
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -10

    def update(self):
        self.animate()
        self.acc = vec(0,PLAYER_GRAV)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_d]:
            self.acc.x = PLAYER_ACC

        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        if abs(self.vel.x)<0.5:
            self.vel.x = 0
        self.pos += self.vel + 0.5 *self.acc #какая-то физформула
        self.rect.midbottom = self.pos

    def animate(self):
        now = pygame.time.get_ticks()
        if self.vel.x !=0:
            self.walking = True
        else:
            self.walking = False

        if self.walking:
            if now - self.last_update > 90:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x >0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if not self.jumping and not self.walking:
            if self.image == self.walk_frames_r[self.current_frame]:
                self.image = self.standing_frames_r[0]
            if self.image == self.walk_frames_l[self.current_frame]:
                self.image = self.standing_frames_l[0]
            bottom = self.rect.bottom
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.platforms
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Mob(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0))  # Красный цвет для видимости
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(2, 0)  # Начальная скорость (2 пикселя вправо)
        self.acc = vec(0, PLAYER_GRAV)  # Гравитация
        self.rect.midbottom = self.pos  # Позиция привязана к низу спрайта
        self.platform = None  # Платформа, на которой находится моб

    def find_platform(self):
        # Находим платформу под мобом
        self.rect.y += 1  # Смещаем вниз для проверки столкновения
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1  # Возвращаем обратно
        if hits:
            # Выбираем ближайшую платформу под ногами
            self.platform = min(hits, key=lambda p: p.rect.top - self.rect.bottom)
        else:
            self.platform = None

    def update(self):
        # Применяем гравитацию
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Проверка столкновений с платформами
        self.rect.midbottom = self.pos
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        for hit in hits:
            if self.vel.y > 0:  # Падение вниз
                self.pos.y = hit.rect.top
                self.vel.y = 0
                self.platform = hit  # Запоминаем платформу, на которой стоим
            elif self.vel.y < 0:  # Удар головой вверх
                self.pos.y = hit.rect.bottom + self.rect.height
                self.vel.y = 0
            self.rect.midbottom = self.pos

        # Если платформа не найдена, ищем её
        if not self.platform:
            self.find_platform()

        # Ограничение движения размерами платформы
        if self.platform:
            if self.pos.x + self.rect.width / 2 > self.platform.rect.right:  # Правая граница платформы
                self.pos.x = self.platform.rect.right - self.rect.width / 2
                self.vel.x = -2  # Разворот влево
            elif self.pos.x - self.rect.width / 2 < self.platform.rect.left:  # Левая граница платформы
                self.pos.x = self.platform.rect.left + self.rect.width / 2
                self.vel.x = 2  # Разворот вправо

        # Синхронизация rect с pos
        self.rect.midbottom = self.pos


class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()
    def get_image(self, x, y, width, height):
        #вырезает изображение из листа с несколькими спрайтами
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        return image





