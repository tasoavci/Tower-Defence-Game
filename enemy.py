import math
import pygame
from pygame.math import Vector2
from enemy_data import ENEMY_DATA
import constants as const


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, waypoints, images):
        pygame.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.health = ENEMY_DATA[enemy_type]["health"]
        self.speed = ENEMY_DATA[enemy_type]["speed"]
        self.angle = 0
        self.original_image = images[enemy_type]
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, world):
        self.move(world)
        self.rotate()
        self.check_alive(world)

    def move(self, world):
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            self.kill()
            world.health -= 5
            world.missed_enemies += 1

        dist = self.movement.length()

        if dist >= (self.speed * world.game_speed):
            self.pos += self.movement.normalize() * (self.speed * world.game_speed)
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1

    def rotate(self):

        self.angle = math.degrees(
            math.atan2(-self.movement.y, self.movement.x))
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def check_alive(self, world):
        if self.health <= 0:
            world.killed_enemies += 1
            world.money += const.MONEY_REWARD
            self.kill()
