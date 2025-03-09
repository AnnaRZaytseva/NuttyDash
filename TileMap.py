import pygame
import pytmx
from Config import *



class TileMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha = True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:

            if isinstance(layer, pytmx.TiledTileLayer):

                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x *self.tmxdata.tilewidth, y * self.tmxdata.tileheight))
    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        temp_surface.fill((0,0,0,0))
        self.render(temp_surface)
        return temp_surface





class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0,0, width, height) #для смещения отрисовки карты
        self.width = width
        self.height = height
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.pos.x + int(WIDTH / 2)
        y = -target.pos.y + int(HEIGHT / 2)

        #Лимит смещения под размер карты
        x = min(0, x) #Лево
        y = min(0, y) #Верх
        x = max(-(self.width - WIDTH), x) #право
        y = max(-(self.height - HEIGHT), y) #низ

        self.camera = pygame.Rect(int(x), int(y), self.width, self.height)
