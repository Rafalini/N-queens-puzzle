import random
import copy
import numpy as np
from operator import attrgetter

# tournamentSize = 2 #encoded
random.seed(0)

class Ant:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, another):
        if not isinstance(another, Ant):
            return NotImplemented
        return self.x == another.x and self.y == another.y
