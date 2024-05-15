import pymunk as pm
from pymunk import Vec2d


#creazione dei personaggi
class Bird():
    def __init__(self, distance, angle, x, y, space):
        self.life = 20
        mass = 5    #dato per definire la massa fisica dell'oggetto
        radius = 12 #l'oggetto fisico e' creato come Circle e definiamo qui il raggio del cerchio
        inertia = pm.moment_for_circle(mass, 0, radius, (0, 0)) #inerzia dell'oggetto per le interazioni fisiche
        body = pm.Body(mass, inertia) #impostiamo i dati del corpo per la fisica
        body.position = x, y    #dove posizioniamo l'oggetto
        power = distance * 53   #forza che usiamo in caso dell'applicazione di un impulso per il movimento dell'oggetto
        impulse = power * Vec2d(1, 0) # calcoliamo l'impulso
        angle = -angle      #invertiamo l'angolo per dare un movimento di direzione corretta
        body.apply_impulse_at_local_point(impulse.rotated(angle))   #applichiamo l'impulso in caso di movimento del corpo. l'impulso e' applicato sull'oggetto
        shape = pm.Circle(body, radius, (0, 0))     #forma per il calcolo della fisica sul corpo
        #dati fisici dell'oggetto fisico forma
        shape.elasticity = 0.70
        shape.friction =1
        shape.collision_type = 0
        space.add(body, shape) ##aggiunta del corpo all'oggetto fisico pere la fisica
        self.body = body

        self.shape = shape


class Pig():
    def __init__(self, x, y, space):
        self.life = 40
        mass = 5
        radius = 14

        inertia = pm.moment_for_circle(mass, 0, radius, (0, 0))
        body = pm.Body(mass, inertia)
        body.position = x, y

        shape = pm.Circle(body, radius, (0, 0))

        shape.elasticity = 0.95
        shape.friction = 1
        shape.collision_type = 1

        space.add(body, shape)
        self.body = body
        self.shape = shape


class KingPig():
    def __init__(self, x, y, space):
        self.life = 40
        mass = 10
        radius = 20

        inertia = pm.moment_for_circle(mass,0,radius,(0,0))
        body = pm.Body(mass, inertia)
        body.position = x, y

        shape = pm.Circle(body, radius, (0, 0))

        shape.elasticity = 0.70
        shape.friction = 0.5
        shape.collision_type = 4

        space.add(body, shape)
        self.body = body
        self.shape = shape


class BeardedPig():
    def __init__(self, x, y, space):
        self.life = 40
        mass = 10
        radius = 20

        inertia = pm.moment_for_circle(mass, 0, radius, (0, 0))
        body = pm.Body(mass, inertia)
        body.position = x, y

        shape = pm.Circle(body, radius, (0, 0))

        shape.elasticity = 0.70
        shape.friction = 0.5
        shape.collision_type = 5

        space.add(body, shape)
        self.body = body
        self.shape = shape
