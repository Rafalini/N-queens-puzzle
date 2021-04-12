import random
import copy
import numpy as np
import progressbar

#tournamentSize = 2 #encoded
random.seed(0)

class Queen:
    def __init__(self, x, y):
        self.x=x
        self.y=y

    def __eq__(self, another):
        if not isinstance(another, Queen):
            return NotImplemented
        return self.x == another.x and self.y == another.y


class Board:
    def __init__(self, boardSize, populate=False):
        #unique field numbers:
        self.boardSize = boardSize
        self.occupiedFields=set()
        self.queenMembers = []
        if populate:
            self.populate()

    def populate(self):
        queenPositions = random.sample(range(0,self.boardSize*self.boardSize-1),self.boardSize) # !!! n>1 !!! or exception will occur
        i=0
        for nr in queenPositions:            #numbers go letf to right, top to bottom
            #self.queenMembers.append(Queen(nr%n,int(nr/n)))
            #self.occupiedFields.add(nr)
            self.queenMembers.append(Queen(i,0))
            self.occupiedFields.add(i)
            i+=1
        # Kth row, Nth collumn, field_nr = n*row + collumn
        # row = field_nr/n   collumn = field_nr%n
        self.updateLossFunction()

    def updateLossFunction(self):
        checks = 0
        for queen1 in self.queenMembers:
            for queen2 in self.queenMembers:
                if queen1 != queen2:
                    if queen1.x == queen2.x: #row
                        checks += 1
                    if queen1.y == queen2.y: #collumn
                        checks += 1
                    if queen1.x - queen1.y == queen2.x - queen2.y: #diagonal
                        checks += 1
                    if - queen1.y - queen1.x == - queen2.x - queen2.y: #-diagonal
                        checks += 1
        self.fitness = checks

    def printBoard(self):
        print("Fitness: "+str(self.fitness))
        for queen in self.queenMembers:
             print("Queen, ox: "+str(queen.x)+" oy: "+str(queen.y))


class Population:
    history = []
    #selection = selection_method
    #boardSize = board side, board with N size has N*N squares on it
    #populationSize = population size
    #seedPopulationSize = how many indyviduals will be mutated and to current population
    def __init__(self, selection, boardSize, populationSize, seedPopulationSize=4, queenMutationProbability=0.1, boardMutationProbability=0.5):
        if boardSize <= 0:
            raise ValueError('Board size cannot be lower than 1!')
        if populationSize <= 0:
            raise ValueError('Population size cannot be lower than 1!')
        if seedPopulationSize <= 0:
            raise ValueError('Seed population size cannot be lower than 1!')
        if populationSize < seedPopulationSize:
            raise ValueError('Population size cannot be lower than seed population for next generation!')
        if queenMutationProbability <= 0 or 1 <= queenMutationProbability:
            raise ValueError('Queen mutation probability must be in range (0;1)')
        if boardMutationProbability <= 0 or 1 <= boardMutationProbability:
            raise ValueError('Board mutation probability must be in range (0;1)')

        self.selection = selection
        self.populationSize = populationSize
        self.boardSize = boardSize
        self.seedPopulationSize = int(seedPopulationSize)
        self.queenMutationProbability = queenMutationProbability
        self.boardMutationProbability = boardMutationProbability
        self.members = [Board(boardSize, True) for i in range(populationSize)]

        self.tournamentDistribution = [1.0/(populationSize * populationSize) * ((populationSize - i) * (populationSize - i) - (populationSize - i - 1) * (populationSize - i - 1)) for i in range(populationSize)]
        self.selectionDict = {  "tournament":self.tournamentSelection,
                                "roulette":self.rouletteSelection,
                                "proportional":self.proportionalSelection,
                                "threshold":self.thresholdSelection,
                                "random":self.randomSelection}


    def tournamentSelection(self):
        selectedBoards = []
        self.members.sort(key=lambda board: board.fitness)
        for i in range(self.seedPopulationSize):
            tournament = np.random.choice(self.members, int(self.seedPopulationSize/self.seedPopulationSize), self.tournamentDistribution).tolist()
            tournament.sort(key=lambda board: board.fitness)
            selectedBoards.append(copy.deepcopy(tournament[0]))
        return selectedBoards

    def rouletteSelection(self): #weight = 1/cost_function  -> the lower cost the better board
        selectedBoards = []
        rouletteeWeights = []
        for i in range(self.populationSize):
            rouletteeWeights.append(1/self.members[i].fitness)
        selectedBoards = np.random.choice(self.members, self.seedPopulationSize, rouletteeWeights).tolist()
        return selectedBoards

    def proportionalSelection(self): #almost ruletteSelectionm, exception: all_weights - min_weight
        selectedBoards = []
        proportionalWeights = []
        minWeight = self.populationSize*self.populationSize
        for i in range(self.populationSize):
            if self.members[i].fitness < minWeight:
                minWeight = self.members[i].fitness
        for i in range(self.populationSize):
            proportionalWeights.append(1/self.members[i].fitness-1/minWeight)
        selectedBoards = np.random.choice(self.members, self.seedPopulationSize, proportionalWeights).tolist()
        return selectedBoards

    def thresholdSelection(self): #all above average have equal chances to be chosen, all below have no chances [P(x)=0]
        selectedBoards = []
        thresholdWeights = []
        costFunSum=0
        for i in range(self.populationSize):
            costFunSum += self.members[i].fitness
        for i in range(self.populationSize):
            if self.members[i].fitness > costFunSum/self.populationSize:
                thresholdWeights.append(1)
            else:
                thresholdWeights.append(0)
        selectedBoards = np.random.choice(self.members, self.seedPopulationSize, thresholdWeights).tolist()
        return selectedBoards

    def randomSelection(self):
        return np.random.choice(self.members, self.seedPopulationSize).tolist()

    def mutatedBoards(self, bestBoards): #for each board, for each queen on it, if rand() > P then change this queen
        for board in bestBoards:
            if board != bestBoards[0] and random.uniform(0, 1) < self.boardMutationProbability:
                for queen in board.queenMembers:
                    if random.uniform(0, 1) < self.queenMutationProbability:
                        field = random.randint(0, self.boardSize*self.boardSize-1)
                        while field in board.occupiedFields:
                            field = random.randint(0, self.boardSize*self.boardSize-1)

                        board.occupiedFields.remove(self.boardSize*queen.y+queen.x)
                        board.occupiedFields.add(field)
                        queen.x = field%self.boardSize
                        queen.y = int(field/self.boardSize)
                    board.updateLossFunction()
        return bestBoards

    def evolve(self, epochs):
        # f = open("log.txt", "a")
        # f.write("Now the file has more content!")
        # f.close()
        for i in progressbar.progressbar(range(epochs)):
            bestBoards = self.selectionDict[self.selection]()
            mutatedBoards = self.mutatedBoards(bestBoards)
            self.members += mutatedBoards
            self.members.sort(key=lambda board: board.fitness)
            self.members = self.members[0:self.populationSize+1]
            self.members.sort(key=lambda board: board.fitness)

            int = 0
            for board in self.members:
                int += board.fitness
            avg = int/len(self.members)
            #print("Epoch nr: "+str(i)+" fittest candidate: "+str(self.members[0].fitness)+"  avg.fit: "+"%.2f" % avg)
            self.history.append({"epoch":i+1, "bestFitness":self.members[0].fitness, "averageFitness":avg})
        self.printStats()

    def printStats(self):
        print("Epochs run: "+str(self.history[-1]["epoch"])+" best fitness: "+ "%.2f"%self.history[-1]["averageFitness"]+ "  method: "+self.selection)
