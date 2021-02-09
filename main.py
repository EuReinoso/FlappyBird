import pygame, sys,random

pygame.init()

WINDOW_SIZE = (640, 480)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Flappy Bird")

DISPLAY_SIZE = (120, 90)
display = pygame.Surface(DISPLAY_SIZE)

loop = True
time = pygame.time.Clock()

ground = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0','0','0','0','0']
pipes = ['0', '0', '0', '0', '0','0', '0', '0', '0', '0']

def random_num(a,b):
    x = random.randint(a,b)
    return x

random_x_pipe = random_num(2,50)
random_y_pipe = random_num(2,50)


bird_img = pygame.image.load("assets/bird.png")
grass_img = pygame.image.load("assets/grass.png")
pipe_img = pygame.image.load("assets/pipe.png")
coin_img = pygame.image.load("assets/coin.png")

TILE_SIZE = 8

bird_rect = pygame.Rect(30, 30, bird_img.get_width(), bird_img.get_height())

y_momentum = 0
Y_VEL = 0.2

JUMP_FORCE = 4

alive = True

ticks = 0

scroll = 0
scroll_vel = 0.5
while loop:

    display.fill((135, 206, 235))

    #scrolling
    if alive:
        scroll += scroll_vel
        if scroll >= 120:
            scroll = 0
            random_x_pipe = random_num(2,10)
            random_y_pipe = random_num(2,10)


    #tiles
    tile_rect = []
    x = 0
    for tile in ground:
        if tile == '0':
            display.blit(grass_img, (x * TILE_SIZE - scroll, 90 - 8))
            display.blit(grass_img, (x * TILE_SIZE - scroll + DISPLAY_SIZE[0], 90 - 8))
            tile_rect.append(pygame.Rect(x * TILE_SIZE - scroll, 90 - 8, TILE_SIZE, TILE_SIZE))
            tile_rect.append(pygame.Rect(x * TILE_SIZE - scroll + DISPLAY_SIZE[0],90-8,TILE_SIZE,TILE_SIZE))
        x += 1

    #pipes

    if ticks == random_num(1,60):
        display.blit(pipe_img,(random_num(1,120) * 16 - scroll + DISPLAY_SIZE[0],90-64 + random_y_pipe))


    #ground collision
    for tile in tile_rect:
        if bird_rect.colliderect(tile):
            bird_rect.bottom = tile.top
            alive = False

    #gravity
    bird_rect.y += y_momentum
    y_momentum += Y_VEL
    if y_momentum >= 2:
        y_momentum = 2

    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: #jump
                if alive:
                    y_momentum -= JUMP_FORCE
    #timer
    ticks += 1
    if ticks >= 60:
        ticks = 0

    display.blit(bird_img, (bird_rect.x, bird_rect.y))
    window.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    time.tick(60)
