import classes
from classes import *
import torch
import torch.nn as nn
from collections import deque
import torch.optim as optim


# ACTIONS = list(range(-61,0,5)) + list(range(1,62,5))
ACTIONS = [-33,-18, -3, 3, 18, 33]  # left-slow, left-fast, right-fast, right-slow
    #WITH CONSTANTS AT TIME OF WRITING: 46 will always hit floor, 31 maintains height
    # positive numbers will eventually jump right, negative left
    # numbers further from zero == longer wait
    # this method always called as jump made, so dx and dy predictable
GAMMA = 0.99  # discount factor

# def find_crash_bounds(blocks, pos):
#     left_max=-40
#     right_max=40
#     check_pos = pygame.Vector2(pos.x, pos.y)
#     check_blocks_left = []
#     check_blocks_right = []
#     for block in blocks:
#         if check_pos.y - cnst.dia_rad - block.y2 < 126: #max height from a jump is ~125
#             if check_pos.x - cnst.dia_rad - block.x2 < 135 and check_pos.x + cnst.dia_rad > block.x1: #40 step traversal in x is 133, check if within max x-traversal
#                 check_blocks_left.append(block)
#             if block.x1 - check_pos.x - cnst.dia_rad < 135 and check_pos.x - cnst.dia_rad < block.x2:
#                 check_blocks_right.append(block)
#
#     dx=-1
#     dy=cnst.dy0
#     if check_pos.x - cnst.dia_rad <= 2:
#         left_max=0
#     for i in range(-left_max): #check next iterations for crash
#         check_pos.x = max(cnst.dia_rad, min(check_pos.x + cnst.x_spd * 1/60 * dx, classes.globalWidth - cnst.dia_rad))
#         dy += cnst.grav
#         check_pos.y += cnst.y_spd * 1/60 * dy
#         for block in check_blocks_left:
#             if block.collide(check_pos, cnst.dia_rad):
#                 left_max=-i
#                 break
#         if -left_max <= i:
#             break
#     dx = 1
#     dy = cnst.dy0
#     check_pos.x=pos.x
#     check_pos.y=pos.y
#     if check_pos.x + cnst.dia_rad >= classes.globalWidth-2:
#         right_max = 0
#     for i in range(right_max): #check next iterations for crash
#         check_pos.x = max(cnst.dia_rad, min(check_pos.x + cnst.x_spd * 1/60 * dx, classes.globalWidth - cnst.dia_rad))
#         dy += cnst.grav
#         check_pos.y += cnst.y_spd * 1/60 * dy
#         for block in check_blocks_right:
#             if block.collide(check_pos, cnst.dia_rad):
#                 right_max=i
#                 break
#         if right_max <= i:
#             break
#     return [left_max,right_max]

def in_reach(block, pos): #find in y within two max jumps or x within one (y harder to control)
    return pos.y - cnst.dia_rad - block.y2 < 250 and (pos.x - cnst.dia_rad - block.x2 < 135 or block.x1 - cnst.dia_rad - pos.x < 135)


class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_size, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, action_size)
        )
    def forward(self, x):
        return self.net(x)



class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)

    def __len__(self):
        return len(self.buffer)


BATCH_SIZE = 64
TARGET_UPDATE = 50  # how often to sync target network

act_size = len(ACTIONS)
#groups * blocks_per_group * amount_coords + amount_pos_coords. 2*4*2+2 = 18

policy_net = DQN(12, act_size)
target_net = DQN(12, act_size)
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

optimizer = optim.Adam(policy_net.parameters(), lr=0.0001)
buffer = ReplayBuffer()
steps = 0




def train_step():
    if len(buffer) < BATCH_SIZE:
        return  # wait until buffer has enough experience

    batch = buffer.sample(BATCH_SIZE)
    states, actions, rewards, next_states, dones = zip(*batch)

    # convert to tensors
    states = torch.tensor(states, dtype=torch.float32)
    next_states = torch.tensor(next_states, dtype=torch.float32)
    actions = torch.tensor([ACTIONS.index(a) for a in actions], dtype=torch.long)
    rewards = torch.tensor(rewards, dtype=torch.float32)
    dones = torch.tensor(dones, dtype=torch.float32)

    # what our network currently predicts for each state
    predicted_q = policy_net(states).gather(1, actions.unsqueeze(1)).squeeze()

    # what we're aiming for - target net gives stable bootstrap target
    with torch.no_grad():
        best_next_q = target_net(next_states).max(1).values
        target_q = rewards + GAMMA * best_next_q * (1 - dones)

    loss = nn.HuberLoss()(predicted_q, target_q)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    # print(f"loss: {loss.item():.4f}, predicted_q mean: {predicted_q.mean().item():.4f}, target_q mean: {target_q.mean().item():.4f}")


def maybe_update_target():
    global steps
    steps += 1
    if steps % TARGET_UPDATE == 0:
        target_net.load_state_dict(policy_net.state_dict())


def choose_action(group_a, group_b, pos):  # decide to randomly test or listen to Q-chart
    if random.random() < cnst.epsilon:
        return random.choice(ACTIONS)  # explore: random action

    state = get_state_tensor(group_a,group_b, pos)  # new helper below
    with torch.no_grad():
        q_values = policy_net(state).squeeze()
    return ACTIONS[q_values.argmax().item()]


def get_state(group_a,group_b, pos):#return a tuple with x and y coordinates of obstacles and diamond
    if group_a.line0.y1>group_b.line0.y1:
        under = group_a
        over = group_b
    else:
        under = group_b
        over = group_a
    blocks=[under.small0,under.line0,under.small1,over.small0,over.line0,over.small1] #makes minimal list of blocks to watch

    result = []

    for b in blocks:
        rx = b.x1 - pos.x
        ry = b.y1 - pos.y
        result += [rx / classes.globalWidth, ry / classes.globalHeight]
    return tuple(result)

def get_state_tensor(group_a, group_b, pos):
    state = get_state(group_a, group_b, pos)  # reuses old tabular Q state
    return torch.tensor(state, dtype=torch.float32).unsqueeze(0)

def get_reward(climbed, hit_floor, hit_block, scoreUp):
    if hit_block:
        return -1
    if hit_floor:
        return -1.5
    return climbed/classes.globalHeight + scoreUp*2

def save_training(path="model.pt"):
    torch.save({
        "policy": policy_net.state_dict(),
        "target": target_net.state_dict(),
        "optimizer": optimizer.state_dict(),
        "epsilon": cnst.epsilon,
        "steps": steps,
        "buffer": list(buffer.buffer)
    }, path)
    print(f"Saved training - epsilon: {cnst.epsilon:.4f}, steps: {steps}")


def load_training(path="model.pt"):
    import os
    global steps
    if not os.path.exists(path):
        return
    data = torch.load(path, weights_only=False)  # weights_only=False needed for buffer
    policy_net.load_state_dict(data["policy"])
    target_net.load_state_dict(data["target"])
    optimizer.load_state_dict(data["optimizer"])
    cnst.epsilon = data["epsilon"]
    steps = data["steps"]
    # print(f"Loaded training - epsilon: {cnst.epsilon:.4f}, steps: {steps}")
    if "buffer" in data:
        buffer.buffer.extend(data["buffer"])