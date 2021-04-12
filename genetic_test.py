import unittest
import copy
from geneticAlgo import Queen
from geneticAlgo import Board
from geneticAlgo import Population

class bcolors:
    GREEN = "\033[96m"
    ENDC = '\033[0m'

class quenTests(unittest.TestCase):
    def testQuen1(self):
        q1 = Queen(1,2)
        self.assertEqual(q1.x, 1)
        self.assertEqual(q1.y, 2)
        print(bcolors.GREEN + "\u2713 Test passed! test:  testQuen1 " + bcolors.ENDC)

    def testQuen2(self):
        q1 = Queen(-1,-2)
        self.assertEqual(q1.x, -1)
        self.assertEqual(q1.y, -2)
        print(bcolors.GREEN + "\u2713 Test passed! test:  testQuen2 " + bcolors.ENDC)

    def testQuenEquality(self):
        q1 = Queen(-1,-2)
        q2 = Queen(-1,-2)
        self.assertEqual(q1, q2)
        self.assertTrue(q1 == q2)
        q2.x = 0
        self.assertNotEqual(q1, q2)
        self.assertFalse(q1 == q2)
        print(bcolors.GREEN + "\u2713 Test passed! test:  testQuenEquality " + bcolors.ENDC)

class boardTests(unittest.TestCase):
    def testBoard1(self):
        b1 = Board(5, True)
        self.assertEqual(len(b1.occupiedFields), 5)
        self.assertEqual(len(b1.queenMembers), 5)
        print(bcolors.GREEN + ".\u2713 Test passed! test:  testBoard1" + bcolors.ENDC)

    def testBoardFitnessSmall(self):
        b1 = Board(2, True)
        self.assertEqual(len(b1.occupiedFields), 2)
        self.assertEqual(len(b1.queenMembers), 2)
        b1.queenMembers[0].x = 0;
        b1.queenMembers[0].y = 0;
        b1.queenMembers[1].x = 1;
        b1.queenMembers[1].y = 1;
        self.assertNotEqual(b1.queenMembers[0].x, b1.queenMembers[1].x)
        self.assertNotEqual(b1.queenMembers[0].y, b1.queenMembers[1].y)
        self.assertFalse(b1.queenMembers[0] == b1.queenMembers[1])
        b1.updateLossFunction()
        self.assertEqual(b1.fitness, 2)
        print(bcolors.GREEN + "\u2713 Test passed! test:  testBoardFitnessSmall " + bcolors.ENDC)

    def testBoardFitnessBig1(self):
        b1 = Board(4, True)
        b1.queenMembers[0].x = 0;
        b1.queenMembers[0].y = 0;
        b1.queenMembers[1].x = 1;
        b1.queenMembers[1].y = 0;
        b1.queenMembers[2].x = 2;
        b1.queenMembers[2].y = 0;
        b1.queenMembers[3].x = 3;
        b1.queenMembers[3].y = 0;
        b1.updateLossFunction()
        self.assertEqual(b1.fitness, 12)
        print(bcolors.GREEN + "\u2713 Test passed! test:  testBoardFitnessBig1 " + bcolors.ENDC)

    def testBoardFitnessBig2(self):
        b1 = Board(4, True)
        b1.queenMembers[0].x = 0;
        b1.queenMembers[0].y = 0;
        b1.queenMembers[1].x = 0;
        b1.queenMembers[1].y = 1;
        b1.queenMembers[2].x = 0;
        b1.queenMembers[2].y = 2;
        b1.queenMembers[3].x = 0;
        b1.queenMembers[3].y = 3;
        b1.updateLossFunction()
        self.assertEqual(b1.fitness, 12)
        print(bcolors.GREEN + "\u2713 Test passed! test:  testBoardFitnessBig2 " + bcolors.ENDC)

    def testBoardFitnessBig3(self):
        b1 = Board(4, True)
        b1.queenMembers[0].x = 0;
        b1.queenMembers[0].y = 0;
        b1.queenMembers[1].x = 1;
        b1.queenMembers[1].y = 1;
        b1.queenMembers[2].x = 2;
        b1.queenMembers[2].y = 2;
        b1.queenMembers[3].x = 3;
        b1.queenMembers[3].y = 3;
        b1.updateLossFunction()
        self.assertEqual(b1.fitness, 12)
        print(bcolors.GREEN + "\u2713 Test passed! test:  testBoardFitnessBig3 " + bcolors.ENDC)

    def testBoardFitnessBig4(self):
        b1 = Board(4, True)
        b1.queenMembers[0].x = 0;
        b1.queenMembers[0].y = 0;
        b1.queenMembers[1].x = 0;
        b1.queenMembers[1].y = 3;
        b1.queenMembers[2].x = 3;
        b1.queenMembers[2].y = 0;
        b1.queenMembers[3].x = 3;
        b1.queenMembers[3].y = 3;
        b1.updateLossFunction()
        self.assertEqual(b1.fitness, 12)
        print(bcolors.GREEN + "\u2713 Test passed! test:  testBoardFitnessBig4 " + bcolors.ENDC)

if __name__ == '__main__':
    unittest.main()
