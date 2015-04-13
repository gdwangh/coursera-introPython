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

LEFT_PADDLE = 0
RIGHT_PADDLE = 1

LEFT_WALL = 0
TOP_WALL = 1
RIGHT_WALL = 2
BOTTOM_WALL = 3

# wall: left, top, right, bottom
wall = [PAD_WIDTH+BALL_RADIUS, BALL_RADIUS, WIDTH - PAD_WIDTH - BALL_RADIUS, HEIGHT - BALL_RADIUS]

keyMap = {'w':[LEFT_PADDLE, -1], 's':[LEFT_PADDLE, 1], "up":[RIGHT_PADDLE, -1], "down":[RIGHT_PADDLE,1]}
          
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
    # inital paddle
    paddle1_pos = [HALF_PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT]
    paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT]          
    
    global paddle   # list [pos, v_speed, score]
    paddle = [[paddle1_pos, 0],[paddle2_pos, 0]]
    
    global score1, score2
    score1 = 0
    score2 = 0
    
    spawn_ball(LEFT)

def update_paddle(number):
    """ update paddle's vertical position, keep paddle on the screen
        and draw it
            number = 0: left paddle, 
                   = 1: right paddle
    """
    # update pos's vertile
    paddle[number][0][1] += paddle[number][1]
    
    # check whether vertile pos is out
    if paddle[number][0][1] < 0:
        paddle[number][0][1] = 0
    elif paddle[number][0][1] > HEIGHT - PAD_HEIGHT - 1:
        paddle[number][0][1] = HEIGHT - PAD_HEIGHT - 1
        
def draw_paddle(canvas, number):
    canvas.draw_line(paddle[number][0],[paddle[number][0][0], paddle[number][0][1]+PAD_HEIGHT], PAD_WIDTH, "White")

def touch_paddle(number):
    return ball_pos[1] >= paddle[number][0][1] and ball_pos[1] <= paddle[number][0][1]+PAD_HEIGHT # strike paddle

def draw(canvas):
    global score1, score2, ball_pos, ball_vel
         
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
    update_paddle(LEFT_PADDLE)    
    update_paddle(RIGHT_PADDLE)        
        
    # draw paddles
    draw_paddle(canvas, LEFT_PADDLE)
    draw_paddle(canvas, RIGHT_PADDLE)
    
    # determine whether paddle and ball collide
    # touch top or bottom
    if (ball_pos[1] < wall[TOP_WALL]) or (ball_pos[1] > wall[BOTTOM_WALL]): 
        ball_vel[1] = - ball_vel[1]
 
    # left or right
    if ball_pos[0] < wall[LEFT_WALL]: # touch left
        if touch_paddle(LEFT): # strike paddle
            ball_vel[0] = ball_vel[0] * (-1.1)
        else:
            spawn_ball(RIGHT)
            score2 += 1
    elif ball_pos[0] > wall[RIGHT_WALL]: # touch right
        if touch_paddle(RIGHT):
            ball_vel[0] = ball_vel[0]*(-1.1)
        else:
            spawn_ball(LEFT)
            score1 += 1
                
    # draw scores
    canvas.draw_text(str(score1), [WIDTH/4, HEIGHT/5], 50, "White")
    canvas.draw_text(str(score2), [WIDTH*3/4, HEIGHT/5], 50, "White")
    
def keydown(key):
    """ keyMap.items: [paddle_id, v] """
    for k in keyMap:
        if key == simplegui.KEY_MAP[k]:
            paddle[keyMap[k][0]][1] = keyMap[k][1]
            
def keyup(key):
    for k in keyMap:
        if key == simplegui.KEY_MAP[k]:
            paddle[keyMap[k][0]][1] = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game)

# start frame
new_game()
frame.start()
