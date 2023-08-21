from random import randint
from sys import exit
import pygame
from datetime import datetime

# Game Settings - Change them to change gameplay!
jump_height = 18
gravity = 1.25
enemy_count = 1
min_s, max_s = 12, 15

# Initialisation
pygame.init()


class Enemy:
    def __init__(self, x, y, colour, enemy_speed):
        self.x = x
        self.y = y
        self.colour = colour
        self.speed = enemy_speed
        self.alive = True
        self.dist = self.x - 50

        self.enemy_surf = pygame.Surface((35, 35))
        self.enemy_rect = self.enemy_surf.get_rect(topleft=(self.x, self.y))
        self.enemy_surf.fill(colour)

    def update(self):
        self.x -= self.speed
        self.enemy_rect = self.enemy_surf.get_rect(topleft=(self.x, self.y))

        if self.x < -35:
            self.alive = False

        self.dist = self.x - 50
        screen.blit(self.enemy_surf, (self.x, self.y))


def check_auto():
    nearest = 999999
    # nearest_en = None
    classified = []
    for en in enemy_list:
        if en.dist < nearest:
            nearest = en.dist
            # nearest_en = en

        if en.y == player_y:
            classified.append("same")

        elif en.y < player_y:
            classified.append("higher")

        else:
            classified.append("lower")

    if nearest < 120:
        if "same" in classified or "lower" in classified:
            return True


def update_enemies(enemies: list):
    for obj in enemies:
        obj.update()


def check_collide_enemies(enemies: list):
    for en in enemies:
        en_rect = en.enemy_surf.get_rect(topleft=(en.x, en.y))
        if player_rect.colliderect(en_rect):
            pygame.quit()
            print(score)
            exit()


def create_enemies(enemy_num: int):
    if enemy_num <= 0:
        return []

    enemy_objects = []
    for en in range(enemy_num):
        en_choice = randint(1, 3)
        if en_choice == 1:
            enemy_objects.append(Enemy(randint(800, 1000), 265, "#361919", randint(min_s, max_s)))

        elif en_choice == 2:
            enemy_objects.append(Enemy(randint(800, 1000), 200, "#361919", randint(min_s, max_s)))

        else:
            enemy_objects.append(Enemy(randint(800, 1000), 299, "#361919", randint(min_s, max_s)))

    return enemy_objects


def strip_list(lis: list):
    new_lis = []
    for i in lis:
        if i != 0:
            new_lis.append(i)

    return new_lis


def check_delete_enemies():
    global enemy_list

    for n in range(len(enemy_list)):
        if not enemy_list[n].alive:
            if len(enemy_list) >= 3:
                # print(f"{len(enemy_list)}: take away")
                increment = randint(0, 1)
            else:
                # print(f"{len(enemy_list)} let it stay")
                increment = randint(1, 2)

            enemy_list += create_enemies(increment)
            enemy_list[n] = 0

    enemy_list = strip_list(enemy_list)


# Game start
enemy_list = create_enemies(enemy_count)

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Glitch Runner")
clock = pygame.time.Clock()

font = pygame.font.Font("Pixeltype.ttf", 50)
score = -1
pre_time = 0
score_surf = font.render(f"Score: {score}", False, "black")

sky = pygame.Surface((800, 400))
sky.fill("#a1f0d3")

player = pygame.Surface((35, 35))
player.fill("#6047ff")

jump = 0
player_y = 265
avail = True
auto = False

ground = pygame.Surface((800, 200))
ground.fill("#4bf542")

while True:
    if check_auto() and avail and auto:
        jump = jump_height
        avail = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            print(score)
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w:
                if avail and not auto:
                    jump = jump_height
                    avail = False

            if event.key == pygame.K_a:
                if auto:
                    auto = False
                    player.fill("#6047ff")

                else:
                    auto = True
                    player.fill("#a917e8")

    if not avail:
        player_y -= jump
        jump -= gravity

        if player_y > 265:
            player_y = 265
            jump = 0
            avail = True

    keys = pygame.key.get_pressed()
    player_rect = player.get_rect(topleft=(50, player_y))
    if keys[pygame.K_DOWN]:
        player = pygame.Surface()
    score_surf = font.render(f"Score: {score}", False, "black")

    cur_time = int(datetime.now().strftime("%S"))
    if cur_time != pre_time:
        score += 1
        pre_time = cur_time

    screen.blit(sky, (0, 0))
    screen.blit(player, (50, player_y))
    screen.blit(ground, (0, 300))
    screen.blit(score_surf, ((screen.get_width() / 2) - (score_surf.get_width() / 2), 50))
    update_enemies(enemy_list)

    pygame.display.update()

    check_collide_enemies(enemy_list)
    check_delete_enemies()

    clock.tick(60)
