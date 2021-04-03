import unittest
import copy
from geneticAlgo import Quen
from geneticAlgo import Board
from geneticAlgo import Population


class quenTests(unittest.TestCase):
    def testQuen1(self):
        q1 = Quen(1,2)
        self.assertEqual(q1.x, 1)
        self.assertEqual(q1.y, 2)

    def testQuen2(self):
        q1 = Quen(-1,-2)
        self.assertEqual(q1.x, -1)
        self.assertEqual(q1.y, -2)

    def testQuenEquality(self):
        q1 = Quen(-1,-2)
        q2 = Quen(-1,-2)
        self.assertEqual(q1, q2)
        self.assertTrue(q1 == q2)
        q2.x = 0
        self.assertNotEqual(q1, q2)
        self.assertFalse(q1 == q2)


class boardTests(unittest.TestCase):
    def testBoard1(self):
        b1 = Board(5)
        self.assertEqual(len(b1.occupiedFields), 5)
        self.assertEqual(len(b1.quenMembers), 5)

    def testBoardFitnessSmall(self):
        b1 = Board(2)
        self.assertEqual(len(b1.occupiedFields), 2)
        self.assertEqual(len(b1.quenMembers), 2)
        b1.quenMembers[0].x = 0;
        b1.quenMembers[0].y = 0;
        b1.quenMembers[1].x = 1;
        b1.quenMembers[1].y = 1;
        self.assertNotEqual(b1.quenMembers[0].x, b1.quenMembers[1].x)
        self.assertNotEqual(b1.quenMembers[0].y, b1.quenMembers[1].y)
        self.assertFalse(b1.quenMembers[0] == b1.quenMembers[1])
        b1.updateLossFunction()
        self.assertEqual(b1.fitness, 2)

    def testBoardFitnessBig1(self):
        b1 = Board(4)
        b1.quenMembers[0].x = 0;
        b1.quenMembers[0].y = 0;
        b1.quenMembers[1].x = 1;
        b1.quenMembers[1].y = 0;
        b1.quenMembers[2].x = 2;
        b1.quenMembers[2].y = 0;
        b1.quenMembers[3].x = 3;
        b1.quenMembers[3].y = 0;
        b1.updateLossFunction()
        self.assertEqual(b1.fitness, 12)

    def testBoardFitnessBig2(self):
        b1 = Board(4)
        b1.quenMembers[0].x = 0;
        b1.quenMembers[0].y = 0;
        b1.quenMembers[1].x = 0;
        b1.quenMembers[1].y = 1;
        b1.quenMembers[2].x = 0;
        b1.quenMembers[2].y = 2;
        b1.quenMembers[3].x = 0;
        b1.quenMembers[3].y = 3;
        b1.updateLossFunction()
        self.assertEqual(b1.fitness, 12)

    def testBoardFitnessBig3(self):
        b1 = Board(4)
        b1.quenMembers[0].x = 0;
        b1.quenMembers[0].y = 0;
        b1.quenMembers[1].x = 1;
        b1.quenMembers[1].y = 1;
        b1.quenMembers[2].x = 2;
        b1.quenMembers[2].y = 2;
        b1.quenMembers[3].x = 3;
        b1.quenMembers[3].y = 3;
        b1.updateLossFunction()
        self.assertEqual(b1.fitness, 12)

    def testBoardFitnessBig4(self):
        b1 = Board(4)
        b1.quenMembers[0].x = 0;
        b1.quenMembers[0].y = 0;
        b1.quenMembers[1].x = 0;
        b1.quenMembers[1].y = 3;
        b1.quenMembers[2].x = 3;
        b1.quenMembers[2].y = 0;
        b1.quenMembers[3].x = 3;
        b1.quenMembers[3].y = 3;
        b1.updateLossFunction()
        self.assertEqual(b1.fitness, 12)

class populationTest(unittest.TestCase):
    def testSimplePopulation1(self):
        p1 = Population(3,4)
        self.assertEqual(len(p1.members), 3)
        for i in range(3):
            self.assertEqual(len(p1.members[i].quenMembers), 4)
            self.assertEqual(len(p1.members[i].occupiedFields), 4)

    def testSimplePopulation2(self):
        p1 = Population(1,4,1) #mutationProb = 1 -> to make all members different
        b1 = list([Board(4)])
        b2 = p1.mutatedBoards(copy.deepcopy(b1))

        self.assertTrue(b1[0].quenMembers[0] != b2[0].quenMembers[0])
        self.assertTrue(b1[0].quenMembers[1] != b2[0].quenMembers[1])
        self.assertTrue(b1[0].quenMembers[2] != b2[0].quenMembers[2])
        self.assertTrue(b1[0].quenMembers[3] != b2[0].quenMembers[3])

    def testSimplePopulation2(self):
        p1 = Population(1,4,0) #mutationProb = 0 -> to make no changes
        b1 = list([Board(4)])
        b2 = p1.mutatedBoards(copy.deepcopy(b1))

        self.assertTrue(b1[0].quenMembers[0] == b2[0].quenMembers[0])
        self.assertTrue(b1[0].quenMembers[1] == b2[0].quenMembers[1])
        self.assertTrue(b1[0].quenMembers[2] == b2[0].quenMembers[2])
        self.assertTrue(b1[0].quenMembers[3] == b2[0].quenMembers[3])


if __name__ == '__main__':
    unittest.main()
