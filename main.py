import copy
import math

import numpy
import pygame

pygame.font.init()

WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conways Game of Life")

RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WORLD_SIZE = 200
DELAY = 300
FONT_SIZE = 30
PHASE_FONT = pygame.font.SysFont('comicsans', FONT_SIZE)
ZOOM_LEVELS = [5, 10, 20, 25, 40]


def get_neighbors(world, row, col):  # Gets the amount of neighbors for a given place.
    neighbors = 0
    max_row = 2
    max_col = 2
    min_row = -1
    min_col = -1

    if row > len(world) - 2:
        max_row = 1
    if col > len(world) - 2:
        max_col = 1

    if row == 0:
        min_row = 0
    if col == 0:
        min_col = 0

    for i in range(min_row, max_row):
        for k in range(min_col, max_col):
            if i == 0 and k == 0:
                continue
            elif world[i + row][k + col] == 1:
                neighbors += 1
    return neighbors


def update_world(world):
    new_world = copy.deepcopy(world)
    for i in range(len(world)):
        for k in range(len(world)):
            if get_neighbors(world, i, k) == 3:
                new_world[i][k] = 1
            elif get_neighbors(world, i, k) < 2 or get_neighbors(world, i, k) > 3:
                new_world[i][k] = 0
    return new_world


def draw_world(win, world, offset_x, offset_y, square_size, play_phase):
    win.fill(WHITE)
    square_x = 0
    square_y = 0
    for y in range(offset_y, offset_y + int(WIDTH / square_size)):
        for x in range(offset_x, offset_x + int(HEIGHT / square_size)):
            if world[y][x] == 1:
                color = RED
            else:
                color = BLACK
            rect = pygame.Rect(square_x, square_y, square_size - 1, square_size - 1)
            pygame.draw.rect(win, color, rect)
            square_x += square_size
        square_x = 0
        square_y += square_size
    pygame.draw.rect(WIN, BLACK, pygame.Rect(0, HEIGHT - 20, 75, 22))
    if play_phase:
        font = PHASE_FONT.render("Playing", 1, RED)
    else:
        font = PHASE_FONT.render("Paused", 1, BLUE)
    WIN.blit(font, (0, HEIGHT - 20))
    pygame.display.update()


def main():
    world = numpy.empty((WORLD_SIZE, WORLD_SIZE))
    square_size = 10
    zoom_level = 1
    run = True  # Variables to control the state of the game.
    play_phase = False
    offset_x = 0
    offset_y = 0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # Checks if program har been quit.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cursor_pos = pygame.mouse.get_pos()
                cursor_pos_x = math.floor((cursor_pos[0] + offset_x * square_size) / square_size)
                cursor_pos_y = math.floor((cursor_pos[1] + offset_y * square_size) / square_size)
                world[cursor_pos_y][cursor_pos_x] += 1
                world[cursor_pos_y][
                    cursor_pos_x] %= 2  # Swaps between 1 and 0. This swaps between dead and alive cells.
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if play_phase:
                        play_phase = False
                    else:
                        play_phase = True
                if event.key == pygame.K_LEFT and offset_x > 0:  # Allows for movement of the camera.
                    offset_x -= 1
                if event.key == pygame.K_RIGHT and offset_x < WORLD_SIZE - WIDTH / square_size:
                    offset_x += 1
                if event.key == pygame.K_UP and offset_y > 0:
                    offset_y -= 1
                if event.key == pygame.K_DOWN and offset_y < WORLD_SIZE - HEIGHT / square_size:
                    offset_y += 1
                if event.key == pygame.K_z and zoom_level > 0:  # Allows the player to zoom.
                    zoom_level -= 1
                    square_size = ZOOM_LEVELS[zoom_level]
                if event.key == pygame.K_x and zoom_level < 4:
                    zoom_level += 1
                    square_size = ZOOM_LEVELS[zoom_level]

        draw_world(WIN, world, offset_x, offset_y, square_size, play_phase)
        if play_phase:
            world = update_world(world)
            pygame.time.delay(DELAY)
    pygame.quit()


if __name__ == "__main__":
    main()
