from geneticAlgo import Population
import geneticTest
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

suite = unittest.TestLoader().loadTestsFromModule(geneticTest)
unittest.TextTestRunner(verbosity=2).run(suite)
print(bcolors.WARNING + "Warning: This may take a while..."+bcolors.ENDC)

print("\n01_ShortPeriodEffi test...\n")
p1 = Population("01_ShortPeriodEffi", "roulette", 50, 100, 20) #boardSize, population, seedPopulation
p1.evolve(100)
p1.setPopulation("proportional", 50, 100, 20) #boardSize, population, seedPopulation
p1.evolve(100)
p1.setPopulation("threshold", 50, 100, 20) #boardSize, population, seedPopulation
p1.evolve(100)
p1.setPopulation("random", 50, 100, 20) #boardSize, population, seedPopulation
p1.evolve(100)
p1.setPopulation("tournament", 50, 100, 20) #boardSize, population, seedPopulation
p1.evolve(100)

print("\n02_LongPeriodEffi test...\n")
p1 = Population("02_LongPeriodEffi", "roulette", 50, 100, 20) #boardSize, population, seedPopulation
p1.evolve(600)
p1.setPopulation("proportional", 50, 100, 20) #boardSize, population, seedPopulation
p1.evolve(600)
p1.setPopulation("threshold", 50, 100, 20) #boardSize, population, seedPopulation
p1.evolve(600)
p1.setPopulation("random", 50, 100, 20) #boardSize, population, seedPopulation
p1.evolve(600)
p1.setPopulation("tournament", 50, 100, 20) #boardSize, population, seedPopulation
p1.evolve(600)

print("\n03_CrossTest test...\n")
p1 = Population("03_CrossTest", "tournament", 50, 100, 20, True) #boardSize, population, seedPopulation
p1.evolve(400)
p1.setPopulation("tournament", 50, 100, 20, False) #boardSize, population, seedPopulation
p1.evolve(400)

print("\n04_PopulationSize test...\n")
p1 = Population("04_PopulationSize", "tournament", 50, 100, 20, True) #boardSize, population, seedPopulation
p1.evolve(300)
p1.setPopulation("tournament", 50, 1000, 20, False) #boardSize, population, seedPopulation
p1.evolve(300)
p1.setPopulation("tournament", 50, 10000, 20, False) #boardSize, population, seedPopulation
p1.evolve(300)

print("\n05_PopulationSize2 test...\n")
p1 = Population("05_PopulationSize2", "tournament", 50, 100, 20, True) #boardSize, population, seedPopulation
p1.evolve(300)
p1.setPopulation("tournament", 50, 1000, 200, False) #boardSize, population, seedPopulation
p1.evolve(300)
p1.setPopulation("tournament", 50, 10000, 2000, False) #boardSize, population, seedPopulation
p1.evolve(300)

print("\n06_LongRun test...\n")
p1 = Population("06_LongRun", "tournament", 50, 100, 20, True) #boardSize, population, seedPopulation
p1.evolve(10000)
p1.setPopulation("proportional", 50, 100, 20) #boardSize, population, seedPopulation
p1.evolve(10000)
p1.setPopulation("threshold", 50, 100, 20) #boardSize, population, seedPopulation
p1.evolve(10000)
p1.setPopulation("random", 50, 100, 20) #boardSize, population, seedPopulation
p1.evolve(10000)
p1.setPopulation("roulette", 50, 100, 20) #boardSize, population, seedPopulation
p1.evolve(10000)
