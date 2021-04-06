from geneticAlgo import Population

if __name__ == '__main__':
    p1 = Population(100, 8, 0.3, 0.4)
    p1.evolve(1000)

