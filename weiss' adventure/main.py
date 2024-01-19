#Created by Alex Roy
import pygame, sys
from button import Button
import time
import random
pygame.font.init()
pygame.init()

WIDTH = 1000
HEIGHT = 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

BG = pygame.image.load("assets/Background.png")
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

PLAYBG = pygame.image.load("assets/nier_background.jpg")
PLAYBG = pygame.transform.scale(PLAYBG, (WIDTH, HEIGHT))

OPTIONSBG = pygame.image.load("assets/options_background.jpg")
OPTIONSBG = pygame.transform.scale(OPTIONSBG, (WIDTH, HEIGHT))

WEISS = pygame.image.load("assets/weiss.png").convert()
WEISS = pygame.transform.scale(WEISS, (22, 28))
DARK_BLAST_IMG = pygame.image.load("assets/dark blast.png")
DARK_BLAST_IMG = pygame.transform.scale(DARK_BLAST_IMG, (20, 20))

PLAYER_WIDTH = 22
PLAYER_HEIGHT = 28
PLAYER_OFFSET = 40
PLAYER_VEL = 5

num_stars = 3
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3
star_add_increment = 1400

FONT = pygame.font.SysFont("TimesNewRoman", 30)
BIG_FONT = pygame.font.SysFont("TimesNewRoman", 40, "Bold")
HUGE_FONT = pygame.font.SysFont("TimesNewRoman", 100, "Bold")
DARK_RED = (185, 36, 56)
NORMAL_RED = (220, 40, 40)
GREY_RED = (133, 75, 75)
PURPLE = (43, 13, 45)
BLACK = (20, 20, 20)

pygame.display.set_caption("Weiss' adventure")

BACK_BUTTON_POS = (WIDTH - 10,10)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def draw(player, elapsed_time, stars):
    SCREEN.blit(PLAYBG, (0,0))
    time_text = FONT.render(f"time: {round(elapsed_time)}s", 1, DARK_RED)
    SCREEN.blit(time_text, (10,10))
    pygame.draw.rect(SCREEN, (255, 0, 0), player)
    SCREEN.blit(WEISS, player)

    back_text = FONT.render(f"Menu", 1, DARK_RED)
    SCREEN.blit(back_text, (WIDTH - 90,10))


    for star in stars:
        pygame.draw.rect(SCREEN, "white", star)
        SCREEN.blit(DARK_BLAST_IMG, star)

    pygame.display.update()


def play():
    global star_add_increment
    SCREEN.fill("black")
    run  = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT - PLAYER_OFFSET, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()
    start_time = time.time()    
    elapsed_time = 0

    star_count = 0
    stars = []
    hit = False
    
    PLAY_BACK = Button(image=None, pos= BACK_BUTTON_POS, 
                            text_input="BACK", font=get_font(75), base_color=DARK_RED, hovering_color=BLACK)

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time
        if star_count > star_add_increment: 
            for _ in range(num_stars):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, - STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_WIDTH + PLAYER_VEL <= WIDTH: 
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = BIG_FONT.render(f"YOU HAVE BEEN SLAIN", 1, DARK_RED)
            SCREEN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            score_text = BIG_FONT.render(f"Lasted: {round(elapsed_time)}s", 1, DARK_RED)
            SCREEN.blit(score_text, (WIDTH/2 - score_text.get_width()/2, HEIGHT/2 + lost_text.get_height()))
            pygame.display.update()
            pygame.time.delay(3000)
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        draw(player, elapsed_time, stars)

        pygame.display.update()


def options():
    while True:
        global num_stars
        global star_add_increment
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(OPTIONSBG, (0,0))

        OPTIONS_TEXT = get_font(45).render("OPTIONS", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(WIDTH/2, 300))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        EASYDIFF = Button(image=None, pos=(WIDTH/2, 375), 
                            text_input="EASY", font=BIG_FONT, base_color=DARK_RED, hovering_color=NORMAL_RED)
        MEDDIFF = Button(image=None, pos=(WIDTH/2, 450), 
                            text_input="MEDIUM", font=BIG_FONT, base_color=DARK_RED, hovering_color=NORMAL_RED)
        HARDDIFF = Button(image=None, pos=(WIDTH/2, 525), 
                            text_input="HARD", font=BIG_FONT, base_color=DARK_RED, hovering_color=NORMAL_RED)
        OPTIONS_BACK = Button(image=None, pos=(WIDTH/2, 625), 
                            text_input="BACK", font=BIG_FONT, base_color=DARK_RED, hovering_color=NORMAL_RED)
        
        for button in [EASYDIFF, MEDDIFF, HARDDIFF, OPTIONS_BACK]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if EASYDIFF.checkForInput(OPTIONS_MOUSE_POS):
                    num_stars = 3
                    star_add_increment = 1400
                if MEDDIFF.checkForInput(OPTIONS_MOUSE_POS):
                    num_stars = 4
                    star_add_increment = 1200
                if HARDDIFF.checkForInput(OPTIONS_MOUSE_POS):
                    star_add_increment = 1000
                    num_stars = 5

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = HUGE_FONT.render("Weiss' adventure", True, BLACK)
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH/2, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(WIDTH/2, 250), 
                            text_input="PLAY", font=HUGE_FONT, base_color= DARK_RED, hovering_color=NORMAL_RED)
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(WIDTH/2, 400), 
                            text_input="OPTIONS", font=HUGE_FONT, base_color= DARK_RED, hovering_color=NORMAL_RED)
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(WIDTH/2, 550), 
                            text_input="QUIT", font=HUGE_FONT, base_color= DARK_RED, hovering_color=NORMAL_RED)

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()