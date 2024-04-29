import sys
import pygame
import pygame as pg

pygame.init()
screen = pygame.display.set_mode((640, 480))
pg.mixer.music.load('mario.mp3')
pg.mixer.music.play()
background_image = pygame.image.load('map.png')
animation_set_right = [pygame.image.load(f"r{i}.png") for i in range(1, 6)]
animation_set_left = [pygame.image.load(f"l{i}.png") for i in range(1, 6)]
animation_set_None=pygame.image.load("0.png")
clock = pygame.time.Clock()
i = 0
x=100
y=340
move=None
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x-=10
                move="left"
            elif event.key == pygame.K_RIGHT:
                x+=10
                move="right"

    if move==None:
        screen.blit(animation_set_None,(x,y))
    elif move=="right":
        screen.blit(animation_set_right[i // 12], (x, y))
        i += 1
        if i == 60:
            i = 0
            move=None
    elif move=="left":
        screen.blit(animation_set_left[i // 12], (x, y))
        i += 1
        if i == 60:
            i = 0
            move=None
    pygame.display.flip()
    clock.tick(60)
    screen.blit(background_image, (0, 0))
    pygame.display.flip()