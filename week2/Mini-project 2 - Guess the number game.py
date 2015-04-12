# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random
import math

max_number = 100

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number, remain_times
    secret_number = random.randrange(0,max_number)
    remain_times = int(math.ceil(math.log(max_number, 2)))
    input_guess.set_text("")
    
    print ""
    print "New game. Range is from 0 to", max_number
    print "Number of remaining guesses is",remain_times
    
    # remove this when you add your code    
    # pass


# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global max_number
    max_number = 100
    new_game()
    
    # remove this when you add your code    
    # pass

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global max_number
    max_number = 1000
    new_game()
    
    # remove this when you add your code     
    # pass
    
def input_guess(guess):
    global remain_times
    remain_times = remain_times - 1
    
    # main game logic goes here	
    guess_number = int(guess)
    print ""
    print "Guess was ", guess_number
    print "Number of remaining guesses is", remain_times
    
    if guess_number == secret_number:
        print "Correct!"
        new_game()
    elif remain_times == 0:
        print "You ran out of guesses.  The number was",secret_number
        new_game()
    elif guess_number < secret_number:
        print "Higher!"
    elif guess_number > secret_number:
        print "Lower!"     
    
    # remove this when you add your code
    # pass

    
# create frame
frame = simplegui.create_frame('Guess number', 200, 200)

# register event handlers for control elements and start frame
button100 = frame.add_button('Range: 0 - 100', range100)
button1000 = frame.add_button('Range: 0 - 1000', range1000)
input_guess = frame.add_input("Guess number", input_guess,50)

frame.start()

# call new_game 
new_game()

# always remember to check your completed program against the grading rubric
