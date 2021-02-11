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
pipe_rect_bottom = []
pipe_rect_top = []
pipe_vel = 0.5

def gen_pipes(y_pos):
    pipe_rect_bottom.append(pygame.Rect(DISPLAY_SIZE[0],90 - 64 + y_pos,32,64))
    pipe_rect_top.append(pygame.Rect(DISPLAY_SIZE[0],90 - 64 -64 - 35 + y_pos,32,64))

def random_num(a,b):
    x = random.randint(a,b)
    return x

bird_img = pygame.image.load("assets/bird.png")
grass_img = pygame.image.load("assets/grass.png")
pipe_img = pygame.image.load("assets/pipe.png")
coin_img = pygame.image.load("assets/coin.png")

TILE_SIZE = 8

bird_rect = pygame.Rect(30, 30, bird_img.get_width(), bird_img.get_height())

y_momentum = 0
Y_VEL = 0.2

JUMP_FORCE = 3.5

alive = True
start  = True

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

    #tiles
    tile_rect = []
    x_1 = 0
    for tile in ground:
        if tile == '0':
            display.blit(grass_img, (x_1 * TILE_SIZE - scroll, 90 - 8))
            display.blit(grass_img, (x_1 * TILE_SIZE - scroll + DISPLAY_SIZE[0], 90 - 8))
            tile_rect.append(pygame.Rect(x_1 * TILE_SIZE - scroll, 90 - 8, TILE_SIZE, TILE_SIZE))
            tile_rect.append(pygame.Rect(x_1 * TILE_SIZE - scroll + DISPLAY_SIZE[0],90-8,TILE_SIZE,TILE_SIZE))
        x_1 += 1

    #pipes
    ticks += 1
    if ticks == 60:
        y_pos =random_num(10,40)
        gen_pipes(y_pos)
        ticks = 0

    for pipe in pipe_rect_bottom:
        pipe.x -= pipe_vel
        if pipe.x <= 0:
            pipe_rect_bottom.pop(0)
    for pipe in pipe_rect_top: 
        pipe.x -= pipe_vel
        if pipe.x <= 0:
            pipe_rect_top.pop(0)

    for pipe in pipe_rect_bottom:
        display.blit(pipe_img,(pipe.x,pipe.y))
    for pipe in pipe_rect_top:
        display.blit(pygame.transform.flip(pipe_img,True,True),(pipe.x,pipe.y))

    #pipe collision
    for pipe in pipe_rect_bottom:
        if bird_rect.colliderect(pipe):
            alive = False
            pipe_vel = 0
    for pipe in pipe_rect_top:
        if bird_rect.colliderect(pipe):
            alive = False
            pipe_vel = 0        

    #ground collision
    for tile in tile_rect:
        if bird_rect.colliderect(tile):
            bird_rect.bottom = tile.top
            alive = False
            game_over = 0

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

    display.blit(bird_img, (bird_rect.x, bird_rect.y))
    window.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    time.tick(60)
