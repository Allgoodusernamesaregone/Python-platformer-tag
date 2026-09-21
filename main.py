import pygame
import sys
from pygame.locals import *


# settings
pygame.init()
screen_width = 1200
screen_height = 800
test_font = pygame.font.Font(None, 50)
tile_size = 80
clock = pygame.time.Clock()
fps = 110

screen = pygame.display.set_mode((screen_width, screen_height))
# static images
bckgrnd = pygame.image.load("assets/staticImages/windowsXpHatter.jpg")
pygame.display.set_caption("Python game")


def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, (255, 255, 255), (0, line *
                         tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line *
                         tile_size, 0), (line * tile_size, screen_height))


class Update:

    def __init__(self, wolfX, wolfY, sheepX, sheepY):
        self.game_over = False
        self.start_time = 0
        # wolf
        self.wolf_surf = pygame.image.load("assets/wolf/wolfstandKicsi.png")
        self.wolf_y_pos = wolfY
        self.wolf_x_pos = wolfX
        self.wolf_rect = self.wolf_surf.get_rect(topleft=(wolfX, wolfY))
        self.wolf_jump_count = 2
        self.wolf_gravity = 0
        self.wolf_width = self.wolf_surf.get_width()
        self.wolf_height = self.wolf_surf.get_height()
        self.wolf_lookRight = False
        self.wolf_lookLeft = True
        # sheep
        self.sheep_surf = pygame.image.load("assets/sheep/sheepStandKicsi.png")
        self.sheep_y_pos = sheepY
        self.sheep_x_pos = sheepX
        self.sheep_rect = self.sheep_surf.get_rect(topleft=(sheepX, sheepY))
        self.sheep_jump_count = 2
        self.sheep_gravity = 0
        self.sheep_width = self.sheep_surf.get_width()
        self.sheep_height = self.sheep_surf.get_height()
        self.sheep_lookRight = True
        self.sheep_lookLeft = False

    def move(self):
        move_speed_x = 0
        move_speed_y = 0
        sheep_move_speed_x = 0
        sheep_move_speed_y = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            move_speed_x += 2
            if self.wolf_lookRight == False:
                self.wolf_surf = pygame.transform.flip(
                    self.wolf_surf, True, False)
                self.wolf_lookRight = True
                self.wolf_lookLeft = False
        if key[pygame.K_a]:
            move_speed_x -= 2
            if self.wolf_lookLeft == False:
                self.wolf_surf = pygame.transform.flip(
                    self.wolf_surf, True, False)
                self.wolf_lookLeft = True
                self.wolf_lookRight = False

        if key[pygame.K_RIGHT]:
            sheep_move_speed_x += 2
            if self.sheep_lookRight == False:
                self.sheep_surf = pygame.transform.flip(
                    self.sheep_surf, True, False)
                self.sheep_lookRight = True
                self.sheep_lookLeft = False
        if key[pygame.K_LEFT]:
            sheep_move_speed_x -= 2
            if self.sheep_lookLeft == False:
                self.sheep_surf = pygame.transform.flip(
                    self.sheep_surf, True, False)
                self.sheep_lookLeft = True
                self.sheep_lookRight = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    if self.wolf_jump_count >= 1:
                        self.wolf_jump_count -= 1
                        self.wolf_gravity = -7

                    # after game-end
                if event.key == pygame.K_RSHIFT:
                    if self.game_over == True:
                        self.game_over = False
                        self.wolf_rect.x = 0
                        self.wolf_rect.y = 200
                        self.sheep_rect.x = 950
                        self.sheep_rect.y = 0
                        self.start_time = int(pygame.time.get_ticks() / 1000)
                        self.wolf_gravity = 0

                if event.key == pygame.K_UP:
                    if self.sheep_jump_count >= 1:
                        self.sheep_jump_count -= 1
                        self.sheep_gravity = -7

        # gravity
        self.wolf_gravity += 0.2
        if self.wolf_gravity > 10:
            self.wolf_gravity = 10
        move_speed_y += self.wolf_gravity

        self.sheep_gravity += 0.2
        if self.sheep_gravity > 10:
            self.sheep_gravity = 10
        sheep_move_speed_y += self.sheep_gravity

        # edges
        if self.wolf_rect.top <= 0:
            self.wolf_rect.top = 0
            self.wolf_gravity += 1
        if self.sheep_rect.top <= 0:
            self.sheep_rect.top = 0
            self.sheep_gravity += 1

        if self.wolf_rect.bottom >= screen_height:
            self.wolf_rect.bottom = screen_height
            self.wolf_jump_count = 2
        if self.sheep_rect.bottom >= screen_height:
            self.sheep_rect.bottom = screen_height
            self.sheep_jump_count = 2

        if self.wolf_rect.right > screen_width:
            self.wolf_rect.right = screen_width
        elif self.wolf_rect.x < 0:
            self.wolf_rect.x = 0
        if self.sheep_rect.right > screen_width:
            self.sheep_rect.right = screen_width
        elif self.sheep_rect.x < 0:
            self.sheep_rect.x = 0

        # collision
            # with wolf
        if self.wolf_rect.colliderect(self.sheep_rect.x + sheep_move_speed_x, self.sheep_rect.y, self.sheep_width, self.sheep_height):
            sheep_move_speed_x = 0
            self.game_over = True
        elif self.wolf_rect.colliderect(self.sheep_rect.x, self.sheep_rect.y + sheep_move_speed_y, self.sheep_width, self.sheep_height):
            if self.sheep_gravity >= 0:
                sheep_move_speed_y = self.wolf_rect.top - \
                    self.sheep_rect.bottom
            elif self.sheep_gravity <= 0:
                sheep_move_speed_y = self.wolf_rect.bottom - self.sheep_rect.top
            # with platforms
        for world.img_rect in world.floor_list:
            if world.img_rect[1].colliderect(self.wolf_rect.x + move_speed_x, self.wolf_rect.y, self.wolf_width, self.wolf_height):
                pygame.draw.rect(
                    screen, "Pink", world.img_rect[1], 2)
                move_speed_x = 0
            elif world.img_rect[1].colliderect(self.wolf_rect.x, self.wolf_rect.y + move_speed_y, self.wolf_width, self.wolf_height):
                pygame.draw.rect(
                    screen, "Pink", world.img_rect[1], 2)
                if self.wolf_gravity < 0:
                    move_speed_y = world.img_rect[1].bottom - \
                        self.wolf_rect.top
                    self.wolf_gravity = 0
                elif self.wolf_gravity >= 0:
                    move_speed_y = world.img_rect[1].top - \
                        self.wolf_rect.bottom
                    self.wolf_jump_count = 2

        for world.img_rect in world.floor_list:
            if world.img_rect[1].colliderect(self.sheep_rect.x + sheep_move_speed_x, self.sheep_rect.y, self.sheep_width, self.sheep_height):
                pygame.draw.rect(
                    screen, "Pink", world.img_rect[1], 2)
                sheep_move_speed_x = 0
            elif world.img_rect[1].colliderect(self.sheep_rect.x, self.sheep_rect.y + sheep_move_speed_y, self.sheep_width, self.sheep_height):
                pygame.draw.rect(
                    screen, "Pink", world.img_rect[1], 2)
                if self.sheep_gravity <= 0:
                    sheep_move_speed_y = world.img_rect[1].bottom - \
                        self.sheep_rect.top
                    self.sheep_gravity = 0
                elif self.sheep_gravity >= 0:
                    sheep_move_speed_y = world.img_rect[1].top - \
                        self.sheep_rect.bottom
                    self.sheep_jump_count = 2
            # with bouncepad
        for world.img_rect in world.bounce_lst:
            if world.img_rect[1].colliderect(self.wolf_rect.x + move_speed_x, self.wolf_rect.y, self.wolf_width, self.wolf_height):
                pygame.draw.rect(
                    screen, "Blue", world.img_rect[1], 2)
                move_speed_x = 0
            elif world.img_rect[1].colliderect(self.wolf_rect.x, self.wolf_rect.y + move_speed_y, self.wolf_width, self.wolf_height):
                pygame.draw.rect(
                    screen, "Blue", world.img_rect[1], 2)
                if self.wolf_gravity < 0:
                    move_speed_y = world.img_rect[1].bottom - \
                        self.wolf_rect.top
                    self.wolf_gravity = 0
                elif self.wolf_gravity >= 0:
                    move_speed_y = world.img_rect[1].top - \
                        self.wolf_rect.bottom
                    self.wolf_jump_count = 1
                    self.wolf_gravity = -15

        for world.img_rect in world.bounce_lst:
            if world.img_rect[1].colliderect(self.sheep_rect.x + sheep_move_speed_x, self.sheep_rect.y, self.sheep_width, self.sheep_height):
                pygame.draw.rect(
                    screen, "Blue", world.img_rect[1], 2)
                sheep_move_speed_x = 0
            elif world.img_rect[1].colliderect(self.sheep_rect.x, self.sheep_rect.y + sheep_move_speed_y, self.sheep_width, self.sheep_height):
                pygame.draw.rect(
                    screen, "Blue", world.img_rect[1], 2)
                if self.sheep_gravity <= 0:
                    sheep_move_speed_y = world.img_rect[1].bottom - \
                        self.sheep_rect.top

                    self.sheep_gravity = 0
                elif self.sheep_gravity >= 0:
                    sheep_move_speed_y = world.img_rect[1].top - \
                        self.sheep_rect.bottom
                    self.sheep_jump_count = 1
                    self.sheep_gravity = -15

        self.wolf_rect.x += move_speed_x
        self.wolf_rect.y += move_speed_y
        self.sheep_rect.x += sheep_move_speed_x
        self.sheep_rect.y += sheep_move_speed_y

        screen.blit(self.sheep_surf, self.sheep_rect)
        screen.blit(self.wolf_surf, self.wolf_rect)
        #pygame.draw.rect(screen, "Black", self.sheep_rect, 4)

        current_time = int((pygame.time.get_ticks() / 1000)) - self.start_time
        time_surf = test_font.render(F" Time: {current_time}", False, "Black")
        screen.blit(time_surf, (0, 0))
        if current_time > 30:
            winner = "The Sheep"
        else:
            winner = "The Wolf"
        win_surf = test_font.render(f"The winner is: {winner}", True, "White")

        # game status

        if self.game_over:
            felirat_surf = test_font.render(
                "Press 'R-SHIFT' to restart", True, "White")
            felirat_length = felirat_surf.get_width()
            screen.fill((94, 129, 162))
            screen.blit(felirat_surf, ((screen_width/2) -
                        felirat_length, screen_height/2))
            screen.blit(win_surf, (200, 300))


