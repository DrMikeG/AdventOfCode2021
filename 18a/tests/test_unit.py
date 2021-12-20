import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'tool_src'))
import advent

class TestSnailFish(unittest.TestCase):

    def test_splitString_01(self):
        self.assertEqual(advent.SnailFishNumber.splitString("[4,[6,6]]") , ("4","[6,6]"))
        self.assertEqual(advent.SnailFishNumber.splitString("[1,2]"), ("1","2"))
        self.assertEqual(advent.SnailFishNumber.splitString("[[1,2],3]"),("[1,2]","3"))
        self.assertEqual(advent.SnailFishNumber.splitString("[9,[8,7]]"),("9","[8,7]"))
        self.assertEqual(advent.SnailFishNumber.splitString("[[1,9],[8,5]]"),("[1,9]","[8,5]"))
        self.assertEqual(advent.SnailFishNumber.splitString("[[[[1,2],[3,4]],[[5,6],[7,8]]],9]"),("[[[1,2],[3,4]],[[5,6],[7,8]]]","9"))
        self.assertEqual(advent.SnailFishNumber.splitString("[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]"),("[[9,[3,8]],[[0,9],6]]","[[[3,7],[4,9]],3]"))
        self.assertEqual(advent.SnailFishNumber.splitString("[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]"),("[[[1,3],[5,3]],[[1,3],[8,7]]]","[[[4,9],[6,9]],[[8,2],[7,3]]]"))

    def test_MakeSnailFishNumbers_01(self):
        advent.SnailFishNumber(None,"[4,[6,6]]")
        advent.SnailFishNumber(None,"[1,2]")
        advent.SnailFishNumber(None,"[[1,2],3]")
        advent.SnailFishNumber(None,"[9,[8,7]]")
        advent.SnailFishNumber(None,"[[1,9],[8,5]]")
        advent.SnailFishNumber(None,"[[[[1,2],[3,4]],[[5,6],[7,8]]],9]")
        advent.SnailFishNumber(None,"[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]")
        advent.SnailFishNumber(None,"[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]")

    def roundTrip(self,inputStr):
        num1 = advent.SnailFishNumber(None,inputStr)
        s2 = num1.toString()
        self.assertEqual(inputStr,s2)
        num2 = advent.SnailFishNumber(None,s2)
        s3 = num2.toString()
        self.assertEqual(inputStr,s3)
        
    
    def test_toString(self):
        self.roundTrip("[1,2]")
        self.roundTrip("[4,[6,6]]")
        self.roundTrip("[[1,2],3]")
        self.roundTrip("[9,[8,7]]")
        self.roundTrip("[[1,9],[8,5]]")
        self.roundTrip("[[[[1,2],[3,4]],[[5,6],[7,8]]],9]")
        self.roundTrip("[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]")
        self.roundTrip("[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]")

    def getMag(self,inputStr,expectedMag):
        num1 = advent.SnailFishNumber(None,inputStr)
        mag= num1.magnitude()
        self.assertEqual(expectedMag,mag)

    def test_magnitude(self):
        self.getMag("[[1,2],[[3,4],5]]",143)
        self.getMag("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]",1384)
        self.getMag("[[[[1,1],[2,2]],[3,3]],[4,4]]",445)
        self.getMag("[[[[3,0],[5,3]],[4,4]],[5,5]]",791)
        self.getMag("[[[[5,0],[7,4]],[5,5]],[6,6]]",1137)
        self.getMag("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",3488)

    
if __name__ == '__main__':
    unittest.main()