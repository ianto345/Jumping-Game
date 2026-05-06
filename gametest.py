from roboPlay import *


def manual():
    #Window dimensions for game, currently leaving locked in dimensions similar to a phone
    WIDTH = classes.globalWidth
    HEIGHT = classes.globalHeight

    #Pygame initialization
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True
    font=pygame.font.Font(None, 36)

    #initial values
    dt=0
    dia_pos=pygame.Vector2(WIDTH/2,4*HEIGHT/5)
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
    group_a = ObstacleGroup(HEIGHT / 5, WIDTH, cnst)
    group_b = ObstacleGroup(HEIGHT / 5 - cnst.goal_distance, WIDTH, cnst)
    
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
            block_corners = [(dia_pos.x - cnst.dia_rad, dia_pos.y), (dia_pos.x, dia_pos.y - cnst.dia_rad),
                             (dia_pos.x + cnst.dia_rad, dia_pos.y), (dia_pos.x, dia_pos.y + cnst.dia_rad)]





            if start:
                #if not the first press, look for new jump then add gravity


                # if keys[pygame.K_a]:#TESTING WASD MOVEMENT
                #     if dia_pos.x>cnst.dia_rad:
                #         dx=-1
                #         dia_pos.x = max(cnst.dia_rad, min(dia_pos.x + cnst.x_spd * dt * dx, WIDTH - cnst.dia_rad))
                # if keys[pygame.K_d]:
                #     if dia_pos.x<WIDTH-cnst.dia_rad:
                #         dx=1
                #         dia_pos.x = max(cnst.dia_rad,min(dia_pos.x+cnst.x_spd * dt * dx,WIDTH-cnst.dia_rad))
                # if keys[pygame.K_s]:
                #     dy=1
                #     dia_pos.y += cnst.y_spd * dt * dy
                # if keys[pygame.K_w]:
                #     dy=-1
                #     dia_pos.y += cnst.y_spd * dt * dy




                if keys[pygame.K_a]:#NORMAL JUMPS
                    if dia_pos.x>cnst.dia_rad:
                        dx = -1
                        dy = cnst.dy0
                if keys[pygame.K_d]:
                    if dia_pos.x<WIDTH-cnst.dia_rad:
                        dx = 1
                        dy = cnst.dy0
                dia_pos.x = max(cnst.dia_rad,min(dia_pos.x+cnst.x_spd * dt * dx,WIDTH-cnst.dia_rad))
                dy+=cnst.grav
                dia_pos.y += cnst.y_spd * dt * dy


                #now check to see if dead
                if dia_pos.y>HEIGHT-cnst.dia_rad:
                    alive = False
                    text = font.render("Press space to reset", True, (0,0,0),(255,255,255))
                    txt = text.get_rect()
                    txt.y = HEIGHT / 2
                    txt.centerx = WIDTH / 2
                if group_a.collide(dia_pos, cnst.dia_rad) or group_b.collide(dia_pos, cnst.dia_rad):
                    alive = False
                    text = font.render("Press space to reset", True, (0,0,0),(255,255,255))
                    txt = text.get_rect()
                    txt.y = HEIGHT / 2
                    txt.centerx = WIDTH / 2
            else:
                #if no press yet then wait for first press before moving to avoid gravity building
                if keys[pygame.K_a]:
                    dx = -1
                    dy = cnst.dy0
                    dia_pos.x += cnst.x_spd * dt * dx
                    dy += cnst.grav
                    dia_pos.y += cnst.y_spd * dt * dy
                    start=True
                if keys[pygame.K_d]:
                    dx = 1
                    dy = cnst.dy0
                    dia_pos.x += cnst.x_spd * dt * dx
                    dy += cnst.grav
                    dia_pos.y += cnst.y_spd * dt * dy
                    start = True
            #check to see if we need to "move camera"
            if dia_pos.y<HEIGHT/2:
                #locks visual height of block at middle and makes everything else fall
                fall=dia_pos.y-math.floor(HEIGHT/2)
                dia_pos.y = math.floor(HEIGHT/2)
                #if any line is falling below capped diamond height, then diamond has reached the line so score up
                if group_a.line0.y2 < HEIGHT / 2 <= group_a.line0.y2 - fall or group_b.line0.y2 < HEIGHT / 2 <= group_b.line0.y2 - fall:
                    score+=1
                    score_txt=font.render(str(score),True,(0,0,0),(255,255,255))
                    scoreboard=score_txt.get_rect()
                group_a.fall(fall)
                group_b.fall(fall)
                #check to see if any group full off-screen and if so then move
                if group_a.small1.y1 > HEIGHT:
                    group_a.reset(group_a.line1.y2 - 2 * cnst.goal_distance)
                if group_b.small1.y1 > HEIGHT:
                    group_b.reset(group_b.line1.y2 - 2 * cnst.goal_distance)

            #after moving done, draw
            group_a.draw(screen)
            group_b.draw(screen)

            pygame.draw.polygon(screen, "black", block_corners)
        else: #if dead allow for restart
            if keys[pygame.K_SPACE]:
                text = font.render("Press 'a' or 'd' to jump", True, (0,0,0),(255,255,255))
                txt = text.get_rect()
                txt.y = HEIGHT / 2
                txt.centerx = WIDTH / 2
                # initial values
                dia_pos = pygame.Vector2(screen.get_width() / 2, 4 * screen.get_height() / 5)
                dx = 0
                dy = 0
                start = False
                alive = True
                score = 0
                score_txt = font.render(str(score), True, (0, 0, 0),(255,255,255))
                scoreboard = score_txt.get_rect()
                #reset starting blocks
                group_a.reset(HEIGHT / 5)
                group_b.reset(HEIGHT/5-cnst.goal_distance)

        if not start or not alive:
            screen.blit(text, txt)
        screen.blit(score_txt,scoreboard)
        #finish render and display
        pygame.display.flip()
        #limit to 60 FPS
        #dt gives time in seconds since last frame
        dt=clock.tick(60)/1000

    pygame.quit()
    return score

