"""
Stopwatch Game
Name: Tri Minh Cao
Email: trimcao@gmail.com
Date: September 2015

Note: the code only works with CodeSkulptor
"""

import simplegui
# template for "Stopwatch: The Game"

# define global variables
time = 0
num_success = 0
num_stops = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    """
    This method will print the current time in format
    A:BC.D where A is minute, BC is second, D is milisec
    """
    minute = t / 600
    sec = t % 600
    milisec = sec % 10
    second1 = (sec / 10) % 10
    second0 = (sec / 100) % 10
    
    return str(minute) + ":" + str(second0) + str(second1) + \
           "." + str(milisec)

#print format(613)
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_handler():
    """
    Handler for Start button
    """
    timer.start()

def stop_handler():
    """
    Handler for Stop button
    """
    global num_success, num_stops
    num_stops += 1
    if (time % 10 == 0):
        num_success += 1        
    timer.stop()

def reset_handler():
    """
    Handler for Reset button
    """    
    global time, num_success, num_stops
    num_success = 0
    num_stops = 0
    time = 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
    """
    Handler for the timer
    """    
    global time
    time += 1
    #print format(time)

# define draw handler
def draw(canvas):
    """
    The Draw Handler
    """    
    canvas.draw_text(format(time), (100, 150), 40, 'White')
    canvas.draw_text("Bingo: " + str(num_success), (220, 20), 15, 'Yellow') 
    canvas.draw_text("Stops: " + str(num_stops), (220, 50), 15, 'Yellow') 
# create frame
frame = simplegui.create_frame("Stopwatch", 300, 300)

# register event handlers
timer = simplegui.create_timer(100, timer_handler)
frame.add_button("Start", start_handler)
frame.add_button("Stop", stop_handler)
frame.add_button("Reset", reset_handler)
frame.set_draw_handler(draw)
# start frame
frame.start()
#timer.start()
# Please remember to review the grading rubric

