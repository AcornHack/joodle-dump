import pygame
import time

# todo
# wrap round off edge of screen
# make screen scrolling smoother?
# add audio?
# new character
# simple character animation?
# tune movement to make it feel good
# add more platforms
# add more items and different types
# fall down to a crisis
# remove platforms that scroll off the bottom of the screen, so player freefalls after fall

pygame.init()
WIDTH = 800
HEIGHT = 1800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)

pygame.key.set_repeat(50,50)
screen = pygame.display.set_mode((WIDTH, SCREEN_HEIGHT))

background_image = pygame.image.load ("blue-sky.jpg")
jumper = pygame.sprite.Sprite()
jumper.image = pygame.image.load("turtle.png")
jumper.rect = jumper.image.get_rect()
jumper.rect.y = 1500
screen.fill(WHITE)

clock = pygame.time.Clock()

# as the player moves up this decreases and the screen scrolls upwards
camera_offset = 1200

#bottom of the screen
bottom = pygame.sprite.Sprite()
bottom.rect = pygame.Rect(-50,HEIGHT - 50, WIDTH+100, 50)

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

def to_camera_space(rect):
  return pygame.Rect(rect.x, rect.y-camera_offset, rect.width, rect.height)

## items!!!
items = pygame.sprite.OrderedUpdates()
items.add(create_item("first_aid", 400,1450)) 

platforms = []
platform_colour = (200, 140, 80)
platforms.append(create_platform(200, 1200+500))
platforms.append(create_platform(400, 1200+300))
platforms.append(create_platform(500, 1000+100))
platforms.append(create_platform(200, 1200+100))

platforms.append(bottom)

## when player presses jump button we set jump_frame to 0
## then each frame we apply the position diff stored in the 
## jump_deltas to produce a parabolic jump
## then when we're finished we set jump_frame back to -1 ready to jump again
jump_frame = -1 # not jumping
jump_deltas = [ x**2 / 1.5 for x in range(10,0,-1)] 

## this tries to move the player, if we collide with a platform
## we don't allow the movement, if we collide with an item we
## collect it
def apply_move(move_x,move_y):
  global camera_offset 
  jumper.rect.x += move_x
  jumper.rect.y += move_y
  jumper_group = pygame.sprite.GroupSingle(jumper)
  if pygame.sprite.groupcollide(jumper_group, platforms, False, False):
    jumper.rect.x -= move_x
    jumper.rect.y -= move_y

  if pygame.sprite.groupcollide(jumper_group, items, False, True):
    print("Item collected!!")
  
  #print("y={:d} camera_offset={:f}" .format(jumper.rect.y, camera_offset) )
  # if player is more than halfway up the screen, scroll the screen upwards
  if jumper.rect.y < camera_offset + SCREEN_HEIGHT / 2 :
    camera_offset = jumper.rect.y - SCREEN_HEIGHT / 2
  # if player is falling off bottom of screen scroll screen downwards
  if jumper.rect.y + jumper.rect.height > camera_offset + SCREEN_HEIGHT:
    camera_offset = jumper.rect.y + jumper.rect.height - SCREEN_HEIGHT + 20
  

pygame.display.update()
gravity = 5
move = 15 # speed
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
      if event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w:
	    # if the player is just above or on a platform we allow a jump
		# to test we form a rectangle just under the player and collide it against
		# the platforms
        feet = pygame.sprite.Sprite()
        feet.rect = pygame.Rect(jumper.rect.x, jumper.rect.y+3+jumper.rect.height,
        jumper.rect.width, 3)
        if pygame.sprite.groupcollide([feet], platforms, False, False):
         jump_frame = 0 # player is allowed to jump - start the jump sequence
      elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        apply_move(-move, 0)
      elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        apply_move(move, 0)


  print("{:f}".format(jumper.rect.x))
  if jumper.rect.x < 0 :
    jumper.rect.x = 800
  elif jumper.rect.x > 800 :
    jumper.rect.x = 0
    
  screen.fill(WHITE)

  if jump_frame != -1:
    apply_move(0, -jump_deltas[jump_frame])
    jump_frame += 1
    if len(jump_deltas) <= jump_frame:
      jump_frame = -1
 
  screen.blit(background_image,(0,0))
  screen.blit(jumper.image, to_camera_space(jumper.rect))

  for platform in platforms:
    screen.fill(platform_colour, to_camera_space(platform.rect))


  for item in items:
    screen.blit(item.image, to_camera_space(item.rect))

  pygame.display.update()

pygame.quit()
