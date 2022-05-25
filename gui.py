from time import sleep
import pygame

SIZE = 1000
DISPLAY_DIMENSIONS = (1.5 * SIZE, SIZE)
PADDLE_HEIGHT = SIZE / 5
PADDLE_WIDTH = PADDLE_HEIGHT / 8
BALL_SIZE = PADDLE_WIDTH

START_COORDS_BALL = ((1.5 * SIZE) / 2  - BALL_SIZE, SIZE / 2 - BALL_SIZE)
START_COORDS_LEFT = (0, SIZE / 2 - PADDLE_HEIGHT / 2)
START_COORDS_RIGHT = (1.5 * SIZE - PADDLE_WIDTH, SIZE / 2 - PADDLE_HEIGHT / 2)

GAME_COLOUR = (0, 0, 0)
DISPLAY_COLOUR = (255, 255, 255)

UP = -1
DOWN = 1

MOVEMENT_RATE = PADDLE_HEIGHT / 4

class Paddle():
    def __init__(self, position):
        self.position = position # Co-ord of top left pixel

    def move(self, move_type):
        curr_height = self.position[1]
        if move_type == UP:
            new_height = max(0, curr_height - MOVEMENT_RATE)
        else:
            new_height = min(SIZE - PADDLE_HEIGHT, curr_height + MOVEMENT_RATE)
        
        self.position = (self.position[0], new_height)
            

class Ball():
    def __init__(self, position):
        self.position = position

    

paddle_left = Paddle(START_COORDS_LEFT)
paddle_right = Paddle(START_COORDS_RIGHT)
ball = Ball(START_COORDS_BALL)

# initialize all imported pygame modules
pygame.init()

win = pygame.display.set_mode(DISPLAY_DIMENSIONS)
pygame.display.set_caption("Pong")
win.fill(DISPLAY_COLOUR)
pygame.display.update()

cont = True
while cont:
    ev = pygame.event.get()
    keys = pygame.key.get_pressed()
    for event in ev:
        if event.type == pygame.QUIT:
            cont = False

    
    if keys[pygame.K_UP]:
        paddle_right.move(UP)
    elif keys[pygame.K_DOWN]:
        paddle_right.move(DOWN)
    
    if keys[pygame.K_w]:
        paddle_left.move(UP)
    elif keys[pygame.K_s]:
        paddle_left.move(DOWN)

    win.fill(DISPLAY_COLOUR)
    pygame.draw.rect(win, GAME_COLOUR, (*paddle_left.position, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(win, GAME_COLOUR, (*paddle_right.position, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(win, GAME_COLOUR, (*ball.position, BALL_SIZE, BALL_SIZE))
    pygame.display.update()
    sleep(0.1)