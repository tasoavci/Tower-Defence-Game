import pygame
import json
from enemy import Enemy
from turret import Turret
from world import World
from button import Button
import constants as const


# initialise game
pygame.init()

# create clock
clock = pygame.time.Clock()


# game window
screen = pygame.display.set_mode(
    (const.WIDTH + const.SIDE_PANEL, const.HEIGHT))
pygame.display.set_caption(const.CAPTION_TEXT)

# variables
game_over = False
game_outcome = 0
level_started = False
place_turret = False
selected_turret = None
last_enemy_spawn = pygame.time.get_ticks()
money_color = "black"


# load images
map_image = pygame.transform.scale(pygame.image.load(
    'assets/tiles/map.png'), (const.WIDTH, const.HEIGHT))

coin_image = pygame.image.load(
    'assets/gui/coin.png')
heart_image = pygame.image.load(
    'assets/gui/heart.png')


enemy_images = {
    "easy": pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
        'assets/enemies/yellow_enemy_easy.png'), (40, 40)), -90),
    "medium": pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
        'assets/enemies/orange_enemy_medium.png'), (50, 50)), -90),
    "hard": pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
        'assets/enemies/red_enemy_hard.png'), (60, 60)), -90),
    "boss": pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
        'assets/enemies/purple_enemy_boss.png'), (70, 70)), -90)

}

# TURRET THINGS #
turret_sheets_list = []
for i in range(1, const.TURRET_LEVEL + 1):
    turret_sheet = pygame.transform.scale(pygame.image.load(
        f"assets/turrets/turret_{i}.png"), (800, 100))
    turret_sheets_list.append(turret_sheet)

cursor_turret = pygame.transform.scale(pygame.image.load(
    "assets/turrets/cursor_turret.png"), (100, 100))

# button images
buy_turret_image = pygame.transform.scale(pygame.image.load(
    "assets/buttons/buy_turret.png"), (140, 50))
cancel_image = pygame.transform.scale(pygame.image.load(
    "assets/buttons/cancel.png"), (110, 50))
begin_image = pygame.transform.scale(pygame.image.load(
    "assets/buttons/begin.png"), (50, 50))
fast_forward_image = pygame.transform.scale(pygame.image.load(
    "assets/buttons/fast_forward.png"), (50, 50))
restart_image = pygame.transform.scale(pygame.image.load(
    "assets/buttons/restart.png"), (50, 50))
upgrade_turret_image = pygame.transform.scale(pygame.image.load(
    "assets/buttons/upgrade_turret.png"), (250, 50))
sell_turret_image = pygame.transform.scale(pygame.image.load(
    "assets/buttons/sell_turret.png"), (200, 50))


with open("level/level.tmj") as file:
    world_data = json.load(file)
small_font = pygame.font.SysFont("Consolas", 18, bold=True)
text_font = pygame.font.SysFont("Consolas", 24, bold=True)
large_font = pygame.font.SysFont("Consolas", 36)


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


# create groups
enemy_group = pygame.sprite.Group()
turret_group = pygame.sprite.Group()

world = World(world_data, map_image)
world.draw(screen)
world.handle_data()
world.handle_enemies()


buy_turret_button = Button(const.WIDTH + 15, 80, buy_turret_image, True)
cancel_button = Button(const.WIDTH + 180, 80, cancel_image, False)
upgrade_button = Button(const.WIDTH + 25, 210, upgrade_turret_image, True)
begin_button = Button(const.WIDTH + 37.5, 145, begin_image, True)
fast_forward_button = Button(const.WIDTH + 125, 145, fast_forward_image, False)
restart_button = Button(const.WIDTH + 212.5, 145, restart_image, True)
sell_turret_button = Button(const.WIDTH + 50, 280, sell_turret_image, True)


run = True


def create_turret(mouse_position):

    mouse_tile_x = mouse_position[0] // const.TILE_SIZE
    mouse_tile_y = mouse_position[1] // const.TILE_SIZE
    mouse_tile_num = (mouse_tile_y * const.ROWS) + mouse_tile_x

    if world.tile_map[mouse_tile_num] == 127:
        is_space_free = True

        for turret in turret_group:

            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x_pos, turret.tile_y_pos):
                is_space_free = False

        if is_space_free:

            new_turret = Turret(turret_sheets_list, mouse_tile_x,
                                mouse_tile_y)
            turret_group.add(new_turret)
            world.money -= const.BUY_COST


def select_turret(mouse_position):
    mouse_tile_x = mouse_position[0] // const.TILE_SIZE
    mouse_tile_y = mouse_position[1] // const.TILE_SIZE

    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x_pos, turret.tile_y_pos):
            return turret


def clear_selection():
    for turret in turret_group:
        turret.selected = False


