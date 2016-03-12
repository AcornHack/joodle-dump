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

class Platform:
  def __init__(self, x, y):
    left = x
    height = 30
    width = 200
    top = y
    self.sprite = pygame.sprite.Sprite()
    self.sprite.rect = pygame.Rect(left, top, width, height)
    

platforms = []
platform_colour = (200, 140, 80)
platforms.append(Platform(200,HEIGHT -  100).sprite)
platforms.append(Platform(400, HEIGHT - 300).sprite)

platforms.append(bottom)

jump_frame = -1 # not jumping
jump_deltas = [ x**2 / 1.5 for x in range(10,0,-1)] 


def apply_move(move_x,move_y):
  jumper.rect.x += move_x
  jumper.rect.y += move_y
  jumper_group = pygame.sprite.GroupSingle(jumper)
  if pygame.sprite.groupcollide([jumper], platforms, False, False):
    jumper.rect.x -= move_x
    jumper.rect.y -= move_y

  if pygame.sprite.groupcollide(jumper_group,items, False, True):
    print("Item collected!!")
  
  

pygame.display.update()
gravity = 5
move = 5 # speed
jump = 50
game_running = True
while game_running:
  clock.tick()
  apply_move(0, gravity)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      game_running = False
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
      game_running = False
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_UP:
        feet = pygame.sprite.Sprite()
        feet.rect = pygame.Rect(jumper.rect.x, jumper.rect.y+3+jumper.rect.height,
        jumper.rect.width, 3)
        if pygame.sprite.groupcollide([feet], platforms, False, False):
         jump_frame = 0
      elif event.key == pygame.K_LEFT:
        apply_move(-move, 0)
      elif event.key == pygame.K_RIGHT:
        apply_move(move, 0)

  if jump_frame != -1:
    apply_move(0, -jump_deltas[jump_frame])
    jump_frame += 1
    if len(jump_deltas) <= jump_frame:
      jump_frame = -1
  
  if jumper.rect.colliderect(bottom):
    print("BOOM")
 
  screen.fill(WHITE)
  screen.blit(jumper.image, jumper.rect)
  screen.fill((50,50,50), bottom)

  for platform in platforms:
    screen.fill(platform_colour, platform.rect)


  for item in items:
    screen.blit(item.image, item.rect)

  pygame.display.update()

pygame.quit()
