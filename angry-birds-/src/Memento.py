class Memento():  # pylint: disable=too-few-public-methods
    "A container of characters attributes"

    def __init__(self, score,  level):
        self.score = score
        self.level = level


class GameCharacter():
    "The Game Character whose state changes"

    def __init__(self):
        self._score = 0
        self._level = 0


    @property
    def score(self):
        "A `getter` for the objects score"
        return self._score

    def register_ImpactPig(self,score):
        "The character kills its enemies as it progesses"
        self._score += score

    def progress_to_next_level(self):
        "The characer progresses to the next level"
        self._level += 1



    def __str__(self):
        return(
            f"Score: {self._score}, "
            f"Level: {self._level}, "


        )

    @ property
    def memento(self):
        "A `getter` for the characters attributes as a Memento"
        return Memento(
            self._score,
            self._level)


    @ memento.setter
    def memento(self, memento):
        self._score = memento.score
        self._level = memento.level


class CareTaker():
    "Guardian. Provides a narrow interface to the mementos"

    def __init__(self, originator):
        self._originator = originator
        self._mementos = []

    def save(self):
        "Store a new Memento of the Characters current state"
        print("CareTaker: Game Save")
        memento = self._originator.memento
        self._mementos.append(memento)

    def restore(self, index):
        """
        Replace the Characters current attributes with the state
        stored in the saved Memento
        """
        print("CareTaker: Restoring Characters attributes from Memento")
        memento = self._mementos[index]
        self._originator.memento = memento


