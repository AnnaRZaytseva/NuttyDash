import pygame
import pygame_widgets
from pygame.mouse import set_visible
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from Main_File import Game
from Config import WIDTH, HEIGHT

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
but_img = pygame.image.load("Menu/Images/button.png")
bg = pygame.image.load("Menu/Images/background.png")
font_name = 'Menu/Sounds/Font.ttf'

# класс с музыкой
class Music():
    def __init__(self):
        pygame.mixer.init()

        self.music_vol = 1
        self.sound_vol = 1
        pygame.mixer.music.load("Menu/Sounds/menu.mp3")
        pygame.mixer.music.play(-1)

        self.click_sound = pygame.mixer.Sound("Menu/Sounds/click.mp3")

    def set_music_vol(self, music_volume):
        pygame.mixer.music.set_volume(music_volume)

    def set_sound_vol(self, sound_volume):
        self.click_sound.set_volume(sound_volume)

    def click_sound_play(self):
        self.click_sound.play()

    #сюда еще другие звуки вставить

#Меню с уровнями
class Levels_menu():
    def __init__(self):
        img = pygame.image.load("Menu/Images/set_btn.png")
        self.lev1 = Button(
            screen, 50, 80, 260, 407,

            text='Уровень 1',
            font=pygame.font.Font(font_name, 30),
            margin=30,
            textColour=(255, 255, 255),
            radius=30,
            onClick = self.level1,
            inactiveColour = (250, 219, 173),
            pressedColour=(250, 219, 173),
            hoverColour = (85, 139, 47),
            image = pygame.image.load("Menu/Images/levels.png")
        )
        self.lev2 = Button(
            screen, 350, 80, 260, 407,

            text='Уровень 2',
            font=pygame.font.Font(font_name, 30),
            margin=30,
            textColour=(255, 255, 255),
            radius=30,
            onClick=self.level2,
            inactiveColour=(250, 219, 173),
            pressedColour=(250, 219, 173),
            hoverColour=(85, 139, 47),
            image=pygame.image.load("Menu/Images/levels.png")
        )
        self.lev3 = Button(
            screen, 650, 80, 260, 407,

            text='Уровень 3',
            font=pygame.font.Font(font_name, 30),
            margin=30,
            textColour=(255, 255, 255),
            radius=30,
            onClick=self.level3,
            inactiveColour=(250, 219, 173),
            pressedColour=(250, 219, 173),
            hoverColour=(85, 139, 47),
            image=pygame.image.load("Menu/Images/levels.png")
        )

        self.set_btn = Button(
            screen, 900, 50, 40, 40,
            margin=30,
            radius=200,
            onClick=lambda: self.change_vis(),
            inactiveColour=(250, 219, 173),
            pressedColour=(250, 219, 173),
            hoverColour=(85, 139, 47),
            # pressedColour=(250, 219, 173),
            image=img
        )

        self.set_vis = False
        self.lev1.hide()
        self.lev2.hide()
        self.lev3.hide()

        self.set_btn.hide()

        self.bg = pygame.image.load("Menu/Images/lev_back.png")

    def level1(self):
       game.current_level = 0
       game.collectible_count = 0
       game.load_data()
       game.new()
       mus.click_sound_play()

    def level2(self):
        game.current_level = 1
        game.collectible_count = 0
        game.load_data()
        game.new()
        mus.click_sound_play()

    def level3(self):
        game.current_level = 0
        game.collectible_count = 0
        game.load_data()
        game.new()
        mus.click_sound_play()

    def change_vis(self):
        self.set_vis = not self.set_vis
        if self.set_vis:
            self.lev1.show()
            self.lev2.show()
            self.lev3.show()
            self.set_btn.show()

        else:
            self.lev1.hide()
            self.lev2.hide()
            self.lev3.hide()
            self.set_btn.hide()
            butts.hide_all(True)

    def screen_blit(self):
        if self.set_vis:
            screen.blit(self.bg, (0, 0))
            self.lev1.draw()
            self.lev2.draw()
            self.lev3.draw()
            self.set_btn.draw()

