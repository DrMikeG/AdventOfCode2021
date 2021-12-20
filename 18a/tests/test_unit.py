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

    def test_add0(self):
        newStr = advent.SnailFishNumber.add("[1,2]","[[3,4],5]")
        self.getMag(newStr,143)

    def test_add1(self):
        newStr = advent.SnailFishNumber.add("[[[[4,3],4],4],[7,[[8,4],9]]]","[1,1]")
        self.assertEqual(newStr,"[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")

    def test_add2(self):
        newStr = advent.SnailFishNumber.add("[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]","[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]")
        self.assertEqual(newStr,"[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]")

    def test_add3(self):
        newStr = advent.SnailFishNumber.add("[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]","[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]")
        self.assertEqual(newStr,"[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]")

    def test_add4(self):
        newStr = advent.SnailFishNumber.add("[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]","[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]")
        self.assertEqual(newStr,"[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]")

    def test_add5(self):
        newStr = advent.SnailFishNumber.add("[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]","[7,[5,[[3,8],[1,4]]]]")
        self.assertEqual(newStr,"[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]")

    def test_add5_detectExplode01(self):
        sn = advent.SnailFishNumber(None,"[[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]],[7,[5,[[3,8],[1,4]]]]]")
        self.assertTrue(sn.triggerFirstExplosion())
        toString = sn.toString()
        self.assertEqual(toString,"[[[[0,[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]],[7,[5,[[3,8],[1,4]]]]]")

    def test_add5_detectExplode02(self):
        sn = advent.SnailFishNumber(None,"[[[[0,[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]],[7,[5,[[3,8],[1,4]]]]]")
        self.assertTrue(sn.triggerFirstExplosion())
        toString = sn.toString()
        self.assertEqual(toString,"[[[[7,0],[[14,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]],[7,[5,[[3,8],[1,4]]]]]")

    def test_add5_detectExplode03(self):
        sn = advent.SnailFishNumber(None,"[[[[7,0],[[14,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]],[7,[5,[[3,8],[1,4]]]]]")
        self.assertTrue(sn.triggerFirstExplosion())
        toString = sn.toString()
        self.assertEqual(toString,"[[[[7,14],[0,[14,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]],[7,[5,[[3,8],[1,4]]]]]")
    
    def test_add5_detectExplode04(self):
        sn = advent.SnailFishNumber(None,"[[[[7,14],[0,[14,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]],[7,[5,[[3,8],[1,4]]]]]")
        self.assertTrue(sn.triggerFirstExplosion())
        toString = sn.toString()
        self.assertEqual(toString,"[[[[7,14],[14,0]],[[[15,7],[8,8]],[[7,7],[8,7]]]],[7,[5,[[3,8],[1,4]]]]]")
   
    def test_add5_detectExplode05(self):
        sn = advent.SnailFishNumber(None,"[[[[7,14],[14,0]],[[[15,7],[8,8]],[[7,7],[8,7]]]],[7,[5,[[3,8],[1,4]]]]]")
        self.assertTrue(sn.triggerFirstExplosion())
        toString = sn.toString()
        self.assertEqual(toString,"[[[[7,14],[14,15]],[[0,[15,8]],[[7,7],[8,7]]]],[7,[5,[[3,8],[1,4]]]]]")
    
    def test_add5_detectExplode06(self):
        sn = advent.SnailFishNumber(None,"[[[[7,14],[14,15]],[[0,[15,8]],[[7,7],[8,7]]]],[7,[5,[[3,8],[1,4]]]]]")
        self.assertTrue(sn.triggerFirstExplosion())
        toString = sn.toString()
        self.assertEqual(toString,"[[[[7,14],[14,15]],[[15,0],[[15,7],[8,7]]]],[7,[5,[[3,8],[1,4]]]]]")

    def test_add5_detectExplode07(self):
        sn = advent.SnailFishNumber(None,"[[[[7,14],[14,15]],[[15,0],[[15,7],[8,7]]]],[7,[5,[[3,8],[1,4]]]]]")
        self.assertTrue(sn.triggerFirstExplosion())
        toString = sn.toString()
        self.assertEqual(toString,"[[[[7,14],[14,15]],[[15,15],[0,[15,7]]]],[7,[5,[[3,8],[1,4]]]]]")

    def test_add5_detectExplode08(self):
        sn = advent.SnailFishNumber(None,"[[[[7,14],[14,15]],[[15,15],[0,[15,7]]]],[7,[5,[[3,8],[1,4]]]]]")
        self.assertTrue(sn.triggerFirstExplosion())
        toString = sn.toString()
        self.assertEqual(toString,"[[[[7,14],[14,15]],[[15,15],[15,0]]],[14,[5,[[3,8],[1,4]]]]]")
        sn.reduce()

    def test_add5_detectExplode09(self):
        sn = advent.SnailFishNumber(None,"[[[[7,14],[14,15]],[[15,15],[15,0]]],[14,[5,[[3,8],[1,4]]]]]")
        self.assertTrue(sn.triggerFirstExplosion())
        toString = sn.toString()
        self.assertEqual(toString,"[[[[7,14],[14,15]],[[15,15],[15,0]]],[14,[8,[0,[9,4]]]]]")
        sn.reduce()

    def test_add5_detectExplode10(self):
        sn = advent.SnailFishNumber(None,"[[[[7,14],[14,15]],[[15,15],[15,0]]],[14,[8,[0,[9,4]]]]]")
        self.assertTrue(sn.triggerFirstExplosion())
        toString = sn.toString()
        self.assertEqual(toString,"[[[[7,14],[14,15]],[[15,15],[15,0]]],[14,[8,[9,0]]]]")
        sn.reduce()

    def test_add5_detectSplit01(self):
        sn = advent.SnailFishNumber(None,"[[[[7,14],[14,15]],[[15,15],[15,0]]],[14,[8,[9,0]]]]")
        self.assertTrue(sn.triggerFirstSplit())
        toString = sn.toString()
        self.assertEqual(toString,"[[[[7,[7,7]],[14,15]],[[15,15],[15,0]]],[14,[8,[9,0]]]]")
        sn.reduce()

    def test_add5_detectExplode11(self):
        sn = advent.SnailFishNumber(None,"[[[[7,[7,7]],[14,15]],[[15,15],[15,0]]],[14,[8,[9,0]]]]")
        self.assertTrue(sn.triggerFirstExplosion())
        toString = sn.toString()
        self.assertEqual(toString,"[[[[14,0],[21,15]],[[15,15],[15,0]]],[14,[8,[9,0]]]]")
        sn.reduce()

    def test_add5_detectExplode02(self):
        sn = advent.SnailFishNumber(None,"[[[[14,0],[21,15]],[[15,15],[15,0]]],[14,[8,[9,0]]]]")
        self.assertTrue(sn.triggerFirstSplit())
        toString = sn.toString()
        self.assertEqual(toString,"[[[[[7,7],0],[21,15]],[[15,15],[15,0]]],[14,[8,[9,0]]]]")
        sn.reduce()
        

    def test_add6(self):
        newStr = advent.SnailFishNumber.add("[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]","[[2,[2,2]],[8,[8,1]]]")
        self.assertEqual(newStr,"[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]")

    def test_add7(self):
        newStr = advent.SnailFishNumber.add("[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]","[2,9]")
        self.assertEqual(newStr,"[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]")

    def test_add8(self):
        newStr = advent.SnailFishNumber.add("[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]","[1,[[[9,3],9],[[9,0],[0,7]]]]")
        self.assertEqual(newStr,"[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]")

    def test_add9(self):
        newStr = advent.SnailFishNumber.add("[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]","[[[5,[7,4]],7],1]")
        self.assertEqual(newStr,"[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]")

    def test_add10(self):
        newStr = advent.SnailFishNumber.add("[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]","[[[[4,2],2],6],[8,7]]")
        self.assertEqual(newStr,"[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")



    def test_detectExplode01(self):
        sn = advent.SnailFishNumber(None,"[[[[[9,8],1],2],3],4]")
        self.assertTrue(sn.triggerFirstExplosion())
        toString = sn.toString()
        self.assertEqual(toString,"[[[[0,9],2],3],4]")

    def test_detectExplode02(self):
        sn = advent.SnailFishNumber(None,"[7,[6,[5,[4,[3,2]]]]]")
        self.assertTrue(sn.triggerFirstExplosion())
        toString = sn.toString()
        self.assertEqual(toString,"[7,[6,[5,[7,0]]]]")
        
    def test_detectExplode03(self):
        sn = advent.SnailFishNumber(None,"[[6,[5,[4,[3,2]]]],1]")
        self.assertTrue(sn.triggerFirstExplosion())
        toString = sn.toString()
        self.assertEqual(toString,"[[6,[5,[7,0]]],3]")

    def test_detectExplode04(self):
        sn = advent.SnailFishNumber(None,"[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
        self.assertTrue(sn.triggerFirstExplosion())
        toString = sn.toString()
        self.assertEqual(toString,"[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
    
    def test_detectExplode05(self):
        sn = advent.SnailFishNumber(None,"[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
        self.assertTrue(sn.triggerFirstExplosion())
        toString = sn.toString()
        self.assertEqual(toString,"[[3,[2,[8,0]]],[9,[5,[7,0]]]]")

    def test_detectSplit01(self):
        sn = advent.SnailFishNumber(None,"[[[[0,7],4],[15,[0,13]]],[1,1]]")
        self.assertTrue(sn.triggerFirstSplit())
        toString = sn.toString()
        self.assertEqual(toString,"[[[[0,7],4],[[7,8],[0,13]]],[1,1]]")

    def test_detectSplit02(self):
        sn = advent.SnailFishNumber(None,"[[[[0,7],4],[[7,8],[0,13]]],[1,1]]")
        self.assertTrue(sn.triggerFirstSplit())
        toString = sn.toString()
        self.assertEqual(toString,"[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]")


if __name__ == '__main__':
    unittest.main()