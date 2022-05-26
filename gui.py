from time import sleep
import pygame

SIZE = 1000
DISPLAY_WIDTH = 1.5 * SIZE
DISPLAY_HEIGHT = SIZE
DISPLAY_DIMENSIONS = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
PADDLE_HEIGHT = SIZE / 5
PADDLE_WIDTH = PADDLE_HEIGHT / 8
BALL_SIZE = PADDLE_WIDTH

START_COORDS_BALL = (DISPLAY_WIDTH / 2  - BALL_SIZE, SIZE / 2 - BALL_SIZE)
START_COORDS_LEFT = (0, SIZE / 2 - PADDLE_HEIGHT / 2)
START_COORDS_RIGHT = (DISPLAY_WIDTH - PADDLE_WIDTH, SIZE / 2 - PADDLE_HEIGHT / 2)

GAME_COLOUR = (0, 0, 0)
DISPLAY_COLOUR = (255, 255, 255)

UP = -1
DOWN = 1

MOVEMENT_RATE = PADDLE_HEIGHT / 12
BALL_SPEED_LIMIT = MOVEMENT_RATE
SPEED_INCREASE_RATE = 1.5 # Rate at which ball increases speed when rebounds of paddle
FPS = 60

class Player():
    def __init__(self, position):
        self.position = position # Co-ord of top left pixel
        self.score = 0

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
        self.direction = (5, 5)
    
    def move(self, player_left, player_right):
        curr_x, curr_y = self.position
        move_x, move_y = self.direction
        new_x, new_y = curr_x, curr_y

        if curr_y + move_y < 0:
            new_y = 0
            move_y = -1 * move_y
        elif curr_y + move_y > DISPLAY_HEIGHT - BALL_SIZE:
            new_y = DISPLAY_HEIGHT - BALL_SIZE
            move_y = -1 * move_y
        else:
            new_y = curr_y + move_y
        
        if curr_x + BALL_SIZE >= DISPLAY_WIDTH - PADDLE_WIDTH:
            paddle_right_y = player_right.position[1]
            if paddle_right_y <= curr_y <= paddle_right_y + PADDLE_HEIGHT or paddle_right_y <= curr_y + BALL_SIZE <= paddle_right_y + PADDLE_HEIGHT:
                move_x = -1 * move_x
                move_x, move_y = speed_up(move_x, move_y)
            # Deal with losing point here
        elif curr_x <= PADDLE_WIDTH:
            paddle_left_y = player_left.position[1]
            if paddle_left_y <= curr_y <= paddle_left_y + PADDLE_HEIGHT or paddle_left_y <= curr_y + BALL_SIZE <= paddle_left_y + PADDLE_HEIGHT:
                move_x = -1 * move_x
                move_x, move_y = speed_up(move_x, move_y)
            # Deal with losing point here
        else:
            new_x = curr_x + move_x


        self.direction = (move_x, move_y)
        self.position = (curr_x + move_x, new_y)


def speed_up(move_x, move_y):
    if move_x ** 2 + move_y ** 2 >= BALL_SPEED_LIMIT ** 2:
        return (move_x, move_y)
    else:
        max_speed_increase_rate = BALL_SPEED_LIMIT / ((move_x ** 2 + move_y ** 2) ** 0.5)
        speed_increase = min(max_speed_increase_rate, SPEED_INCREASE_RATE)
        return (move_x * speed_increase, move_y * speed_increase)

player_left = Player(START_COORDS_LEFT)
player_right = Player(START_COORDS_RIGHT)
ball = Ball(START_COORDS_BALL)

clock = pygame.time.Clock()

# initialize all imported pygame modules
pygame.init()

win = pygame.display.set_mode(DISPLAY_DIMENSIONS)
pygame.display.set_caption("Pong")
win.fill(DISPLAY_COLOUR)
pygame.display.update()

cont = True
while cont:
    clock.tick(FPS)
    ball.move(player_left, player_right)

    ev = pygame.event.get()
    keys = pygame.key.get_pressed()
    for event in ev:
        if event.type == pygame.QUIT:
            cont = False

    
    if keys[pygame.K_UP]:
        player_right.move(UP)
    elif keys[pygame.K_DOWN]:
        player_right.move(DOWN)
    
    if keys[pygame.K_w]:
        player_left.move(UP)
    elif keys[pygame.K_s]:
        player_left.move(DOWN)

    win.fill(DISPLAY_COLOUR)
    pygame.draw.rect(win, GAME_COLOUR, (*player_left.position, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(win, GAME_COLOUR, (*player_right.position, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(win, GAME_COLOUR, (*ball.position, BALL_SIZE, BALL_SIZE))
    pygame.display.update()