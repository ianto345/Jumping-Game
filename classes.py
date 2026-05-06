import random
import pygame
import math
from dataclasses import dataclass

@dataclass
class Constants:
    grav: float = 0.25
    dia_rad: int = 15
    small_size: int = 30
    line_thick: int = 40
    gap_width: int = 170
    x_spd: int = 200
    y_spd: int = 250
    goal_distance: int = 500
    dy0: float = -4.0

cnst = Constants()  # single shared instance

globalHeight = 736
globalWidth = 414


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

        x_gap = int(min(abs(self.x1 - pos.x), abs(self.x2 - pos.x)))
        y_gap = int(min(abs(self.y1 - pos.y), abs(self.y2 - pos.y)))

        #check if pos is within x or y bounds of Block to update gap to 0
        if self.x1 < pos.x < self.x2:
            x_gap = 0
        if self.y1 < pos.y < self.y2:
            y_gap = 0
        #print(x_gap + y_gap)
        return x_gap + y_gap < size

class ObstacleGroup: #Group of 4 Blocks
    def __init__(self, goal_y, width, cnst):

        self.small0 = Block(0, 0, 0, 0,"purple")
        self.small1 = Block(0, 0, 0, 0,"purple")
        self.line0 = Block(0, 0, 0, 0,"purple")
        self.line1 = Block(0, 0, 0, 0,"purple")
        self.cnst = cnst
        self.width = width
        self.reset(goal_y)

    def reset(self, goal_y):
        rand_move_group(self.small0, self.small1, self.line0, self.line1,
                        self.cnst.small_size, self.cnst.line_thick,
                        self.cnst.gap_width, goal_y, self.width)

    def fall(self, dist):
        for b in self.all(): b.fall(dist)

    def draw(self, screen):
        for b in self.all(): b.draw(screen)

    def collide(self, pos, size):
        return any(b.collide(pos, size) for b in self.all())

    def all(self):
        return [self.small0, self.small1, self.line0, self.line1]


def rand_move_group(small0,small1,line0,line1, smallsize, linethick, gapwidth, goal_y, width):
    #given a group of line Blocks and the two small Blocks guarding the gap, updates their positions
    #moves them around a new goal height with randomized x locations and guard y gaps
    tile = 10
    color=random.choice(["red","green","blue","yellow","purple"]) #new color fun :)
    #random x coord of gap in line and move line Blocks
    gapx=random.randrange(math.ceil(width/40),width-math.floor(width/40)-gapwidth)
    gapx-=gapx%tile
    line0.update(-5,gapx,goal_y-linethick,goal_y,color)
    line1.update(gapx+gapwidth,width+5,goal_y-linethick,goal_y,color)
    #make random distance from gap for guard below
    dy=random.randrange(-linethick,linethick)/2
    dy-=dy%tile
    x=random.randrange(gapx-smallsize,gapx+smallsize+gapwidth)
    x-=x%tile
    small0.update(x,x+smallsize,goal_y+3*smallsize+dy,goal_y+dy+4*smallsize, color)
    #again for guard above
    dy=random.randrange(-linethick,linethick)/2
    dy-=dy%tile
    x=random.randrange(gapx-smallsize,gapx+smallsize+gapwidth)
    x-=x%tile
    small1.update(x,x+smallsize,goal_y-linethick+dy-4*smallsize,goal_y-linethick-3*smallsize+dy, color)
