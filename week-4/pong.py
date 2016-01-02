
"""
Pong
Name: Isco Alarcon 
Date: September 2015
"""
# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

ball_pos = [0, 0]
ball_vel = [0, 0]
paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2
paddle1_vel = [0, 0]
paddle2_vel = [0, 0]

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    # wait or 2 seconds before spawning a new ball
    
    ball_vel[0] = float(random.randrange(120, 240)) / 60
    ball_vel[1] = -float(random.randrange(60, 180)) / 60
    if (direction == LEFT):
        ball_vel[0] *= -1
    
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    #ball_vel = [-40.0 / 60.0,  5.0 / 60.0]
    #ball_vel = [1.0,  -5.0]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0, 0]
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = [0, 0]
    paddle2_vel = [0, 0]
    
    coin = random.randrange(2)
    if (coin == 0):
        spawn_ball(RIGHT)
    else:
        spawn_ball(LEFT)
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_circle([WIDTH / 2, HEIGHT / 2], 40, 1, 'White')
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    # check for collision
    if (ball_pos[1] <= BALL_RADIUS) or (HEIGHT - ball_pos[1] <= BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
    # check for collision with gutters
    # left goal
    if (ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH)):
        # check for collision with paddle1
        if (ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT - BALL_RADIUS) and (ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT + BALL_RADIUS):
            ball_vel[0] = -1.2 * ball_vel[0]
        else:
            # we have a goal
            score2 +=1
            spawn_ball(LEFT)
            
    # right goal    
    if ((WIDTH - ball_pos[0]) <= (BALL_RADIUS + PAD_WIDTH)):
        if (ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT - BALL_RADIUS) and (ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT + BALL_RADIUS):
            ball_vel[0] = -1.2 * ball_vel[0]
        else:
            score1 += 1
            spawn_ball(RIGHT)
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos + paddle1_vel[1] < HALF_PAD_HEIGHT) or (paddle1_pos + paddle1_vel[1] > HEIGHT - HALF_PAD_HEIGHT):
        pass
    else:
        paddle1_pos += paddle1_vel[1]

    if (paddle2_pos + paddle2_vel[1] < HALF_PAD_HEIGHT) or (paddle2_pos + paddle2_vel[1] > HEIGHT - HALF_PAD_HEIGHT):
        pass
    else:
        paddle2_pos += paddle2_vel[1]    
    
     
    # draw paddles
    #canvas.draw_polygon([(0, paddle1_pos), (PAD_WIDTH, paddle1_pos), (PAD_WIDTH, paddle1_pos + PAD_HEIGHT), (0, paddle1_pos + PAD_HEIGHT)], 1, 'Blue', 'White')
    canvas.draw_polygon([(0, paddle1_pos - HALF_PAD_HEIGHT),
                         (PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT),
                         (PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT),
                         (0, paddle1_pos + HALF_PAD_HEIGHT)],
                        1, 'White', 'White')
    canvas.draw_polygon([(WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT),
                         (WIDTH, paddle2_pos - HALF_PAD_HEIGHT),
                         (WIDTH, paddle2_pos + HALF_PAD_HEIGHT),
                         (WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT)],
                        1, 'White', 'White')    
    # determine whether paddle and ball collide    
    
    # draw scores
    canvas.draw_text(str(score1), (150, 40), 40, 'White', 'sans-serif')
    canvas.draw_text(str(score2), (450, 40), 40, 'White', 'sans-serif')
    
def restart_handler():
    new_game()
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 5
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel[1] += acc
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel[1] -= acc
    
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel[1] += acc
    elif key==simplegui.KEY_MAP["w"]:
        paddle1_vel[1] -= acc    
        
    #print paddle2_vel[1]    
        
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    acc = 5
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel[1] -= acc
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel[1] += acc
    
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel[1] -= acc
    elif key==simplegui.KEY_MAP["w"]:
        paddle1_vel[1] += acc      


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
button1 = frame.add_button('Restart', restart_handler)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
#print paddle1_pos
#print PAD_WIDTH
#print paddle1_pos + PAD_HEIGHT
#canvas.draw_polygon([(0, paddle1_pos), (PAD_WIDTH, paddle1_pos), (PAD_WIDTH, paddle1_pos + PAD_HEIGHT), (0, paddle1_pos + PAD_HEIGHT)], 1, 'Blue', 'White')

