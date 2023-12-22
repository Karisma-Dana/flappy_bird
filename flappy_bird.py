import pygame
from pygame.locals import *
import os
import sys
import time
import random


pygame.init()
pygame.mixer.init()

# PETTTING SCREEN
SCREEN_WIDTH = 863
SCREEN_HEIGHT = 936

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("flappy bird")
pygame.display.set_icon(
    pygame.image.load(os.path.join("element game(flappy)/flappy--(bird)", "bird1.png"))
)


# difine game variables
GROUND_SCROLL = 0
SCROLL_SPEED = 0
FLYING = False
GAME_OVER = False
PIPE_GAP = 150
PIPE_FREQUENCY = 4000  # millisecond
LAST_PIPE = pygame.time.get_ticks() - PIPE_FREQUENCY
SCORE_GAME = 0
PASS_PIPE = False
rekor_player = []


# load music-----------------------
pygame.mixer.music.load("whus.mp3")
pygame.mixer.music.load("menu.mp3")
pygame.mixer.music.load("die2.mp3")

# chhannel music------------------
back_sound = pygame.mixer.Channel(0)
whus_sound = pygame.mixer.Channel(2)
die_sound = pygame.mixer.Channel(1)


BACKGROUND = pygame.image.load(
    os.path.join("element game(flappy)/flappy--(bg)", "bg.png")
)
GROUND = pygame.image.load(
    os.path.join("element game(flappy)/flappy--(bg)", "ground.png")
)
BIRD = [
    pygame.image.load(os.path.join("element game(flappy)/flappy--(bird)", "bird1.png")),
    pygame.image.load(os.path.join("element game(flappy)/flappy--(bird)", "bird2.png")),
    pygame.image.load(os.path.join("element game(flappy)/flappy--(bird)", "bird3.png")),
]
RESTART = pygame.image.load(
    os.path.join("element game(flappy)/flappy--(bg)", "restart.png")
)
PIPE = pygame.image.load(os.path.join("element game(flappy)/flappy--(bg)", "pipe.png"))