# RL constant init
EPSILON_DECAY = 0.9999
EPSILON_MIN = 0.05
#state and action init
state = None
direction_timer = None
prev_move = direction_timer

def play(runCount):
    #negative runcount sets manual play
    global epsilon, state
    if runCount < 0:
        return manual()
    #runCount of zero draws
    scores=[]
    drawBool = False
    if runCount == 0:
        drawBool = True
    WIDTH = classes.globalWidth
    HEIGHT = classes.globalHeight
    screen=None
    clock=None


    #pygame initialization for bug testing
    pygame.init()
    if drawBool:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()

    #initial values
    dt=0
    dia_pos=pygame.Vector2(WIDTH/2,4*HEIGHT/5)
    dx=0
    dy=0
    start = False
    alive = True
    score=0

    #generate starting locations of first two levels
    group_a = ObstacleGroup(HEIGHT / 5, WIDTH, cnst)
    group_b = ObstacleGroup(HEIGHT / 5 - cnst.goal_distance, WIDTH, cnst)
    blockList = group_a.all() + group_b.all()

    running = True

    #reward var init
    climbedY=0
    scoreUp=0
    hit_floor=False
    hit_block=False
    #state and action init
    state = get_state(group_a, group_b ,dia_pos)
    direction_timer = choose_action(group_a, group_b , dia_pos , epsilon)
    prev_move = direction_timer

    while running:#start game logic
        #if drawing need to quit with window X
        if drawBool:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        if alive:
            #drawing features for bug test

            if drawBool:
                screen.fill("white")

                #block corners needed only for drawing
                diamond_corners = [(dia_pos.x - cnst.dia_rad, dia_pos.y), (dia_pos.x, dia_pos.y - cnst.dia_rad),
                                 (dia_pos.x + cnst.dia_rad, dia_pos.y), (dia_pos.x, dia_pos.y + cnst.dia_rad)]
            if start:
                #unsure if the start/wait logic needed for roboPlay, but left in for continuity
                if direction_timer < 0: #negative timer jumps left
                    direction_timer += 1
                    if direction_timer >= -1:
                        if dia_pos.x>cnst.dia_rad:
                            dx = -1
                            dy = cnst.dy0
                        direction_timer = choose_action(group_a, group_b , dia_pos , epsilon)
                        prev_move = direction_timer
                        # RL Q update
                        reward = get_reward(climbedY, hit_floor, hit_block, scoreUp)
                        scoreUp = 0
                        prev_state = state
                        state = get_state(group_a, group_b ,dia_pos)
                        update_q(prev_state, prev_move, reward, state)
                        climbedY = 0  # reset so next action starts fresh
                elif direction_timer > 0: #positive timer jumps right
                    direction_timer -= 1
                    if direction_timer <= 1:
                        if dia_pos.x<WIDTH-cnst.dia_rad:
                            dx = 1
                            dy = cnst.dy0
                        direction_timer = choose_action(group_a, group_b , dia_pos , epsilon)
                        prev_move = direction_timer
                        # RL Q update
                        reward = get_reward(climbedY, hit_floor, hit_block, scoreUp)
                        scoreUp = 0
                        prev_state = state
                        state = get_state(group_a, group_b ,dia_pos)
                        update_q(prev_state, prev_move, reward, state)
                        climbedY = 0  # reset so next action starts fresh
                #after checking for jump, move with physics
                dia_pos.x = max(cnst.dia_rad, min(dia_pos.x + cnst.x_spd * dt * dx, WIDTH - cnst.dia_rad))
                dy += cnst.grav
                dia_pos.y += cnst.y_spd * dt * dy
                climbedY -= cnst.y_spd *dt *dy
                #checks for death
                if dia_pos.y > HEIGHT - cnst.dia_rad:
                    hit_floor = True
                    alive = False
                    # RL Q update
                    reward = get_reward(climbedY, hit_floor, hit_block, scoreUp)
                    scoreUp=0
                    prev_state = state
                    state = get_state(group_a, group_b ,dia_pos)
                    update_q(prev_state, prev_move, reward, state)
                    climbedY = 0  # reset so next action starts fresh
                if group_a.collide(dia_pos, cnst.dia_rad) or group_b.collide(dia_pos, cnst.dia_rad):
                    hit_block = True
                    alive = False
                    # RL Q update
                    reward = get_reward(climbedY, hit_floor, hit_block, scoreUp)
                    scoreUp=0
                    prev_state = state
                    state = get_state(group_a, group_b ,dia_pos)
                    update_q(prev_state, prev_move, reward, state)
                    climbedY = 0  # reset so next action starts fresh

            else: #main physics logic for after first move
                if direction_timer < 0: #negative timer jumps left
                    direction_timer += 1
                    if direction_timer >= -1:
                        if dia_pos.x>cnst.dia_rad:
                            dx = -1
                            dy = cnst.dy0
                            dia_pos.x += cnst.x_spd * dt * dx
                            dy += cnst.grav
                            dia_pos.y += cnst.y_spd * dt * dy
                            climbedY -= cnst.y_spd *dt *dy
                            start = True
                        direction_timer = choose_action(group_a, group_b , dia_pos , epsilon)
                        prev_move=direction_timer
                        # RL Q update
                        reward = get_reward(climbedY, hit_floor, hit_block, scoreUp)
                        scoreUp = 0
                        prev_state = state
                        state = get_state(group_a, group_b ,dia_pos)
                        update_q(prev_state, prev_move, reward, state)
                        climbedY = 0  # reset so next action starts fresh
                elif direction_timer >= 0: #positive timer jumps right
                    direction_timer -= 1
                    if direction_timer <= 1:
                        if dia_pos.x<WIDTH-cnst.dia_rad:
                            dx = 1
                            dy = cnst.dy0
                            dia_pos.x += cnst.x_spd * dt * dx
                            dy += cnst.grav
                            dia_pos.y += cnst.y_spd * dt * dy
                            climbedY -= cnst.y_spd *dt *dy
                            start = True
                        direction_timer = choose_action(group_a, group_b , dia_pos , epsilon)
                        prev_move=direction_timer
                        # RL Q update
                        reward = get_reward(climbedY, hit_floor, hit_block, scoreUp)
                        scoreUp = 0
                        prev_state = state
                        state = get_state(group_a, group_b ,dia_pos)
                        update_q(prev_state, prev_move, reward, state)
                        climbedY = 0  # reset so next action starts fresh

                #after moving check for camera movement/fall
            if dia_pos.y < HEIGHT / 2:
                # locks visual height of diamond at middle and makes everything else fall
                fall = dia_pos.y - math.floor(HEIGHT / 2)
                dia_pos.y = math.floor(HEIGHT / 2)
                # if any line is falling below capped diamond height, then diamond has reached the line so score up
                if group_a.line0.y2 < HEIGHT / 2 <= group_a.line0.y2 - fall or group_b.line0.y2 < HEIGHT / 2 <= group_b.line0.y2 - fall:
                    score += 1
                    scoreUp+=1
