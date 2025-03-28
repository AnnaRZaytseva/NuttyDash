import pygame
from Config import *
from Sprites import *
from os import path
from TileMap import *
import random

class Game:
    def __init__(self):
        # Размер окна и приведение к готовности запуска
        pygame.init()
        pygame.mixer.init()  # для звука
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)  # размер окна
        pygame.display.set_caption(TITLE)  # название игры
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500,100)
        self.load_data()
        self.GameRunning = True
        self.paused = False
        self.health = 3

    def draw_text(self, text, font_name, size,color, x, y, align="nw"):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
    def show_start_screen(self):
        pass
        #Начальный экран/ меню

    def load_data(self):
        game_folder = path.dirname(__file__)
        map_folder = path.join(game_folder, 'Maps')
        sprite_folder = path.join(game_folder, 'Sprites')
        self.font = path.join(game_folder, 'font.ttf')
        self.dim_screen = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.map = TileMap(path.join(map_folder, 'test.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.spritesheet_player = Spritesheet(path.join(sprite_folder, 'sq_spritesheet.png'))
        self.heart_img = pygame.image.load('heart.png')
        self.helth_img = pygame.transform.scale(self.heart_img, (20, 20))

    def new(self):
        #Начать новую игру
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()

        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'platform':
                Obstacles(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)

        # Поиск тайлов для спавна мобов
        spawn_layer = self.map.tmxdata.get_layer_by_name('Spawn')  # Назови слой в Tiled, например, "SpawnLayer"
        for x, y, gid in spawn_layer:
            if gid == 1:  # Замени 5 на нужный ID тайла
                Mob(self, x, y)

        self.camera = Camera(self.map.width, self.map.height)
        self.run()
        self.paused = False
        self.GameRunning = True

    def run(self):
        # Игровой цикл
        self.playing = True
        while self.playing:
            # FPS
            self.clock.tick(FPS)
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def update(self):
        # Обновление кадров
        self.all_sprites.update()
        self.camera.update(self.player)
        # Проверка на столкновение с мобами
        mob_hits = pygame.sprite.spritecollide(self.player, self.mobs, False)
        if mob_hits:
            self.playing = False  # Останавливаем игровой цикл
            self.check_health()  # Уменьшаем здоровье игрока
        #Проверка на столкновение, только если падает
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                #min для поиска самой высокой платформы предотвращает ненужное перемещение на более низкие платформы.
                highest_platform = min(hits, key=lambda p: p.rect.top)
                if self.player.pos.y < highest_platform.rect.centery:
                    self.player.pos.y = highest_platform.rect.top #прилипание
                    self.player.vel.y = 0
                    self.player.jumping = False

    def events(self):
        # События
        for event in pygame.event.get():
            # Закрытие окна
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.GameRunning = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.GameRunning = False
                if event.key == pygame.K_q:
                    self.paused = not self.paused

                if event.key == pygame.K_SPACE:
                        self.player.jump()


    def draw(self):
        # Рендер

        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.font, 105, (0, 250, 154), WIDTH / 2, HEIGHT / 2, align="center")
        self.show_health()
        pygame.display.flip()

    def show_start_screen(self):
        #Начальный экран/ меню
        pass

    def show_gameover_screen(self):
        #Экран при проигрыше
        self.screen.fill((0, 0, 0))  # Черный фон
        self.draw_text("Game Over", self.font, 74, (0, 250, 154), WIDTH / 2, HEIGHT / 2 - 50, align="center")
        self.draw_text("Press R to Restart or ESC to Quit", self.font, 36, (0, 250, 154), WIDTH / 2, HEIGHT /  2 + 50, align="center")
        pygame.display.flip()

        # Очистка очереди событий перед ожиданием ввода
        pygame.event.clear()

        # Ожидание ввода пользователя
        waiting = True

        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.GameRunning = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Перезапуск
                        waiting = False
                        self.health = 3
                        self.new()  # Запускаем новую игру прямо здесь

                    if event.key == pygame.K_ESCAPE:  # Выход
                        self.GameRunning = False
                        waiting = False



    def show_health(self):
        show = 0
        x = 20
        while show != self.health:
            self.screen.blit(self.heart_img, (x, 20))
            x+=20
            show+=1

    def check_health(self):
        self.health = self.health - 1
        if self.health == 0:
            self.show_gameover_screen()

# Основной цикл игры (упрощен)
game = Game()
game.show_start_screen()
while game.GameRunning:
    game.new()
pygame.quit()