class World:
    def __init__(self, map):

        self.floor_list = []
        self.bounce_lst = []

        # load images
        self.dirt_img = pygame.image.load('assets/staticImages/dirt.png')
        self.bouncepad_img = pygame.image.load("assets/staticImages/bouncepad.png")

        row_count = 0
        for row in map:
            col_count = 0
            for tile in row:
                # render images
                if tile == 1:
                    img = pygame.transform.scale(
                        self.dirt_img, (tile_size, tile_size))
                    self.img_rect = img.get_rect()
                    self.img_rect.x = col_count * tile_size
                    self.img_rect.y = row_count * tile_size
                    element = (img, self.img_rect)
                    self.floor_list.append(element)
                if tile == 2:
                    img = pygame.transform.scale(
                        self.bouncepad_img, (tile_size, tile_size)
                    )
                    self.img_rect = img.get_rect()
                    self.img_rect.x = col_count * tile_size
                    self.img_rect.y = row_count * tile_size
                    element = (img, self.img_rect)
                    self.bounce_lst.append(element)

                col_count += 1
            row_count += 1

    def draw(self):
        screen.blit(bckgrnd, (0, 0))

        for tile in self.floor_list:
            screen.blit(tile[0], tile[1])
        for tile in self.bounce_lst:
            screen.blit(tile[0], tile[1])


# player
update = Update(0, 200,  950, 0)


# map

world_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    [2, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1]

]
world = World(world_map)


while True:

    world.draw()

    clock.tick(fps)

    update.move()
    # draw_grid()
    pygame.display.update()
