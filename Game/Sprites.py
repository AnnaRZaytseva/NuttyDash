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

        # Применяем трение
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        if abs(self.vel.x) < 0.5:
            self.vel.x = 0

        # Рассчитываем новую позицию
        new_pos = self.pos + self.vel + 0.5 * self.acc

        # Ограничение по горизонтали (X)
        map_width = self.game.map.width  # Используем ширину карты из TileMap 
        half_width = self.rect.width / 2
        if new_pos.x - half_width < 0:  # Левая граница
            new_pos.x = half_width
            self.vel.x = 0
        elif new_pos.x + half_width > map_width:  # Правая граница
            new_pos.x = map_width - half_width
            self.vel.x = 0

        # Применяем новую позицию
        self.pos = new_pos
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
        # Проверяем, стоит ли игрок на платформе
        self.rect.y += 2  # Смещаем вниз для проверки
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2  # Возвращаем обратно
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -11  # Скорость прыжка вверх
            self.pos.y += self.vel.y  # Немедленно начинаем движение вверх

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
        self.load_images()  # Загружаем изображения из спрайт-листа
        self.image = self.walk_frames_r[0]  # Начальный кадр (вправо)
        self.image.set_colorkey((0, 0, 0))  # Убираем черный фон
        self.rect = self.image.get_rect()
        self.pos = vec(x * TILESIZE, y * TILESIZE)  # Позиция в пикселях с учетом размера тайла
        self.vel = vec(2, 0)  # Начальная скорость (2 пикселя вправо)
        self.acc = vec(0, PLAYER_GRAV)  # Гравитация
        self.rect.midbottom = self.pos  # Позиция привязана к низу спрайта
        self.platform = None
        self.walking = True  # Моб всегда движется
        self.current_frame = 0  # Текущий кадр анимации
        self.last_update = 0  # Время последнего обновления кадра

    def load_images(self):
        # Пример координат и размеров кадров (замените на свои)
        self.walk_frames_l = [
            self.game.spritesheet_mob.get_image(48, 60, 62, 70),    # Кадр 1 влево
            self.game.spritesheet_mob.get_image(208, 66, 60, 62),
            self.game.spritesheet_mob.get_image(368, 62, 60, 66),
            self.game.spritesheet_mob.get_image(528, 58, 60, 70),
            self.game.spritesheet_mob.get_image(688, 60, 60, 68),
            self.game.spritesheet_mob.get_image(848, 66, 60, 62),
            self.game.spritesheet_mob.get_image(1008, 62, 60, 66),
            self.game.spritesheet_mob.get_image(1168, 58, 60, 70)
        ]
        for frame in self.walk_frames_l:
            frame.set_colorkey((0, 0, 0))  # Убираем черный фон

        # Отражаем кадры для движения влево
        self.walk_frames_r = []
        for frame in self.walk_frames_l:
            self.walk_frames_r.append(pygame.transform.flip(frame, True, False))
            frame.set_colorkey((0, 0, 0))

    def animate(self):
        now = pygame.time.get_ticks()
        if self.walking and now - self.last_update > 200:  # Скорость анимации (200 мс между кадрами)
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.walk_frames_r)
            bottom = self.rect.bottom  # Сохраняем нижнюю позицию для плавности
            if self.vel.x > 0:  # Движение вправо
                self.image = self.walk_frames_r[self.current_frame]
            elif self.vel.x < 0:  # Движение влево
                self.image = self.walk_frames_l[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom  # Восстанавливаем позицию

    def find_platform(self):
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
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
                self.platform = hit
            elif self.vel.y < 0:  # Удар головой вверх
                self.pos.y = hit.rect.bottom + self.rect.height
                self.vel.y = 0
            self.rect.midbottom = self.pos

        # Если платформа не найдена, ищем её
        if not self.platform:
            self.find_platform()

        # Ограничение движения размерами платформы
        if self.platform:
            if self.pos.x + self.rect.width / 2 > self.platform.rect.right:
                self.pos.x = self.platform.rect.right - self.rect.width / 2
                self.vel.x = -2  # Разворот влево
            elif self.pos.x - self.rect.width / 2 < self.platform.rect.left:
                self.pos.x = self.platform.rect.left + self.rect.width / 2
                self.vel.x = 2  # Разворот вправо

        # Обновляем анимацию
        self.animate()

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
class Collectible(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.collectibles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # Загружаем изображение шишки
        self.image = game.spritesheet_player.get_image(0, 0, 32, 42)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.center = self.pos

    def update(self):
        # Проверка столкновения с игроком
        if pygame.sprite.collide_rect(self, self.game.player):
            self.game.collectible_count += 1
            self.kill()  # Удаляем шишку после сбора


class Nut(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites  # Орех только в all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.spritesheet_player.get_image(856, 0, 64, 64)  # Настройте координаты
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.center = self.pos

    def update(self):
        if pygame.sprite.collide_rect(self, self.game.player):
            self.game.next_level()
            self.kill()





