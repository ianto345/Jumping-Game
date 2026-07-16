from DQN import *


def manual():
    # Window dimensions for game, currently leaving locked in dimensions similar to a phone
    WIDTH = classes.globalWidth
    HEIGHT = classes.globalHeight

    # Pygame initialization
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font(None, 36)

    # initial values
    dt = 0
    dia_pos = pygame.Vector2(WIDTH / 2, 4 * HEIGHT / 5)
    dx = 0
    dy = 0
    start = False
    alive = True
    text = font.render("Press 'a' or 'd' to jump", True, (0, 0, 0), (255, 255, 255))
    txt = text.get_rect()
    txt.y = HEIGHT / 2
    txt.centerx = WIDTH / 2
    score = 0
    score_txt = font.render(str(score), True, (0, 0, 0), (255, 255, 255))
    scoreboard = score_txt.get_rect()
    scoreboard.x = 10
    scoreboard.y = 10

    # generate starting locations of first two levels
    group_a = ObstacleGroup(HEIGHT / 5, WIDTH, cnst)
    group_b = ObstacleGroup(HEIGHT / 5 - cnst.goal_distance, WIDTH, cnst)

    while running:
        # looking for window X press to close loop and window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if alive:
            # fill screen with white background to clear previous loop
            screen.fill("white")
            # Render here
            block_corners = [(dia_pos.x - cnst.dia_rad, dia_pos.y), (dia_pos.x, dia_pos.y - cnst.dia_rad),
                             (dia_pos.x + cnst.dia_rad, dia_pos.y), (dia_pos.x, dia_pos.y + cnst.dia_rad)]

            if start:
                # if not the first press, look for new jump then add gravity

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

                if keys[pygame.K_a]:  # NORMAL JUMPS
                    if dia_pos.x > cnst.dia_rad:
                        dx = -1
                        dy = cnst.dy0
                if keys[pygame.K_d]:
                    if dia_pos.x < WIDTH - cnst.dia_rad:
                        dx = 1
                        dy = cnst.dy0
                dia_pos.x = max(cnst.dia_rad, min(dia_pos.x + cnst.x_spd * dt * dx, WIDTH - cnst.dia_rad))
                dy += cnst.grav
                dia_pos.y += cnst.y_spd * dt * dy

                # now check to see if dead
                if dia_pos.y > HEIGHT - cnst.dia_rad:
                    alive = False
                    text = font.render("Press space to reset", True, (0, 0, 0), (255, 255, 255))
                    txt = text.get_rect()
                    txt.y = HEIGHT / 2
                    txt.centerx = WIDTH / 2
                if group_a.collide(dia_pos, cnst.dia_rad) or group_b.collide(dia_pos, cnst.dia_rad):
                    alive = False
                    text = font.render("Press space to reset", True, (0, 0, 0), (255, 255, 255))
                    txt = text.get_rect()
                    txt.y = HEIGHT / 2
                    txt.centerx = WIDTH / 2
            else:
                # if no press yet then wait for first press before moving to avoid gravity building
                if keys[pygame.K_a]:
                    dx = -1
                    dy = cnst.dy0
                    dia_pos.x += cnst.x_spd * dt * dx
                    dy += cnst.grav
                    dia_pos.y += cnst.y_spd * dt * dy
                    start = True
                if keys[pygame.K_d]:
                    dx = 1
                    dy = cnst.dy0
                    dia_pos.x += cnst.x_spd * dt * dx
                    dy += cnst.grav
                    dia_pos.y += cnst.y_spd * dt * dy
                    start = True
            # check to see if we need to "move camera"
            if dia_pos.y < HEIGHT / 2:
                # locks visual height of block at middle and makes everything else fall
                fall = dia_pos.y - math.floor(HEIGHT / 2)
                dia_pos.y = math.floor(HEIGHT / 2)
                # if any line is falling below capped diamond height, then diamond has reached the line so score up
                if group_a.line0.y2 < HEIGHT / 2 <= group_a.line0.y2 - fall or group_b.line0.y2 < HEIGHT / 2 <= group_b.line0.y2 - fall:
                    score += 1
                    score_txt = font.render(str(score), True, (0, 0, 0), (255, 255, 255))
                    scoreboard = score_txt.get_rect()
                group_a.fall(fall)
                group_b.fall(fall)
                # check to see if any group full off-screen and if so then move
                if group_a.small1.y1 > HEIGHT:
                    group_a.reset(group_a.line1.y2 - 2 * cnst.goal_distance)
                if group_b.small1.y1 > HEIGHT:
                    group_b.reset(group_b.line1.y2 - 2 * cnst.goal_distance)

            # after moving done, draw
            group_a.draw(screen)
            group_b.draw(screen)

            pygame.draw.polygon(screen, "black", block_corners)
        else:  # if dead allow for restart
            if keys[pygame.K_SPACE]:
                text = font.render("Press 'a' or 'd' to jump", True, (0, 0, 0), (255, 255, 255))
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
                score_txt = font.render(str(score), True, (0, 0, 0), (255, 255, 255))
                scoreboard = score_txt.get_rect()
                # reset starting blocks
                group_a.reset(HEIGHT / 5)
                group_b.reset(HEIGHT / 5 - cnst.goal_distance)

        if not start or not alive:
            screen.blit(text, txt)
        screen.blit(score_txt, scoreboard)
        # finish render and display
        pygame.display.flip()
        # limit to 60 FPS
        # dt gives time in seconds since last frame
        dt = clock.tick(60) / 1000

    pygame.quit()
    return score



