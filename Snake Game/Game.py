import pygame
import random
import os

pygame.init()
pygame.display.set_caption("Snake Game")  # Título da janela
width, height = 800, 600
screen = pygame.display.set_mode((width, height))  # Janela do jogo
clock = pygame.time.Clock()

# Cores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Parâmetros
square_size = 20
font = pygame.font.SysFont("Helvetica", 35)
high_score_file = "high_score.txt"

# Função para desenhar texto na tela
def draw_text(text, color, x, y):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Função para carregar a pontuação mais alta
def load_high_score():
    if os.path.exists(high_score_file):
        with open(high_score_file, "r") as file:
            return int(file.read())
    return 0

# Função para salvar a pontuação mais alta
def save_high_score(score):
    with open(high_score_file, "w") as file:
        file.write(str(score))

# Tela do menu
def menu():
    running = True
    while running:
        screen.fill(black)
        draw_text("Snake Game", white, width // 2 - 100, height // 2 - 100)
        draw_text("Press ENTER to Start", green, width // 2 - 150, height // 2)
        draw_text("Press ESC to Quit", red, width // 2 - 150, height // 2 + 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Inicia o jogo ao pressionar Enter
                    return  # Sai do menu e inicia o jogo
                elif event.key == pygame.K_ESCAPE:  # Encerra o programa com ESC
                    pygame.quit()
                    exit()

# Função para gerar comida
def generate_food():
    return (random.randint(0, (width - square_size) // square_size) * square_size,
            random.randint(0, (height - square_size) // square_size) * square_size)

# Função para gerar obstáculos
def generate_obstacles(level):
    obstacles = []
    for _ in range(level * 5):  # Aumenta o número de obstáculos com o nível
        obstacles.append((random.randint(0, (width - square_size) // square_size) * square_size,
                          random.randint(0, (height - square_size) // square_size) * square_size))
    return obstacles

def game():
    running = True
    x, y = width // 2, height // 2
    x_speed, y_speed = square_size, 0  # Inicializa a velocidade para mover a cobra para a direita
    snake = [(x, y)]
    food = generate_food()
    snake_length = 1
    level = 1
    goal = 5  # Número de comidas por nível
    speed = 10  # Velocidade inicial
    obstacles = generate_obstacles(level)
    score = 0
    high_score = load_high_score()

    while running:
        screen.fill(black)

        # Manipula os eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and y_speed == 0:
                    x_speed, y_speed = 0, -square_size
                elif event.key == pygame.K_DOWN and y_speed == 0:
                    x_speed, y_speed = 0, square_size
                elif event.key == pygame.K_LEFT and x_speed == 0:
                    x_speed, y_speed = -square_size, 0
                elif event.key == pygame.K_RIGHT and x_speed == 0:
                    x_speed, y_speed = square_size, 0

        # Atualiza a posição da cobra
        x += x_speed
        y += y_speed
        snake.append((x, y))

        # Verifica colisões
        if x < 0 or x >= width or y < 0 or y >= height or (x, y) in snake[:-1] or (x, y) in obstacles:
            running = False  # Fim do jogo se bater nas bordas, no corpo ou nos obstáculos

        # Verifica se a cobra comeu a comida
        if (x, y) == food:
            food = generate_food()
            snake_length += 1
            goal -= 1
            score += 10  # Incrementa a pontuação

        # Ajusta o comprimento da cobra
        if len(snake) > snake_length:
            del snake[0]

        # Desenha a comida
        pygame.draw.rect(screen, green, (*food, square_size, square_size))

        # Desenha a cobra
        for segment in snake:
            pygame.draw.rect(screen, white, (*segment, square_size, square_size))

        # Desenha os obstáculos
        for obstacle in obstacles:
            pygame.draw.rect(screen, blue, (*obstacle, square_size, square_size))

        # Desenha o nível, a meta e a pontuação
        draw_text(f"Level: {level}", red, 10, 10)
        draw_text(f"Goal: {goal}", green, 10, 50)
        draw_text(f"Score: {score}", white, 10, 90)
        draw_text(f"High Score: {high_score}", white, 10, 130)

        # Verifica progressão de nível
        if goal == 0:
            level += 1
            goal = 5 + level  # Aumenta a meta no próximo nível
            speed += 2  # Aumenta a velocidade no próximo nível
            snake_length = 1  # Redefine o tamanho da cobra
            snake = [(x, y)]  # Redefine a posição da cobra
            obstacles = generate_obstacles(level)  # Gera novos obstáculos

            # Tela de transição de nível
            screen.fill(black)
            draw_text(f"Level {level}", white, width // 2 - 50, height // 2 - 20)
            pygame.display.update()
            pygame.time.wait(2000)  # Pausa antes de iniciar o próximo nível

        pygame.display.update()
        clock.tick(speed)

    # Atualiza a pontuação mais alta se necessário
    if score > high_score:
        high_score = score
        save_high_score(high_score)

    # Tela de Game Over
    screen.fill(black)
    draw_text("Game Over", red, width // 2 - 100, height // 2 - 50)
    draw_text(f"Score: {score}", white, width // 2 - 50, height // 2)
    draw_text(f"High Score: {high_score}", white, width // 2 - 50, height // 2 + 50)
    draw_text("Press R to Restart or ESC to Quit", white, width // 2 - 250, height // 2 + 100)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reinicia o jogo com "R"
                    return  # Reinicia o jogo
                elif event.key == pygame.K_ESCAPE:  # Encerra o jogo com ESC
                    pygame.quit()
                    exit()

# Loop principal
while True:
    menu()
    game()