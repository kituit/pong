import random
from time import sleep
import pygame
import pygame.freetype

SIZE = 1000
DISPLAY_WIDTH = 1.5 * SIZE
DISPLAY_HEIGHT = SIZE
DISPLAY_DIMENSIONS = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
PADDLE_HEIGHT = SIZE / 5
PADDLE_WIDTH = PADDLE_HEIGHT / 8
BALL_SIZE = PADDLE_WIDTH
FONT_SIZE = PADDLE_HEIGHT

START_COORDS_BALL = (DISPLAY_WIDTH / 2  - BALL_SIZE, SIZE / 2 - BALL_SIZE)
START_COORDS_LEFT = (0, SIZE / 2 - PADDLE_HEIGHT / 2)
START_COORDS_RIGHT = (DISPLAY_WIDTH - PADDLE_WIDTH, SIZE / 2 - PADDLE_HEIGHT / 2)

GAME_COLOUR = (0, 0, 0)
DISPLAY_COLOUR = (255, 255, 255)

UP = -1
DOWN = 1

MOVEMENT_RATE = PADDLE_HEIGHT / 12
BALL_SPEED_LIMIT = 1.5 * MOVEMENT_RATE
BALL_SPEED_BASE = BALL_SPEED_LIMIT / 3
BALL_SPEEDS_START = (list(range(int(0.66 * BALL_SPEED_BASE), int(1.33 * BALL_SPEED_BASE))) + 
                    list(range(int(-1.33 * BALL_SPEED_BASE), int(-0.66 * BALL_SPEED_BASE))))
SPEED_INCREASE_RATE = 1.3 # Rate at which ball increases speed when rebounds of paddle
FPS = 60

# initialize all imported pygame modules
pygame.init()
pygame.font.init()

def speed_up(move_x, move_y):
    if move_x ** 2 + move_y ** 2 >= BALL_SPEED_LIMIT ** 2:
        return (move_x, move_y)
    else:
        max_speed_increase_rate = BALL_SPEED_LIMIT / ((move_x ** 2 + move_y ** 2) ** 0.5)
        speed_increase = min(max_speed_increase_rate, SPEED_INCREASE_RATE)
        return (move_x * speed_increase, move_y * speed_increase)

def generate_random_direction():
    return tuple(random.choices(BALL_SPEEDS_START, k=2))

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
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.position = START_COORDS_BALL
        self.direction = generate_random_direction()
    
    def move(self, player_left, player_right):
        curr_x, curr_y = self.position
        move_x, move_y = self.direction
        new_x, new_y = curr_x, curr_y

        # Vertical movememnt bounds checking
        if curr_y + move_y < 0:
            new_y = 0
            move_y = -1 * move_y
        elif curr_y + move_y > DISPLAY_HEIGHT - BALL_SIZE:
            new_y = DISPLAY_HEIGHT - BALL_SIZE
            move_y = -1 * move_y
        else:
            new_y = curr_y + move_y
        
        # Horizontal movemement bounds checking + point detection
        if curr_x + BALL_SIZE >= DISPLAY_WIDTH - PADDLE_WIDTH:
            paddle_right_y = player_right.position[1]
            if paddle_right_y <= curr_y <= paddle_right_y + PADDLE_HEIGHT or paddle_right_y <= curr_y + BALL_SIZE <= paddle_right_y + PADDLE_HEIGHT:
                move_x = -1 * move_x
                move_x, move_y = speed_up(move_x, move_y)
            else:
                player_left.score += 1
                self.reset()
                sleep(0.5)
                return
        elif curr_x <= PADDLE_WIDTH:
            paddle_left_y = player_left.position[1]
            if paddle_left_y <= curr_y <= paddle_left_y + PADDLE_HEIGHT or paddle_left_y <= curr_y + BALL_SIZE <= paddle_left_y + PADDLE_HEIGHT:
                move_x = -1 * move_x
                move_x, move_y = speed_up(move_x, move_y)
            else:
                player_right.score += 1
                self.reset()
                sleep(0.5)
                return
        new_x = curr_x + move_x

        self.direction = (move_x, move_y)
        self.position = (new_x, new_y)


class Game():
    def __init__(self):
        self.player_left = Player(START_COORDS_LEFT)
        self.player_right = Player(START_COORDS_RIGHT)
        self.ball = Ball()
        self.clock = pygame.time.Clock()

        self.win = pygame.display.set_mode(DISPLAY_DIMENSIONS)
        self.font = pygame.freetype.SysFont('Sans', FONT_SIZE)
        icon = pygame.image.load('img/Icon.jpg')
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Pong")
        self.win.fill(DISPLAY_COLOUR)
        pygame.display.update()
    
    def draw_screen(self):
        self.win.fill(DISPLAY_COLOUR)
        text_left_score, _ = self.font.render(f'{self.player_left.score}', GAME_COLOUR)
        text_right_score, _ = self.font.render(f'{self.player_right.score}', GAME_COLOUR)
        self.win.blit(text_left_score, (DISPLAY_WIDTH / 4, 0))
        self.win.blit(text_right_score, (3 * DISPLAY_WIDTH / 4, 0))
        pygame.draw.rect(self.win, GAME_COLOUR, (*self.player_left.position, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(self.win, GAME_COLOUR, (*self.player_right.position, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(self.win, GAME_COLOUR, (*self.ball.position, BALL_SIZE, BALL_SIZE))
        pygame.display.update()
    
    def play(self):
        cont = True
        while cont:
            self.clock.tick(FPS)
            self.ball.move(self.player_left, self.player_right)

            ev = pygame.event.get()
            keys = pygame.key.get_pressed()
            for event in ev:
                if event.type == pygame.QUIT:
                    cont = False

            # Player right movement
            if keys[pygame.K_UP]:
                self.player_right.move(UP)
            elif keys[pygame.K_DOWN]:
                self.player_right.move(DOWN)
            
            # Player left movemement
            if keys[pygame.K_w]:
                self.player_left.move(UP)
            elif keys[pygame.K_s]:
                self.player_left.move(DOWN)
            
            self.draw_screen()


if __name__ == '__main__':
    g = Game()
    g.play()
