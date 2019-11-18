import pygame
import random
import Blocks

pygame.font.init()

s_width = 800
s_height = 750
play_width = 300
play_height = 700
block_size = 30
 
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

shapes = Blocks.shapes
shape_colors = Blocks.shape_colors
 
 
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if(j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():
    global shapes, shape_colors

    return Piece(5, 2, random.choice(shapes))
 
 
def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('Poppins', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label,
                 (top_left_x + play_width / 2 - (label.get_width()/2),
                  top_left_y + play_height/2 - 50 - label.get_height()/2))


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid) - 1):
        i += 1
        pygame.draw.line(surface, (36, 36, 36), (sx, sy + i * block_size), (sx+play_width, sy + i * block_size))
        for j in range(len(grid[i]) - 1):
            j += 1
            pygame.draw.line(surface, (36, 36, 36), (sx + j * block_size, sy), (sx + j * block_size, sy + play_height - 100))


def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if(0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key = lambda x: x[1]) [::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('Poppins', 30)
    label = font.render('Next', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 75
    format = shape.shape[shape.rotation % len(shape.shape)]
    pygame.draw.rect(surface, (30, 30, 30), (sx, sy - 200, 5 * block_size, 5 * block_size), 0)

    (r, g, b) = shape.color
    brighter = (r + 30, g + 30, b + 30)
    darker = (abs(r - 30), abs(g - 30), abs(b - 30))

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                make_rectangle(surface, sx + j*block_size, sy + i*block_size + (block_size/2) - 200, shape.color)

    surface.blit(label, (sx + 50, sy - 230))


def update_score(nscore):
    score = max_score()
    if(nscore == 0): return
    with open('scores.txt', 'w') as f:
        if int(score) < nscore:
            f.write(str(nscore))


def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    return score


def make_rectangle(surface, x, y, color):
    (r, g, b) = color
    brighter = (r + 30, g + 30, b + 30)
    darker = (abs(r - 30), abs(g - 30), abs(b - 30))
    pygame.draw.rect(surface, brighter, (x, y, block_size - 1, block_size - 1), 0)
    pygame.draw.rect(surface, darker, (x + 3, y + 3, block_size - 1 - 3, block_size - 1 - 3), 0)
    pygame.draw.rect(surface, color, (x + 3, y + 3, block_size - 1 - 6, block_size - 1 - 6), 0)


def draw_window(surface, grid, score=0, last_score=0):
    surface.fill((0, 0, 0))
    sx = 50
    sy = top_left_y + play_height / 2

    font = pygame.font.SysFont('Poppins', 60)
    label = font.render('Python Tetris!', 1, (255, 255, 255))
    surface.blit(label, (0, sy - 400))

    font = pygame.font.SysFont('Poppins', 30)
    label = font.render('Curr Score: ' + str(score), 1, (255, 255, 255))

    surface.blit(label, (sx + 10, sy - 275))

    label = font.render('High Score: ' + last_score, 1, (255, 255, 255))

    surface.blit(label, (sx + 10, sy - 175))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            (r, g, b) = grid[i][j]
            if r != 0 or g != 0 or b != 0:
                make_rectangle(surface, top_left_x + j * block_size, top_left_y + i * block_size, grid[i][j])
            else:
                pygame.draw.rect(surface, grid[i][j], (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255,255,255), (top_left_x - 3, top_left_y - 3, play_width + 8, play_height + 8 - 100), 5)

    draw_grid(surface, grid)


def main(win):
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = .27
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                level_time -= 0.009

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    print("spacebar pressed")
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.display.quit()
                if event.key == pygame.K_SPACE:
                    print("spacebar pressed")
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1

        shape_pos = convert_shape_format(current_piece)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            number_cleared = clear_rows(grid, locked_positions)
            score += number_cleared * number_cleared * 10

        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            update_score(score)
            draw_text_middle("YOU LOST", 80, (255,255,255), win)
            pygame.display.update()
            pygame.time.delay(1500)
            run = False

 
def main_menu(win):
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle('Press Any Key To Play', 60, (255,255,255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)  # start game