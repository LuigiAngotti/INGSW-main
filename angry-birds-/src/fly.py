
import pymunk as pm
from pymunk import Vec2d

import math
import pygame
'''
La classe WoodImages memorizza le immagini di travi e colonne come variabili di classe e fornisce 
un metodo per restituire l'immagine appropriata per un determinato tipo di elemento. 
La classe Polygon accetta un'istanza di WoodImages come argomento nel suo costruttore e la memorizza come variabile di istanza.
Ciò consente a ciascun oggetto Polygon di accedere alle immagini condivise senza crearne una nuova istanza.
'''
class WoodImages:
    # Load the images in the class constructor
    def __init__(self):
        self.beam_image = pygame.image.load("../resources/images/wood.png").convert_alpha()
        self.column_image = pygame.image.load("../resources/images/wood2.png").convert_alpha()

        # Create a rectangle for the beam image
        rect = pygame.Rect(251, 357, 86, 22)
        self.beam_image = self.beam_image.subsurface(rect).copy()

        # Create a rectangle for the column image
        rect = pygame.Rect(16, 252, 22, 84)
        self.column_image = self.column_image.subsurface(rect).copy()

    def get_image(self, element):
        if element == 'beams':
            return self.beam_image
        elif element == 'columns':
            return self.column_image
        else:
            raise ValueError('Invalid element type: {}'.format(element))

class Polygon:
    def __init__(self, pos, length, height, space, mass=5.0,wood_images=None):
        # Set up the physical properties of the polygon as before
        moment = 1000
        body = pm.Body(mass, moment)
        body.position = Vec2d(*pos)
        shape = pm.Poly.create_box(body, (length, height))
        shape.color = (0, 0, 255)
        shape.friction = 0.5
        shape.collision_type = 2
        space.add(body, shape)

        self.body = body
        self.shape = shape

        # Store the wood images instance as an instance variable
        self.wood_images = wood_images

    def to_pygame(self, p):
        return int(p.x), int(-p.y+600)

    def draw_poly(self, element, screen):
        # Get the appropriate image for the element type
        if self.wood_images is not None:
            image = self.wood_images.get_image(element)
        else:
            # Use a default image if wood_images is None
            image = pygame.Surface((20, 20))
            image.fill((255, 255, 255))

        # Draw the polygon shape as before
        poly = self.shape
        ps = poly.get_vertices()
        ps.append(ps[0])
        ps = map(self.to_pygame, ps)
        ps = list(ps)
        color = (255, 0, 0)
        pygame.draw.lines(screen, color, False, ps)

        # Rotate and offset the image
        p = poly.body.position
        p = Vec2d(*self.to_pygame(p))
        angle_degrees = math.degrees(poly.body.angle) + 180
        rotated_logo_img = pygame.transform.rotate(image, angle_degrees)
        offset = Vec2d(*rotated_logo_img.get_size()) / 2.
        p = p - offset

        # Blit the rotated image onto the screen
        screen.blit(rotated_logo_img, p)