#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, pygame, random

size = width, height = 500, 500
black = ( 0,  0,  0)
white = ( 255, 255, 255)



class Ball(pygame.sprite.Sprite):
    def __init__(self, color,id):
        """Класс описывает шарик и его поведение"""
        pygame.sprite.Sprite.__init__(self)
        self.color =str(random.randrange(0, 5, 1))
        self.image = pygame.image.load('ball' + self.color + '.png').convert()
        self.image.set_colorkey(color)
        self.rect = self.image.get_rect()
        self.fall = True
        self.id = id

    def check_falling(self, obstacles):
        """Проверка - падает ли шарик. obstacles - с кем должен сталкиваться"""
        self.rect.move_ip(0, 1)
        collisions = pygame.sprite.spritecollide(self, obstacles, False)
        if self.rect.y < height-self.rect.height:
            self.fall = True
            for item in collisions:
                if not item == self and (self.rect.y > item.rect.y-50 and self.rect.x == item.rect.x):
                   self.fall = False
        else: self.fall = False
        self.rect.move_ip(0, -1)

    def update(self):
        """Если падаем - падаем"""
        if self.fall:
            self.rect.y += 2


class Control(object):
    """Класс для обработки действий игры"""
    def __init__(self):
        """Инициализация игровой сцены"""
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.done = False
        self.ball_elements = self.make_ball_elements()
        self.elements_to_deletion = []

    def make_ball_elements(self):
        """Создание игрового пространства"""
        ball_elements = []
        for i in range(int(width/50)):
             for j in range(int(height/50)):
                 block = Ball(white, i*10+j)
                 block.rect.x = i*50
                 block.rect.y = j*50
                 ball_elements.append(block)
        return pygame.sprite.Group(ball_elements)

    def delete_clicked_elements(self, deleted_block):
        """Удаление нажатого элемента и схожих по цвету соседей"""

        #TODO: Убрать эту жесть на что нибудь попригляднее
        allCollisions = []
        deleted_block.rect.move_ip(0,-3)
        deleted_block.rect.inflate_ip(0,20)
        allCollisions += pygame.sprite.spritecollide(deleted_block, self.ball_elements, False)
        deleted_block.rect.inflate_ip(0,-20)
        deleted_block.rect.move_ip(0,3)

        allCollisions.remove(deleted_block)

        deleted_block.rect.move_ip(-3,0)
        deleted_block.rect.inflate_ip(20,0)
        allCollisions += pygame.sprite.spritecollide(deleted_block, self.ball_elements, False)
        deleted_block.rect.inflate_ip(-20,0)
        deleted_block.rect.move_ip(3,0)
        allCollisions.remove(deleted_block)

        for item in allCollisions:
            if item.color == deleted_block.color and item not in self.elements_to_deletion:
                self.elements_to_deletion.append(item)
                self.delete_clicked_elements(item)
        for elem in self.elements_to_deletion:
            self.ball_elements.remove(elem)

    def event_loop(self):
        """Обработка комманд игрока"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                clicked_sprites = [s for s in self.ball_elements if s.rect.collidepoint(pos)]
                for item in clicked_sprites:
                    self.delete_clicked_elements(item)


    def update(self):
        """Обновление игровой среды"""
        self.keys = pygame.key.get_pressed()
        for i in self.ball_elements:
            i.check_falling(self.ball_elements)
            i.update()

    def draw(self):
        """Прорисовка игровой среды"""
        self.screen.fill(white)
        self.ball_elements.draw(self.screen)


    def main_loop(self):
        """Основной цикл игры"""
        while not self.done:
            self.event_loop()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(size)
    run_it = Control()
    run_it.main_loop()
    pygame.quit()
    sys.exit()
