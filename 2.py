from random import randint

import pygame
pygame.init()

# MUSIC
pygame.mixer.music.load('sounds/Main_theme.wav')
pygame.mixer.music.play(-1)

display_width = 900     # 1275 - full screen
display_height = 770    # 750 - full screen

win = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("Vanishing of Hao Melnik")

time = pygame.time.Clock()

walkRight = [pygame.image.load('sprites/R1.png'),
             pygame.image.load('sprites/R2.png'),
             pygame.image.load('sprites/R3.png'),
             pygame.image.load('sprites/R4.png'),
             pygame.image.load('sprites/R5.png'),
             pygame.image.load('sprites/R6.png')]

walkLeft = [pygame.image.load('sprites/L1.png'),
            pygame.image.load('sprites/L2.png'),
            pygame.image.load('sprites/L3.png'),
            pygame.image.load('sprites/L4.png'),
            pygame.image.load('sprites/L5.png'),
            pygame.image.load('sprites/L6.png')]

bg = pygame.image.load('sprites/Background.png')

char = [pygame.image.load('sprites/standing1.png'),
        pygame.image.load('sprites/standing2.png'),
        pygame.image.load('sprites/standing3.png'),
        pygame.image.load('sprites/standing4.png')]

# MAIM CHARACTER


class Character(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 10
        self.Jump = False
        self.count = 10
        self.left = False
        self.right = False
        self.walk = 0
        self.stand = 1
        self.hitbox = (self.x + 26, self.y, 28, 30)

    def display(self, win):
        if self.walk + 1 >= 25:
            self.walk = 0

        if self.left:
            win.blit(walkLeft[self.walk // 6], (self.x, self.y))
            self.walk += 1

        elif self.right:
            win.blit(walkRight[self.walk // 6], (self.x, self.y))
            self.walk += 1

        else:
            print(self.stand)
            win.blit(char[self.stand // 2], (self.x, self.y))
            if self.stand == 6:
                self.stand = 0
            else:
                self.stand += 1

        self.hitbox = (self.x + 26, self.y, 28, 80)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

# SHOOTING


class Bullet(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.velocity = 8 * facing

    def display(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

# ENEMY


class Villain(object):
    animationRight = [pygame.image.load('sprites/E1.png'),
                      pygame.image.load('sprites/E2.png'),
                      pygame.image.load('sprites/E3.png'),
                      pygame.image.load('sprites/E4.png'),
                      pygame.image.load('sprites/E5.png'),
                      pygame.image.load('sprites/E6.png'),
                      pygame.image.load('sprites/E7.png'),
                      pygame.image.load('sprites/E8.png'),
                      pygame.image.load('sprites/E9.png'),
                      pygame.image.load('sprites/E10.png')]

    animationLeft = [pygame.image.load('sprites/A1.png'),
                     pygame.image.load('sprites/A2.png'),
                     pygame.image.load('sprites/A3.png'),
                     pygame.image.load('sprites/A4.png'),
                     pygame.image.load('sprites/A5.png'),
                     pygame.image.load('sprites/A6.png'),
                     pygame.image.load('sprites/A7.png'),
                     pygame.image.load('sprites/A8.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.count = 0
        self.velocity = 3
        self.path = [self.x, self.end]
        self.hitbox = (self.x + 70, self.y + 50, 50, 80)


    def display(self, win):
        self.move()
        if self.count + 1 >= 25:
            self.count = 0

        if self.velocity > 0:
            win.blit(self.animationRight[self.count //3], (self.x, self.y))
            self.count += 1
        else:
            win.blit(self.animationLeft[self.count // 3], (self.x, self.y))
            self.count += 1

        self.hitbox = (self.x + 10, self.y - 50, 100, 100)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.velocity > 0:
            if self.x + self.velocity < self.path[1]:
                self.x += self.velocity
            else:
                self.velocity = self.velocity * -1
                self.count = 0
        else:
            if self.x - self.velocity > self.path[0]:
                self.x += self.velocity
            else:
                self.velocity = self.velocity * -1
                self.count = 0

    def hit(self):
        print('HIT')


def win_update():
    win.blit(bg, (0, 0))
    knight.display(win)
    enemy.display(win)
    for arrow in arrows:
        arrow.display(win)

    pygame.display.update()


knight = Character(450, 650, 50, 50)
enemy = Villain(10, 680, 50, 50, 800)
arrows = []
run = True
while run:
    time.tick(25)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(event)
            run = False

    for arrow in arrows:
        if arrow.y - arrow.radius < enemy.hitbox[1] + enemy.hitbox[3] and arrow.y + arrow.radius > enemy.hitbox[1]:
            if arrow.x + arrow.radius > enemy.hitbox[0] and arrow.x - arrow.radius < enemy.hitbox[1] + enemy.hitbox[2]:
                enemy.hit()
                arrows.pop(arrows.index(arrow))

        if arrow.x < 700 and arrow.x > 0:
            arrow.x += arrow.velocity
        else:
            arrows.pop(arrows.index(arrow))

    keys = pygame.key.get_pressed()

# MOVEMENT

    if keys[pygame.K_SPACE]:
        if knight.left:
            facing = -3
        else:
            facing = 0
        if len(arrows) < 4:
            arrows.append(Bullet(round(knight.x + knight.width // 2),
                                 round(knight.y + knight.height // 2), 6, (0, 0, 0), facing))

    if keys[pygame.K_LEFT] and knight.x > knight.velocity:
        knight.x -= knight.velocity
        knight.left = True
        knight.right = False

    elif keys[pygame.K_RIGHT] and knight.x < 900 - knight.width - knight.velocity:
        knight.x += knight.velocity
        knight.right = True
        knight.left = False

    else:
        knight.right = False
        knight.left = False
        knight.walk = 0

# JUMPING
    if not knight.Jump:
        if keys[pygame.K_UP]:
            knight.Jump = True
            knight.right = False
            knight.left = False
            knight.walk = 0
    else:
        if knight.count >= -10:
            down = 1
            if knight.count < 0:
                down = -1
            knight.y -= (knight.count ** 2) * 0.2 * down
            knight.count -= 1
        else:
            knight.Jump = False
            knight.count = 10

    win_update()

pygame.quit()
