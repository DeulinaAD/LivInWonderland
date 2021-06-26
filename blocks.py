#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import os

ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 100
PLATFORM_COLOR = "#FF6262"

class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = image.load("blocks/platform.png")
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("%s/blocks/dieBlock.png" % ICON_DIR)
        self.rect = Rect(x + PLATFORM_WIDTH / 4, y + PLATFORM_HEIGHT / 4, PLATFORM_WIDTH - PLATFORM_WIDTH / 2, PLATFORM_HEIGHT - PLATFORM_HEIGHT / 2)

class Okai(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("%s/blocks/OkBlock.png" % ICON_DIR)
        
class Princess(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x,y)
        self.image = image.load("%s/blocks/cloud.png" % ICON_DIR)
class secret(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x,y)
