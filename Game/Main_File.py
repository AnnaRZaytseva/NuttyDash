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

    def load_data(self):
        game_folder = path.dirname(__file__)
        map_folder = path.join(game_folder, 'Maps')
        sprite_folder = path.join(game_folder, 'Sprites')
        self.map = TileMap(path.join(map_folder, 'test.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.spritesheet_player = Spritesheet(path.join(sprite_folder, 'sq_spritesheet.png'))

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

    def run(self):
        # Игровой цикл
        self.playing = True
        while self.playing:
            # FPS
            self.clock.tick(FPS)
            self.events()
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
            self.show_gameover_screen()  # Показываем экран Game Over

        #Проверка на столкновение,только если падает
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
                if event.key == pygame.K_SPACE:
                    self.player.jump()
    def draw(self):
        # Рендер

        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pygame.display.flip()

    def show_start_screen(self):
        #Начальный экран/ меню
        pass
    def show_gameover_screen(self):
        #Экран при проигрыше
        self.screen.fill((0, 0, 0))  # Черный фон
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 0, 0))  # Красный текст
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 50))
        self.screen.blit(text, text_rect)

        font = pygame.font.Font(None, 36)
        restart_text = font.render("Press R to Restart or ESC to Quit", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))
        self.screen.blit(restart_text, restart_rect)

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
                        self.new()  # Запускаем новую игру прямо здесь
                    if event.key == pygame.K_ESCAPE:  # Выход
                        self.GameRunning = False
                        waiting = False

# Основной цикл игры (упрощен)
game = Game()
game.show_start_screen()
while game.GameRunning:
    game.new()
pygame.quit()







