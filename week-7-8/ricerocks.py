"""
RiceRocks (Asteroids clone)
Name: Tri Minh Cao
Email: trimcao@gmail.com
Date: November 2015

NOTE: Only runs with CodeSkulptor
"""
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
asteroid_image_list = []
asteroid1 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
asteroid2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_brown.png")
asteroid3 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")
asteroid_image_list.extend([asteroid1, asteroid2, asteroid3])

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
explosion_image_list = []
explosion1 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")
explosion2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue.png")
explosion3 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue2.png")
explosion4 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
explosion_image_list.extend([explosion1, explosion2, explosion3, explosion4])

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius    
        
    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        #canvas.draw_image(image, center_source, width_height_source, center_dest, width_height_dest, rotation)
        if (self.thrust):
            thrust_center = [self.image_center[0] + self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, thrust_center, self.image_size,
                              self.pos, self.image_size, self.angle)
            ship_thrust_sound.play()
        else:    
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
            ship_thrust_sound.rewind()

    def update(self):
        
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel
        
        if self.thrust:        
            forward = angle_to_vector(self.angle)
            # update velocity += a constant * forward vector
            self.vel[0] += 0.17 * forward[0]
            self.vel[1] += 0.17 * forward[1]
        
        # add friction
        self.vel[0] = 0.985 * self.vel[0]
        self.vel[1] = 0.985 * self.vel[1]
        
    def update_angle_vel(self, amount):
        self.angle_vel += amount
        
    def turn_thruster(self):
        if (self.thrust == True):
            self.thrust = False
        else:
            self.thrust = True
        
    def shoot(self):
        global missile_group
        # generate parameters for the missile
        forward = angle_to_vector(self.angle)
        x_vel = self.vel[0] + 5 * forward[0]
        y_vel = self.vel[1] + 5 * forward[1]        
        
        x_pos = self.pos[0] + self.image_size[0] / 2 * forward[0] 
        y_pos = self.pos[1] + self.image_size[1] / 2 * forward[1]
        a_missile = Sprite([x_pos, y_pos], [x_vel, y_vel],
                            0, 0, missile_image, missile_info, missile_sound)  
        missile_group.add(a_missile)
    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        #print "draw"
        if not self.animated:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            old_center = self.image_center
            width = self.image_size[0]
            new_center = [old_center[0] + self.age * width, old_center[1]]
            canvas.draw_image(self.image, new_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        
    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel
        self.age += 1
        if (self.age > self.lifespan):
            return True
        else:
            return False        
            
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def collide(self, other):
        pos1 = self.get_position()
        pos2 = other.get_position()
        distance = ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5
        collision_dist = self.get_radius() + other.get_radius()
        if (distance <= collision_dist):
            return True
        else:
            return False
        
          
def draw(canvas):
    global time, lives, score, started
       
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())  
        return
    
    # draw and update ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(rock_group, canvas)	
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)    
    
    # check for collision
    if (group_collide(rock_group, my_ship)):
        lives -= 1
        
    # check for game over
    if (lives == 0):
        started = False
        new_game()
    
    gain = group_group_collide(rock_group, missile_group)
    score += gain
     
    # update ship and sprites
    my_ship.update()
    
    # draw remaining lives and scores
    #canvas.draw_text(text, point, font_size, font_color)
    canvas.draw_text("Lives: " + str(lives), [0.75 * WIDTH, 0.1 * HEIGHT], 25, "White")
    canvas.draw_text("Score: " + str(score), [0.1 * WIDTH, 0.1 * HEIGHT], 25, "White")
     

        
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    #print len(rock_group)
    rock_radius = 40
    spawned = False
    if (len(rock_group) >= 12 or (not started)):
        pass
    else: 
        # generate random parameters for a rock
        # postition, velocity, angle_velocity
        while not spawned: 
            # x_pos is between 0.1 * WIDTH and 0.9 * WIDTH
            x_pos = random.random() * (0.8 * WIDTH) + (0.1 * WIDTH)
            # y_pos is between 0.1 * HEIGHT and 0.9 * HEIGHT
            y_pos = random.random() * (0.8 * HEIGHT) + (0.1 * HEIGHT)
            ship_pos = my_ship.get_position()
            distance = ((x_pos - ship_pos[0]) ** 2 + (y_pos - ship_pos[1]) ** 2) ** 0.5
            collision_dist = 40 + my_ship.get_radius()
            if (distance > (collision_dist + 20)):
                spawned = True
           
        # velocity is between -3 and 3
        x_vel = random.random() * 6 - 3
        y_vel = random.random() * 6 - 3
        angle_vel = random.random() * 0.1
        
        asteroid_img = random.choice(asteroid_image_list)
        a_rock = Sprite([x_pos, y_pos], [x_vel, y_vel], 0, angle_vel, asteroid_img, asteroid_info)
        rock_group.add(a_rock)
      
    
# keyboard handler
def keydown(key):
    if (not started):
        pass
    elif key==simplegui.KEY_MAP["left"]:
        my_ship.update_angle_vel(-0.1)
    elif key==simplegui.KEY_MAP["right"]:
        my_ship.update_angle_vel(0.1) 
    elif key==simplegui.KEY_MAP["up"]:    
        my_ship.turn_thruster()
    elif key==simplegui.KEY_MAP["space"]:
        my_ship.shoot()
    
        
def keyup(key):
    if (not started):
        pass
    elif key==simplegui.KEY_MAP["left"]:
        my_ship.update_angle_vel(0.1)
    elif key==simplegui.KEY_MAP["right"]:
        my_ship.update_angle_vel(-0.1)   
    elif key==simplegui.KEY_MAP["up"]:    
        my_ship.turn_thruster()

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True   
        soundtrack.play()
        

def process_sprite_group(group, canvas):
    for each in set(group):
        each.draw(canvas)
        if (each.update()):
            group.remove(each)

def group_collide(group, other_object):
    collided = False
    for each in set(group):
        if each.collide(other_object):
            collided = True
            # create a new explosion
            explosion_img = random.choice(explosion_image_list)
            new_explosion = Sprite(each.get_position(), [0, 0], 0,
                                   0, explosion_img, explosion_info, sound = explosion_sound)
            explosion_group.add(new_explosion)
            group.remove(each)
    return collided

def group_group_collide(group1, group2):
    num_collide = 0
    for each in set(group1):
        if (group_collide(group2, each)):
            num_collide += 1
            group1.remove(each)
    return num_collide

def new_game():
    global my_ship, explosion_group, rock_group, missile_group, lives, score
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
    rock_group = set()
    missile_group = set()
    explosion_group = set()
    
    lives = 3
    score = 0
    ship_thrust_sound.rewind()
    soundtrack.rewind()
    soundtrack.play()
    # reset keys
    #keydown(simplegui.KEY_MAP["a"])
    #keydown(simplegui.KEY_MAP["left"])
    #keydown(simplegui.KEY_MAP["right"])
    #keyup(simplegui.KEY_MAP["a"])
    #keyup(simplegui.KEY_MAP["up"])
    #keyup(simplegui.KEY_MAP["right"])

    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
new_game()
#my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#rock_group = set()
#missile_group = set()
#explosion_group = set()
soundtrack.play()


# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1500.0, rock_spawner)

# get things rolling
timer.start()
frame.start()

