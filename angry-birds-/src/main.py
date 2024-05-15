import os
import sys
import math
import time
import pygame
import pygetwindow
current_path = os.getcwd()
import pymunk as pm
from characters import Bird
from level2 import Level
import Mento2 as m2
pos_x_screen = 0
pos_y_screen = 0
os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (0, 0)

game=m2.Game()
pygame.init()
#inizializziamo la finestra
screen = pygame.display.set_mode((1200,600),pygame.NOFRAME) #dimensione della finestra, se lasciata vuota diventa full scree

#pygame.display.set_caption("My Game")

#carichiamo tutte le immagini usate dai modelli nel gioco
redbird = pygame.image.load(
    "../resources/images/red-bird3.png").convert_alpha()
Menu = pygame.image.load(
    "../resources/images/Menu_Items.jpg").convert_alpha()
background2 = pygame.image.load(
    "../resources/images/background3.png").convert_alpha()
sling_image = pygame.image.load(
    "../resources/images/sling-3.png").convert_alpha()
full_sprite = pygame.image.load(
    "../resources/images/full-sprite.png").convert_alpha()

demagebird=pygame.image.load("../resources/images/puff.png").convert_alpha()
#tagliamo le immagine che includono piu' modelli
rect = pygame.Rect(181, 1050, 50, 50)
cropped = full_sprite.subsurface(rect).copy()
pig_image = pygame.transform.scale(cropped, (30, 30))
#immagine pig base dannegiato
rect = pygame.Rect(131,1050, 50,50)
cropped2 = full_sprite.subsurface(rect).copy()
damaged_pig_image = pygame.transform.scale(cropped2, (40,40))
#immagine king pig
rect = pygame.Rect(40,0,130,155)
croppedKing = full_sprite.subsurface(rect).copy()
king_pig_image = pygame.transform.scale(croppedKing, (45,45))
#immagine king pig dannegiato
rect = pygame.Rect(171,0,130,155)
croppedKingDmg = full_sprite.subsurface(rect).copy()
king_pig_dmg_img = pygame.transform.scale(croppedKingDmg, (45,45))
#immagine bearded pig
rect = pygame.Rect(645,200,105,100)
croppedBeard = full_sprite.subsurface(rect).copy()
bearded_pig_img = pygame.transform.scale(croppedBeard, (45,45))
#immagine bearded pig dannegiato
rect = pygame.Rect(245,340, 110,100)
croppedBeardDmg = full_sprite.subsurface(rect).copy()
bearded_pig_dmg_img = pygame.transform.scale(croppedBeardDmg, (45,45))

buttons = pygame.image.load(
    "../resources/images/selected-buttons.png").convert_alpha()
pig_happy = pygame.image.load(
    "../resources/images/pig_failed.png").convert_alpha()
stars = pygame.image.load(
    "../resources/images/stars-edited.png").convert_alpha()
rect = pygame.Rect(164, 10, 60, 60)
pause_button = buttons.subsurface(rect).copy()
rect = pygame.Rect(24, 4, 100, 100)
replay_button = buttons.subsurface(rect).copy()
rect = pygame.Rect(142, 365, 130, 100)
next_button = buttons.subsurface(rect).copy()

#icone stars
rect = pygame.Rect(0, 0, 200, 200)
star1 = stars.subsurface(rect).copy()
rect = pygame.Rect(204, 0, 200, 200)
star2 = stars.subsurface(rect).copy()
rect = pygame.Rect(426, 0, 200, 200)
star3 = stars.subsurface(rect).copy()

#impostimao un orologio per la refresh rate
clock = pygame.time.Clock()
rect = pygame.Rect(18, 212, 100, 100)
play_button = buttons.subsurface(rect).copy()
clock = pygame.time.Clock()

running = True  #variabile per loop principale del gioco

# base della fisica
space = pm.Space()
space.gravity = (0.0, -700.0)

#contenitori oggetti
pigs = []
birds = []
king_pigs = []
bearded_pigs = []
balls = []
polys = []
beams = []
columns = []
poly_points = []
ball_number = 0
polys_dict = {}

