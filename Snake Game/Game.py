import pygame
import random

pygame.init()
pygame.display.set_caption("Snake Game") # Set the title of the window
widht = 800
height = 600
screen = pygame.display.set_mode((widht, height)) # Set the size of the window
clock = pygame.time.Clock() # Create a clock object to control the speed of the game

# Colors RGB
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# Snake parameters
square_size = 10
game_speed = 15

# Functions

#fuction to generate food
def generate_food():
    food_x = round(random.randrange(0, widht - square_size ) / 10.0) * 10.0
    food_y = round(random.randrange(0, height - square_size ) / 10.0) * 10.0
    return food_x, food_y

#function to draw the food
def draw_food(size,food_x, food_y):
    pygame.draw.rect(screen, green, (food_x, food_y, size, size))

#Game
def game():
    end_game = False

    x = height / 2
    y = widht / 2

    x_speed = 0
    y_speed = 0

    snake_size = 1
    snake = [] # pixels of the snake

    food_x ,food_y = generate_food()

    while not end_game:
        screen.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game = True


        #draw the food
        draw_food(square_size, food_x, food_y)


        #draw the snake


        #draw the points


        #update the screen
        pygame.display.update()
        clock.tick(game_speed)

