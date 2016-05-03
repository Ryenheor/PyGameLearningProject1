#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, pygame, os, random
pygame.init()

size = width, height = 500, 500
black = ( 0,  0,  0)
white = ( 255, 255, 255)


class Ball(pygame.sprite.Sprite):

    def __init__(self, color,id):
        """Шарик"""
        pygame.sprite.Sprite.__init__(self)
        self.color =str(random.randrange(0, 5, 1))
        self.image = pygame.image.load('ball' + self.color + '.png').convert()
        self.image.set_colorkey(color)
        self.rect = self.image.get_rect()
        self.fall = True
        self.id = id

    def check_falling(self, obstacles):
        """Проверка - падает ли шарик."""
        self.rect.move_ip(0,1)
        collisions = pygame.sprite.spritecollide(self, obstacles, False)
        if self.rect.y<500-50:
            self.fall = True
            for item in collisions:
                if not item==self and (self.rect.y > item.rect.y-50 and self.rect.x == item.rect.x):
                   self.fall = False
        else: self.fall = False

        self.rect.move_ip(0,-1)

    def update(self):
        """Обработка падения шарика - есть есть, куда падать"""
        if self.fall:
            self.rect.y += 2


class Control(object):

    def __init__(self):
        """Класс обработки действий игры"""
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.done = False
        self.ball_elements = self.make_ball_elements()

    def make_ball_elements(self):
        """Создаем кучу шариков на игровой площадке"""
        ball_elements = []
        for i in range(int(width/50)):
             for j in range(int(height/50)):
                 block = Ball(white, i*10+j)
                 block.rect.x =  i*50
                 block.rect.y = j*50
                 ball_elements.append(block)
        return pygame.sprite.Group(ball_elements)



    def delete_clicked_elements(self, deleted_block):
        """Удаляем шарик"""
        self.ball_elements.remove(deleted_block)



    def event_loop(self):
        """Обработка взаимодействий с игроком"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                clicked_sprites = [s for s in self.ball_elements if s.rect.collidepoint(pos)]
                for item in clicked_sprites:
                    self.delete_clicked_elements(item)


    def update(self):
        """Обновление всех данных"""
        self.keys = pygame.key.get_pressed()
        for i in self.ball_elements:
            i.check_falling(self.ball_elements)
            i.update()

    def draw(self):
        """Прорисовка"""
        self.screen.fill(white)
        self.ball_elements.draw(self.screen)


    def main_loop(self):
        """Основной цикл"""
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
