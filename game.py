import pygame
import random
import os

pygame.mixer.init()

pygame.init()



# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (11, 100, 255)
light_blue = (26, 109, 255)
light_yellow = (244, 251, 15)

# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

#Background Image

start_img = pygame.image.load("start_screen.jpg")
start_img = pygame.transform.scale(start_img, (screen_width, screen_height)) 

game_over_img = pygame.image.load("game_over.jpg")
game_over_img = pygame.transform.scale(game_over_img, (screen_width, screen_height)) 

bgimg = pygame.image.load("bg2.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height))

bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha() 
game_over = pygame.transform.scale(game_over_img, (screen_width, screen_height)).convert_alpha() 

# Game Title
pygame.display.set_caption("SnakeClub Made By Ashutosh")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((233,210,229))

        gameWindow.blit(start_img, (0, 0))
        text_screen("Welcome to Snakes", white, 260, 250)
        text_screen("Press Any Key To Play", white, 232, 290)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            elif event.type == pygame.KEYDOWN:
                gameloop()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                gameloop()

            elif event.type == pygame.MOUSEBUTTONUP:
                gameloop()

        pygame.display.update()
        clock.tick(60)


# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    difference = 15

    # Check if hiscore file exists
    if(not os.path.exists("hiscore.txt")):
        with open("hiscore.txt", "w") as f:
            f.write("0")
    with open("hiscore.txt", "r") as f:

        hiscore = f.read()
        try:
            hiscore = int(hiscore)
        except Exception as e:
            print(f"The error is {e}")
            with open("hiscore.txt", "w") as f:
                hiscore = 0
                f.write(str(hiscore))

        # validate hiscore
        # print(isinstance(hiscore, int))

        if not isinstance(hiscore, int):
            with open("hiscore.txt", "w") as f:
                hiscore = 0
                f.write(str(hiscore))

    food_x = random.randint(0, screen_width /2)
    food_y = random.randint(0, screen_height - 100)
    score = 0
    init_velocity = 5
    snake_size = 30
    fps = 60
    while not exit_game:
        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))
            gameWindow.fill(white) 
            gameWindow.blit(game_over_img, (0, 0))
            text_screen("Game Over! Press Any To Continue", light_blue, 120, 400)
            text_screen("Made By Ashutosh", light_yellow, screen_width / 2 - 150, 450)


            pygame.display.update() 


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    gameloop()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    gameloop()

                elif event.type == pygame.MOUSEBUTTONUP:
                    gameloop()
                        

        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    init_velocity = init_velocity + 0.1
                    print(f"\n  The Current speed is {init_velocity}  \n")
                    if event.key == pygame.K_d:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_a:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_w:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_s:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_q:
                        score +=10

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            fit_abs = 12

            if abs(snake_x - food_x)<fit_abs and abs(snake_y - food_y)<fit_abs:
                score +=10
                food_x = random.randint(0, screen_width)
                food_y = random.randint(0, screen_height)
                snk_length +=5
                if score>int(hiscore):
                    hiscore = score

            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            text_screen("Score: " + str(score) + "  Hiscore: "+str(hiscore), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])


            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                # pygame.mixer.music.load('gameover.mp3')
                # pygame.mixer.music.play()

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                # pygame.mixer.music.load('gameover.mp3')
                # pygame.mixer.music.play()
            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()
