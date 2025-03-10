import pygame
from Config import *
from Sprites import *
from os import path
from TileMap import *

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

        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'platform':
                Obstacles(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)

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
        pass

game = Game()
game.show_start_screen()
while game.GameRunning:
    game.new()
    game.show_gameover_screen()
pygame.quit()







