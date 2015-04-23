# implementation of Spaceship - program template for RiceRocks
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

Max_ROCK_NUM = 12
MINI_INIT_DIST = 100
GAME_TIME = 60*60*5  # 60s
remain_time = GAME_TIME

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

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.ogg")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.ogg")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.ogg")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.ogg")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
    
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
            
        self.vel[0] *= .99
        self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
        
    def shoot(self):
        # global a_missile
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
    
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
        self.sound = sound
        
        if sound:
            sound.rewind()
            sound.play()
   
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def draw(self, canvas):
        if self.animated:
            # title_image
            center_pos = [self.image_center[0] + self.age * self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, center_pos, self.image_size,
                          self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        self.age += 1
        if self.age >= self.lifespan:
            if self.sound:
                self.sound.pause()
                
            return True	  # come to lifespan,  to remove it
        else:
            return False  # no come to lifespan, to keep it
        
    def collide(self, other_object):
        pos1 = self.pos
        pos2 = other_object.get_pos()
        pos_dist = dist(pos1, pos2)
        if pos_dist < self.radius + other_object.get_radius(): 
            return True
        else:
            return False
                
# help functions 
def process_sprite_group(canvas, sprite_group):
    removed = set([])
    
    for sprite_obj in sprite_group:
        sprite_obj.draw(canvas)
        over_lifespan = sprite_obj.update()
        if over_lifespan:
            removed.add(sprite_obj)
            
    if len(removed)>0:
        sprite_group.difference_update(removed)

def group_collide(other_object, group):
    removed = set([])
    
    # check collide
    for obj in group:
        if obj.collide(other_object):
            removed.add(obj)
            explore_at(obj.get_pos())
            
    # remove collided obj from group
    if len(removed) > 0:
        group.difference_update(removed)
        return True
    else:
        return False

def group_group_collide(group1, group2):
    removed = set([])
    for obj in group1:
        if group_collide(obj, group2):
            removed.add(obj)
            
    n = len(removed)
    group1.difference_update(removed)
    return n

def new_game():
    global score, lives, time, remain_time
    score = 0
    lives = 3
    time = 0
    remain_time = GAME_TIME

    global my_ship, rock_group, missile_group
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
    rock_group = set([])
    missile_group = set([])

def explore_at(pos):
    a_explosion = Sprite(pos, [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)
    explosion_group.add(a_explosion)
    
# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    
    if (not started) and inwidth and inheight:
        started = True
        new_game()
        soundtrack.rewind()
        soundtrack.play()
    
def draw(canvas):
    global time, started
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # check collide
    global lives, score, rock_group
    if group_collide(my_ship, rock_group):
        lives -= 1
        
    if lives==0 or time >= GAME_TIME:
        started = False
        rock_group = set([])  # removed all rocks 
        soundtrack.pause()

    score += group_group_collide(missile_group, rock_group)
        
    # draw ship and sprites
    my_ship.draw(canvas)
    
    # draw and update rock
    # a_rock.draw(canvas)
    process_sprite_group(canvas, rock_group)

    # draw and update missile
    # a_missile.draw(canvas)
    process_sprite_group(canvas, missile_group)

    # draw and update missile
    process_sprite_group(canvas, explosion_group)
        
    # update ship and sprites
    my_ship.update()
    # a_rock.update()
    # a_missile.update()
    
    # draw UI
    global remain_time
    if started:
        remain_time -= 1
        
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text("Remain", [350, 50], 22, "White")    
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")
    canvas.draw_text(str(remain_time//60)+" sec", [350,80],22, "White")
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

# timer handler that spawns a rock    
def rock_spawner():
    if started and len(rock_group)<Max_ROCK_NUM:
        # global a_rock
        center_dist = 0
        ship_pos = my_ship.get_pos()
        ship_radius = my_ship.get_radius()
        rock_radius = asteroid_info.get_radius()
        min_dist = MINI_INIT_DIST + ship_radius + rock_radius

        while center_dist < MINI_INIT_DIST:
            rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
            rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
            rock_avel = random.random() * .2 - .1
            
            center_dist = dist(rock_pos, ship_pos)
            
        a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
        rock_group.add(a_rock)

def unload_timer_check():
    def gct():
        try:
            return frame.get_canvas_textwidth("t",12)
        except:
            return 0
        
    t = gct()
    if t==0:   # frame was closed
        unload_timer.stop()
        soundtrack.pause()
        
# initialize stuff
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
# a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, .1, asteroid_image, asteroid_info)
rock_group = set([])

# a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
missile_group = set([])

explosion_group = set([])

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

unload_timer = simplegui.create_timer(1000,unload_timer_check)
unload_timer.start()

# get things rolling
timer.start()
frame.start()
