from pygame import *
import sys
from time import sleep

class GameSprite(sprite.Sprite):
    def __init__(self, w, h, picture, x, y):
        super().__init__()
        self.image = image.load(picture)
        self.image = transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, w, h, picture, x, y):
        super().__init__(w, h, picture, x, y)
        self.speed_x = 0
        self.speed_y = 0
    def update(self):
        self.speed_y = 0
        self.speed_x = 0
        keys = key.get_pressed()
        if keys[K_d]:
            self.speed_x = 2
        if keys[K_a]:
            self.speed_x = -2
        if keys[K_w]:
            self.speed_y = -2
        if keys[K_s]:
            self.speed_y = 2
        self.rect.x += self.speed_x
        walls_touched = sprite.spritecollide(self, stenas, False)
        if self.speed_x > 0:
            for wall in walls_touched:
                self.rect.right = min(self.rect.right, wall.rect.left)
        if self.speed_x < 0:
            for wall in walls_touched:
                self.rect.left = max(self.rect.left, wall.rect.right)
        self.rect.y += self.speed_y
        walls_touched = sprite.spritecollide(self, stenas, False)
        if self.speed_y < 0:
            for wall in walls_touched:
                self.rect.top = max(self.rect.top, wall.rect.bottom)
        if self.speed_y > 0:
            for wall in walls_touched:
                self.rect.bottom = min(self.rect.bottom, wall.rect.top)

class Enemy(GameSprite):
    def __init__(self, w, h, picture, x, y, speed, x_left, x_right):
        super().__init__(w, h, picture, x, y)
        self.speed = speed
        self.x_left = x_left
        self.x_right = x_right
    def update(self):
        self.rect.x = self.rect.x + self.speed
        if self.rect.x > self.x_right:
            self.speed = -abs(self.speed)
        if self.rect.x < self.x_left:
            self.speed = abs(self.speed)

w = 1280
h = 720
window = display.set_mode((w, h))
display.set_caption('Лабиринт')
display.set_icon(image.load('images/labirint.jpg'))
images = image.load('images/фон.jpg') #загрузка картинки
images = transform.scale(images, (w, h)) #изменение размеров картинки
clock = time.Clock()
stena = GameSprite(100, 100, 'images/стена.jpg', 200, 200)
enemy = Enemy(50, 50, 'images/i.png', 100, 360, 2, 100, 1180)
boy = Player(64, 96, 'images/персанаж.png', 640, 360)
winner = GameSprite(100, 100, 'images/winner.png', 50, 600)
stenas = sprite.Group(stena,
                      GameSprite(50, 200, 'images/стена.jpg', 500, 250),
                      GameSprite(50, 200, 'images/стена.jpg', 500, 100),
                      GameSprite(100, 100, 'images/стена.jpg', 250, 250))
enemys = sprite.Group(enemy)
ladno = False
while True:
    for e in event.get(): #цикл который перебирает все события
        if e.type == QUIT: #если тип события = закрытия игры
            sys.exit()
    window.blit(images, (0, 0)) #отображает задние фон
    if winner.rect.colliderect(boy.rect):
        images = image.load('images/patrik.jpeg')
        images = transform.scale(images, (w, h))
        window.blit(images, (0, 0))
        display.update()
        sleep(3)
        sys.exit()
    if sprite.spritecollide(boy, enemys, False):
        images = image.load('images/gameoverezz.jpg')
        images = transform.scale(images, (w, h))
        window.blit(images, (0, 0))
        ladno = True
        display.update()
        sleep(3)
        sys.exit()
    if not ladno:
        boy.reset()
        boy.update()
        winner.reset()
        enemys.draw(window)
        enemys.update()
        stenas.draw(window)
    display.update()
    clock.tick(120)