# RL constant init
EPSILON_DECAY = 0.9999
EPSILON_MIN = 0.05
#state and action init
state = None
direction_timer = None
prev_move = direction_timer



def play(run_count, draw_interval, mid_avg_print):
    #negative runcount sets manual play
    global state
    if run_count < 0:
        return manual()
    if run_count == 0:
        return 0
    #values of or below 0 never activate
    if draw_interval <= 0:
        draw_interval = run_count+1
    if mid_avg_print <=0:
        mid_avg_print = run_count+1
    scores=[]
    drawBool = False
    WIDTH = classes.globalWidth
    HEIGHT = classes.globalHeight
    run_num = 0
    rec_total = 0
    rec_max=0

    #pygame initialization for bug testing
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill("white")
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

    running = True

    #reward var init
    climbedY=0
    scoreUp=0
    hit_floor=False
    hit_block=False
    #state and action init
    state = get_state(group_a, group_b ,dia_pos)
    direction_timer = choose_action(group_a, group_b , dia_pos)
    prev_move = direction_timer

    while running:#start game logic
        #if drawing need to quit with window X
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if alive:
            #drawing features for bug test
            if run_num != 0 and run_num % draw_interval == 0:
                drawBool = True
            if drawBool:
                screen.fill("white")

                #block corners needed only for drawing
                diamond_corners = [(dia_pos.x - cnst.dia_rad, dia_pos.y), (dia_pos.x, dia_pos.y - cnst.dia_rad),
                                 (dia_pos.x + cnst.dia_rad, dia_pos.y), (dia_pos.x, dia_pos.y + cnst.dia_rad)]
            if start:
                #unsure if the start/wait logic needed for roboPlay, but left in for continuity

                direction_timer -= 1
                if direction_timer <= 1:
                    direction_timer = choose_action(group_a, group_b , dia_pos)
                    if direction_timer < 0 and dia_pos.x > cnst.dia_rad:
                        dx = -1
                        dy = cnst.dy0
                    elif direction_timer > 0 and dia_pos.x < WIDTH - cnst.dia_rad:
                        dx = 1
                        dy = cnst.dy0
                    # RL Q update
                    reward = get_reward(climbedY, hit_floor, hit_block, scoreUp)
                    scoreUp = 0
                    prev_state = state
                    state = get_state(group_a, group_b ,dia_pos)
                    if prev_move in ACTIONS:
                        buffer.push(prev_state, prev_move, reward, state, not alive)
                        train_step()
                        maybe_update_target()
                    prev_move = direction_timer #record what move made for next state Q update
                    climbedY = 0  # reset so next action starts fresh
                    direction_timer = abs(direction_timer) #set timer positive for further loop reduction

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
                    if prev_move in ACTIONS:
                        buffer.push(prev_state, prev_move, reward, state, not alive)
                        train_step()
                        maybe_update_target()
                    climbedY = 0  # reset so next action starts fresh
                if group_a.collide(dia_pos, cnst.dia_rad) or group_b.collide(dia_pos, cnst.dia_rad):
                    hit_block = True
                    alive = False
                    # RL Q update
                    reward = get_reward(climbedY, hit_floor, hit_block, scoreUp)
                    scoreUp=0
                    prev_state = state
                    state = get_state(group_a, group_b ,dia_pos)
                    if prev_move in ACTIONS:
                        buffer.push(prev_state, prev_move, reward, state, not alive)
                        train_step()
                        maybe_update_target()
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
                        direction_timer = choose_action(group_a, group_b , dia_pos)
                        # RL Q update
                        reward = get_reward(climbedY, hit_floor, hit_block, scoreUp)
                        scoreUp = 0
                        prev_state = state
                        state = get_state(group_a, group_b ,dia_pos)
                        if prev_move in ACTIONS:
                            buffer.push(prev_state, prev_move, reward, state, not alive)
                            train_step()
                            maybe_update_target()
                        prev_move = direction_timer
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
                        direction_timer = choose_action(group_a, group_b , dia_pos)
                        # RL Q update
                        reward = get_reward(climbedY, hit_floor, hit_block, scoreUp)
                        scoreUp = 0
                        prev_state = state
                        state = get_state(group_a, group_b ,dia_pos)
                        if prev_move in ACTIONS:
                            buffer.push(prev_state, prev_move, reward, state, not alive)
                            train_step()
                            maybe_update_target()
                        prev_move=direction_timer
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


        else: #dead so raise run_num and if reached run_count then quit
            drawBool = False
            scores.append(score)
            rec_max = max(score,rec_max)
            rec_total += score
            cnst.epsilon = max(EPSILON_MIN, cnst.epsilon * EPSILON_DECAY)
            run_num+=1
            if run_num % mid_avg_print == 0:
                print(f"Round {run_num}-\tSince last print - Avg: {rec_total / mid_avg_print:.4f}\tMax: {rec_max}")
                rec_total = 0
                rec_max = 0
            if(run_num >= run_count):
                running=False
            else: #reset
                # reward var init
                climbedY = 0
                hit_floor = False
                hit_block = False
                # state and action init
                state = get_state(group_a, group_b ,dia_pos)
                direction_timer = choose_action(group_a, group_b , dia_pos)
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


        if drawBool:
            pygame.display.flip()
            # limit to 60 FPS
            # dt gives time in seconds since last frame
            clock.tick(60)
            dt = 1/60
        else:
            dt = 1/60
            if run_num % 1000 == 0:
                pygame.event.pump()
    pygame.quit()
    print(f"After {run_count} rounds-\tAvg: {sum(scores)/len(scores):.4f}\tMax: {max(scores)}")
    print(f"")
    save_training()
    return cnst.epsilon


def run(total, shown_step, observe, mid_avg_print):
    #run the game {total} times with every {shown_step}th game drawn
    #negative total lets manual play
    if total <= 0:
        manual()
        return
    load_training()
    if shown_step >total or shown_step <=0:
        play(total,0, mid_avg_print)
    else:
        play(total, shown_step, mid_avg_print)
    play(observe,1, 0)
    save_training()

play_manually = String(input("Play manually? (y/n): "))
if play_manually == "y":
    manual()
else:
    tot = int(input("Total Rounds: "))
    shown_step = int(input("Shown Round interval: "))
    observe = int(input("Observed Rounds after Total finished: "))
    mid_print = int(input("Mid Status Print interval: "))
    run(tot,shown_step, observe, mid_print)
