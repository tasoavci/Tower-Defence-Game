import pygame
import constants as const
import math
from turret_data import TURRET_DATA


class Turret(pygame.sprite.Sprite):
    def __init__(self, sprite_sheets, tile_x_pos, tile_y_pos, selected = False ):
        pygame.sprite.Sprite.__init__(self)
        self.tile_x_pos = tile_x_pos
        self.tile_y_pos = tile_y_pos
        self.x = tile_x_pos * const.TILE_SIZE
        self.y = tile_y_pos * const.TILE_SIZE

        self.target = None

        self.selected = selected
        


        self.max_upgrade_level = const.TURRET_LEVEL
        self.upgrade_level = 1
        self.range = TURRET_DATA[self.upgrade_level - 1]["range"]
        self.cooldown = TURRET_DATA[self.upgrade_level - 1]["cooldown"]
        self.damage = TURRET_DATA[self.upgrade_level - 1]["damage"]

        self.last_shot = pygame.time.get_ticks()

        self.sprite_sheets = sprite_sheets
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        self.angle = 0
        self.original_image = self.animation_list[self.frame_index]
        self.image = pygame.transform.rotate(self.original_image,self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x + const.TILE_SIZE / 2,
                            self.y + const.TILE_SIZE/2)
        #range circle of turret
        self.range_image = pygame.Surface((self.range * 2 ,self.range *2))
        self.range_image.fill((0,0,0))
        self.range_image.set_colorkey((0,0,0))
        pygame.draw.circle(self.range_image,'gray100',(self.range,self.range),self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center




    def load_images(self,sprite_sheet):
        size_height = sprite_sheet.get_height()
        size_width = sprite_sheet.get_width()
        size_turret = size_width / 8
        animation_list = []


        for i in range(const.ANIMATION_STEPS):
            temp_image = sprite_sheet.subsurface(
                i * size_turret, 0, size_turret, size_height)
            animation_list.append(temp_image)
        return animation_list

    def update(self,enemy_group,world ):

        self.pick_target(enemy_group)
        if self.target:
            if pygame.time.get_ticks() - self.last_shot > (self.cooldown / world.game_speed + 2):
                self.play_animation()
        
    def upgrade(self):
        self.upgrade_level += 1
        if self.upgrade_level >= self.max_upgrade_level:
            self.upgrade_level = self.max_upgrade_level
        self.range = TURRET_DATA[self.upgrade_level - 1]["range"]
        self.cooldown = TURRET_DATA[self.upgrade_level - 1]["cooldown"]
        self.damage = TURRET_DATA[self.upgrade_level - 1]["damage"]
        
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.original_image = self.animation_list[self.frame_index]

        #upgrade range
        self.range_image = pygame.Surface((self.range * 2 ,self.range *2))
        self.range_image.fill((0,0,0))
        self.range_image.set_colorkey((0,0,0))
        pygame.draw.circle(self.range_image,'gray100',(self.range,self.range),self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center






    def play_animation(self):
        self.original_image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > const.ANIMATION_DELAY:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                self.last_shot = pygame.time.get_ticks()
                self.target = None

    def pick_target(self, enemy_group):
        x_dist = 0
        y_dist = 0

        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)

                if dist < self.range:
                    self.target = enemy
                    self.angle = 270 - math.degrees(math.atan2(enemy.pos[1] - self.y,enemy.pos[0] - self.x))
                    self.target.health -= self.damage

                    break





            


    def draw(self, surface):
        ############LINE TO ENEMY#################
        # pygame.draw.line(surface,'gray100',(self.rect.center),(enemy.pos[0],enemy.pos[1]))
        ##########################################
        self.image = pygame.transform.rotate(self.original_image,self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x + const.TILE_SIZE / 2,
                            self.y + const.TILE_SIZE/2)
        
        if self.selected:
            surface.blit(self.range_image,self.range_rect)

