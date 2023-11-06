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


#Here I am going to call all of my import statements that I will need for my game as needed. 
import pygame
from pygame.locals import *
import sys
import random

pygame.init()


# Constants for my screen
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 900 #basic screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #basic variable using the screen variables width and height above
pygame.display.set_caption('TribalSandbox   Tristan Dombroski     Version 0.001 "Place and Replace"') #this sets a caption for the application itself

clock = pygame.time.Clock() #this will be used to measure time/frames in the game


# In the beginning of the file, after pygame.init() load the player and assign a rectangle along with other important variables (classes could also be used)
player_image = pygame.image.load('graphics/player.png').convert_alpha()
player_rect = player_image.get_rect()
player_x, player_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2  # Initial player position
player_speed = 5  # Adjust the speed as needed


#following the player I want to establish a few tiles to visually enchance my world
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()
grass_surface = pygame.image.load('graphics/grass.png').convert_alpha()
water_surface = pygame.image.load('graphics/water.png').convert_alpha()
blockwall_surface = pygame.image.load('graphics/blockwall.png').convert_alpha()

#Here I want to make the hotbarfor my game
hotbar_image = pygame.image.load('graphics/hotbar.png')
hotbar_rect = hotbar_image.get_rect()

# Coordinates for the top-left corner of the hotbar slots
hotbar_slot_x, hotbar_slot_y = 400, 64

# Width of each slot in the hotbar
hotbar_slot_width = 64


# Load tile icon images
wood_tile_icon = pygame.image.load('graphics/wood_tile.png').convert_alpha()
stone_tile_icon = pygame.image.load('graphics/stone_tile.png').convert_alpha()

# Coordinates for the top-left corner of each slot in the hotbar
wood_tile_slot_x, wood_tile_slot_y = 10, 10
stone_tile_slot_x, stone_tile_slot_y = 84, 10



# Define tile types (you can use numbers to represent different tile types)
GROUND = 0
GRASS = 1
WATER = 2

# Define more tile types or tile variables as needed...
MAX_POND_AMOUNT = 5  # Set the maximum number of ponds allowed
pond_count = 0

#size of world
MAP_SIZE = 96

#size of tiles
TILE_SIZE = 64

# Create a 10x10 tilemap filled with ground tiles
tilemap = [[GROUND for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]



# Populate tilemap with ground tiles
# Populate tilemap with ground tiles
for row in range(MAP_SIZE):
    for col in range(MAP_SIZE):
        if tilemap[row][col] == GROUND:
            tilemap[row][col] = GROUND

for _ in range(int(0.02 * MAP_SIZE ** 2)):  # Adjust the density of grass tiles as needed
    row, col = random.randint(0, MAP_SIZE - 1), random.randint(0, MAP_SIZE - 1)
    tilemap[row][col] = GRASS



camera_x, camera_y = 0, 0


#my variable set to True to create my game loop
running = True
selected_tile_type = "wood"  # Initial selected tile type

if selected_tile_type == "wood":
    pygame.draw.rect(screen, (255, 0, 0), (hotbar_slot_x, hotbar_slot_y, hotbar_slot_width, hotbar_slot_width), 2)
    screen.blit(wood_tile_icon, (hotbar_slot_x, hotbar_slot_y))
elif selected_tile_type == "stone":
    pygame.draw.rect(screen, (255, 0, 0), (hotbar_slot_x + hotbar_slot_width, hotbar_slot_y, hotbar_slot_width, hotbar_slot_width), 2)
    screen.blit(stone_tile_icon, (hotbar_slot_x + hotbar_slot_width, hotbar_slot_y))

while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            world_x, world_y = mouse_x + camera_x, mouse_y + camera_y
            tile_x, tile_y = world_x // TILE_SIZE, world_y // TILE_SIZE

            # Left mouse button clicked
            if event.button == 1:
                if 0 <= tile_x < MAP_SIZE and 0 <= tile_y < MAP_SIZE:
                    tilemap[tile_y][tile_x] = selected_tile_type

            # Right mouse button clicked
            elif event.button == 3:
                if 0 <= tile_x < MAP_SIZE and 0 <= tile_y < MAP_SIZE:
                    tilemap[tile_y][tile_x] = GROUND
    #here I am going to attempt to place the camera variables and purpose within the running loop
    # Update camera position based on player's position
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
    keys = pygame.key.get_pressed()
    #keys to handle hotbar
    if keys[K_1]:
        selected_tile_type = "wood"
    if keys[K_2]:
        selected_tile_type = "stone"


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
            elif tile_type == "wood":
                screen.blit(wood_tile_icon, (tile_x, tile_y))
            elif tile_type == "stone":
                screen.blit(stone_tile_icon, (tile_x, tile_y))

            # Check for border tiles
            if row == 0 or row == MAP_SIZE - 1 or col == 0 or col == MAP_SIZE - 1:
                screen.blit(blockwall_surface, (tile_x, tile_y))
                    

            
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

    #keys to handle hotbar
    if keys[K_1]:
        selected_tile_type = "wood"
    if keys[K_2]:
        selected_tile_type = "stone"

    #keys to handle inventory and other options like interact, click might be interact.

    # Draw Game Elements Here
    
    # Draw the player on the screen relative to the camera position
    screen.blit(player_image, (player_x - camera_x, player_y - camera_y))

    #draw the hotbar onto the screen relative to the camera position
    #screen.blit(hotbar_image, (500, 64))

    # Render selected tile type in the hotbar
    # Draw game elements
    screen.blit(hotbar_image, (hotbar_slot_x, hotbar_slot_y))

    # Always render wood tile icon at the first slot in the hotbar
    screen.blit(wood_tile_icon, (hotbar_slot_x, hotbar_slot_y))

    # Always render stone tile icon at the second slot in the hotbar
    screen.blit(stone_tile_icon, (hotbar_slot_x + hotbar_slot_width, hotbar_slot_y))

    # Highlight selected tile type in the hotbar
    # Draw selected tile type icon in the hotbar with red border
    if selected_tile_type == "wood":
        pygame.draw.rect(screen, (255, 0, 0), (hotbar_slot_x, hotbar_slot_y, hotbar_slot_width, hotbar_slot_width), 2)
    elif selected_tile_type == "stone":
        pygame.draw.rect(screen, (255, 0, 0), (hotbar_slot_x + hotbar_slot_width, hotbar_slot_y, hotbar_slot_width, hotbar_slot_width), 2)


    # Update the Display
    pygame.display.flip() #I still dont know the different between pygame.display.flip() and pygame.display.update()

    # Limit Frames Per Second
    clock.tick(60)  # Limit the game to 60 frames per second

pygame.quit()
sys.exit()