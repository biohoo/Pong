import random

import pygame


class Pong:

    def __init__(self, screensize):

        self.screensize = screensize

        self.centerx = int(screensize[0]*0.1)
        self.centery = int(screensize[1]*0.5)

        self.radius = 8

        self.rect = pygame.Rect(self.centerx-self.radius,
                                self.centery-self.radius,
                                self.radius*2, self.radius*2)

        self.color = (100,100,255)

        self.direction = [1,1]

        self.speedx = 15
        self.speedy = 2
        #CODE TASK: change speed/radius as game progresses to make it harder
        #CODE BONUS: adjust ratio of x and y speeds to make it harder as game progresses

        self.hit_edge_left = False
        self.hit_edge_right = False

    def update(self, player_paddle, ai_paddle, evil_object):

        self.centerx += self.direction[0]*self.speedx
        self.centery += self.direction[1]*self.speedy

        self.rect.center = (self.centerx, self.centery)

        if self.rect.top <= 0:
            self.direction[1] = 1
        elif self.rect.bottom >= self.screensize[1]-1:
            self.direction[1] = -1

        if self.rect.right >= self.screensize[0]-1:
            self.hit_edge_right = True
        elif self.rect.left <= 0:
            self.hit_edge_left = True

        #CODE TASK: Change the direction of the pong, based on where it hits the paddles (HINT: check the center points of each)

        if self.rect.colliderect(player_paddle.rect):

            # change the x angle
            self.direction[0] = random.randrange(-1, 0)

            if player_paddle.rect.center[1] < self.rect.center[1]:
                self.direction[1] = random.randrange(1, 3)
            else:
                self.direction[1] = random.randint(-3, -1)



        if self.rect.colliderect(ai_paddle.rect):
            self.direction = [1,random.random()]
            self.speedx += AIPaddle.paddleLength   # Increase the speed every time the AI hits.
            self.radius = random.randint(3,24)  # Change the size of the pong if ai hits.
            ai_paddle.rect.height -= 10

        if self.rect.colliderect(evil_object.rect):

            # Banked off of the top or bottom
            if abs(self.rect.bottom - evil_object.rect.top) <= 3 or \
                abs(self.rect.top - evil_object.rect.bottom) <= 3:
                self.direction[1] = -self.direction[1]
            else:
                # Both sides
                self.direction[0] = -self.direction[0]
                self.direction[1] = -self.direction[1]

                # Shrink the object.
                evil_object.rect = pygame.Rect(0, evil_object.centery - int(evil_object.height * 0.5), evil_object.width-10, evil_object.height-20)

        if self.speedx > 10 or self.speedx <= 1:
            self.speedx = random.randrange(2,10)

        # Make sure it never just vertically bounces.
        if self.direction[0] == 0:
            self.direction[0] += 0


    def render(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius, 0)
        pygame.draw.circle(screen, (0,0,0), self.rect.center, self.radius, 1)


class AIPaddle:

    paddleLength = 0.5

    def __init__(self, screensize):

        self.screensize = screensize

        self.centerx = 5
        self.centery = int(screensize[1]*0.5)

        self.height = 100 * self.paddleLength
        self.width = 100

        self.rect = pygame.Rect(0, self.centery-int(self.height*0.5), self.width, self.height)

        self.color = (255,100,100)

        #CODE TASK: Adjust size of AI paddle as match progresses to make it more difficult

        self.speed = 2


    def update(self, pong):
        if pong.rect.bottom - 5 < self.rect.top:
            self.centery -= self.speed

        elif pong.rect.top + 5 > self.rect.bottom:
            self.centery += self.speed

        self.rect.center = (self.centerx, self.centery)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0,0,0), self.rect, 1)


class EvilObject:
    def __init__(self, screensize):
        self.screensize = screensize

        self.centerx = int(screensize[0] / 2)
        self.centery = int(screensize[1]/2)

        self.height = 100
        self.width = 100

        self.rect = pygame.Rect(0, self.centery-int(self.height*0.5), self.width, self.height)

        self.color = (100,255,100)

        self.speed = 4
        self.direction = 1

    def update(self, pong):

        # pong gets close to object, object stops to prevent overlap.
        if abs(self.rect.center[0] - pong.rect.center[0]) <= self.width and\
                abs(self.rect.center[1] - pong.rect.center[1]) <= self.height:
            self.speed = 0
        else:
            self.speed = 5

        # Object hits top and bottom, change direction.
        self.centery += self.direction*self.speed
        if self.centery < 0:
            self.centery = 0 + (self.height/2)
            self.direction = 1

        elif self.centery > self.screensize[1]:
            self.centery = self.screensize[1] - (self.height /2)
            self.direction = -1

        # Object overlaps offscreen, change to center on screen.
        self.rect.center = (self.centerx, self.centery)
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screensize[1]-1:
            self.rect.bottom = self.screensize[1]-1

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0,0,0), self.rect, 1)


class PlayerPaddle:
    def __init__(self, screensize):
        self.screensize = screensize

        self.centerx = screensize[0]-5
        self.centery = int(screensize[1]*0.5)

        self.height = 100
        self.width = 100

        self.rect = pygame.Rect(0, self.centery-int(self.height*0.5), self.width, self.height)

        self.color = (100,255,100)

        #CODE TASK: Adjust size of Player paddle as match progresses to make it more difficult

        self.speed = 9
        self.direction = 0

    def update(self):
        self.centery += self.direction*self.speed
        if self.centery < 0:
            self.centery = 0 + (self.height/2)
        elif self.centery > self.screensize[1]:
            self.centery = self.screensize[1] - (self.height /2)

        self.rect.center = (self.centerx, self.centery)
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screensize[1]-1:
            self.rect.bottom = self.screensize[1]-1

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0,0,0), self.rect, 1)