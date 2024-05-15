import pymunk as pm
from pymunk import Vec2d
import pygame
import math

#oggetto che ci permette l'aggiunta degli altri oggetti visibili nel mondo del gioco
class Polygon:
    def __init__(self, pos, length, height, space, mass=5.0):
        #per ogni oggetto che deve essere presente nel mondo, settiamo i dati fisici
        moment = 1000   #momento per il movimento dell'oggetto
        body = pm.Body(mass, moment)    #corpo fisico dell'oggetto modellato
        body.position = Vec2d(*pos)     #posizione del corpo
        shape = pm.Poly.create_box(body, (length, height))  #forma del box di collisione

        #dati personali della forma
        shape.color = (0, 0, 255)   #colore blue
        shape.friction = 0.5    #frizione che l'oggetto deve avere
        shape.collision_type = 2    #tipo di collisione 1-> ground , 2-> dinamico

        space.add(body, shape)  #aggiungiamo sia il corpo che la forma nel modno del gioco

        self.body = body
        self.shape = shape

        wood = pygame.image.load("../resources/images/wood.png").convert_alpha()    #carichiamo immagini per costruzione delle colonne
        wood2 = pygame.image.load("../resources/images/wood2.png").convert_alpha()  #e delle travi

        # creaiamo un rettangolo per prenderci le coordinate della colonna/trave che ci interassa nella immagine
        # i primi due sono le coordinate del punto da dove iniziare a tagliare la immagine, 86 e' la lunghezza 22 e' l'altezza
        rect = pygame.Rect(251, 357, 86, 22)
        self.beam_image = wood.subsurface(rect).copy()

        #stesso per la trave
        rect = pygame.Rect(16, 252, 22, 84)
        self.column_image = wood2.subsurface(rect).copy()

    def to_pygame(self, p):
        """Convert pymunk to pygame coordinates"""
        #pymunk usa diverse coordinate da pygame ( librerai che crea la finestra e dieegna gli oggetti)
        return int(p.x), int(-p.y+600)

    def draw_poly(self, element, screen):
        """Draw beams and columns"""
        #disegniamo effettivamente le colonne e le travi
        poly = self.shape

        ps = poly.get_vertices()

        ps.append(ps[0])
        ps = map(self.to_pygame, ps) #trasformiamo le coordinate pymunk in coordinate pygame
        ps = list(ps)

        color = (255, 0, 0)
        pygame.draw.lines(screen, color, False, ps) #disegniamo le colonne e travi con l'uso delle linee fisiche dipygame

        # a secondo dell'oggetto ruotiamo e aggiustiamo l'errore attraverso il parametro offset
        if element == 'beams':
            p = poly.body.position
            p = Vec2d(*self.to_pygame(p))

            angle_degrees = math.degrees(poly.body.angle) + 180 #calcolo l'angolo di rotazine della immagine
            rotated_logo_img = pygame.transform.rotate(self.beam_image, #immagine ruotata per angolo calcolato
                                                       angle_degrees)
            offset = Vec2d(*rotated_logo_img.get_size()) / 2.   #margine di errore
            p = p - offset  #calcolo dei vertici aggiustati per l'errore
            np = p
            screen.blit(rotated_logo_img, (np.x, np.y)) #blit -> permette di viusalizzare una superficie su un a'tro oggetto
        if element == 'columns':
            p = poly.body.position
            p = Vec2d(*self.to_pygame(p))
            angle_degrees = math.degrees(poly.body.angle) + 180
            rotated_logo_img = pygame.transform.rotate(self.column_image,
                                                       angle_degrees)
            offset = Vec2d(*rotated_logo_img.get_size()) / 2.
            p = p - offset
            np = p
            screen.blit(rotated_logo_img, (np.x, np.y))
