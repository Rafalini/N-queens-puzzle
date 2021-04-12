from geneticAlgo import Quen
from geneticAlgo import Board
from geneticAlgo import Population
import genetic_test
import unittest

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    GREEN = "\033[96m"
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# print(bcolors.HEADER + "Warning: HEADER?" + bcolors.HEADER)
# print(bcolors.OKBLUE + "Warning: OKBLUE?" + bcolors.OKBLUE)
# print(bcolors.OKCYAN + "Warning: OKCYAN?" + bcolors.OKCYAN)
# print(bcolors.WARNING + "Warning: WARNING?" + bcolors.WARNING)
# print(bcolors.FAIL + "Warning: FAIL?" + bcolors.FAIL)
# print(bcolors.ENDC + "Warning: ENDC?" + bcolors.ENDC)
# print(bcolors.BOLD + "Warning: BOLD?" + bcolors.BOLD)
# print(bcolors.GREEN + "Warning: UNDERLINE? \u2713   \u2718" + bcolors.GREEN)

suite = unittest.TestLoader().loadTestsFromModule(genetic_test)
unittest.TextTestRunner(verbosity=2).run(suite)
print(bcolors.WARNING + "Warning: This may take a while... WARNING"+bcolors.ENDC)

p1 = Population("tournament", 50, 2000, 20) #boardSize, population, seedPopulation
p1.evolve(1500)
p1 = Population("roulette", 50, 2000, 20) #boardSize, population, seedPopulation
p1.evolve(1500)
p1 = Population("proportional", 50, 2000, 20) #boardSize, population, seedPopulation
p1.evolve(1500)
p1 = Population("threshold", 50, 2000, 20) #boardSize, population, seedPopulation
p1.evolve(1500)
p1 = Population("random", 50, 2000, 20) #boardSize, population, seedPopulation
p1.evolve(1500)