# class  bird---------------------------------
class Bird(pygame.sprite.Sprite):
    global FLYING, play_music

    def __init__(self, x: int, y: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(
                os.path.join("element game(flappy)/flappy--(bird)", f"bird{num}.png")
            )
            self.images.append(img)
        self.image = self.images[self.index]

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.val = 0
        self.presButton = False

    def update(self) -> None:
        global FLYING
        if FLYING == True:
            # gravity animation-------------------
            self.val += 0.5
            if self.val > 8:
                self.val = 8
            if self.rect.bottom < 763:
                self.rect.y += int(self.val)

        # jump animation----------------------
        if GAME_OVER == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.presButton == False:
                whus_sound.play(pygame.mixer.Sound("whus.mp3"), loops=0)
                self.presButton = True
                self.val = -9
            if pygame.mouse.get_pressed()[0] == 0:
                self.presButton = False
            if self.rect.y < 0:
                self.rect.y = 0

            # handle the animation------------------
            self.counter += 1
            flap_cooldown = 4
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
            self.image = pygame.transform.rotate(self.images[self.index], self.val * -2)

        elif GAME_OVER == True:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, position: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = PIPE
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(PIPE_GAP / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(PIPE_GAP / 2)]

    def update(self):
        self.rect.x -= SCROLL_SPEED
        if self.rect.right < 0:
            self.kill()


class Setting_level:
    def __init__(self, level: int) -> None:
        self.level = level
        self.list_level = list(range(1, 5))
        self.level_1 = list(range(0, 3))
        self.level_2 = list(range(3, 7))
        self.level_3 = list(range(7, 26))
        self.level_4 = list(range(26, 41))
        self.level_5 = list(range(41, 51))
        self.font = pygame.font.Font("freesansbold.ttf", 20)

    def update(self):
        if self.level in self.level_1:
            self.level = 1
        elif self.level in self.level_2:
            self.level = 2
        elif self.level in self.level_3:
            self.level = 3
        elif self.level in self.level_4:
            self.level = 4
        elif self.level in self.level_5:
            self.level = 5

        if level in self.list_level:
            self.list_level.remove(self.level)
        self.score = self.level

    def draw(self, SCREEN):
        text_level = self.font.render(f"level : {str(self.level)}", True, (0, 0, 0))
        text_levelRect = text_level.get_rect()
        text_levelRect.center = (800, 40)
        SCREEN.blit(text_level, text_levelRect)


def player_record(rekor_playe: list, time_player: int, score_player: int) -> None:
    if len(rekor_player) == 0:
        rekor_player.append({"Time": time_player, "Score": score_player})
    elif len(rekor_player) >= 0:
        new_dict = {"Time": time_player, "Score": score_player}

        if new_dict["Score"] > rekor_player[0]["Score"]:
            rekor_player.clear()
            rekor_player.append({"Time": time_player, "Score": score_player})
        elif (
            new_dict["Score"] == rekor_player[0]["Score"]
            and new_dict["Time"] < rekor_player[0]["Time"]
        ):
            rekor_player.clear()
            rekor_player.append({"Time": time_player, "Score": score_player})


def main():
    global GROUND_SCROLL, SCROLL_SPEED, FLYING, GAME_OVER, LAST_PIPE, PASS_PIPE, SCORE_GAME, pipe_frequency, rekor_player, level, rekor_player, pipe_height
    # list score adn level ----------------------------
    level = 0
    # flaying bird animation----------------------------
    bird_group = pygame.sprite.Group()
    pipe_group = pygame.sprite.Group()
    flappy = Bird(100, int(SCREEN_HEIGHT / 2))
    bird_group.add(flappy)
    # pipe height--------------------------------------
    pipe_height = random.randint(-100, 100)
    # fps setting--------------------------------------
    clock = pygame.time.Clock()
    fps = 60
    # font setting
    font = pygame.font.Font("freesansbold.ttf", 20)
    font2 = pygame.font.SysFont("Bauhaus 93", 60)

    def backround():
        SCREEN.blit(BACKGROUND, (0, 0))
        bird_group.draw(SCREEN)
        bird_group.update()
        pipe_group.draw(SCREEN)
        SCREEN.blit(GROUND, (GROUND_SCROLL, 768))

    def pipe_setting(score: int) -> None:
        global LAST_PIPE, GROUND_SCROLL, pipe_height
        time_now = pygame.time.get_ticks()
        if time_now - LAST_PIPE > PIPE_FREQUENCY and score <= 47:
            # pipe location-----------------------------------
            btm_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, -1)
            top_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            LAST_PIPE = time_now

        GROUND_SCROLL -= SCROLL_SPEED
        if abs(GROUND_SCROLL) > 35:
            GROUND_SCROLL = 0
        pipe_group.update()

    def time_game():
        global real_time

        # upgrade point
        real_time = (current_time - start_time) // 1000
        text = font.render(f"time : {str(real_time )}", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (800, 20)
        SCREEN.blit(text, textRect)

    def score_text(text, text_col, x, y):
        img = font2.render(text, True, text_col)
        SCREEN.blit(img, (x, y))

    def score_setting():
        global SCORE_GAME, PIPE_FREQUENCY, SCROLL_SPEED, pipe_height, GAME_OVER

        if SCORE_GAME >= 0 and SCORE_GAME <= 2:
            PIPE_FREQUENCY = 4000
            SCROLL_SPEED = 4
            pipe_height = -30
        elif SCORE_GAME >= 3 and SCORE_GAME <= 6:
            PIPE_FREQUENCY = 3600
            SCROLL_SPEED = 4
            pipe_height = random.randint(-100, 100)
        elif SCORE_GAME >= 7 and SCORE_GAME <= 25:
            PIPE_FREQUENCY = 1700
            SCROLL_SPEED = 4
            pipe_height = random.choice([85, -100, 90, 70, -70, -80, -150, 0])
        elif SCORE_GAME >= 26 and SCORE_GAME <= 40:
            SCROLL_SPEED = 4.5
            PIPE_FREQUENCY = 1500
            pipe_height = random.choice(
                [80, 90, 0, 70, -200, -150, -125, 100, 30, -100]
            )
        elif SCORE_GAME >= 41 and SCORE_GAME <= 51:
            SCROLL_SPEED = 5
            PIPE_FREQUENCY = 1100
            pipe_height = random.choice([-200, 100, -100, 80])

    # time start------------------------------------------
    start_time = pygame.time.get_ticks()
    back_sound.play(pygame.mixer.Sound("menu.mp3"), loops=-1)

    # runnign game------------------------------------
    run = True
    while run:
        clock.tick(fps)
        # running fps game
        backround()
        if len(pipe_group) > 0:
            if (
                bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left
                and bird_group.sprites()[0].rect.right
                < pipe_group.sprites()[0].rect.right
                and PASS_PIPE == False
            ):
                PASS_PIPE = True
            if PASS_PIPE == True:
                if (
                    bird_group.sprites()[0].rect.left
                    > pipe_group.sprites()[0].rect.right
                ):
                    SCORE_GAME += 1
                    PASS_PIPE = False

        score_text(str(SCORE_GAME), (255, 255, 255), int(SCREEN_WIDTH / 2), 20)
        if (
            pygame.sprite.groupcollide(bird_group, pipe_group, False, False)
            or flappy.rect.top < 0
        ):
            GAME_OVER = True
            bird_group.update()

        if flappy.rect.bottom >= 765:
            GAME_OVER = True
            FLYING = False

        if GAME_OVER == False and FLYING == True:
            set_level = Setting_level(SCORE_GAME)
            pipe_setting(SCORE_GAME)
            set_level.update()
            set_level.draw(SCREEN)

        score_setting()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and FLYING == False
                and GAME_OVER == False
            ):
                FLYING = True

        # time stop---------------------------------
        current_time = pygame.time.get_ticks()
        if FLYING == True:
            time_game()
        if GAME_OVER == True:
            die_sound.play(pygame.mixer.Sound("die2.mp3"), loops=0)
            back_sound.stop()
            player_record(rekor_player, real_time, SCORE_GAME)
            time.sleep(1.5)
            Home_menu()

        pygame.display.update()


