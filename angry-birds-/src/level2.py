from characters import Pig
from characters import BeardedPig
from characters import KingPig
from fly import Polygon, WoodImages

class StructureFactory:

    @staticmethod
    def create_open_flat( x, y, n, columns, beams, space, wood_images):
        """Create a open flat struture"""
        y0 = y
        for i in range(n):
            y = y0+100+i*100
            p = (x, y)
            columns.append(Polygon(p, 20, 85, space, wood_images=wood_images))
            p = (x+60, y)
            columns.append(Polygon(p, 20, 85, space, wood_images=wood_images))
            p = (x+30, y+50)
            beams.append(Polygon(p, 85, 20, space, wood_images=wood_images))

    @staticmethod
    def create_closed_flat( x, y, n, columns, beams, space, wood_images):
        """Create a closed flat struture"""
        y0 = y
        for i in range(n):
            y = y0+100+i*125
            p = (x+1, y+22)
            columns.append(Polygon(p, 20, 85, space, wood_images=wood_images))
            p = (x+60, y+22)
            columns.append(Polygon(p, 20, 85, space, wood_images=wood_images))
            p = (x+30, y+70)
            beams.append(Polygon(p, 85, 20, space, wood_images=wood_images))
            p = (x+30, y-30)
            beams.append(Polygon(p, 85, 20, space, wood_images=wood_images))
    @staticmethod
    def create_horizontal_pile( x, y, n, columns, beams, space, wood_images):
        """Create a horizontal pile"""
        y += 70
        for i in range(n):
            p = (x, y+i*20)
            beams.append(Polygon(p, 85, 20, space, wood_images=wood_images))

    @staticmethod
    def create_vertical_pile( x, y, n, columns, beams, space, wood_images):
        """Create a vertical pile"""
        y += 10
        for i in range(n):
            p = (x, y+85+i*85)
            columns.append(Polygon(p, 20, 85, space, wood_images=wood_images))

    @staticmethod
    def create(structure_type, x, y, n, columns, beams, space, wood_images):
        if structure_type == "open_flat":
            return StructureFactory.create_open_flat( x, y, n,columns, beams, space, wood_images)
        elif structure_type == "closed_flat":
            return StructureFactory.create_closed_flat( x, y, n,columns, beams, space, wood_images)
        elif structure_type == "horizontal_pile":
            return StructureFactory.create_horizontal_pile( x, y, n,columns, beams, space, wood_images)
        elif structure_type == "vertical_pile":
            return StructureFactory.create_vertical_pile( x, y, n,columns, beams, space, wood_images)
        else:
            return None

class Level:
    def __init__(self, pigs, bearded_pigs, king_pigs, columns, beams, space):
        self.pigs = pigs
        self.bearded_pigs = bearded_pigs
        self.king_pigs = king_pigs
        self.columns = columns
        self.beams = beams
        self.space = space
        self.number = 0
        self.number_of_birds = 4
        self.one_star = 30000
        self.two_star = 40000
        self.three_star = 60000
        self.bool_space = False
        self.wood_images = WoodImages()
        self.factory = StructureFactory()

    def build_0(self):
        pig1 = Pig(750, 80, self.space)
        pig2 = BeardedPig(985, 100, self.space)
        self.pigs.append(pig1)
        self.bearded_pigs.append(pig2)
        structure_type = "open_flat"
        self.factory.create(structure_type, 950, 20, 1,self.columns,self.beams,self.space,self.wood_images)
        structure_type = "closed_flat"
        self.factory.create(structure_type, 600, 20, 1,self.columns,self.beams,self.space,self.wood_images)
        structure_type = "horizontal_pile"
        self.factory.create(structure_type, 400, 20, 1,self.columns,self.beams,self.space,self.wood_images)
        structure_type = "vertical_pile"
        self.factory.create(structure_type, 200, 20, 1,self.columns,self.beams,self.space,self.wood_images)
        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

        self.one_star = 30000
        self.two_star = 40000
        self.three_star = 60000
        # creiamo altre strutture
        #self.factory.create("closed_flat", 1000, 200, 1,self.columns,self.beams,self.space,self.wood_images)


    def build_1(self):
        pig1 = BeardedPig(750, 80, self.space)
        pig2 = KingPig(985, 100, self.space)
        self.bearded_pigs.append(pig1)
        self.king_pigs.append(pig2)
        structure_type = "open_flat"
        self.factory.create(structure_type, 950, 20, 1,self.columns,self.beams,self.space,self.wood_images)
        structure_type = "closed_flat"
        self.factory.create(structure_type, 600, 20, 1,self.columns,self.beams,self.space,self.wood_images)
        structure_type = "horizontal_pile"
        self.factory.create(structure_type, 400, 20, 1,self.columns,self.beams,self.space,self.wood_images)
        structure_type = "vertical_pile"
        self.factory.create(structure_type, 200, 20, 1,self.columns,self.beams,self.space,self.wood_images)
        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

        self.one_star = 30000
        self.two_star = 40000
        self.three_star = 60000

    def load_level(self):
        try:
            build_name = "build_"+str(self.number)
            getattr(self, build_name)()
        except AttributeError:
            self.number = 0
            build_name = "build_"+str(self.number)
            getattr(self, build_name)()