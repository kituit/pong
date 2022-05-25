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

class Paddle():
    def __init__(self, position):
        self.position = position # Co-ord of top left pixel

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
win.fill((255, 255, 255))
pygame.display.update()

cont = True
while cont:
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.QUIT:
            cont = False
    pygame.draw.rect(win, (0, 0, 0), (*paddle_left.position, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(win, (0, 0, 0), (*paddle_right.position, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(win, (0, 0, 0), (*ball.position, BALL_SIZE, BALL_SIZE))
    pygame.display.update()
    sleep(0.5)