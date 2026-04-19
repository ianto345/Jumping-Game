import random
import pygame
import math

class Block: #Block class provides obstacles to avoid
    x1, x2, y1, y2 = 0, 0, 0, 0
    color = "black"

    def __init__(self, x1, x2, y1, y2, color):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.color = color

    def update(self, x1, x2, y1, y2, color):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.color = color

    def fall(self, dist):
        self.y1-=dist
        self.y2-=dist

    def draw(self, scrn):
        pygame.draw.rect(scrn, self.color, (self.x1, self.y1, self.x2-self.x1, self.y2-self.y1))

    #checks for collision with diamond centered at pos(x,y) with corners (size) pixels away from pos
    def collide(self, pos, size):
        #due to equal sides of given diamond, collision with Block happens if walk along x-y bases is < size pixels
        #from closest point of Block

        x_gap = min(abs(self.x1 - pos.x), abs(self.x2 - pos.x))
        y_gap = min(abs(self.y1 - pos.y), abs(self.y2 - pos.y))

        #check if pos is within x or y bounds of Block to update gap to 0
        if self.x1 < pos.x < self.x2:
            x_gap = 0
        if self.y1 < pos.y < self.y2:
            y_gap = 0
        #print(x_gap + y_gap)
        return x_gap + y_gap < size

def rand_move_group(small0,small1,line0,line1, smallsize, linethick, gapwidth, goal_y, width):
    #given a group of line Blocks and the two small Blocks guarding the gap, updates their positions
    #moves them around a new goal height with randomized x locations and guard y gaps
    color=random.choice(["red","green","blue","yellow","purple"]) #new color fun :)
    #random x coord of gap in line and move line Blocks
    gapx=random.randrange(math.ceil(width/40),width-math.floor(width/40)-gapwidth)
    line0.update(-5,gapx,goal_y-linethick,goal_y,color)
    line1.update(gapx+gapwidth,width+5,goal_y-linethick,goal_y,color)
    #make random distance from gap for guard below
    dy=random.randrange(-linethick,linethick)/2
    x=random.randrange(gapx-smallsize,gapx+smallsize+gapwidth)
    small0.update(x,x+smallsize,goal_y+3*smallsize+dy,goal_y+dy+4*smallsize, color)
    #again for guard above
    dy=random.randrange(-linethick,linethick)/2
    x=random.randrange(gapx-smallsize,gapx+smallsize+gapwidth)
    small1.update(x,x+smallsize,goal_y-linethick+dy-4*smallsize,goal_y-linethick-3*smallsize+dy, color)

