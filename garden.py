
import pgzrun
import pygame
import pgzero
from random import randint
from pgzero.builtins import Actor
import time


WIDTH = 800
HEIGHT = 800
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2
pygame.display.set_mode((WIDTH, HEIGHT))

# Flag Variables
game_over = False
finalized = False
garden_happy = True
fangflower_collision = False
raining = False

time_elapsed = 0
start_time = time.time()

cow = Actor("cow")
cow.pos = 500, 500 # Starting position

flower_list = []
wilted_list = []
fangflower_list = []

fangflower_vy_list = [] # velocities of the fangflowers along the y-axis.
fangflower_vx_list = [] # velocities of the fangflowers along the x-axis.

def draw():
    global game_over, time_elapsed, finalized, raining # Adding a global variable for rain
    if not game_over:
        raining = True # Make Rain True for entire game
        screen.clear()
        screen.blit("garden-raining", (0, 0))
        cow.draw()
        for flower in flower_list:
            flower.draw()
        for fangflower in fangflower_list:
            fangflower.draw()
        time_elapsed = int(time.time() - start_time)
        screen.draw.text(
            "Garden happy for: " +
            str(time_elapsed) + " seconds",
            topleft=(10, 10), color="black"
        )
    else:
        if not finalized:
            cow.draw()
            #happiness of the garden 
            screen.draw.text(
                "Garden happy for: " +
                str(time_elapsed) + " seconds",
                topleft=(10, 10), color="black"
            )
        if (not garden_happy):
            #game over display
            screen.draw.text(
                "GARDEN UNHAPPY... GAME OVER!", color="black",
                topleft=(10, 50)
            )
            finalized = True
        else:  # 
            # draws a message on the screen to show the game ending 
            screen.draw.text(
                "FANGFLOWER ATTACK... GAME OVER!", color="black",
                topleft=(10, 50)
            )
            finalized = True # exit the code 
    return
# Add a Flower
def new_flower():
    global flower_list, wilted_list # Global Variables
    flower_new = Actor("flower") # new Flower Actor
    flower_new.pos = randint(50, WIDTH - 50), randint(150, HEIGHT - 100) # Position of new flower.
    flower_list.append(flower_new) # Adds new flower to the list of flowers.
    wilted_list.append("happy") # Let's Program know that the flower is not wilted.
    return

# Adding more flowers to the garden
def add_flowers():
    global game_over
    if not game_over:
        new_flower() # Calls the function new_flower to create new flowers
        clock.schedule(add_flowers, 2) # New Flower every 2 seconds !!! Changed from 4 seconds
    return

def check_wilt_times():
    global wilted_list, game_over, garden_happy
    if wilted_list: # This checks if there are any items in the wilted_list.
        for wilted_since in wilted_list: # code loops over each item in the wilted_list.
            if (not wilted_since == "happy"): # check if the flower is wilted and work out how long it’s been wilted.
                time_wilted = int(time.time() - wilted_since)
                if (time_wilted) > 15.0: # check if flower is wilted 
             
                    garden_happy = False
                    game_over = True
                    break
    return

def wilt_flower():
    global flower_list, wilted_list, game_over
    if not game_over:
        if flower_list:
            rand_flower = randint(0, len(flower_list) - 1) # generates random list index of the list of flowers 
        if (flower_list[rand_flower].image == "flower"): # Checks if the flowers in the list are wilted or not
            flower_list[rand_flower].image = "flower-wilt" 
            wilted_list[rand_flower] = time.time() # Resets the time 
        clock.schedule(wilt_flower, 3) # shows wilted flower 
    return

def check_flower_collision():
    global cow, flower_list, wilted_list # Global Variables
    index = 0 
    for flower in flower_list: # loops through all the flowers in the list
        if(flower.colliderect(cow) and flower.image == "flower-wilt"): # Condition if cow is next to the flower we're looking at
            flower.image = "flower" # Change wilted flower image back to original version
            wilted_list[index] = "happy" # Stops counting how long the flower's been wilted
            break # Stops the loop from checking the other flowers
        index = index + 1 # updates the program to move through the lists
    return