#                    print(f"Climbed up to {score}")
                group_a.fall(fall)
                group_b.fall(fall)
                climbedY-=fall
                # check to see if any group full off-screen and if so then move
                if group_a.small1.y1 > HEIGHT:
                    group_a.reset(group_a.line1.y2 - 2 * cnst.goal_distance)
                if group_b.small1.y1 > HEIGHT:
                    group_b.reset(group_b.line1.y2 - 2 * cnst.goal_distance)

            if drawBool:   # after moving done, draw if needed
                group_a.draw(screen)
                group_b.draw(screen)

                pygame.draw.polygon(screen, "black", diamond_corners)


        else: #dead so reduce runCount and if zero then quit
            # if score>0:
            #     print(f"Round {runCount} score: {score}")
            scores.append(score)
            epsilon = max(EPSILON_MIN, epsilon * EPSILON_DECAY)
            runCount-=1
            if(runCount <= 0):
                running=False
            else: #reset
                # reward var init
                climbedY = 0
                hit_floor = False
                hit_block = False
                # state and action init
                state = get_state(group_a, group_b ,dia_pos)
                direction_timer = choose_action(group_a, group_b , dia_pos , epsilon)
                dt = 0
                dia_pos = pygame.Vector2(WIDTH/2,4*HEIGHT/5)
                dx = 0
                dy = 0
                start = False
                alive = True
                score = 0
                # reset starting blocks
                group_a.reset(HEIGHT / 5)
                group_b.reset(HEIGHT / 5 - cnst.goal_distance)


        if (drawBool):
            pygame.display.flip()
            # limit to 60 FPS
            # dt gives time in seconds since last frame
            dt = clock.tick(60) / 1000
        else:
            dt = 1/60
    pygame.quit()
    if not drawBool:
        print(f"Avg: {sum(scores)/len(scores):.4f}")
        print(f"Max: {max(scores)}")
    return score

def run(total, shown_step, observe = 1):
    #run the game {total} times with every {shown_step}th game drawn
    #negative total lets manual play
    load_training()
    if total < 0:
        manual()
        return
    elif shown_step >total or shown_step <=0:
        play(total)
    else:
        for x in range(math.floor(total/shown_step)):
            if x % 2 == 1:
                play(0)
            else:
                play(shown_step-1)
    for i in range(observe):
        play(0)
    save_training()

run(1000000,100000, observe = 0)
# manual()
