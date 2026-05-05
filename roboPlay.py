import classes
from classes import *
from classes import Block

#set up RL algorithm
Q = {}
epsilon = 1.0
# ACTIONS = list(range(-61,0,5)) + list(range(1,62,5))
ACTIONS = [-33,-18, -3, 3, 18, 33]  # left-slow, left-fast, right-fast, right-slow
    #WITH CONSTANTS AT TIME OF WRITING: 46 will always hit floor, 31 maintains height
    # positive numbers will eventually jump right, negative left
    # numbers further from zero == longer wait
    # this method always called as jump made, so dx and dy predictable
ALPHA = 0.1   # learning rate
GAMMA = 0.9  # discount factor

def find_crash_bounds(blocks, pos):
    left_max=-40
    right_max=40
    check_pos = pygame.Vector2(pos.x, pos.y)
    check_blocks_left = []
    check_blocks_right = []
    for block in blocks:
        if check_pos.y - cnst.dia_rad - block.y2 < 126: #max height from a jump is ~125
            if check_pos.x - cnst.dia_rad - block.x2 < 135 and check_pos.x + cnst.dia_rad > block.x1: #40 step traversal in x is 133, check if within max x-traversal
                check_blocks_left.append(block)
            if block.x1 - check_pos.x - cnst.dia_rad < 135 and check_pos.x - cnst.dia_rad < block.x2:
                check_blocks_right.append(block)

    dx=-1
    dy=cnst.dy0
    if check_pos.x - cnst.dia_rad <= 1:
        left_max=0
    for i in range(41): #check next iterations for crash
        if -i>left_max:
            for block in check_blocks_left:
                if block.collide(check_pos, cnst.dia_rad):
                    left_max=-i
                    break
            check_pos.x = max(cnst.dia_rad, min(check_pos.x + cnst.x_spd * 1/60 * dx, classes.globalWidth - cnst.dia_rad))
            dy += cnst.grav
            check_pos.y += cnst.y_spd * 1/60 * dy
    dx = 1
    dy = cnst.dy0
    check_pos.x=pos.x
    check_pos.y=pos.y
    if check_pos.x + cnst.dia_rad >= classes.globalWidth-1:
        right_max = 0
    for i in range(41): #check next iterations for crash
        if i<right_max:
            for block in check_blocks_right:
                if block.collide(check_pos, cnst.dia_rad):
                    right_max=i
                    break
            check_pos.x = max(cnst.dia_rad, min(check_pos.x + cnst.x_spd * 1/60 * dx, classes.globalWidth - cnst.dia_rad))
            dy += cnst.grav
            check_pos.y += cnst.y_spd * 1/60 * dy
    return [left_max,right_max]

def get_q(state, action):
    return Q.get(state, {}).get(action,1.0)

def set_q(state, action, value):
    if state not in Q:
        Q[state] = {}
    Q[state][action] = value

def in_reach(block, pos): #find in y within two max jumps or x within one (y harder to control)
    return pos.y - cnst.dia_rad - block.y2 < 250 and (pos.x - cnst.dia_rad - block.x2 < 135 or block.x1 - cnst.dia_rad - pos.x < 135)

def get_state(group_a,group_b, pos):#return a tuple with x and y coordinates of obstacles and diamond
    tile = 10
    OFFSCREEN = -20*classes.globalHeight

    if group_a.line0.y1>group_b.line0.y1:
        under = group_a
        over = group_b
    else:
        under = group_b
        over = group_a
    blocks=[under.small1,over.small0,over.line0,over.small1] #makes minimal list of blocks to watch

    result = []

    for b in blocks:
        if(in_reach(b,pos)):
            rx = b.x1 - pos.x
            ry = b.y1 - pos.y
            result += [rx-rx%tile,ry-ry%tile]
        else:
            result += [OFFSCREEN, OFFSCREEN]
    return tuple(result)

def choose_action(group_a, group_b, pos, epsilon): #decide to randomly test or listen to Q-chart
    bound=find_crash_bounds(group_a.all()+group_b.all(), pos)
    if bound[0]>-5 and bound[1]<5: #if too small bounds then just crash :(
        return 10
    left=[] if bound[0]>-3 else list(range(3,-bound[0],15))
    acts=[] if bound[1]<3 else list(range(3,bound[1],15))
    for x in left:
        acts.insert(0,-x)#create truncated action list
    if random.random() < epsilon:
        return random.choice(acts)  # explore: random action
    else:
        q_values = {a: get_q(get_state(group_a,group_b,pos), a) for a in acts}
        return max(q_values, key=q_values.get)  # exploit: best known action

def update_q(state, action, reward, next_state, valid_actions=None):
    actions = valid_actions or ACTIONS
    best_next = max(get_q(next_state, a) for a in actions)
    old_q = get_q(state, action)
    new_q = old_q + ALPHA * (reward + GAMMA * best_next - old_q)
    set_q(state, action, new_q)
    # print("Action: "+str(action)+"\tReward: "+str(reward))

def get_reward(climbed, hit_floor, hit_block, scoreUp):
    if hit_block:
        return -20
    if hit_floor:
        return -100
    return climbed*1000/classes.globalHeight + scoreUp*10

def save_training(path="training.json"):
    import json
    global Q, epsilon
    data = {
        "epsilon": epsilon,
        "Q": {str(k): v for k, v in Q.items()}
    }
    with open(path, "w") as f:
        json.dump(data, f)

def load_training(path="training.json"):
    import json, os, ast
    global Q, epsilon
    if not os.path.exists(path):
        return
    with open(path, "r") as f:
        data = json.load(f)
    epsilon = data["epsilon"]
    Q = {ast.literal_eval(k): v for k, v in data["Q"].items()}