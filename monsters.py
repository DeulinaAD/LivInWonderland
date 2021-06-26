#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import pygame
import pyganim
from pygame import *
from pyganim import *
from player import *
from blocks import *

MONSTER_WIDTH = 100
MONSTER_HEIGHT = 100
MONSTER_COLOR = "#2110FF"
ANIMATION_DELAY = 0.1
MOVE_SPEED = 1
GRAVITY = 0.35
ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами

ANIMATION_STIL = [('%s/monsters/l1.png' % ICON_DIR)]
ANIMATION_MONSTERHORYSONTALleft = [(),
                      ('%s/monsters/l2.png' % ICON_DIR )]
ANIMATION_MONSTERHORYSONTALright = [('%s/monsters/r1.png' % ICON_DIR),
                      ('%s/monsters/r2.png' % ICON_DIR )]


class Monster(sprite.Sprite):
    def __init__(self, x, y, right, maxLengthRight, maxLengthLeft, left):
        sprite.Sprite.__init__(self)
        self.starLEFT = left
        self.starRIGHT = right
        self.image = Surface((MONSTER_WIDTH, MONSTER_HEIGHT))
        self.image.fill(Color(MONSTER_COLOR))
        self.rect = Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
        self.image.set_colorkey(Color(MONSTER_COLOR))
        self.startX = x # начальные координаты
        self.startY = y
        self.onGround = False # На земле ли я?
        self.isFly = False
        self.maxLengthLeft = maxLengthLeft # максимальное расстояние, которое может пройти в одну сторону
        self.maxLengthRight = maxLengthRight
#        self.maxLengthUp= maxLengthUp # максимальное расстояние, которое может пройти в одну сторону, вертикаль
        self.xvel = 0 # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = 0 # скорость движения по вертикали, 0 - не двигается
        #зададим врагу поле зрения. то есть, дадим ему глаза и возможность этими глазами глазеть либо вправо, либо влево
        #
        
        boltAniml = []
        for anim in ANIMATION_MONSTERHORYSONTALleft:
            boltAniml.append((anim, ANIMATION_DELAY))
        self.boltAniml = pyganim.PygAnimation(boltAniml)
        self.boltAniml.play()
        
        boltAnimr = []
        for anim in ANIMATION_MONSTERHORYSONTALright:
            boltAnimr.append((anim, ANIMATION_DELAY))
        self.boltAnimr = pyganim.PygAnimation(boltAnimr)
        self.boltAnimr.play()
         

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
                if sprite.collide_rect(self, p): # если есть пересечение платформы с игроком

                    if self.xvel > 0:                      # если движется вправо
                        self.rect.right = p.rect.left # то не движется вправо
                        self.xvel = 0

                    if self.xvel < 0:                      # если движется влево
                        self.rect.left = p.rect.right # то не движется влево
                        self.xvel = 0
                    if yvel > 0:                      # если падает вниз
                        self.rect.bottom = p.rect.top # то не падает вниз
                        self.onGround = True          # и становится на что-то твердое
                        self.yvel = 0                 # и энергия падения пропадает

                    if yvel < 0:                      # если движется вверх
                        self.rect.top = p.rect.bottom # то не движется вверх
                        self.yvel = 0                 # и энергия прыжка пропадает
   

    def update(self, platforms): # по принципу героя
            self.image.fill(Color(MONSTER_COLOR))
            self.boltAniml.blit(self.image, (0, 0))
            #if self.xvel == 0 and self.yvel == 0
            #if self.xvel == self.starLEFT:
            #    self.xvel -= MOVE_SPEED
            #elif self.xvel == self.starRIGHT:
            #    self.xvel +- MOVE_SPEED

            if not self.onGround:
                self.yvel +=  GRAVITY

            self.onGround = False;
            
            self.collide(self.xvel, 0, platforms)
            if Player.rect.x - self.rect.x > 17:
                self.xvel += MOVE_SPEED
            elif Player.rect.x - self.rect.x < 17:
                self.xvel -= MOVE_SPEED
            else:
                self.xvel = 0
            self.collide(self.xvel, 0, platforms)    
                #если рядом игрок, начинаем идти в сторону игрока
            
