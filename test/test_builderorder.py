'''
Created on 2020/05/05

@author: ukai
'''
import unittest
from ConcBuildOrder import ConcBuildOrder
import json


class Test(unittest.TestCase):


    def test001(self):
        
        arg = dict(
            nIteration=100,
            nSeq=2,
            nHorizonValueOptimization=3,
            nIntervalPolicyOptimization=4,
            nBatchPolicyOptimization=5,
            nSaveInterval=6,
            description="test message 20201634",
            tConstant = 10,  
            nHiddenValueApproximator = 2**3, 
            sdPolicy = 0.1,
            nActionsSampledFromPolicy = 2**3,
            )
        
        buildOrder = ConcBuildOrder(**arg)
        
        arg2 = buildOrder.toDict()
        
        for key in arg:
            assert arg[key] == arg2[key]
        
        
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test001']
    unittest.main()