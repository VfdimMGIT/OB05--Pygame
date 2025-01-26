import pygame
import sys

# Инициализация Pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-Понг")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Параметры ракеток
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 5

# Параметры мяча
BALL_SIZE = 20
BALL_SPEED_X, BALL_SPEED_Y = 4, 4

# Шрифты
font = pygame.font.Font(None, 50)
menu_font = pygame.font.Font(None, 74)

# Состояния игры
MENU = 0
SINGLE_PLAYER = 1
TWO_PLAYERS = 2
current_state = MENU

# Создание ракеток
paddle1 = pygame.Rect(30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle2 = pygame.Rect(WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Создание мяча
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Направление мяча
ball_dx, ball_dy = BALL_SPEED_X, BALL_SPEED_Y

# Счет игроков
score1, score2 = 0, 0

# Функция для отрисовки текста
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Функция для отрисовки меню
def draw_menu():
    screen.fill(BLACK)
    draw_text("Пинг-Понг", menu_font, WHITE, WIDTH // 2, HEIGHT // 4)
    draw_text("1. Один игрок", font, WHITE, WIDTH // 2, HEIGHT // 2)
    draw_text("2. Два игрока", font, WHITE, WIDTH // 2, HEIGHT // 2 + 50)
    pygame.display.flip()

# Функция для сброса игры
def reset_game():
    global ball_dx, ball_dy, score1, score2
    ball.x, ball.y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2
    ball_dx, ball_dy = BALL_SPEED_X, BALL_SPEED_Y
    score1, score2 = 0, 0

# Основной игровой цикл
clock = pygame.time.Clock()
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if current_state == MENU:
                if event.key == pygame.K_1:
                    current_state = SINGLE_PLAYER
                    reset_game()
                if event.key == pygame.K_2:
                    current_state = TWO_PLAYERS
                    reset_game()

    # Логика игры
    if current_state in [SINGLE_PLAYER, TWO_PLAYERS]:
        # Управление ракетками
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddle1.top > 0:
            paddle1.y -= PADDLE_SPEED
        if keys[pygame.K_s] and paddle1.bottom < HEIGHT:
            paddle1.y += PADDLE_SPEED
        if current_state == TWO_PLAYERS:
            if keys[pygame.K_UP] and paddle2.top > 0:
                paddle2.y -= PADDLE_SPEED
            if keys[pygame.K_DOWN] and paddle2.bottom < HEIGHT:
                paddle2.y += PADDLE_SPEED
        else:
            # Логика для ракетки компьютера
            if paddle2.centery < ball.centery and paddle2.bottom < HEIGHT:
                paddle2.y += PADDLE_SPEED
            if paddle2.centery > ball.centery and paddle2.top > 0:
                paddle2.y -= PADDLE_SPEED

        # Движение мяча
        ball.x += ball_dx
        ball.y += ball_dy

        # Отскок мяча от верхней и нижней границ
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_dy *= -1

        # Отскок мяча от ракеток
        if ball.colliderect(paddle1) or ball.colliderect(paddle2):
            ball_dx *= -1

        # Проверка на выход мяча за пределы экрана
        if ball.left <= 0:
            score2 += 1
            ball.x, ball.y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2
            ball_dx, ball_dy = BALL_SPEED_X, BALL_SPEED_Y
        if ball.right >= WIDTH:
            score1 += 1
            ball.x, ball.y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2
            ball_dx, ball_dy = BALL_SPEED_X, BALL_SPEED_Y

        # Отрисовка объектов
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, paddle1)
        pygame.draw.rect(screen, WHITE, paddle2)
        pygame.draw.ellipse(screen, RED, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Отображение счета
        draw_text(f"{score1} : {score2}", font, WHITE, WIDTH // 2, 20)

        # Обновление экрана
        pygame.display.flip()

    # Если игра в меню
    elif current_state == MENU:
        draw_menu()

    # Ограничение FPS
    clock.tick(60)

# Завершение игры
pygame.quit()
sys.exit()