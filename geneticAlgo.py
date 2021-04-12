import random
import copy
import numpy as np
import progressbar

#tournamentSize = 2 #encoded
random.seed(0)

class Quen:
    def __init__(self, x, y):
        self.x=x
        self.y=y

    def __eq__(self, another):
        if not isinstance(another, Quen):
            return NotImplemented
        return self.x == another.x and self.y == another.y


class Board:
    def __init__(self, n):
        #unique field numbers:
        self.occupiedFields=set()
        self.quenMembers = []
        quenPositions = random.sample(range(0,n*n-1),n) # !!! n>1 !!! or exception will occur
        i=0
        for nr in quenPositions:            #numbers go letf to right, top to bottom
            #self.quenMembers.append(Quen(nr%n,int(nr/n)))
            #self.occupiedFields.add(nr)
            self.quenMembers.append(Quen(i,0))
            self.occupiedFields.add(i)
            i+=1
        # Kth row, Nth collumn, field_nr = n*row + collumn
        # row = field_nr/n   collumn = field_nr%n
        self.updateLossFunction()

    def updateLossFunction(self):
        checks = 0
        for quen1 in self.quenMembers:
            for quen2 in self.quenMembers:
                if quen1 != quen2:
                    if quen1.x == quen2.x: #row
                        checks += 1
                    if quen1.y == quen2.y: #collumn
                        checks += 1
                    if quen1.x - quen1.y == quen2.x - quen2.y: #diagonal
                        checks += 1
                    if - quen1.y - quen1.x == - quen2.x - quen2.y: #-diagonal
                        checks += 1
        self.fitness = checks

    def printBoard(self):
        print("Fitness: "+str(self.fitness))
        for quen in self.quenMembers:
             print("Quen, ox: "+str(quen.x)+" oy: "+str(quen.y))


class Population:
    history = []

    def __init__(self, selection, boardSize, populationSize, seedPopulationSize=4, quenMutationProbability=0.02, boardMutationProbability=0.01):
        if boardSize <= 0:
            raise ValueError('Board size cannot be lower than 1!')
        if populationSize <= 0:
            raise ValueError('Population size cannot be lower than 1!')
        if seedPopulationSize <= 0:
            raise ValueError('Seed population size cannot be lower than 1!')
        if populationSize < seedPopulationSize:
            raise ValueError('Population size cannot be lower than seed population for next generation!')
        if quenMutationProbability <= 0 or 1 <= quenMutationProbability:
            raise ValueError('Quen mutation probability must be in range (0;1)')
        if boardMutationProbability <= 0 or 1 <= boardMutationProbability:
            raise ValueError('Board mutation probability must be in range (0;1)')

        self.selection = selection
        self.populationSize = populationSize
        self.boardSize = boardSize
        self.seedPopulationSize = int(seedPopulationSize)
        self.quenMutationProbability = quenMutationProbability
        self.boardMutationProbability = boardMutationProbability
        self.members = [Board(boardSize) for i in range(populationSize)]

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

    def thresholdSelection(self): #all above average have equal chances to be chosen
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

    def mutatedBoards(self, bestBoards):
        for board in bestBoards:
            if board != bestBoards[0] and random.uniform(0, 1) < self.boardMutationProbability:
                for quen in board.quenMembers:
                    if random.uniform(0, 1) < self.quenMutationProbability:
                        field = random.randint(0, self.boardSize*self.boardSize-1)
                        while field in board.occupiedFields:
                            field = random.randint(0, self.boardSize*self.boardSize-1)

                        board.occupiedFields.remove(self.boardSize*quen.y+quen.x)
                        board.occupiedFields.add(field)
                        quen.x = field%self.boardSize
                        quen.y = int(field/self.boardSize)
                    board.updateLossFunction()
        return bestBoards

    def evolve(self, epochs):
        # f = open("demofile2.txt", "a")
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
