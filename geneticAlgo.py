import random
import copy
import numpy as np

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
            # self.quenMembers.append(Quen(nr%n,int(nr/n)))
            # self.occupiedFields.add(nr)
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
    def __init__(self, populationSize, boardSize, quenMutationProbability=0.02, boardMutationProbability=0.01):
        self.populationSize = populationSize
        self.boardSize = boardSize
        self.quenMutationProbability = quenMutationProbability
        self.boardMutationProbability = boardMutationProbability
        self.members = [Board(boardSize) for i in range(populationSize)]
        self.distribution = [1.0/(populationSize * populationSize) * ((populationSize - i) * (populationSize - i) - (populationSize - i - 1) * (populationSize - i - 1)) for i in range(populationSize)]

    def tournamentSelection(self):
        bestBoards = []
        self.members.sort(key=lambda board: board.fitness)
        for i in range(self.populationSize):
            tournament = np.random.choice(self.members, 2, self.distribution)
            if tournament[0].fitness > tournament[1].fitness:
                bestBoards.append(copy.deepcopy(tournament[0]))
            else:
                bestBoards.append(copy.deepcopy(tournament[1]))
        return bestBoards

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
        for i in range(epochs):
            bestBoards = self.tournamentSelection()
            mutatedBoards = self.mutatedBoards(bestBoards)
            self.members += mutatedBoards
            self.members.sort(key=lambda board: board.fitness)
            self.members = self.members[0:self.populationSize+1]
            self.members.sort(key=lambda board: board.fitness)

            int = 0
            for board in self.members:
                int += board.fitness
            avg = int/len(self.members)
            print("Epoch nr: "+str(i)+" fittest candidate: "+str(self.members[0].fitness)+"  avg.fit: "+"%.2f" % avg)