mouse_distance = 0  #variabile del mouse per l'azione della fionda
rope_lenght = 90    #variabile della fionda per il lancio dei bird
angle = 0   #angolo per il calcolo del percorso dei bird lanciati

#posizone del mouse
x_mouse = 0
y_mouse = 0
count = 0
t2 =0
mouse_pressed = False

#variabili temporali
t1 = 0
tick_to_next_circle = 10

#colori per i modelli e le loro forme
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#posizoni della fiodna
sling_x, sling_y = 135, 450
sling2_x, sling2_y = 160, 450
score = 0   #punteggio
game_state = 0  #variabile per modificare lo stato del gioco: chiusura, reset

bird_path = []

counter = 0
restart_counter = False
bonus_score_once = True

#fonts per la scrittura
bold_font = pygame.font.SysFont("arial", 30, bold=True)
bold_font2 = pygame.font.SysFont("arial", 40, bold=True)
bold_font3 = pygame.font.SysFont("arial", 50, bold=True)
wall = False

# pavimento fisico statico
static_body = pm.Body(body_type=pm.Body.STATIC)
static_lines = [pm.Segment(static_body, (0.0, 060.0), (1200.0, 060.0), 0.0)]
static_lines1 = [pm.Segment(static_body, (1200.0, 060.0), (1200.0, 800.0), 0.0)]
for line in static_lines:
    line.elasticity = 0.7
    line.friction = 100
    line.collision_type = 3
for line in static_lines1:
    line.elasticity = 0.7
    line.friction = 100
    line.collision_type = 3
space.add(static_body)
for line in static_lines:
    space.add(line)
for line in static_lines1:
    space.add(line)
    
