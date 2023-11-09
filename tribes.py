#Tribes 
#A top down building game
#start date 10/28/2023

'''

I had a fair idea where I create a top down building game, one of the mechanics is rune stones and rune dust inspired by the minecraft mod the runic dust mod,
which is no longer around.anyways, there is an huge island with a few mixed biomes, there are plants, tress, the typical flora and fauna. I am thinking of a style
similar to realm of the mad god mixed with a child of minecraft and terraria. The player starts off with the bare minimum by being washed up on the beach. The game 
is not necessarily intended to be survival against mobs, but they will be there to hinder the player and provide a combat purpose. The name will be Tribes. The
map itself will be the same and so will the biomes, but certain objects like plants, structures, objects, enemies, treasures, and passive mobs could be randomly
generated at one point. 

'''

#11/06/23 adding in a crafting window

#Here I am going to call all of my import statements that I will need for my game as needed. 

import pygame
from pygame.locals import *
import sys
import random

pygame.init()


# Constants for my screen
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 900 #basic screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #basic variable using the screen variables width and height above
pygame.display.set_caption('TribalSandbox   Tristan Dombroski     Version 0.003 "Blocks and Berrysnacks"') #this sets a caption for the application itself

clock = pygame.time.Clock() #this will be used to measure time/frames in the game

#world variables
#size of world
MAP_SIZE = 96

#size of tiles
TILE_SIZE = 64

#camera
camera_x, camera_y = 0, 0

# In the beginning of the file, after pygame.init() load the player and assign a rectangle along with other important variables (classes could also be used)
player_image = pygame.image.load('graphics/player.png').convert_alpha()
player_rect = player_image.get_rect()
player_x, player_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2  # Initial player position
player_speed = 8  # Adjust the speed as needed
interact = False


#following the player I want to establish a few tiles to visually enchance my world
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()
grass_surface = pygame.image.load('graphics/grass.png').convert_alpha()
water_surface = pygame.image.load('graphics/water.png').convert_alpha()
blockwall_surface = pygame.image.load('graphics/blockwall.png').convert_alpha()


#following images will be displayed on crafting window for now
# Load building tiles icon images
#trying to keep building blocks icons and other things as images
#wood tile
wood_tile_icon = pygame.image.load('graphics/wood_tile.png').convert_alpha()
wood_tile_icon_rect = wood_tile_icon.get_rect(midleft=(500, 550))
#stone tile
stone_tile_icon = pygame.image.load('graphics/stone_tile.png').convert_alpha()
stone_tile_icon_rect = stone_tile_icon.get_rect(midleft=(600, 650))


#here is an image for the crafting window, its a wood_spear
wood_spear_image = pygame.image.load('graphics/wood_spear.png')
wood_spear_image_rect = wood_spear_image.get_rect(midleft=(450,475))

#first consumable item
#Red Berry Snack
redberrysnack_image = pygame.image.load('graphics/redberrysnack.png')
redberrysnack_icon_rect = redberrysnack_image.get_rect(midleft=(600, 550))

#here I am going to make and blit a help window in the top right
help_window = pygame.image.load('graphics/help_window.png')
help_window_rect = help_window.get_rect(topleft=(1100,100))
#Here I want to make the hotbarfor my game
hotbar_image = pygame.image.load('graphics/hotbar.png')
hotbar_rect = hotbar_image.get_rect()
#hotbar = [None] * 9
# Coordinates for the top-left corner of the hotbar slots
hotbar_slot_x, hotbar_slot_y = 400, 64
# Width of each slot in the hotbar
hotbar_slot_width = 64
selected_slot = 0 #sets the inital value to 0 for bordering


#here I am going to attempt the 2nd crafting window
crafting_window_image = pygame.image.load('graphics/crafting_window.png').convert_alpha()
crafting_window_rect = crafting_window_image.get_rect(midleft=(400,550))
show_crafting_window = False
show_help_window = True



#first enemy entity being lazy with it just making a variable image and rect and will blit to a random location
weak_enemies = []
num_weak_enemies = 10

class WeakEnemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('graphics/grassmonster.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

for _ in range(num_weak_enemies):
    x = random.randint(0, (MAP_SIZE - 1) * TILE_SIZE)
    y = random.randint(0, (MAP_SIZE - 1) * TILE_SIZE)
    weak_enemy = WeakEnemy(x, y)
    weak_enemies.append(weak_enemy)


class Hotbar:
    def __init__(self, size, image):
        self.size = size
        self.items = [None] * size
        self.image = image  # Assign the hotbar image to the instance

    def add_item(self, item):
        # Add item to the first available slot in the hotbar
        for i in range(self.size):
            if self.items[i] is None:
                self.items[i] = item
                break
    def remove_item(self, item):
        # Remove the specified item from the hotbar, if present
        if item in self.items:
            self.items.remove(item)

#creating a hotbar instance with a size of 9
hotbar = Hotbar(9, hotbar_image)


# Defining Redberrybush class (similar to how I handled other objects)
class Redberrybush:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('graphics/redberrybush.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # List of items that can be dropped from the bush
        self.dropped_items = ['woodstick.png', 'redberry.png', 'bushleaf.png', 'redberryseed.png']

    def harvest(self):
        # Remove the bush from the list of redberry bushes (assuming you have a list named redberrybushes)
        redberrybushes.remove(self)

        # Randomly select an item from the dropped items list
        dropped_item = random.choice(self.dropped_items)

       
        return(dropped_item)
        

# Create a list to store redberrybush objects
redberrybushes = []
MAX_REDBERRYBUSHES = 16
REDBERRYBUSH_SPAWN_COOLDOWN = 5  # 500 milliseconds (5 seconds)
# Initialize timer variables
redberrybush_spawn_timer = 0
current_redberrybush_count = 0



# Spawn redberrybushes randomly on the map
for _ in range(MAX_REDBERRYBUSHES):  # MAX_REDBERRYBUSHES is your defined maximum count
    x = random.randint(0, MAP_SIZE - 1) * TILE_SIZE
    y = random.randint(0, MAP_SIZE - 1) * TILE_SIZE
    redberrybush = Redberrybush(x, y)
    redberrybushes.append(redberrybush)



#here I am going to make a copper crop class to spawn in like my bushes for damian
class Coppercrop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('graphics/copper_crop.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # List of items that can be dropped from the bush
        self.dropped_items = ['copper_chunk.png', 'stone_chunk.png']

    def harvest(self):
        # Remove the bush from the list of redberry bushes (assuming you have a list named redberrybushes)
        coppercrops.remove(self)

        # Randomly select an item from the dropped items list
        dropped_item = random.choice(self.dropped_items)

        return(dropped_item)



# Create a list to store redberrybush objects
coppercrops = []
MAX_COPPERCROPS = 8

# Spawn cropper crops randomly on the map
for _ in range(MAX_COPPERCROPS):  # MAX_COPPERCROPS is your defined maximum count
    x = random.randint(0, MAP_SIZE - 1) * TILE_SIZE
    y = random.randint(0, MAP_SIZE - 1) * TILE_SIZE
    coppercrop = Coppercrop(x, y)
    coppercrops.append(coppercrop)

class CraftedItem:
    def __init__(self, image, recipe):
        self.image = image  # Image path of the crafted item
        self.recipe = recipe  # Recipe pattern for crafting this item


#crafting format goes: { (('material','material'),): 'crafted_item', (('material','material'),): 'crafted_item', }
crafting_recipes = {
    (('woodstick.png', 'woodstick.png', 'leaf.png'),): 'wood_tile.png',
    (('copper_chunk.png', 'copper_chunk.png', 'woodstick.png'),): 'wood_spear.png',
    (('redberry.png', 'redberry.png', 'bushleaf.png'),): 'redberrysnack.png',
    (('stone_chunk.png', 'stone_chunk.png'),): 'stone_tile.png'
    # Add more recipes as desired
}

#variable for crafting window
items_to_remove = []  # Define items_to_remove outside the event loop



# Define tile types (you can use numbers to represent different tile types)
GROUND = 0
GRASS = 1
WATER = 2
WOODTILE = 3
STONETILE = 4

# Define more tile types or tile variables as needed...
MAX_POND_AMOUNT = 5  # Set the maximum number of ponds allowed
pond_count = 0


# Create a 10x10 tilemap filled with ground tiles
tilemap = [[GROUND for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]


# Populate tilemap with ground tiles

for row in range(MAP_SIZE):
    for col in range(MAP_SIZE):
        if tilemap[row][col] == GROUND:
            tilemap[row][col] = GROUND

for _ in range(int(0.02 * MAP_SIZE ** 2)):  # Adjust the density of grass tiles as needed
    row, col = random.randint(0, MAP_SIZE - 1), random.randint(0, MAP_SIZE - 1)
    tilemap[row][col] = GRASS




running = True



while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == KEYDOWN:
            if event.key == K_e:
                interact = True

            elif event.key == K_z:
                # Remove the selected item from the hotbar
                selected_item = hotbar.items[selected_slot]
                if selected_item:
                    hotbar.remove_item(selected_item)

            elif event.key == K_h:
                show_help_window = True

            if event.key in [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9]:
                # Subtracting K_1 from the pressed key gives the slot index (0-8)
                selected_slot = event.key - K_1

            if event.key == K_c:
                show_crafting_window = not show_crafting_window

        elif event.type == KEYUP:
            if event.key == K_e:
                interact = False
            if event.key == K_h:
                show_help_window = not show_help_window

        #elif event.type == MOUSEBUTTONDOWN:
        #    mouse_x, mouse_y = event.pos
        #    world_x, world_y = mouse_x + camera_x, mouse_y + camera_y
        #    tile_x, tile_y = world_x // TILE_SIZE, world_y // TILE_SIZE

        elif event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            items_to_remove.clear() #this clears the list of items that will be used in crafting for later purposes
            selected_item = hotbar.items[selected_slot] #this variable allows me to check what is selected in the hotbar and perform actions with it


            #the initial code sections below are for crafting
            # Check for mouse click on wood_spear icon
            if wood_spear_image_rect.collidepoint(mouse_x, mouse_y):
                if all(item in hotbar.items for item in ('woodstick.png', 'copper_chunk.png')):
                    #this following code line is for testing purposes
                    #print('you clicked here')
                    #show_crafting_window = False
                    # add the crafted item, wood_spear               
                    hotbar.add_item('wood_spear.png')
                    #remove the crafting materials
                    hotbar.remove_item('woodstick.png')
                    hotbar.remove_item('copper_chunk.png')
                    show_crafting_window = False


            # Check for mouse click on wood_tile icon
            elif wood_tile_icon_rect.collidepoint(mouse_x, mouse_y):
                # Craft wood_tile if player has required materials in the hotbar
                if all(item in hotbar.items for item in ('woodstick.png', 'bushleaf.png')):
                    hotbar.add_item('wood_tile.png')
                    # Remove consumed materials from the hotbar
                    hotbar.remove_item('woodstick.png')
                    hotbar.remove_item('bushleaf.png')
                    show_crafting_window = False

            # Check for mouse click on wood_tile icon
            elif stone_tile_icon_rect.collidepoint(mouse_x, mouse_y):
                # Craft wood_tile if player has required materials in the hotbar
                if all(item in hotbar.items for item in ('stone_chunk.png', 'stone_chunk.png')):
                    hotbar.add_item('stone_tile.png')
                    # Remove consumed materials from the hotbar
                    hotbar.remove_item('stone_chunk.png')
                    hotbar.remove_item('stone_chunk.png')
                    show_crafting_window = False


            # Check for mouse click on redberrysnack icon
            elif redberrysnack_icon_rect.collidepoint(mouse_x, mouse_y):
                # Craft redberrysnack if player has required materials in the hotbar
                if all(item in hotbar.items for item in ('redberry.png', 'bushleaf.png')):
                    hotbar.add_item('redberrysnack.png')
                    # Remove consumed materials from the hotbar
                    hotbar.remove_item('redberry.png')
                    hotbar.remove_item('bushleaf.png')
                    show_crafting_window = False
            # Check for mouse click on other item icons and handle crafting logic similarly...




            # Check if the selected item via the number keys and the variable selected slot is a wood tile
            if selected_item == 'wood_tile.png':
                # Get the tile coordinates where the player clicked
                tile_x = (mouse_x + camera_x) // TILE_SIZE
                tile_y = (mouse_y + camera_y) // TILE_SIZE

                # Place the wood tile on the ground if it's a valid position (e.g., not on water)
                if tilemap[tile_y][tile_x] != WATER:
                    # Update the tilemap
                    tilemap[tile_y][tile_x] = WOODTILE

                    # Remove one wood tile from the hotbar
                    hotbar.remove_item(selected_item)

            # Check if the selected item via the number keys and the variable selected slot is a stone tile
            if selected_item == 'stone_tile.png':
                # Get the tile coordinates where the player clicked
                tile_x = (mouse_x + camera_x) // TILE_SIZE
                tile_y = (mouse_y + camera_y) // TILE_SIZE

                # Place the wood tile on the ground if it's a valid position (e.g., not on water)
                if tilemap[tile_y][tile_x] != WATER:
                    # Update the tilemap
                    tilemap[tile_y][tile_x] = STONETILE

                    # Remove one wood tile from the hotbar
                    hotbar.remove_item(selected_item)





            # Remove consumed materials from the hotbar
            for item in items_to_remove:
                hotbar.remove_item(item)
        #By using a separate list (items_to_remove) to store the items that need to be removed and removing them outside the loop, you avoid modifying the hotbar list while iterating over it. This should prevent unexpected behavior and potential crashes in your game.
        #Additionally, ensure that the item names and file paths are correct to avoid any issues with item identification.



    
    camera_x = player_x - SCREEN_WIDTH // 2
    camera_y = player_y - SCREEN_HEIGHT // 2
    # Clamp camera position to stay within the world boundaries
    camera_x = max(0, min(camera_x, (MAP_SIZE * TILE_SIZE) - SCREEN_WIDTH))
    camera_y = max(0, min(camera_y, (MAP_SIZE * TILE_SIZE) - SCREEN_HEIGHT))

   
    # Render the visible portion of the tilemap based on camera position
    start_row = camera_y // TILE_SIZE
    end_row = start_row + (SCREEN_HEIGHT // TILE_SIZE) + 1
    start_col = camera_x // TILE_SIZE
    end_col = start_col + (SCREEN_WIDTH // TILE_SIZE) + 1

    # Render the tilemap
    # Render the visible portion of the tilemap based on camera position
    # Render the tilemap
    

    #this handles blitting my tiles into the game itself so it becomes the environment
    for row in range(start_row, min(end_row, MAP_SIZE)):
        for col in range(start_col, min(end_col, MAP_SIZE)):
            tile_type = tilemap[row][col]
            tile_x, tile_y = (col * TILE_SIZE) - camera_x, (row * TILE_SIZE) - camera_y

            if tile_type == GROUND:
                screen.blit(ground_surface, (tile_x, tile_y))
            elif tile_type == GRASS:
                screen.blit(grass_surface, (tile_x, tile_y))
            elif tile_type == WATER:
                screen.blit(water_surface, (tile_x, tile_y))

            #here I assume is where I put a code line to handle building tiles 
            elif tile_type == WOODTILE:
                screen.blit(wood_tile_icon, (tile_x, tile_y))

            elif tile_type == STONETILE:
                screen.blit(stone_tile_icon, (tile_x, tile_y))

            # Check for border tiles
            if row == 0 or row == MAP_SIZE - 1 or col == 0 or col == MAP_SIZE - 1:
                screen.blit(blockwall_surface, (tile_x, tile_y))
                    

    # Update redberry bush spawn timer
    current_time = pygame.time.get_ticks()  # Get current time in milliseconds
    if current_time - redberrybush_spawn_timer > REDBERRYBUSH_SPAWN_COOLDOWN and current_redberrybush_count < MAX_REDBERRYBUSHES:
        # Spawn a new redberry bush
        x = random.randint(0, MAP_SIZE - 1) * TILE_SIZE
        y = random.randint(0, MAP_SIZE - 1) * TILE_SIZE
        redberrybush = Redberrybush(x, y)
        redberrybushes.append(redberrybush)
        
        # Update timer and redberry bush count
        redberrybush_spawn_timer = current_time
        current_redberrybush_count += 1
    #here I want to blit or display my plants
    for redberrybush in redberrybushes:
        bush_x, bush_y = redberrybush.x - camera_x, redberrybush.y - camera_y
        screen.blit(redberrybush.image, (bush_x, bush_y))

    #here I want to blit or display my copper crops
    for coppercrop in coppercrops:
        crop_x, crop_y = coppercrop.x - camera_x, coppercrop.y - camera_y
        screen.blit(coppercrop.image, (crop_x, crop_y))

    #here I want to display my weak enemies
    for weak_enemy in weak_enemies:
        weak_enemy.rect.topleft = (weak_enemy.x - camera_x, weak_enemy.y - camera_y)
        screen.blit(weak_enemy.image, weak_enemy.rect)

    # You can add additional logic here, like enemy movement, collision checks, etc.
            

    # Generate ponds only if the number of existing ponds is less than MAX_POND_AMOUNT
    
    if pond_count < MAX_POND_AMOUNT:
        pond_count += 1
        pond_row = random.randint(0, MAP_SIZE - 9)
        pond_col = random.randint(0, MAP_SIZE - 9)
        for row in range(pond_row, pond_row + 9):
            for col in range(pond_col, pond_col + 9):
                tilemap[row][col] = WATER

    
            
    # Update Game Logic Here
    # Update player_rect position
    player_rect.topleft = (player_x, player_y)

    keys = pygame.key.get_pressed()
    

    #keys to handle movement
    if keys[K_a]:
        player_x -= player_speed
    if keys[K_d]:
        player_x += player_speed
    if keys[K_w]:
        player_y -= player_speed
    if keys[K_s]:
        player_y += player_speed


    #keys to handle inventory and other options like interact, click might be interact.
    # Inside your game loop, after checking for 'E' key press
    if interact:
        # Check if the player is near a redberry bush and harvest it
        
        # Check if the player is near a redberry bush and harvest it
        for redberrybush in redberrybushes:
            if player_rect.colliderect(redberrybush.rect) and interact:
                dropped_item = redberrybush.harvest()
                
                hotbar.add_item(dropped_item)

        #checks to see if player is colliding with a copper crop and interacting
        for coppercrop in coppercrops:
            if player_rect.colliderect(coppercrop.rect) and interact:
                dropped_item = coppercrop.harvest()
                
                hotbar.add_item(dropped_item)
                
                #item_image = pygame.image.load(f'graphics/{dropped_item}').convert_alpha()
                #screen.blit(item_image, (200, 200))  # Blit the dropped item at (200, 200) for verification
                

    # Draw Game Elements Here
    if show_crafting_window: 
        screen.blit(crafting_window_image, crafting_window_rect.topleft)#this is the window that gets displayed when I press c
        screen.blit(wood_spear_image, wood_spear_image_rect) #this is an icon of an item I want the player to be able to click on and craft if they have the right materials
        screen.blit(wood_tile_icon, wood_tile_icon_rect)
        screen.blit(redberrysnack_image, redberrysnack_icon_rect)
        screen.blit(stone_tile_icon, stone_tile_icon_rect)


    # Draw the player on the screen relative to the camera position
    screen.blit(player_image, (player_x - camera_x, player_y - camera_y))

    if show_help_window:
        screen.blit(help_window, help_window_rect)
    

  
    screen.blit(hotbar.image, (hotbar_slot_x, hotbar_slot_y))

   

    for i, item in enumerate(hotbar.items):
        if item:
            item_icon = pygame.image.load(f'graphics/{item}').convert_alpha()
            item_x = hotbar_slot_x + i * hotbar_slot_width
            item_y = hotbar_slot_y
            screen.blit(item_icon, (item_x, item_y))


    # Draw a border around the selected hotbar slot
    selected_slot_x = hotbar_slot_x + selected_slot * hotbar_slot_width
    pygame.draw.rect(screen, (255, 0, 0), (selected_slot_x, hotbar_slot_y, hotbar_slot_width, hotbar_slot_width), 2)

    # Update the Display
    pygame.display.flip() #I still dont know the different between pygame.display.flip() and pygame.display.update()

    # Limit Frames Per Second
    clock.tick(60)  # Limit the game to 60 frames per second

pygame.quit()
sys.exit()