import random
import copy
import numpy as np

random.seed(0)

class Queen:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, another):
        if not isinstance(another, Queen):
            return NotImplemented
        return self.x == another.x and self.y == another.y

class Board:
    def __init__(self, n, ifNeedsPopulating):
        # unique field numbers:
        self.occupiedFields = set()
        self.queenMembers = []
        if (ifNeedsPopulating):
            self.populate(n)
        else:
            self.queenMembers = [0 for x in range(n)]
        self.updateLossFunction()

    def populate(self, n):
        queenPositions = random.sample(range(0, n * n - 1), n)  # !!! n>1 !!! or exception will occur
        for nr in queenPositions:  # numbers go left to right, top to bottom
            self.queenMembers.append(Queen(nr % n, int(nr / n)))
            self.occupiedFields.add(nr)
        # Kth row, Nth collumn, field_nr = n*row + collumn
        # row = field_nr/n   collumn = field_nr%n

    def updateLossFunction(self):
        checks = 0

        for queen1 in self.queenMembers:
            for queen2 in self.queenMembers:
                if queen1 != queen2:
                    if queen1.x == queen2.x:  # row
                        checks += 1
                    if queen1.y == queen2.y:  # collumn
                        checks += 1
                    if queen1.x - queen1.y == queen2.x - queen2.y:  # diagonal
                        checks += 1
                    if - queen1.y - queen1.x == - queen2.x - queen2.y:  # -diagonal
                        checks += 1
        self.fitness = checks

    def printBoard(self):
        print("Fitness: " + str(self.fitness))
        for queen in self.queenMembers:
            print("Queen, ox: " + str(queen.x) + " oy: " + str(queen.y))

class Population:
    def __init__(self, populationSize, boardSize, queenMutationProbability=0.1, boardMutationProbability=0.5):
        self.populationSize = populationSize
        self.boardSize = boardSize
        self.queenMutationProbability = queenMutationProbability
        self.boardMutationProbability = boardMutationProbability
        self.members = [Board(boardSize, True) for i in range(populationSize)]
        self.distribution = [1.0 / (populationSize * populationSize) * (
                (populationSize - i) * (populationSize - i) - (populationSize - i - 1) * (populationSize - i - 1))
                             for i in range(populationSize)]

    def crossover(self, board1, board2):
        tournament = []
        tournament.append(board1)
        tournament.append(board2)

        index = random.randint(0, self.boardSize - 1)
        lengthOfSegm = random.randint(1, self.boardSize - index)
        newBoard = Board(self.boardSize, False)
        for x in range(lengthOfSegm):
            newBoard.queenMembers[index + x] = copy.deepcopy(tournament[0].queenMembers[index + x])
            newBoard.occupiedFields.add(
                tournament[0].queenMembers[index + x].y * self.boardSize
                + tournament[0].queenMembers[index + x].x)

        newIndexChild = index + lengthOfSegm
        newIndexParent = index + lengthOfSegm
        while newIndexChild != index:
            if (newIndexChild >= self.boardSize):
                newIndexChild = 0
                continue
            if (newIndexParent >= self.boardSize):
                newIndexParent = 0
                continue
            field = tournament[1].queenMembers[newIndexParent].y * self.boardSize + tournament[1].queenMembers[
                newIndexParent].x
            if (field in newBoard.occupiedFields):
                newIndexParent += 1
            else:
                newBoard.queenMembers[newIndexChild] = copy.deepcopy(tournament[1].queenMembers[newIndexParent])
                newBoard.occupiedFields.add(
                    tournament[1].queenMembers[newIndexParent].y * self.boardSize
                    + tournament[1].queenMembers[newIndexParent].x)

                newIndexChild += 1
                newIndexParent += 1
        newBoard.updateLossFunction()
        return newBoard

    def tournamentSelection(self):
        children = []
        for i in range(self.populationSize):
            tournament = np.random.choice(self.members, 2, self.distribution)
            children.append(self.crossover(tournament[0],tournament[1]))
        return children

    def mutatedBoards(self, bestBoards):
        for board in bestBoards:
            if random.uniform(0, 1) < self.boardMutationProbability:
                for queen in board.queenMembers:
                    if random.uniform(0, 1) < self.queenMutationProbability:
                        field = random.randint(0, self.boardSize * self.boardSize - 1)
                        while field in board.occupiedFields:
                            field = random.randint(0, self.boardSize * self.boardSize - 1)
                        board.occupiedFields.remove(self.boardSize * queen.y + queen.x)
                        board.occupiedFields.add(field)
                        queen.x = field % self.boardSize
                        queen.y = int(field / self.boardSize)
                    board.updateLossFunction()
        return bestBoards

    def evolve(self, epochs):
        filename = "log_tournament_evol_"+str(self.boardSize)+"_"+str(self.populationSize)+"_"+str(self.queenMutationProbability)+"_"+str(self.boardMutationProbability)
        f = open(filename, "w")
        f.write("Epochs,Best fitness,Average fitness\n")
        for i in range(epochs):
            bestBoards = self.tournamentSelection()
            mutatedBoards = self.mutatedBoards(bestBoards)
            temp = mutatedBoards + self.members
            temp.sort(key=lambda board: board.fitness)
            self.members = temp[0:len(self.members)]

            sumOfFitness = 0
            fittest = 100000
            fittestBoard = ''
            for board in self.members:
                if board.fitness < fittest:
                    fittest = board.fitness
                    fittestBoard = board
                sumOfFitness += board.fitness
            avgFit = sumOfFitness / len(self.members)
            f.write(str(i+1)+","+str(fittest)+","+str(avgFit)+"\n")
            print("Epoch nr: " + str(i) + " fittest candidate: " + str(fittest) + "  avg.fit: " + "%.2f" % avgFit)