#conversione delle coordinate di pymunk che carica gli oggetti in coordinate di pygame che crea la finestra
def to_pygame(p):
    """Convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)

#calcolo del vettore punti x e y
def vector(p0, p1):
    """Return the vector of the points
    p0 = (xo,yo), p1 = (x1,y1)"""
    a = p1[0] - p0[0]
    b = p1[1] - p0[1]
    return (a, b)

# calcolo dei punti del vettore calcolato
def unit_vector(v):
    """Return the unit vector of the points
    v = (a,b)"""
    h = ((v[0]**2)+(v[1]**2))**0.5
    if h == 0:
        h = 0.000000000000001
    ua = v[0] / h
    ub = v[1] / h
    return (ua, ub)

# calcolo della distanza tra punti per collisioni, fionda ed etc
def distance(xo, yo, x, y):
    """distance between points"""
    dx = x - xo
    dy = y - yo
    d = ((dx ** 2) + (dy ** 2)) ** 0.5
    return d

#caricamento dela musica del gioco
def load_music():
    """Load the music"""
    song1 = '../resources/sounds/angry-birds.ogg'
    pygame.mixer.music.load(song1)
    pygame.mixer.music.play(-1)

#azione della fionda
def sling_action():
    """Set up sling behavior"""
    global mouse_distance
    global rope_lenght
    global angle
    global x_mouse
    global y_mouse
    # posizionamento del bird sulla fionda
    v = vector((sling_x, sling_y), (x_mouse, y_mouse))
    uv = unit_vector(v)
    uv1 = uv[0]
    uv2 = uv[1]
    mouse_distance = distance(sling_x, sling_y, x_mouse, y_mouse)   #distanza dell' azione di tiro bird per allungamento della corda della fionda
    pu = (uv1*rope_lenght+sling_x, uv2*rope_lenght+sling_y)
    bigger_rope = 102
    x_redbird = x_mouse - 20
    y_redbird = y_mouse - 20
    if mouse_distance > rope_lenght:    #disegno dell'alungamento della corda della fionda nell'azione di tiro del bird
        pux, puy = pu
        pux -= 20
        puy -= 20
        pul = pux, puy
        screen.blit(redbird, pul)
        pu2 = (uv1*bigger_rope+sling_x, uv2*bigger_rope+sling_y)
        pygame.draw.line(screen, (0, 0, 0), (sling2_x, sling2_y), pu2, 5)
        screen.blit(redbird, pul)
        pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y), pu2, 5)

    else:
        mouse_distance += 10
        pu3 = (uv1*mouse_distance+sling_x, uv2*mouse_distance+sling_y)
        pygame.draw.line(screen, (0, 0, 0), (sling2_x, sling2_y), pu3, 5)
        screen.blit(redbird, (x_redbird, y_redbird))
        pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y), pu3, 5)
    # calcolo dell'angolo dell'impulso
    dy = y_mouse - sling_y
    dx = x_mouse - sling_x
    if dx == 0: #variabile per correggere l'angolo.x in caso di tiro orizzontale
        dx = 0.00000000000001   #varole dato da pymunk
    angle = math.atan((float(dy))/dx)

#disegno del menu quando un livello viene completato
def draw_level_cleared():
    """Draw level cleared"""
    global game_state
    global bonus_score_once
    global score
    
    rect = pygame.Rect(0,0,527,600)
    MenuBackground = Menu.subsurface(rect).copy()

    
    level_cleared = bold_font3.render("Level Cleared!", 1, WHITE)
    score_level_cleared = bold_font2.render(str(score), 1, WHITE)
    
    #calcolo del punteggio in caso in base a :
    #numeor di bird rimasti
    #colonne e travi distrutte
    #per il calcolo del numero di stelle da renderizzare
    if level.number_of_birds >= 0 and len(pigs) == 0 and len(king_pigs) == 0 and len(bearded_pigs) == 0:
        if bonus_score_once:
            score += (level.number_of_birds-1) * 10000
        bonus_score_once = False
        game_state = 4

        screen.blit(MenuBackground, (275,0))
        screen.blit(level_cleared, (380, 90))

        if score >= level.one_star and score <= level.two_star:
            screen.blit(star1, (310, 190))
        if score >= level.two_star and score <= level.three_star:
            screen.blit(star1, (310, 190))
            screen.blit(star2, (500, 170))
        if score >= level.three_star:
            screen.blit(star1, (310, 190))
            screen.blit(star2, (500, 170))
            screen.blit(star3, (700, 200))
        #inserimento dei bottoni
        screen.blit(score_level_cleared, (500, 400))
        screen.blit(replay_button, (340, 480))
        screen.blit(next_button, (620, 480))

#disegno menu in caso di fallimento del livello
def draw_level_failed():
    """Draw level failed"""
    global game_state
    failed = bold_font3.render("Level Failed", 1, WHITE)
    
    rect = pygame.Rect(0,0,527,600)
    MenuBackground = Menu.subsurface(rect).copy()

    if level.number_of_birds <= 0 and time.time() - t2 > 5 and (len(pigs) > 0 or len(bearded_pigs) > 0 or len(king_pigs) > 0):
        game_state = 3
        screen.blit(MenuBackground, (275,0))

        screen.blit(failed, (400, 90))
        screen.blit(pig_happy, (350, 120))
        screen.blit(replay_button, (500, 460))

#restart del livello
def restart():
    """Delete all objects of the level"""
    #contenitore dei modelli rimasti sullo schermo che devono essere eliminati
    global score
    
    pigs_to_remove = []
    kingpigs_to_remove = []
    beardedpigs_to_remove = []
    
    birds_to_remove = []
    
    columns_to_remove = []
    beams_to_remove = []
    #per ogni modlelo rimasto, aggiunta nel contenitore dell'oggetto, ed eliminazione dell'oggeto nel mondo
    for pig in pigs:
        pigs_to_remove.append(pig)
    for kpig in king_pigs:
        kingpigs_to_remove.append(kpig)
    for bpig in bearded_pigs:
        beardedpigs_to_remove.append(bpig)
        
    for pig in pigs_to_remove:
        space.remove(pig.shape, pig.shape.body)
        pigs.remove(pig)
    for kpig in kingpigs_to_remove:
        space.remove(kpig.shape, kpig.shape.body)
        king_pigs.remove(kpig)
    for bpig in beardedpigs_to_remove:
        space.remove(bpig.shape, bpig.shape.body)
        bearded_pigs.remove(bpig)
        
    for bird in birds:
        birds_to_remove.append(bird)
    for bird in birds_to_remove:
        space.remove(bird.shape, bird.shape.body)
        birds.remove(bird)
        
    for column in columns:
        columns_to_remove.append(column)
    for column in columns_to_remove:
        space.remove(column.shape, column.shape.body)
        columns.remove(column)
        
    for beam in beams:
        beams_to_remove.append(beam)
    for beam in beams_to_remove:
        space.remove(beam.shape, beam.shape.body)
        beams.remove(beam)
    score = 0


#calcolo della collisione tra bird e pig
def post_solve_bird_pig(arbiter, space, _):
    """Collision between bird and pig"""
    surface=screen
    a, b = arbiter.shapes
    bird_body = a.body
    pig_body = b.body

    p = to_pygame(bird_body.position)   #posiziooni
    p2 = to_pygame(pig_body.position)
    r = 30
    pygame.draw.circle(surface, BLACK, p, r, 4) #cerchi per la collisione
    pygame.draw.circle(surface, RED, p2, r, 4)
    pigs_to_remove = []
    for pig in pigs:
        # se dopo la collisone, ed il calcolo della nuova vita (-20) si ha un valore <0
        # il pig viene rimosso e si aggiunge un punteggio pari a 10000
        if pig_body == pig.body:
            pig.life -= 20
            pigs_to_remove.append(pig)
            global score

            score += 10000
            game.set_score(score)
            #m.GameCharacter.register_ImpactPig(self=GAME_CHARACTER,score=score+10000)
    #rimozione dal mondo del gioco dei pig colpiti
    for pig in pigs_to_remove:
        space.remove(pig.shape, pig.shape.body)
        pigs.remove(pig)

        
 #collisone tra bird e il king pig
def post_solve_bird_kingpig(arbiter, space, _):
    """Collision between bird and king pig"""
    surface = screen
    a, b = arbiter.shapes
    bird_body = a.body
    king_body = b.body
    p = to_pygame(bird_body.position)
    p2 = to_pygame(king_body.position)
    r = 20
    pygame.draw.circle(surface,BLACK,p,r,4)
    pygame.draw.circle(surface,RED, p2, r, 4)
    king_pigs_to_remove = []
    for kpig in king_pigs:
        if king_body == kpig.body:
            kpig.life -= 20
            if kpig.life <= 0:
                king_pigs_to_remove.append(kpig)
                global score
                score += 20000
    for kpig in king_pigs_to_remove:
        space.remove(kpig.shape, kpig.shape.body)
        king_pigs.remove(kpig)

#collisione tra bird e il bearded pig
def post_solve_bird_bearded(arbiter, space, _):
    """Collision between bird and bearded pig"""
    surface = screen
    a,b = arbiter.shapes
    bird_body = a.body
    bearded_body = b.body
    p = to_pygame(bird_body.position)
    p2 = to_pygame(bearded_body.position)
    r = 20
    pygame.draw.circle(surface, BLACK, p, r, 4)
    pygame.draw.circle(surface, RED, p2, r, 4)
    bearded_pigs_to_remove = []
    for bpig in bearded_pigs:
        if bearded_body == bpig.body:
            bpig.life -= 20
            if bpig.life <= 0:
                bearded_pigs_to_remove.append(bpig)
                global score
                score += 15000
    for bpig in bearded_pigs_to_remove:
        space.remove(bpig.shape, bpig.shape.body)
        bearded_pigs.remove(bpig)
        
# funzione del calcolo delle collisioni tra bird e colonne/travi
start=0
cont=0
start2=0
cont2=0
def post_solve_ground(arbiter, space, _):
    global cont
    global start
    global cont2
    global start2
    a,b=arbiter.shapes

    if  a.collision_type == 3 or b.collision_type == 3:
        # Imposta la velocità del corpo su zero
        #a.body.velocity = (3, 3)
        #a.body.velocity==(-1,-1)
        cont+=1
        if(cont==1):
            start=time.time()
        #print(time.time()-start)
        if(time.time()-start>3):
            cont=0

            a.body.velocity = (0, 0)


    birds_to_remove=[]
    for bird in birds:
        if bird.body==a.body:
            if(bird.body.velocity==(0,0)):
                cont2+=1
                if(cont2==1):
                    print("ciao")
                    start2=time.time()

                if(time.time()-start2>10):
                    birds_to_remove.append(bird)
                    cont2=0

    for bird in birds_to_remove:
        space.remove(bird.shape, bird.shape.body)
        birds.remove(bird)




def post_solve_bird_wood(arbiter, space, _):
    """Collision between bird and wood"""
    global start
    poly_to_remove = []
    birds_to_remove=[]
    # in questo caso si controlla che la forza di impatto sia maggiore di 100
    # a confronto dell'impulso dato all'oggetti colonne e travi
    # se si, si riuove la collonna/trave
    # e si aggiunge un punetggio di 5000
    if arbiter.total_impulse.length < 1100:
        a, b = arbiter.shapes
        #a.body.velocity=(0,0)
        for bird in birds:
            if bird.body==a.body:
                bird.life-=0.1



    if arbiter.total_impulse.length > 1100:
        a, b = arbiter.shapes




        for bird in birds:
            if a.body==bird.body:
                bird.life-=2

                bird.body.velocity=(1,1)
                birds_to_remove.append(bird)
                #space.remove(bird.shape, bird.shape.body)
                #birds.remove(bird)
        for column in columns:
            if b == column.shape:
                poly_to_remove.append(column)
        for beam in beams:
            if b == beam.shape:
                poly_to_remove.append(beam)
        for poly in poly_to_remove:
            if poly in columns:
                columns.remove(poly)
            if poly in beams:
                beams.remove(poly)
        space.remove(b, b.body)



        #for bird in birds_to_remove:
         #   space.remove(bird.shape, bird.shape.body)
          #  birds.remove(bird)

        global score
        score += 5000
        game.set_score(score)



# calcolo della collisone di un pig e del legno
def post_solve_pig_wood(arbiter, space, _):
    """Collision between pig and wood"""
    pigs_to_remove = []
    # dato che si ha una collisone tra pig e legno
    # solo se un bird e' stato lanciato, l'impulso richiesto
    # e' minore di quello tra bird e legno
    # comunque si calcolo il punteggio come se il pig sia stato colpito da un bird
    # essendo conseguenza del lancio di un bird
    if arbiter.total_impulse.length > 700:
        pig_shape, wood_shape = arbiter.shapes
        for pig in pigs:
            if pig_shape == pig.shape:
                pig.life -= 20
                global score

                score += 10000
                game.set_score(score)
                #m.GameCharacter.register_ImpactPig(self=GAME_CHARACTER,score=score)
                if pig.life <= 0:
                    pigs_to_remove.append(pig)
    for pig in pigs_to_remove:
        space.remove(pig.shape, pig.shape.body)
        pigs.remove(pig)

#collisione king pig e wood
def post_solve_kpig_wood(arbiter, space, _):
    """Collsion between king pig and wood"""
    king_pigs_to_remove = []
    if arbiter.total_impulse.length > 800:
        kpig_shape, wood_shape = arbiter.shapes
        for kpig in king_pigs:
            if kpig_shape == kpig.shape:
                kpig.life -= 20
                if kpig.life <= 0:
                    king_pigs_to_remove.append(kpig)
                    global score
                    score += 20000
    for kpig in king_pigs_to_remove:
        space.remove(kpig.shape, kpig.shape.body)
        king_pigs.remove(kpig)
 
#collisione bearded pig e wood
def post_solve_bpig_wood(arbiter, space, _):
    """Collsion between bearded pig and wood"""
    bearded_pigs_to_remove = []
    if arbiter.total_impulse.length > 750:
        bpig_shape, wood_shape = arbiter.shapes
        for bpig in bearded_pigs:
            bpig.life -= 20
            if bpig.life <= 0:
                bearded_pigs_to_remove.append(bpig)
                global score
                score += 15000
    for bpig in bearded_pigs_to_remove:
        space.remove(bpig.shape, bpig.shapes.body)
        bearded_pigs.remove(bpig)
        
        
# aggiunta del gestore di collsione tra bird e pig
space.add_collision_handler(0, 1).post_solve=post_solve_bird_pig
#  aggiunta del gestore di collsione tra bird e wood
space.add_collision_handler(0, 2).post_solve=post_solve_bird_wood
#  aggiunta del gestore di collsione tra wood e pig
space.add_collision_handler(1, 2).post_solve=post_solve_pig_wood
space.add_collision_handler(0, 3).post_solve=post_solve_ground

space.add_collision_handler(0,4).post_solve = post_solve_bird_kingpig
# aggiunta del gestore di collisioni tra bird e bearded pig
space.add_collision_handler(0,5).post_solve = post_solve_bird_bearded
# aggiunta del gestore di collisioni tra king pig e wood
space.add_collision_handler(2,4).post_solve = post_solve_kpig_wood
#aggiunta del gestore di collisoni tra bearded pig e wood
space.add_collision_handler(2,5).post_solve = post_solve_bpig_wood

#iniza la musica
#load_music()
#si crea lo spazio fisico per il livello
level = Level(pigs, bearded_pigs, king_pigs, columns, beams, space)


# si imposta che livello deve essere caricato
level.number = 0
# si carica il livello dal numero dato, se il numero e' errato la funzione load_level() settera number a 0

level.load_level()
start=0
cont=0

ecco=False
timer_duration = 1.0
def run():
    global running
    global bird_path
    global cont
    global ecco
    global mouse_pressed
    global t1
    global t2
    global start
    global colore_scia
    global counter
    global restart_counter
    global score
    global game_state
    global mouse_distance
    global x_mouse
    global y_mouse
    while running:

        # gestione delgi input, chiusura o start del gioco

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                # aggiunta del muro fisico per eveitare l'uscita dai bordi della finestra
                if wall:
                    for line in static_lines1:
                        space.remove(line)
                    wall = False
                else:
                    for line in static_lines1:
                        space.add(line)
                    wall = True

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                space.gravity = (0.0, -10.0)
                level.bool_space = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                space.gravity = (0.0, -700.0)
                level.bool_space = False
            if (pygame.mouse.get_pressed()[0] and x_mouse > 100 and
                    x_mouse < 250 and y_mouse > 370 and y_mouse < 550):
                mouse_pressed = True
            if (event.type == pygame.MOUSEBUTTONUP and
                    event.button == 1 and mouse_pressed):
                print("ciao")

                # Rilascio del bird
                mouse_pressed = False
                if level.number_of_birds > 0:
                    level.number_of_birds -= 1
                    t1 = time.time()*1000
                    xo = 154
                    yo = 156
                    if mouse_distance > rope_lenght:
                        mouse_distance = rope_lenght
                    if x_mouse < sling_x+5:
                        bird = Bird(mouse_distance, angle, xo, yo, space)
                        #bird.body.velocity=(10,10)
                        birds.append(bird)
                    else:
                        bird = Bird(-mouse_distance, angle, xo, yo, space)
                        birds.append(bird)
                    if level.number_of_birds == 0:
                        t2 = time.time()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if (x_mouse < 60 and y_mouse < 155 and y_mouse > 90):
                    game_state = 1
                if game_state == 1:
                    if x_mouse > 500 and y_mouse > 200 and y_mouse < 300:
                        # Ritorno al gioco dal menu pausa
                        game_state = 0
                    if x_mouse > 500 and y_mouse > 300:
                        # Rinizio il livello nel menu
                        restart()
                        level.load_level()
                        game_state = 0

                        bird_path = []
                if game_state == 3:
                    # Rinizio il livello in caso di fallimento
                    if x_mouse > 500 and x_mouse < 620 and y_mouse > 450:
                        restart()
                        level.load_level()
                        game_state = 0

                        bird_path = []
                        score = 0
                        game.set_score(0)
                        #game.set_level(level.number)
                        #m.GameCharacter.register_ImpactPig(self=GAME_CHARACTER,score=0)

                if game_state == 4:
                    # Calcolo il prossimo livello
                    if x_mouse > 610 and y_mouse > 450:
                        restart()

                        level.number += 1
                        game.save_game()
                        game.set_level(level.number)
                        print(pygame.mouse.get_pos())
                        print(game.get_level())
                        #m.GameCharacter.progress_to_next_level(self=GAME_CHARACTER)
                        game_state = 0
                        level.load_level()
                        score = 0
                        game.set_score(score)
                       # m.GameCharacter.register_ImpactPig(self=GAME_CHARACTER,score=0)
                        game.set_score(score)
                        #game.set_level(level.number)
                        bird_path = []
                        bonus_score_once = True
                    if x_mouse < 610 and x_mouse > 500 and y_mouse > 450:
                        # Rinizio il livello nel menu di livello completato
                        restart()
                        level.load_level()
                        game_state = 0
                        bird_path = []
                        score = 0
        x_mouse, y_mouse = pygame.mouse.get_pos()
        # Disegno il background
        screen.fill((130, 200, 100))

        screen.blit(background2, (0, -50))
        # Disegno la prima parte della fionda
        rect = pygame.Rect(50, 0, 70, 220)
        screen.blit(sling_image, (138, 420), rect)
        bird_point=False
        # Disegno il percorso effettuto dal bird lanciato
        #DOBBIAMO CORREGGERE LA SCIA INFINITAAA magari aggiunta timer

        #for point in bird_path:

           #pygame.draw.circle(screen, WHITE, point, 4, 0)
        birds_to_remove2=[]
        for bird in birds:
            if bird.life<20:
                bird.life-=0.1

                #print(bird.life)
            if(bird.life<=0):

                #print("OK")
                birds_to_remove2.append(bird)
                #birds.remove(bird)


        for bird in birds_to_remove2:
            space.remove(bird.shape, bird.shape.body)
            birds.remove(bird)




        # Disegno i bird nella lista di attesa dietro la fionda
        if level.number_of_birds > 0:
            for i in range(level.number_of_birds-1):
                x = 100 - (i*35)
                screen.blit(redbird, (x, 508))
        # Disegno il comportamento della fionda
        if mouse_pressed and level.number_of_birds > 0:
            sling_action()
        else:
            if time.time()*1000 - t1 > 300 and level.number_of_birds > 0:
                screen.blit(redbird, (130, 426))
            else:
                pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y-8),
                                 (sling2_x, sling2_y-7), 5)
        birds_to_remove = []
        pigs_to_remove = []
        king_pigs_to_remove = []
        bearded_pigs_to_remove = []
        
        counter += 1
        
        # Disegno i birds
        for bird in birds:

            if bird.shape.body.position.y < 0:
                birds_to_remove.append(bird)
            p = to_pygame(bird.shape.body.position)
            x, y = p
            x -= 22
            y -= 20

            screen.blit(redbird, (x, y))
            #pygame.draw.circle(screen, BLUE,
                               #p, int(bird.shape.radius), 2)
            if counter >= 3 and time.time() - t1 < 5:
                bird_path.append(p)
                restart_counter = True
        if restart_counter:
            counter = 0
            restart_counter = False
        # Rimuovi i pigs e i bird
        for bird in birds_to_remove:
            space.remove(bird.shape, bird.shape.body)
            birds.remove(bird)
        for pig in pigs_to_remove:
            space.remove(pig.shape, pig.shape.body)
            pigs.remove(pig)
        for kpig in king_pigs_to_remove:
            space.remove(kpig.shape, kpig.shape.body)
            king_pigs.remove(kpig)
        for bpig in bearded_pigs_to_remove:
            space.remove(bpig.shape, bpig.shape.body)
            
        # Disegno le linee statiche del pavimento
        for line in static_lines:
            body = line.body
            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            p1 = to_pygame(pv1)
            p2 = to_pygame(pv2)
            pygame.draw.lines(screen, (150, 150, 150), False, [p1, p2])
        i = 0
        # Disegno i pigs
        for pig in pigs:
            i += 1
            pigShape = pig.shape
            if pigShape.body.position.y < 0:
                pigs_to_remove.append(pigShape)

            p = to_pygame(pigShape.body.position)
            x, y = p
            angle_degrees = math.degrees(pigShape.body.angle)

            if pig.life >= 40:
                img = pygame.transform.rotate(pig_image, angle_degrees)
                w,h = img.get_size()
                x -= w*0.5
                y -= h*0.5
                screen.blit(img, (x, y))
            elif pig.life <= 30:
                img = pygame.transform.rotate(damaged_pig_image, angle_degrees)
                w,h = img.get_size()
                x -= w*0.5
                y -= h*0.5
                screen.blit(img, (x,y))

        for kpig in king_pigs:
            i += 1
            kingpigshape = kpig.shape
            if kingpigshape.body.position.y < 0:
                king_pigs_to_remove.append(kingpigshape)

            p = to_pygame(kingpigshape.body.position)
            x, y = p

            angle_degrees_king = math.degrees(kingpigshape.body.angle)

            if kpig.life >= 40:
                img = pygame.transform.rotate(king_pig_image, angle_degrees_king)
                w, h = img.get_size()
                x -= w * 0.5
                y -= h * 0.5
                screen.blit(img, (x, y))
            elif kpig.life <= 20:
                img = pygame.transform.rotate(king_pig_dmg_img, angle_degrees_king)
                w, h = img.get_size()
                x -= w * 0.5
                y -= h * 0.5
                screen.blit(img, (x, y))

        for bpig in bearded_pigs:
            i += 1
            beardedpigshape = bpig.shape
            if beardedpigshape.body.position.y < 0:
                bearded_pigs_to_remove.append(beardedpigshape)

            p = to_pygame(beardedpigshape.body.position)
            x, y = p

            angle_degrees_bearded = math.degrees(beardedpigshape.body.angle)

            if bpig.life >= 40:
                img = pygame.transform.rotate(bearded_pig_img, angle_degrees_bearded)
                w, h = img.get_size()
                x -= w * 0.5
                y -= h * 0.5
                screen.blit(img, (x, y))
            elif bpig.life <= 20:
                img = pygame.transform.rotate(bearded_pig_dmg_img, angle_degrees_bearded)
                w, h = img.get_size()
                x -= w * 0.5
                y -= h * 0.5
                screen.blit(img, (x, y))
           # pygame.draw.circle(screen, BLUE, p, pig.radius, 2)
        
        # Disegno le colonne e travi
        for column in columns:
            column.draw_poly('columns', screen)
        for beam in beams:
            beam.draw_poly('beams', screen)
            
        # Aggiorno la fisica
        dt = 1.0/50.0/2.
        for x in range(2):
            space.step(dt) # impostando dt /50/2 faccio un update dei frame rate di 2 a frame
            
        # Disegno la seconda parte della fionda
        rect = pygame.Rect(0, 0, 60, 200)
        screen.blit(sling_image, (120, 420), rect)
        
        # disegno il punteggio
        score_font = bold_font.render("SCORE", 1, WHITE)
        number_font = bold_font.render(str(score), 1, WHITE)
        screen.blit(score_font, (1060, 90))
        
        if score == 0:
            screen.blit(number_font, (1100, 130))
        else:
            screen.blit(number_font, (1060, 130))
        screen.blit(pause_button, (10, 90))
        
        # Opzini del menu pausa
        if game_state == 1:
            screen.blit(play_button, (500, 200))
            screen.blit(replay_button, (500, 300))
        draw_level_cleared()
        
       # print(pygame.mouse.get_pos())
        draw_level_failed()
        pygame.display.flip()
        #m.CareTaker.save(self=CARETAKER)

        clock.tick(50)
        print(game.get_level())
        print(game.get_score())
       # print(GAME_CHARACTER)
    #pygame.display.set_caption("fps: " + str(clock.get_fps()))





if __name__ == "__main__":
    run()
