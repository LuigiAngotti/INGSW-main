import pygame
import button
import  main
import level as l

pygame.init()
c=0
#create game window
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

#game variables
game_paused = False
menu_state = "main"

#define fonts
font = pygame.font.SysFont("arialblack", 40)

#define colours
TEXT_COL = (255, 255, 255)

#load button images
resume_img = pygame.image.load("../resources/images/livello_uno.png").convert_alpha()
options_img = pygame.image.load("../resources/images/levello2.png").convert_alpha()
quit_img = pygame.image.load("../resources/images/button_quit.png").convert_alpha()
video_img = pygame.image.load('../resources/images/button_video.png').convert_alpha()
audio_img = pygame.image.load('../resources/images/button_audio.png').convert_alpha()
keys_img = pygame.image.load('../resources/images/button_keys.png').convert_alpha()
back_img = pygame.image.load('../resources/images/button_back.png').convert_alpha()

#create button instances
resume_button = button.Button(304, 125, resume_img, 1)
options_button = button.Button(297, 250, options_img, 1)
quit_button = button.Button(336, 375, quit_img, 1)
video_button = button.Button(226, 75, video_img, 1)
audio_button = button.Button(225, 200, audio_img, 1)
keys_button = button.Button(246, 325, keys_img, 1)
back_button = button.Button(332, 450, back_img, 1)
rect = pygame.Rect(0, 0, 200, 200)


def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#game loop
run = True
def run():
  global run
  while run:
    global game_paused
    global menu_state
    global resume_button
    global c

    screen.fill((52, 78, 91))

    #check if game is paused
    if game_paused == True:
      #check menu state
      main.running=False
      if menu_state == "main":
        #draw pause screen buttons
        if resume_button.draw(screen):
          game_paused = False
          main.running=True
          main.run()
          #memento = main.game.caretaker.get_memento(0)
          #score = memento.score
          if main.level.number>=1:
            c=main.game.load_game(main.level.number-1)
            print("score leve",c.score)

          if(c.score>=20000 and c.score<40000):
            resume_img = pygame.image.load("../resources/images/livello_uno copia.png").convert_alpha()
            resume_button = button.Button(304, 125, resume_img, 1)
          elif c.score>=40000 and c.score<60000:
             resume_img = pygame.image.load("../resources/images/livello_uno copia 2stra.png").convert_alpha()
             resume_button = button.Button(304, 125, resume_img, 1)
          elif c.score>=60000:
            resume_img = pygame.image.load("../resources/images/livello_uno copia 3stra copia.png").convert_alpha()
            resume_button = button.Button(304, 125, resume_img, 1)
          if resume_button.draw(screen):


            main.running=True
            main.run()


        if quit_button.draw(screen):
          run = False
      #check if the options menu is open
      if menu_state == "options":
        #draw the different options buttons
        if video_button.draw(screen):
          print("Video Settings")
        if audio_button.draw(screen):
          print("Audio Settings")
        if keys_button.draw(screen):
          print("Change Key Bindings")
        if back_button.draw(screen):
          menu_state = "main"
    else:
      draw_text("Press SPACE to pause", font, TEXT_COL, 160, 250)

    #event handler
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          game_paused = True
      if event.type == pygame.QUIT:
        run = False

    pygame.display.update()

  pygame.quit()