def Home_menu():
    global GAME_OVER, FLYING, real_time, SCORE_GAME, rekor_player, font3, rekor_player
    run = True
    font3 = pygame.font.Font("freesansbold.ttf", 25)
    highest_score = rekor_player[0]["Score"]
    highest_time = rekor_player[0]["Time"]

    def font_menu(text: str, width: int, height: int, SCREEN) -> None:
        global font3
        text = font3.render(text, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (width, height)
        SCREEN.blit(text, text_rect)

    while run:
        SCREEN.blit(BACKGROUND, (0, 0))

        # text setting-----------------------------------
        font_menu(
            "Press any key to Restart",
            (SCREEN_WIDTH // 2),
            (SCREEN_HEIGHT // 2 - 250),
            SCREEN,
        )

        # menu score setting------------------------------------
        font_menu(
            f"Score : {SCORE_GAME}",
            (SCREEN_WIDTH // 2),
            (SCREEN_HEIGHT // 2 - 200),
            SCREEN,
        )

        # menu time setting----------------------------------
        font_menu(
            f"time   : {real_time} ",
            (SCREEN_WIDTH // 2 + 5),
            (SCREEN_HEIGHT // 2 + 80 - 250),
            SCREEN,
        )

        # menu line setting-----------------------------------
        font_menu(
            "________________________________",
            (SCREEN_WIDTH // 2),
            (SCREEN_HEIGHT // 2 + 110 - 250),
            SCREEN,
        )

        # mahkota---------------------------------------------
        font_menu(
            "player points record",
            (SCREEN_WIDTH // 2),
            (SCREEN_HEIGHT // 2 + 150 - 250),
            SCREEN,
        )
        font_menu(
            f"Score : {highest_score}",
            (SCREEN_WIDTH // 2),
            (SCREEN_HEIGHT // 2 + 180 - 250),
            SCREEN,
        )
        font_menu(
            f"time   : {highest_time} ",
            (SCREEN_WIDTH // 2 + 5),
            (SCREEN_HEIGHT // 2 + 210 - 250),
            SCREEN,
        )

        # restart image setting----------------------------
        button_restart = RESTART.get_rect(
            topleft=(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 320)
        )
        SCREEN.blit(RESTART, (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 320))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                print(rekor_player)
                sys.exit()

            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (
                button_restart.collidepoint(mouse_x, mouse_y)
                and event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):
                FLYING = False
                GAME_OVER = False
                SCORE_GAME = 0
                time.sleep(0.5)
                main()

            if event.type == pygame.KEYDOWN:
                print(level)
                FLYING = False
                GAME_OVER = False
                SCORE_GAME = 0
                main()
        pygame.display.update()


if __name__ == "__main__" : 
    main()