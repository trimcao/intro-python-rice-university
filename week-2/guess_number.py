"""
Guess The Number game
Intro to Python - Week 2
Tri Minh Cao
trimcao@gmail.com
September 2015
"""
# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import random
import simplegui

secret_number = -1
mode = 1 # mode 1 is range100, mode 2 is range1000
guess_count = 0

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number, mode, guess_count
    guess_count = 0
    secret_number = -1
    secret_number = random.randrange(100)
    if (mode == 1):
        secret_number = random.randrange(100)
        print "\nA new Game has started in range [0, 100)"
    else:
        secret_number = random.randrange(1000)
        print "\nA new Game has started in range [0, 1000)"

    

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global mode
    mode = 1
    new_game()
       

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global mode
    mode = 2
    new_game()
    
def input_guess(guess):
    # main game logic goes here	
    global guess_count
    guess_count += 1
    guess_number = int(guess)
    print "Guess was", guess_number
    if (secret_number > guess_number):
        print "Higher"
    elif (secret_number == guess_number):
        print "Correct!"
        new_game()
    else:
        print "Lower"
    print
    
    if (mode == 1):
        if (guess_count >= 7):
            print "Game Over! The secret number is", secret_number
            new_game()
        elif (guess_count > 0):
            print "You have", 7 - guess_count, "remaining guess(es)\n"
    else:
        if (guess_count >= 10):
            print "Game Over! The secret number is", secret_number
            new_game()
        elif (guess_count > 0):
            print "You have", 10 - guess_count, "remaining guess(es)\n"
    

    
# create frame
frame = simplegui.create_frame("Guess the Number", 200, 200)


# register event handlers for control elements and start frame
inp = frame.add_input('Your guess:', input_guess, 50)
button1 = frame.add_button('Range is [0,100)', range100)
button2 = frame.add_button('Range is [0,1000)', range1000)
# call new_game 
new_game()
frame.start()


# always remember to check your completed program against the grading rubric

