#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyganim
import blocks
import monsters
from pygame import *
import os

STEP_SPEED = 1
MOVE_SPEED = 4
MOVE_EXTRA_SPEED = 5
JUMP_EXTRA_POWER = 3
WIDTH = 100
HEIGHT = 100
COLOR =  "#888888"
JUMP_POWER = 15
GRAVITY = 0.35 # Сила, которая будет тянуть нас вниз
ANIMATION_DELAY = 0.1 # скорость смены кадров
ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами

ANIMATION_RIGHT = [('%s/liv/r1.png' % ICON_DIR),
            ('%s/liv/r2.png' % ICON_DIR)]
ANIMATION_LEFT = [('%s/liv/l1.png' % ICON_DIR),
            ('%s/liv/l2.png' % ICON_DIR)]
ANIMATION_JUMP = [('%s/liv/j.png' % ICON_DIR, 0.1)]
ANIMATION_STAY = [('%s/liv/0.png' % ICON_DIR, 0.1)]

class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0   #скорость перемещения. 0 - стоять на месте
        self.startX = x # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.yvel = 0 # скорость вертикального перемещения
        self.onGround = False # На земле ли я?
        self.isFly = False
        self.image = Surface((WIDTH,HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT) # прямоугольный объект
        self.image.set_colorkey(Color(COLOR)) # делаем фон прозрачным
#        Анимация движения вправо
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
#        Анимация движения влево        
        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        
        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0)) # По-умолчанию, стоим
        
        self.boltAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()
        self.winner = False

       
    def collide(self, xvel, yvel, platforms):
            for p in platforms:
                if sprite.collide_rect(self, p): # если есть пересечение платформы с игроком

                    if xvel > 0:                      # если движется вправо
                        self.rect.right = p.rect.left # то не движется вправо

                    if xvel < 0:                      # если движется влево
                        self.rect.left = p.rect.right # то не движется влево

                    if yvel > 0:                      # если падает вниз
                        self.rect.bottom = p.rect.top # то не падает вниз
                        self.onGround = True          # и становится на что-то твердое
                        self.yvel = 0                 # и энергия падения пропадает

                    if yvel < 0:                      # если движется вверх
                        self.rect.top = p.rect.bottom # то не движется вверх
                        self.yvel = 0                 # и энергия прыжка пропадает
                    if isinstance(p, blocks.BlockDie) or isinstance(p, monsters.Monster): # если пересакаемый блок - blocks.BlockDie
                         self.die()# умираем
                    elif isinstance(p, blocks.Princess): # если коснулись принцессы
                         self.winner = True # победили!!!
    def update(self, left, right, up, running, platforms):
        
        if up:
            if self.onGround: # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
                if running and (left or right): # если есть ускорение и мы движемся
                    self.yvel -= JUMP_EXTRA_POWER # то прыгаем выше

        if left:
            if self.xvel < 0:
                self.xvel = -MOVE_SPEED # Лево = x- n
            else:
                self.xvel = -STEP_SPEED
            if running: # если усkорение
                self.xvel-=MOVE_EXTRA_SPEED # то передвигаемся быстрее

        if right:
            if self.xvel > 0:
                self.xvel = MOVE_SPEED
            else:
                self.xvel = STEP_SPEED
            if running: # если усkорение
                self.xvel+=MOVE_EXTRA_SPEED # то передвигаемся быстрее

        self.image.fill(Color(COLOR))
        if self.isFly:
            if self.xvel < 0:
                self.boltAnimJumpLeft.blit(self.image, (0, 0)) # отображаем анимацию прыжка
            elif self.xvel > 0:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimJump.blit(self.image, (0, 0))
        else:
           if running:
                if self.xvel < 0:
                    self.boltAnimLeft.blit(self.image, (0, 0)) # отображаем анимацию движения
                elif self.xvel > 0:
                    self.boltAnimRight.blit(self.image, (0, 0))
                else:
                    self.boltAnimStay.blit(self.image, (0, 0))
           else:
                if self.xvel < 0:
                    self.boltAnimLeft.blit(self.image, (0, 0)) # отображаем анимацию движения
                elif self.xvel > 0:
                    self.boltAnimRight.blit(self.image, (0, 0))
                else:
                    self.boltAnimStay.blit(self.image, (0, 0))


         
        if not(left or right) and not self.isFly: # стоим, когда нет указаний идти
            self.xvel = 0
        if not self.onGround:
            self.yvel +=  GRAVITY

        self.onGround = False; # Мы не знаем, когда мы на земле((   
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)
        
    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY
        
    def die(self):
        time.wait(500)
        self.xvel = 0
        self.yvel = 0
        self.teleporting(self.startX, self.startY) # перемещаемся в начальные координаты
