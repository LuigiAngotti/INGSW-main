class Memento:
    def __init__(self, score, level):
        self.score = score
        self.level = level

class Originator:
    def __init__(self, score, level):
        self.score = score
        self.level = level

    def create_memento(self):
        return Memento(self.score, self.level)

    def set_memento(self, memento):
        self.score = memento.score
        self.level = memento.level

class Caretaker:
    def __init__(self):
        self.mementos = []

    def add_memento(self, memento):
        self.mementos.append(memento)

    def get_memento(self, index):
        return self.mementos[index]

class Game:
    def __init__(self):
        self.originator = Originator(score=0, level=0)
        self.caretaker = Caretaker()

    def save_game(self):
        self.caretaker.add_memento(self.originator.create_memento())

    def load_game(self, index):
        memento = self.caretaker.get_memento(index)
        self.originator.set_memento(memento)
        return memento

    def set_score(self, score):
        self.originator.score = score

    def set_level(self, level):
        self.originator.level = level

    def get_level(self):
        return self.originator.level

    def get_score(self):
        return self.originator.score