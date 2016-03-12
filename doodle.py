import pygame
import time

pygame.init()
WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)

pygame.key.set_repeat(50,50)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
jumper = pygame.sprite.Sprite()
jumper.image = pygame.image.load("elephant.bmp")
jumper.rect = jumper.image.get_rect()
screen.fill(WHITE)

clock = pygame.time.Clock()

#bottom of the screen
bottom = pygame.sprite.Sprite()
bottom.rect = pygame.Rect(0,HEIGHT - 50, WIDTH, 50)

def create_platform(x, y):
  width = 200
  height = 30
  platform = pygame.sprite.Sprite();
  platform.rect = pygame.Rect(x, y, width, height)
  return platform

def create_item(type, x, y):
  item = pygame.sprite.Sprite()
  item.image = pygame.image.load("firstaid.bmp")
  item.rect = item.image.get_rect()
  item.rect.x = x
  item.rect.y = y
  return item

## items!!!
items = pygame.sprite.OrderedUpdates()
items.add(create_item("first_aid", 400,300)) 

platforms = []
platform_colour = (200, 140, 80)
platforms.append(create_platform(200, 500))
platforms.append(create_platform(400, 300))

platforms.append(bottom)

## when player presses jump button we set jump_frame to 0
## then each frame we apply the position diff stored in the 
## jump_deltas to produce a parabolic jump
## then when we're finished we set jump_frame back to -1 ready to jump again
jump_frame = -1 # not jumping
jump_deltas = [ x**2 / 1.5 for x in range(10,0,-1)] 

## this tries to move the player, if we collide with a platform
## we don't allow the movement
def apply_move(move_x,move_y):
  jumper.rect.x += move_x
  jumper.rect.y += move_y
  jumper_group = pygame.sprite.GroupSingle(jumper)
  if pygame.sprite.groupcollide(jumper_group, platforms, False, False):
    jumper.rect.x -= move_x
    jumper.rect.y -= move_y

  if pygame.sprite.groupcollide(jumper_group, items, False, True):
    print("Item collected!!")
  
  

pygame.display.update()
gravity = 5
move = 5 # speed
jump = 50
game_running = True
while game_running:
  clock.tick(30) # limit framerate to 30fps
  apply_move(0, gravity) 

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      game_running = False
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
      game_running = False
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_UP:
	    # if the player is just above or on a platform we allow a jump
		# to test we form a rectangle just under the player and collide it against
		# the platforms
        feet = pygame.sprite.Sprite()
        feet.rect = pygame.Rect(jumper.rect.x, jumper.rect.y+3+jumper.rect.height,
        jumper.rect.width, 3)
        if pygame.sprite.groupcollide([feet], platforms, False, False):
         jump_frame = 0 # player is allowed to jump - start the jump sequence
      elif event.key == pygame.K_LEFT:
        apply_move(-move, 0)
      elif event.key == pygame.K_RIGHT:
        apply_move(move, 0)

  if jump_frame != -1:
    apply_move(0, -jump_deltas[jump_frame])
    jump_frame += 1
    if len(jump_deltas) <= jump_frame:
      jump_frame = -1
 
  screen.fill(WHITE)
  screen.blit(jumper.image, jumper.rect)
  screen.fill((50,50,50), bottom)

  for platform in platforms:
    screen.fill(platform_colour, platform.rect)


  for item in items:
    screen.blit(item.image, item.rect)

  pygame.display.update()

pygame.quit()