def check_fangflower_collision():
    # Global Variables
    global cow, fangflower_list, fangflower_collision
    global game_over
    for fangflower in fangflower_list:
        if fangflower.colliderect(cow): # Checks if cow and fangflower are next to each other
            cow.image = "zap" # Cow images of cow being zapped
            game_over = True # Tells program it is a game over
            break # Stops loop
    return

def velocity():
     random_dir = randint(0, 1) # generates a number that represents the direction of the fangflower.
     random_velocity = randint(2, 3) # generates the velocity of the fangflower with no direction yet.
     if random_dir == 0: # If the direction is 0, this returns a negative velocity
         return -random_velocity
     else: # If the direction is 1, this returns a positive velocity.
         return random_velocity

def mutate():
      # global variables
      global flower_list, fangflower_list, fangflower_vy_list
      global fangflower_vx_list, game_over
      # If the game is not over and there are still flowers left to mutate, this block of code will run.
      if not game_over and flower_list:
          rand_flower = randint(0, len(flower_list) - 1) # picks a random flower to mutate
          fangflower_pos_x = flower_list[rand_flower].x
          fangflower_pos_y = flower_list[rand_flower].y
          del flower_list[rand_flower] # removes the mutated flower from the list of flowers.
          fangflower = Actor("fangflower")
          fangflower.pos = fangflower_pos_x, fangflower_pos_y # sets the fangflower at the same position as the flower it mutated from.
          fangflower_vx = velocity() # sets how fast the fangflower is moving left or right on the screen.
          fangflower_vy = velocity() # sets how fast the fangflower is moving up or down on the screen
          fangflower = fangflower_list.append(fangflower) # adds a new fangflower to the list of fangflowers.
          # fangflower’s velocities are added to these lists.
          fangflower_vx_list.append(fangflower_vx)
          fangflower_vy_list.append(fangflower_vy)
          clock.schedule(mutate, 5) # schedules a call to mutate a flower every 15 seconds!!! Changed from 20 seconds
          return

def update_fangflowers():
    # Global Variables
    global fangflower_list, game_over
    if not game_over:
        index = 0 # Keeps track of which item it is dealing with
        for fangflower in fangflower_list: # Loops over all the fangflowers in list
            # x and y velocities of the fangflowers
            fangflower_vx = fangflower_vx_list[index]
            fangflower_vy = fangflower_vy_list[index]
            # new positon of the fangflower
            fangflower.x = fangflower.x + fangflower_vx
            fangflower.y = fangflower.y + fangflower_vy
            if fangflower.left < 0: # If the fangflower touches the left edge of the screen, this will make it start moving to the right.
                fangflower_vx_list[index] = -fangflower_vx
            if fangflower.right > WIDTH:
                fangflower_vx_list[index] = -fangflower_vx
            if fangflower.top < 150:
                fangflower_vy_list[index] = -fangflower_vy
            if fangflower.bottom > HEIGHT: # By changing its y velocity, the fangflower is brought back into the screen
                fangflower_vy_list[index] = -fangflower_vy
            index = index + 1
            return


def reset_cow():
    global game_over
    if not game_over: # if the game is not over yet
        cow.image = "cow" # Revert cow to original cow image
    return

# add flowers 
add_flowers()
#star killing flowers 
wilt_flower()



def update():
    global score, game_over, fangflower_collision
    global flower_list, fangflower_list, time_elapsed
    fangflower_collision = check_fangflower_collision()
    check_wilt_times()
    if not game_over:
        if keyboard.space: 
            cow.image = "cow-water" 
            clock.schedule(reset_cow, 0.5) 
            check_flower_collision() 
        if keyboard.left and cow.x > 0:
            cow.x -= 5
        elif keyboard.right and cow.x < WIDTH:
            cow.x += 5
        elif keyboard.up and cow.y > 150:
            cow.y -= 5
        elif keyboard.down and cow.y < HEIGHT:
            cow.y += 5
        
        if time_elapsed > 15 and not fangflower_list:
            mutate() # mutate flower 
        update_fangflowers() 

pgzrun.go()
