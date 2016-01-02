"""
Name: Tri Minh Cao
Email: trimcao@gmail.com
Date: October 2015

Mini-project #6 - Blackjack

NOTE: the gui only works with CodeSkulptor
"""

# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self._cards = []
        #self._values = 0

    def __str__(self):
        # return a string representation of a hand
        string = ''
        for card in self._cards:
            string += str(card)
            string += ', '
        return string

    def add_card(self, card):
        # add a card object to a hand
        self._cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        for card in self._cards:
            card_rank = card.get_rank()
            value += VALUES[card_rank]
            if (card_rank == 'A'):
                if (value + 10 <= 21):
                    value += 10
        return value       

   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        # draw the first five cards in a hand
        current_pos = list(pos)
        for idx in range(min(len(self._cards), 5)):
            self._cards[idx].draw(canvas, current_pos)
            current_pos[0] += (CARD_SIZE[0] + 15)
            
 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self._cards = []
        for each_suit in SUITS:
            for each_rank in RANKS:
                self._cards.append(Card(each_suit, each_rank))               
                

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self._cards)

    def deal_card(self):
        # deal a card object from the deck
        return self._cards.pop()
    
    def __str__(self):
        # return a string representing the deck
        string = ''
        for card in self._cards:
            string += str(card)
            string += ', '
        return string


#deck = Deck()
#player = Hand()
#dealer = Hand()
score = 0    
abandon = False
#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player, dealer, score, abandon
    # if click deal() in middle of a player, the player loses point
    if (in_play):
        score -= 1
        abandon = True
    else:
        abandon = False
    
    outcome = ''
    deck = Deck()
    player = Hand()
    dealer = Hand()

    # your code goes here
    deck.shuffle()
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    
    #print "Player's hand: ", str(player)
    #print "Dealer's hand: ", str(dealer)
    
    in_play = True

def hit():
    global player, in_play, outcome, score
    # if the hand is in play, hit the player
    if (in_play):
        player.add_card(deck.deal_card()) 
        #print "My hand: " + str(player)
        #print "Current Value: " + str(player.get_value())
        #print
   
        # if busted, assign a message to outcome, update in_play and score
        if (player.get_value() > 21):
            in_play = False
            score -= 1
            outcome = "You have busted"
       
def stand():
    global in_play, player, dealer, score, outcome
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if (in_play):
        while (dealer.get_value() < 17):
            dealer.add_card(deck.deal_card())
            #print dealer.get_value()

        # assign a message to outcome, update in_play and score
        in_play = False
        dealer_score = dealer.get_value()
        player_score = player.get_value()
        if (dealer_score > 21): 
            outcome = "Dealer has busted"
            score += 1
        elif (player_score > dealer_score):    
            #outcome = "Player wins with " + str(player_score) + ". Dealer has " + str(dealer_score)
            outcome = "You win"
            score += 1
        elif (player_score <= dealer_score):    
            outcome = "Dealer wins"
            score -= 1

#def abandon(canvas):
#    canvas.draw_text('You lost one point for giving up last round', [370, 50], 30, 'White')

# draw handler    
def draw(canvas):
    # draw 'Blackjack' text
    canvas.draw_text('Blackjack', [30, 50], 40, 'White')
    
    # draw player's hand
    canvas.draw_text('Player', [120, 370], 30, 'White')
    player.draw(canvas, [120, 400])
    
    # draw dealer's hand
    canvas.draw_text('Dealer', [120, 200], 30, 'White')
    dealer.draw(canvas, [120, 230])

    # draw instruction for player, and final scores
    if (in_play):
        canvas.draw_text('Hit or Stand?', [350, 370], 30, 'White')
        canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, [120 + CARD_CENTER[0], 230 + CARD_CENTER[1]], CARD_SIZE)
    else:    
        canvas.draw_text('New Deal?', [350, 370], 30, 'White')	
        canvas.draw_text(outcome, [350, 200], 30, 'White')
    # draw score
    canvas.draw_text('Score: ' + str(score), [350, 50], 30, 'White')
    
    if (abandon):
        canvas.draw_text('You lost one point for giving up last round', [30, 100], 20, 'White')

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
