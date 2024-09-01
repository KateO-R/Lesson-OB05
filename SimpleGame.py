import pygame
import sys

# Инициализация Pygame
pygame.init()

# Параметры экрана и объектов
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Pong Game")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Параметры платформы
paddle_width, paddle_height = 100, 10
paddle_x = (screen_width - paddle_width) // 2
paddle_y = screen_height - 30
paddle_speed = 5

# Параметры мяча
ball_radius = 10
ball_x, ball_y = screen_width // 2, paddle_y - ball_radius
ball_speed_x, ball_speed_y = 4, -4

# Параметры кирпичей
brick_width, brick_height = 60, 20
bricks = [(x, 50) for x in range(0, screen_width, brick_width + 10)]

# Настройка FPS
clock = pygame.time.Clock()
fps = 60

# Основной игровой цикл
run = True
while run:
    # Проверка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Получение состояния клавиш
    keys = pygame.key.get_pressed()

    # Движение платформы
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width:
        paddle_x += paddle_speed

    # Движение мяча
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Столкновение с краями экрана
    if ball_x <= 0 or ball_x >= screen_width - ball_radius:
        ball_speed_x = -ball_speed_x
    if ball_y <= 0:
        ball_speed_y = -ball_speed_y
    if ball_y >= screen_height:
        # Сброс мяча
        ball_x, ball_y = screen_width // 2, paddle_y - ball_radius
        ball_speed_y = -ball_speed_y

    # Столкновение с кирпичами
    brick_rects = [pygame.Rect(brick[0], brick[1], brick_width, brick_height) for brick in bricks]
    for i, brick_rect in enumerate(brick_rects):
        if brick_rect.collidepoint(ball_x, ball_y):
            bricks.pop(i)  # Удаление кирпича
            ball_speed_y = -ball_speed_y  # Изменение направления мяча
            break  # Выход после уничтожения одного кирпича, чтобы не удалять несколько за один кадр

    if paddle_x <= ball_x <= paddle_x + paddle_width and paddle_y <= ball_y + ball_radius <= paddle_y + paddle_height:
        ball_speed_y = -ball_speed_y

        # Очистка экрана
    screen.fill(BLACK)

    # Рисование кирпичей
    for brick in bricks:
        pygame.draw.rect(screen, WHITE, pygame.Rect(brick[0], brick[1], brick_width, brick_height))

    # Рисование платформы и мяча
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height))
    pygame.draw.circle(screen, BLUE, (ball_x, ball_y), ball_radius)

    # Обновление экрана
    pygame.display.flip()

    # Контроль FPS
    clock.tick(fps)

pygame.quit()
sys.exit()