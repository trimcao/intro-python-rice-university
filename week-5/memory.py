
"""
Name: Tri Minh Cao
Email: trimcao@gmail.com
Date: October 2015
implementation of card game - Memory
"""

import simplegui
import random

no_turn = 0
first_open = -1 # index of the card player opens first
second_open = -1 # index of the card player opens second
# initialize a deck of cards, with each card appearing twice
deck = range(8)
deck.extend(range(8))
# exposed list to represent a card is exposed (1) or not (0)
exposed = [0 for idx in range(len(deck))]

random.shuffle(deck)
#exposed[7] = 1

state = 0 # game has three states

# helper function to initialize globals
def new_game():
    global exposed, deck, first_open, second_open, no_turn, state
    deck = range(8)
    deck.extend(range(8))
    random.shuffle(deck)
    exposed = [0 for idx in range(len(deck))] 
    no_turn = 0
    first_open = -1
    second_open = -1  
    state = 0
    label.set_text("Turns = " + str(no_turn))
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, no_turn, first_open, second_open
    card_index = pos[0] // 50
    if not (exposed[card_index] == 1):
        #print "State: ", state 
        if (state == 0):
            state = 1       
            exposed[card_index] = 1
            first_open = card_index
        elif (state == 1):
            state = 2
            no_turn += 1
            exposed[card_index] = 1
            second_open = card_index
        elif (state == 2):
            #print (first_open)
            #print second_open
            #print
            # check if two recently exposed cards are the same
            if (deck[first_open] == deck[second_open]):
                exposed[first_open] = 1
                exposed[second_open] = 1
            else:
                exposed[first_open] = 0
                exposed[second_open] = 0
            # reset second_open
            second_open = -1
            state = 1
            #no_turn += 1
            exposed[card_index] = 1
            first_open = card_index

         
    label.set_text("Turns = " + str(no_turn))     
                 
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    # draw the number associates with each card on canvas
    #pos = [20, 50]
    cover_pos = [0, 100]
    for idx in range(len(deck)):
        if (exposed[idx] == 1):           
            canvas.draw_polygon([cover_pos, (cover_pos[0] + 100, cover_pos[1]),
                                 (cover_pos[0] + 100, cover_pos[1] - 100),
                                 (cover_pos[0], cover_pos[1] - 100)],
                                 2, 'Yellow', 'Black')
            
            canvas.draw_text(str(deck[idx]), (cover_pos[0] + 20, cover_pos[1] - 40),
                             30, "Yellow")     
        else:
            canvas.draw_polygon([cover_pos, (cover_pos[0] + 100, cover_pos[1]),
                                (cover_pos[0] + 100, cover_pos[1] - 100),
                                 (cover_pos[0], cover_pos[1] - 100)],
                                 2, 'Yellow', 'Green')
        #pos[0] += 50
        cover_pos[0] += 50
        

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = " + str(no_turn))

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric

