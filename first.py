#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import pygame
import tmxreader # Может загружать tmx файлы
import helperspygame # Преобразует tmx карты в формат  спрайтов pygame
import pyganim
from monsters import *
from pygame import *
from pyganim import *
from player import *
from blocks import *


#Объявляем переменные

WIN_WIDTH = 1000 #Ширина создаваемого окна
WIN_HEIGHT = 640 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#004400"
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 100
PLATFORM_COLOR = "#FF6262"
CENTER_OF_SCREEN = WIN_WIDTH / 2, WIN_HEIGHT / 2


FILE_DIR = os.path.dirname(__file__)

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

    def reverse(self, pos):# получение внутренних координат из глобальных
        return pos[0] - self.state.left, pos[1] - self.state.top

def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-WIN_WIDTH), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-WIN_HEIGHT), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h) 


def loadLevel(name):
    global playerX, playerY # объявляем глобальные переменные, это координаты героя
    global total_level_height, total_level_width
    global sprite_layers # все слои карты

    world_map = tmxreader.TileMapParser().parse_decode('%s/%s.tmx' % (FILE_DIR, name)) # загружаем карту
    resources = helperspygame.ResourceLoaderPygame() # инициируем преобразователь карты 
    resources.load(world_map) # и преобразуем карту в понятный pygame формат
    
    sprite_layers = helperspygame.get_layers_from_map(resources) # получаем все слои карты
    
    # берем слои по порядку 0 - слой фона, 1- слой блоков, 2 - слой смертельных блоков
    # 3 - слой объектов монстров, 4 - слой объектов телепортов
    platforms_layer = sprite_layers[1] 
    dieBlocks_layer = sprite_layers[2]

    for row in range(0, platforms_layer.num_tiles_x): # перебираем все координаты тайлов
        for col in range(0, platforms_layer.num_tiles_y):
            if platforms_layer.content2D[col][row] is not None:
                pf = Platform(row * PLATFORM_WIDTH, col * PLATFORM_WIDTH)# как и прежде создаем объкты класса Platform
                platforms.append(pf)
            if dieBlocks_layer.content2D[col][row] is not None:
                bd = BlockDie(row * PLATFORM_WIDTH, col * PLATFORM_WIDTH)
                platforms.append(bd)

    monsters_layer = sprite_layers[3]
    for monster in monsters_layer.objects:
        try:
            x = monster.x
            y = monster.y
            if monster.name == "Player":
                playerX = x
                playerY = y - PLATFORM_HEIGHT
            elif monster.name == "Princess":
                pr = Princess(x, y - PLATFORM_HEIGHT)
                platforms.append(pr)
                entities.add(pr)
                animatedEntities.add(pr)
            else:
                right = int(monster.properties["right"])
                maxLengthRight = int(monster.properties["maxLengthRight"])
                left = int(monster.properties["left"])
                maxLengthLeft = int(monster.properties["maxLengthLeft"])
                mn = Monster(x, y - PLATFORM_HEIGHT, right, maxLengthRight, maxLengthLeft, left)
                entities.add(mn)
                platforms.append(mn)
                monsters.add(mn)
        except:
            print(u"Ошибка на слое монстров")

    total_level_width = platforms_layer.num_tiles_x * PLATFORM_WIDTH # Высчитываем фактическую ширину уровня
    total_level_height = platforms_layer.num_tiles_y * PLATFORM_HEIGHT   # высоту
def main():
    pygame.init() # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY) # Создаем окошко
    pygame.display.set_caption("Liv in WonDerLand") # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT)) # Создание видимой поверхности
    # будем использовать как фон

    renderer = helperspygame.RendererPygame() # визуализатор
    for lvl in range(1,4):
        loadLevel("levels/map_%s" % lvl)
        bg.fill(Color(BACKGROUND_COLOR))     # Заливаем поверхность сплошным цветом

        left = right = False # по умолчанию - стоим
        up = False
        running = False
        try:
            hero = Player(playerX, playerY) # создаем героя по (x,y) координатам
            entities.add(hero)
        except:
            print (u"Не удалось на карте найти героя, взяты координаты по-умолчанию")
            hero = Player(65, 65)
        entities.add(hero)

        timer = pygame.time.Clock()

        camera = Camera(camera_configure, total_level_width, total_level_height)

        while not hero.winner: # Основной цикл программы
            timer.tick(60)
            for e in pygame.event.get(): # Обрабатываем события
                if e.type == KEYDOWN and e.key == K_UP:
                    up = True
                if e.type == KEYDOWN and e.key == K_LEFT:
                    left = True
                if e.type == KEYDOWN and e.key == K_RIGHT:
                    right = True
                if e.type == KEYDOWN and e.key == K_LSHIFT:
                    running = True

                if e.type == KEYUP and e.key == K_UP:
                    up = False
                if e.type == KEYUP and e.key == K_RIGHT:
                    right = False
                if e.type == KEYUP and e.key == K_LEFT:
                    left = False
                if e.type == KEYUP and e.key == K_LSHIFT:
                    running = False
            for sprite_layer in sprite_layers: # перебираем все слои
                if not sprite_layer.is_object_group: # и если это не слой объектов
                   renderer.render_layer(screen, sprite_layer) # отображаем его

            for e in entities:
                screen.blit(e.image, camera.apply(e))
            animatedEntities.update() # показываеaм анимацию
            monsters.update(platforms) # передвигаем всех монстров
            camera.update(hero) # центризируем камеру относительно персонаж
            center_offset = camera.reverse(CENTER_OF_SCREEN)
            renderer.set_camera_position_and_size(center_offset[0], center_offset[1], \
                                                  WIN_WIDTH, WIN_HEIGHT, "center")
            hero.update(left, right, up, running, platforms) # передвижение
            pygame.display.update()     # обновление и вывод всех изменений на экран
            screen.blit(bg, (0, 0))      # Каждую итерацию необходимо всё перерисовывать
        for sprite_layer in sprite_layers:
            if not sprite_layer.is_object_group:
                renderer.render_layer(screen, sprite_layer)
        # когда заканчиваем уровень
        for e in entities:
            screen.blit(e.image, camera.apply(e)) # еще раз все перерисовываем
        font=pygame.font.SysFont("comicsansms", 30) 
        text=font.render(("Opening the portal to the..."), 1,(255,255,255))# выводим надпись
        screen.blit(text, (10,100))
        pygame.display.update()
        del(monsters_layer)
        del(dieBlocks_layer)
        del(platforms_layer)
        time.wait(10000) # ждем 10 секунд и после - переходим на следующий уровень
        
level = []
entities = pygame.sprite.Group() # Все объекты
animatedEntities = pygame.sprite.Group() # все анимированные объекты, за исключением героя
monsters = pygame.sprite.Group() # Все передвигающиеся объекты
platforms = [] # то, во что мы будем врезаться или опираться
if __name__ == "__main__":
    main()
