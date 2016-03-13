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
  item.image = pygame.image.load("coin.png")
  item.rect = item.image.get_rect()
  item.rect.x = x
  item.rect.y = y
  return item

def to_camera_space(rect):
  return pygame.Rect(rect.x, rect.y-camera_offset, rect.width, rect.height)

## items!!!
items = pygame.sprite.OrderedUpdates()
items.add(create_item("coin", 400,1450)) 
items.add(create_item("coin", 600,1050)) 

platforms = []
platform_colour = (200, 140, 80)
platforms.append(create_platform(200, 1200+500))
platforms.append(create_platform(400, 1200+300))
platforms.append(create_platform(500, 1000+100))
platforms.append(create_platform(200, 1200+100))

platforms.append(create_platform(600, 1000+100))
platforms.append(create_platform(200, 900))

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
score = 0
def apply_move(move_x,move_y):
  global score
  global camera_offset 
  jumper.rect.x += move_x
  jumper.rect.y += move_y
  jumper_group = pygame.sprite.GroupSingle(jumper)
  if pygame.sprite.groupcollide(jumper_group, platforms, False, False):
    jumper.rect.x -= move_x
    jumper.rect.y -= move_y

  if pygame.sprite.groupcollide(jumper_group, items, False, True):
    print("Item collected!!" + str(score))
    score +=1
  
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

  keys = pygame.key.get_pressed();
  if keys[pygame.K_UP] or keys[pygame.K_SPACE] or keys[pygame.K_w]:
    # if the player is just above or on a platform we allow a jump
    # to test we form a rectangle just under the player and collide it against
    # the platforms
    feet = pygame.sprite.Sprite()
    feet.rect = pygame.Rect(jumper.rect.x, jumper.rect.y+3+jumper.rect.height,
    jumper.rect.width, 3)
    if pygame.sprite.groupcollide([feet], platforms, False, False):
        jump_frame = 0 # player is allowed to jump - start the jump sequence
  if keys[pygame.K_LEFT] or keys[pygame.K_a]:
    apply_move(-move, 0)
  if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
    apply_move(move, 0)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      game_running = False
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
      game_running = False
      
  #print("{:f}".format(jumper.rect.x))
  if jumper.rect.x < 0 :
    jumper.rect.x = 800
  elif jumper.rect.x > 800 :
    jumper.rect.x = 0
    
      for platform in platforms:
    if platform.rect.y > camera_offset+SCREEN_HEIGHT:
      print("kill platform")
      
  screen.fill(WHITE)

  if jump_frame != -1:
    apply_move(0, -jump_deltas[jump_frame])
    jump_frame += 1
    if len(jump_deltas) <= jump_frame:
      jump_frame = -1
 
  screen.blit(background_image,(0,0))
  screen.blit(jumper.image, to_camera_space(jumper.rect))
  font = pygame.font.Font(None, 36)
  text_image = font.render("score: "+str(score), True,(153, 45, 189))
  text_rect = text_image.get_rect(centerx=100, centery=50)
  screen.blit(text_image, text_rect)
  

  for platform in platforms:
    screen.fill(platform_colour, to_camera_space(platform.rect))


  for item in items:
    screen.blit(item.image, to_camera_space(item.rect))

  pygame.display.update()

pygame.quit()
