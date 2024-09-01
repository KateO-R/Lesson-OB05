import pygame
import random
import sys

# Размеры окна в пикселях
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

CELL_SIZE = 20

# Размеры сетки в ячейках
WIDTH = int(WINDOW_WIDTH / CELL_SIZE)
HEIGHT = int(WINDOW_HEIGHT / CELL_SIZE)

# Цвета
BG_COLOR = (0, 0, 0)
GRID_COLOR = (40, 40, 40)
APPLE_COLOR = (255, 0, 0)
APPLE_OUTER_COLOR = (155, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SNAKE_OUTER_COLOR = (0, 155, 0)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0
FPS = 5

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def main():
    global FPS_CLOCK
    global DISPLAY

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Wormy')

    while True:
        run_game()

def run_game():
    apple = Cell(20, 10)
    snake = [Cell(3, 10), Cell(4, 10), Cell(5, 10)]
    direction = RIGHT

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                new_direction = get_direction(event, direction)
                if new_direction:
                    direction = new_direction

            if snake_hit_edge(snake) or snake_hit_self(snake):
                return

        if snake_hit_apple(snake, apple):
            snake_grow(snake)
            apple = new_apple(snake)
        else:
            move_snake(snake, direction)

        draw_frame(snake, apple)
        FPS_CLOCK.tick(FPS)

def draw_frame(snake, apple):
    DISPLAY.fill(BG_COLOR)
    draw_grid()
    draw_snake(snake)
    draw_apple(apple)
    pygame.display.update()

def draw_grid():
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(DISPLAY, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(DISPLAY, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))

def draw_apple(apple):
    draw_cell(apple, APPLE_OUTER_COLOR, APPLE_COLOR)

def draw_snake(snake):
    for cell in snake:
        draw_cell(cell, SNAKE_OUTER_COLOR, SNAKE_COLOR)

def draw_cell(cell, outer_color, inner_color):
    outer_rect = pygame.Rect(cell.x * CELL_SIZE, cell.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    inner_rect = pygame.Rect(cell.x * CELL_SIZE + 4, cell.y * CELL_SIZE + 4, CELL_SIZE - 8, CELL_SIZE - 8)
    pygame.draw.rect(DISPLAY, outer_color, outer_rect)
    pygame.draw.rect(DISPLAY, inner_color, inner_rect)

def move_snake(snake, direction):
    new_head = get_snake_new_head(snake, direction)
    snake.insert(0, new_head)
    snake.pop()

def get_snake_new_head(snake, direction):
    head = snake[HEAD]
    if direction == UP:
        return Cell(head.x, head.y - 1)
    elif direction == DOWN:
        return Cell(head.x, head.y + 1)
    elif direction == LEFT:
        return Cell(head.x - 1, head.y)
    elif direction == RIGHT:
        return Cell(head.x + 1, head.y)

def snake_hit_edge(snake):
    head = snake[HEAD]
    return head.x < 0 or head.x >= WIDTH or head.y < 0 or head.y >= HEIGHT

def snake_hit_apple(snake, apple):
    return snake[HEAD].x == apple.x and snake[HEAD].y == apple.y

def snake_grow(snake):
    snake.append(snake[-1])

def new_apple(snake):
    while True:
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        new_apple = Cell(x, y)
        if new_apple not in snake:
            return new_apple

def get_direction(event, current_direction):
    if event.key == pygame.K_LEFT and current_direction != RIGHT:
        return LEFT
    elif event.key == pygame.K_RIGHT and current_direction != LEFT:
        return RIGHT
    elif event.key == pygame.K_UP and current_direction != DOWN:
        return UP
    elif event.key == pygame.K_DOWN and current_direction != UP:
        return DOWN
    return None

def snake_hit_self(snake):
    head = snake[HEAD]
    return any(head.x == cell.x and head.y == cell.y for cell in snake[1:])

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()