# implementation of card game - Memory

import simplegui
import random

CARD_WIDTH = 50
CARD_HEIGHT = 100
CARD_NUM = 8
turn_counter = 0

# helper function to initialize globals
def new_game():
    global cards_list, exposed_list, state, turn_counter
    cards_list = range(8) 
    cards_list.extend(cards_list)
    random.shuffle(cards_list)
    
    exposed_list = [False for card in cards_list]
    state = 0
    turn_counter = 0
    
# define event handlers
def mouseclick(pos):
    # add game state logic here
    card_idx = pos[0] // CARD_WIDTH
    
    global state, exposed_list, card1, card2, turn_counter
    if exposed_list[card_idx] == True:
        return 
    
    if state == 0:   # 1st card is exposed
        state = 1
        card1 = card_idx
        turn_counter += 1
    elif state == 1:  # 2nd card is exposed
        state = 2
        card2 = card_idx
    else:		# 3th card is exposed
        state = 1
        if (cards_list[card1] != cards_list[card2]):
            exposed_list[card1] = False
            exposed_list[card2] = False
            
        card1 = card_idx
        turn_counter += 1

    exposed_list[card_idx] = True
    
# cards are logically 50x100 pixels in size    
def draw(canvas):
    card_left_upper = [0,0]
    
    for card, exposed in zip(cards_list, exposed_list):
        card_loc = [card_left_upper, 
                    [card_left_upper[0], card_left_upper[1]+CARD_HEIGHT], 
                    [card_left_upper[0]+CARD_WIDTH, card_left_upper[1]+CARD_HEIGHT],
                    [card_left_upper[0]+CARD_WIDTH, 0]]
        if exposed:   # exposed == True
            canvas.draw_text(str(card), (card_left_upper[0]+10,card_left_upper[1]+70), 60, "White")
        else:
            canvas.draw_polygon(card_loc, 5, "GREY", "GREEN")
        card_left_upper[0] += CARD_WIDTH
    label.set_text("Turns = "+str(turn_counter))

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
