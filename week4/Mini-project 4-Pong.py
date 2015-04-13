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

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos = [WIDTH/2, HEIGHT/2]
    
    h_v = random.randrange(120, 240)/60
    v_v = random.randrange(60, 180)/60
    
    if direction == LEFT:  # upper and left
        ball_vel = [-h_v,-v_v]
    elif direction == RIGHT:   # upper and right
        ball_vel = [h_v, -v_v]
        
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    paddle1_pos = [HALF_PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT]
    paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT]          
    paddle1_vel = 0
    paddle2_vel = 0
    
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    
    spawn_ball(LEFT)
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
         
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
       
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS-1, 1, "White","White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[1] += paddle1_vel
    if paddle1_pos[1]<0:
        paddle1_pos[1] = 0
    elif paddle1_pos[1] > HEIGHT - PAD_HEIGHT - 1:
        paddle1_pos[1] = HEIGHT - PAD_HEIGHT - 1
        
    paddle2_pos[1] += paddle2_vel
    if paddle2_pos[1]<0:
        paddle2_pos[1] = 0
    elif paddle2_pos[1] > HEIGHT - PAD_HEIGHT - 1:
        paddle2_pos[1] = HEIGHT - PAD_HEIGHT - 1        
        
    # draw paddles
    canvas.draw_line(paddle1_pos,[paddle1_pos[0], paddle1_pos[1]+PAD_HEIGHT], PAD_WIDTH, "White")
    canvas.draw_line(paddle2_pos,[paddle2_pos[0], paddle2_pos[1]+PAD_HEIGHT], PAD_WIDTH, "White")
    
    # determine whether paddle and ball collide  
    if (ball_pos[1] - BALL_RADIUS <= 0):
        ball_vel[1] = -ball_vel[1]
    else:
        if ball_pos[1] + BALL_RADIUS >= HEIGHT - 1:  
            ball_vel[1] = -ball_vel[1]
            
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH - 1: # touch left
        if ball_pos[1] >= paddle1_pos[1] and ball_pos[1] <= paddle1_pos[1]+PAD_HEIGHT: # strike paddle
            ball_vel[0] = -ball_vel[0]*1.1
        else:
            spawn_ball(RIGHT)
            score2 += 1
    else:
        if ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH - 1: # touch right
            if ball_pos[1] >= paddle2_pos[1] and ball_pos[1] <= paddle2_pos[1]+PAD_HEIGHT: # strike paddle
                ball_vel[0] = -ball_vel[0]*1.1
            else:
                spawn_ball(LEFT)
                score1 += 1
                
    # draw scores
    canvas.draw_text(str(score1), [WIDTH/4, HEIGHT/5], 50, "White")
    canvas.draw_text(str(score2), [WIDTH*3/4, HEIGHT/5], 50, "White")
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -1
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 1
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -1
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 1

def keyup(key):
    global paddle1_vel, paddle2_vel

    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game)

# start frame
new_game()
frame.start()