#класс с настройками
class Setting():
    def __init__(self):
        self.set_screen = pygame.image.load("Menu/Images/settings.png")
        img = pygame.image.load("Menu/Images/set_btn.png")
        self.set_btn = Button(
            screen, 630, 115, 50, 50,
            margin = 30,
            radius = 200,
            onClick = lambda: self.change_visible(),
            inactiveColour = (250, 219, 173),
            hoverColour=(250, 219, 173),
            #pressedColour=(250, 219, 173),
            image = img
        )

        self.slider1 = Slider(screen, 390, 240, 260, 10, min=0, max=99, step=1, initial = 100,
                              colour = (109, 76, 65), handleColour = (109, 76, 65))
        self.slider2 = Slider(screen, 390, 340, 260, 10, min=0, max=99, step=1, initial = 100,
                              colour = (109, 76, 65), handleColour = (109, 76, 65))
        self.set_btn.hide()
        self.slider1.hide()
        self.slider2.hide()

        self.set_vis = False

    def change_visible(self):
        self.set_vis = not (self.set_vis)
        if not self.set_vis:
            self.set_btn.hide()
            self.slider1.hide()
            self.slider2.hide()
        else:
            self.set_btn.show()
            self.slider1.show()
            self.slider2.show()

        mus.click_sound_play()

    def screen_blit(self):
        if self.set_vis:
            screen.blit(self.set_screen, (280, 80))

            self.set_btn.draw()
            self.slider1.draw()
            self.slider2.draw()

            music_volume = self.slider1.getValue() / 100.0
            mus.set_music_vol(music_volume)

            sound_volume = self.slider2.getValue() / 100.0
            mus.set_sound_vol(sound_volume)

#класс с кнопками
class Buttons():
    def __init__(self):
        self.start_b = Button(
            screen, 60, 460, 190, 60,

            text='Играть',
            font=pygame.font.Font(font_name, 30),
            margin=30,
            textColour=(255, 255, 255),
            radius=200,
            onClick=lambda: self.play(),
            image=but_img
        )

        self.levels_b = Button(
            screen, 280, 460, 190, 60,

            text='Уровни',
            font=pygame.font.Font(font_name, 30),
            margin=30,
            textColour=(255, 255, 255),
            radius=200,
            onClick=lambda: self.levels(),
            image=but_img
        )

        self.settings_b = Button(
            screen, 500, 460, 190, 60,

            text='настройки',
            font=pygame.font.Font(font_name, 30),
            margin=30,
            textColour=(255, 255, 255),
            radius=200,
            onClick=lambda: self.settings(),
            image=but_img
        )

        self.exit_b = Button(
            screen, 720, 460, 190, 60,

            text='выход',
            font=pygame.font.Font(font_name, 30),
            margin=30,
            textColour=(255, 255, 255),
            radius=200,
            onClick=lambda: quit(),
            #hoverColour = (0,0,0),
            image=but_img
        )

    def hide_all(self, set_vis):
        if not set_vis:
            self.exit_b.hide()
            self.levels_b.hide()
            self.start_b.hide()
            self.settings_b.hide()
        else:
            self.exit_b.show()
            self.levels_b.show()
            self.start_b.show()
            self.settings_b.show()

    def play(self):
        game.new()
        mus.click_sound_play()

    def levels(self):
        mus.click_sound_play()
        lev_menu.change_vis()
        self.hide_all(False)

    def settings(self):
        sets.change_visible()

run = True
sets =  Setting()
butts = Buttons()
mus = Music()
lev_menu = Levels_menu()
game = Game()
while run:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()

    screen.fill((255, 255, 255))
    screen.blit(bg, (0, 0))

    sets.screen_blit()
    lev_menu.screen_blit()
    pygame_widgets.update(events)
    pygame.display.update()