while run:
    clock.tick(const.FPS)

    screen.fill('gray100')

    screen.blit(map_image, (0, 0))

    # ENEMY PATH LINE
    # pygame.draw.lines(screen, 'gray100', False, world.waypoints)
    if game_over == False:
        if world.health <= 0:
            game_over = True
            game_outcome = -1  # loss
        if world.level > const.TOTAL_LEVELS:
            game_over = True
            game_outcome = 1  # win
            world.level = const.TOTAL_LEVELS

    ###################
    # UPDATE SECTION
    ###################
        enemy_group.update(world)
        for turret in turret_group:
            turret.draw(screen)
            turret.update(enemy_group, world)

        if selected_turret:
            selected_turret.selected = True

    ###################
    # DRAW SECTION
    ###################
    ###################
    screen.blit(coin_image, (const.WIDTH + 15, 15))
    screen.blit(heart_image, (const.WIDTH + 165, 15))

    # draw group
    enemy_group.draw(screen)
    turret_group.draw(screen)
    if world.money < const.BUY_COST and world.money < const.UPGRADE_COST:
        money_color = "red"
    else:
        money_color = "black"

    draw_text(str(world.health), text_font, "black", const.WIDTH + 200, 20)
    draw_text(str(world.money), text_font, money_color, const.WIDTH + 50, 20)
    draw_text(f"Wave: {world.level}/{const.TOTAL_LEVELS}", large_font,
              "black", const.WIDTH + 40, 400)
    draw_text(f"Turret Price: {const.BUY_COST} coins",
              small_font, "black", const.WIDTH + 20, 500)
    draw_text(f"Sell Price: {const.SELL_PRICE} coins",
              small_font, "black", const.WIDTH + 20, 550)
    draw_text(f"Upgrade Cost: {const.UPGRADE_COST} coins",
              small_font, "black", const.WIDTH + 20, 600)
    if game_over == False:
        if level_started == False:
            if begin_button.draw(screen):
                level_started = True
        else:
            world.game_speed = 1
            if fast_forward_button.draw(screen):
                world.game_speed = 2
                print(world.game_speed)
            if pygame.time.get_ticks() - last_enemy_spawn > const.SPAWN_COOLDOWN:
                if world.spawned_enemies < len(world.enemy_list):
                    enemy_type = world.enemy_list[world.spawned_enemies]
                    enemy = Enemy(enemy_type, world.waypoints, enemy_images)
                    enemy_group.add(enemy)
                    world.spawned_enemies += 1
                    last_enemy_spawn = pygame.time.get_ticks()
        if world.check_level_complete() == True:
            world.level += 1
            level_started = False
            last_enemy_spawn = pygame.time.get_ticks()
            world.reset_level()
            world.handle_enemies()

        if buy_turret_button.draw(screen):
            place_turret = True

        if place_turret:
            cursor_rect = cursor_turret.get_rect()
            cursor_pos = pygame.mouse.get_pos()
            cursor_rect.center = cursor_pos
            if cursor_pos[0] <= const.WIDTH:
                screen.blit(cursor_turret, cursor_rect)

        if cancel_button.draw(screen):
            place_turret = False

        if fast_forward_button.draw(screen):
            pass

        if restart_button.draw(screen):
            pass

        if selected_turret:
            if sell_turret_button.draw(screen):
                world.money += const.SELL_PRICE
                selected_turret.kill()
            if selected_turret.upgrade_level < const.TURRET_LEVEL:
                if upgrade_button.draw(screen):
                    if world.money >= const.UPGRADE_COST:
                        world.money -= const.UPGRADE_COST
                        selected_turret.upgrade()
    else:

        pygame.draw.rect(screen, "yellow", (200, 200,
                         400, 200), border_radius=20)
        if game_outcome == -1:
            draw_text("GAME OVER", large_font, "black", 310, 280)
        if game_outcome == 1:
            draw_text("YOU WIN!", large_font, "black", 315, 280)
            world.level = const.TOTAL_LEVELS
        if restart_button.draw(screen):
            game_over = False
            level_started = False
            place_turret = False
            selected_turret = None
            last_enemy_spawn = pygame.time.get_ticks()

            # RECREATE THE WORLD
            world = World(world_data, map_image)
            world.draw(screen)
            world.handle_data()
            world.handle_enemies()

            # empty groups
            enemy_group.empty()
            turret_group.empty()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_position = pygame.mouse.get_pos()
            if mouse_position[0] < const.WIDTH and mouse_position[1] < const.HEIGHT:
                selected_turret = None
                clear_selection()
                if place_turret == True:
                    if world.money >= const.BUY_COST:
                        create_turret(mouse_position)
                        place_turret = False
                else:
                    selected_turret = select_turret(mouse_position)

    pygame.display.update()

pygame.quit()
