import pygame
from pygame.locals import *

from sprites import Pong, AIPaddle, EvilObject, PlayerPaddle

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BRIGHT_RED = (255, 100, 100)
BRIGHT_GREEN = (100, 255, 100)


class PongGame:

    def __init__(self):
        self.screensize = (1800, 700)
        self.mode = pygame.display.set_mode(self.screensize)
        self.score = 0
        self.typed = ''


    def main(self):

        pygame.init()
        clock = pygame.time.Clock()

        pong = Pong(self.screensize)
        ai_paddle = AIPaddle(self.screensize)
        player_paddle = PlayerPaddle(self.screensize)
        evil_object = EvilObject(self.screensize)

        running = True

        while running:

            #fps limiting/reporting phase
            clock.tick(64)

            #event handling phase
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        player_paddle.direction = -1
                    elif event.key == K_DOWN:
                        player_paddle.direction = 1

                    if event.unicode in 'abcdefghijklmnopqrstuvwxyz':
                        self.typed += event.unicode
                        if len(self.typed) > 700:
                            self.typed = ''

                        if 'jonathanlovessamantha' in self.typed:
                            self.score += 100
                            self.typed = ''

                        if 'lower' in self.typed:
                            self.score -= 10
                            self.typed = ''

                        if 'reset' in self.typed:
                            del pong
                            pong = Pong(self.screensize)
                            self.score = 0
                            self.typed = ''

                    print(self.typed)

                if event.type == KEYUP:
                    if event.key == K_UP and player_paddle.direction == -1:
                        player_paddle.direction = 0
                    elif event.key == K_DOWN and player_paddle.direction == 1:
                        player_paddle.direction = 0

            #object updating phase
            ai_paddle.update(pong)
            player_paddle.update()
            evil_object.update(pong)
            pong.update(player_paddle, ai_paddle, evil_object)


            #CODE TASK: make some text on the screen over everything else saying you lost/won, and then exit on keypress
            #CODE BONUS: allow restarting of the game (hint: you can recreate the Pong/Paddle objects the same way we made them initially)


            if pong.hit_edge_left:
                self.score += 1
                del pong
                pong = Pong(self.screensize)
                del ai_paddle
                ai_paddle = AIPaddle(self.screensize)
                if self.score >= 2:
                    self.mode.fill((255, 255, 255))
                    self.game_over(clock, self.screensize, self.mode, "You WIN!")
                    running = False
            elif pong.hit_edge_right:
                self.score -= 1
                del pong
                pong = Pong(self.screensize)
                if self.score <= -2:
                    self.mode.fill((255, 255, 255))
                    self.game_over(clock, self.screensize, self.mode, "You Lose.")
                    running = False

            #rendering phase
            self.mode.fill((255, 255, 255))

            ai_paddle.render(self.mode)
            player_paddle.render(self.mode)
            pong.render(self.mode)
            evil_object.render(self.mode)

            self.show_score()

            pygame.display.flip()
        pygame.quit()

    def text_objects(self, text, font):
        textSurface = font.render(text, True, BLACK)
        return textSurface, textSurface.get_rect()

    def game_over(self, clock, screensize, screen, message):
        display_width, display_height = screensize
        largeText = pygame.font.SysFont("comicsansms", 115)
        TextSurf, TextRect = self.text_objects(message, largeText)
        TextRect.center = ((display_width / 2), (display_height / 3))
        screen.blit(TextSurf, TextRect)
        TextSurf, TextRect = self.text_objects("Press q to quit.", largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        screen.blit(TextSurf, TextRect)

        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == KEYDOWN:
                    if event.key == K_q:
                        pygame.quit()
                        quit()

            pygame.display.update()
            clock.tick(15)

    def show_score(self):
        largeText = pygame.font.SysFont("comicsansms",18)
        TextSurf, TextRect = self.text_objects(f'score: {self.score}', largeText)
        TextRect.left = 0
        self.mode.blit(TextSurf, TextRect)

pg = PongGame()

pg.main()