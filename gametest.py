import pygame
import math
from classes import Block
from classes import rand_move_group

#Window dimensions for game, currently leaving locked in dimensions similar to a phone
WIDTH = 414
HEIGHT = 736

#Pygame initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
font=pygame.font.Font(None, 36)


#Game physics constants
GRAV=0.25
SIZE=15
SMALLSIZE=30
LINETHICK=40
GAPWIDTH=170
XSPEED=200
YSPEED=250
GOALDISTANCE=500
DY0=-4

#initial values
dt=0
block_pos=pygame.Vector2(WIDTH/2,4*HEIGHT/5)
dx=0
dy=0
start = False
alive = True
text=font.render("Press 'a' or 'd' to jump", True, (0,0,0),(255,255,255))
txt=text.get_rect()
txt.y=HEIGHT/2
txt.centerx=WIDTH/2
score=0
score_txt=font.render(str(score),True,(0,0,0),(255,255,255))
scoreboard=score_txt.get_rect()
scoreboard.x=10
scoreboard.y=10

#generate starting locations of first two levels
small_a0 = Block(0,0,0,0,"purple")
small_a1 = Block(0,0,0,0,"purple")
line_a0 = Block(0,0,0,0,"purple")
line_a1 = Block(0,0,0,0,"purple")
rand_move_group(small_a0,small_a1,line_a0,line_a1,SMALLSIZE,LINETHICK,GAPWIDTH,HEIGHT/5,WIDTH)

small_b0 = Block(0,0,0,0,"purple")
small_b1 = Block(0,0,0,0,"purple")
line_b0 = Block(0,0,0,0,"purple")
line_b1 = Block(0,0,0,0,"purple")
rand_move_group(small_b0,small_b1,line_b0,line_b1,SMALLSIZE,LINETHICK,GAPWIDTH,HEIGHT/5-GOALDISTANCE,WIDTH)
while running:
    #looking for window X press to close loop and window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    keys = pygame.key.get_pressed()
    if alive:
        # fill screen with white background to clear previous loop
        screen.fill("white")
        #Render here
        block_corners = [(block_pos.x - SIZE, block_pos.y), (block_pos.x, block_pos.y - SIZE),
                         (block_pos.x + SIZE, block_pos.y), (block_pos.x, block_pos.y + SIZE)]





        if start:
            #if not the first press, look for new jump then add gravity

            if keys[pygame.K_a]:
                if block_pos.x>SIZE:
                    dx = -1
                    dy = DY0
            if keys[pygame.K_d]:
                if block_pos.x<WIDTH-SIZE:
                    dx = 1
                    dy = DY0
            block_pos.x = max(SIZE,min(block_pos.x+XSPEED * dt * dx,WIDTH-SIZE))
            dy+=GRAV
            block_pos.y += YSPEED * dt * dy
            #now check to see if dead
            if block_pos.y>HEIGHT-SIZE:
                alive = False
                text = font.render("Press space to reset", True, (0,0,0),(255,255,255))
                txt = text.get_rect()
                txt.y = HEIGHT / 2
                txt.centerx = WIDTH / 2
            if (small_a0.collide(block_pos,SIZE) or small_a1.collide(block_pos,SIZE) or small_b0.collide(block_pos,SIZE)
                    or small_b1.collide(block_pos,SIZE) or line_a0.collide(block_pos,SIZE) or
                    line_a1.collide(block_pos,SIZE) or line_b0.collide(block_pos,SIZE) or line_b1.collide(block_pos,SIZE)):
                alive = False
                text = font.render("Press space to reset", True, (0,0,0),(255,255,255))
                txt = text.get_rect()
                txt.y = HEIGHT / 2
                txt.centerx = WIDTH / 2
        else:
            #if no press yet then wait for first press before moving to avoid gravity building
            if keys[pygame.K_a]:
                dx = -1
                dy = DY0
                block_pos.x += XSPEED * dt * dx
                dy += GRAV
                block_pos.y += YSPEED * dt * dy
                start=True
            if keys[pygame.K_d]:
                dx = 1
                dy = DY0
                block_pos.x += XSPEED * dt * dx
                dy += GRAV
                block_pos.y += YSPEED * dt * dy
                start = True
        #check to see if we need to "move camera"
        if block_pos.y<HEIGHT/2:
            #locks visual height of block at middle and makes everything else fall
            fall=block_pos.y-math.floor(HEIGHT/2)
            block_pos.y = math.floor(HEIGHT/2)
            #if any line is falling below capped diamond height, then diamond has reached the line so score up
            if line_a0.y2 < HEIGHT / 2 <= line_a0.y2 - fall or line_b0.y2 < HEIGHT / 2 <= line_b0.y2 - fall:
                score+=1
                score_txt=font.render(str(score),True,(0,0,0),(255,255,255))
                scoreboard=score_txt.get_rect()
            small_a0.fall(fall)
            small_a1.fall(fall)
            small_b0.fall(fall)
            small_b1.fall(fall)
            line_a0.fall(fall)
            line_a1.fall(fall)
            line_b0.fall(fall)
            line_b1.fall(fall)
            #check to see if any group full off-screen and if so then move
            if small_a1.y1>HEIGHT:
                rand_move_group(small_a0, small_a1, line_a0, line_a1, SMALLSIZE, LINETHICK, GAPWIDTH,
                                line_a1.y2-2*GOALDISTANCE, WIDTH)
            if small_b1.y1>HEIGHT:
                rand_move_group(small_b0, small_b1, line_b0, line_b1, SMALLSIZE, LINETHICK, GAPWIDTH,
                                line_b1.y2 - 2 * GOALDISTANCE, WIDTH)

        #after moving done, draw
        small_a0.draw(screen)
        small_a1.draw(screen)
        line_a0.draw(screen)
        line_a1.draw(screen)

        small_b0.draw(screen)
        small_b1.draw(screen)
        line_b0.draw(screen)
        line_b1.draw(screen)

        pygame.draw.polygon(screen, "black", block_corners)
    else: #if dead allow for restart
        if keys[pygame.K_SPACE]:
            text = font.render("Press 'a' or 'd' to jump", True, (0,0,0),(255,255,255))
            txt = text.get_rect()
            txt.y = HEIGHT / 2
            txt.centerx = WIDTH / 2
            # initial values
            dt = 0
            block_pos = pygame.Vector2(screen.get_width() / 2, 4 * screen.get_height() / 5)
            dx = 0
            dy = 0
            start = False
            alive = True
            score = 0
            score_txt = font.render(str(score), True, (0, 0, 0),(255,255,255))
            scoreboard = score_txt.get_rect()
            #reset starting blocks
            rand_move_group(small_a0, small_a1, line_a0, line_a1, SMALLSIZE, LINETHICK, GAPWIDTH, HEIGHT / 5, WIDTH)
            rand_move_group(small_b0,small_b1,line_b0,line_b1,SMALLSIZE,LINETHICK,GAPWIDTH,HEIGHT/5-GOALDISTANCE,WIDTH)

    if not start or not alive:
        screen.blit(text, txt)
    screen.blit(score_txt,scoreboard)
    #finish render and display
    pygame.display.flip()
    #limit to 60 FPS
    #dt gives time in seconds since last frame
    dt=clock.tick(60)/1000

pygame.quit()


