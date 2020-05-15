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
            nLevers=7,
            )
        
        buildOrder = ConcBuildOrder(**arg)
        
        arg2 = buildOrder.toDict()
        
        assert arg == arg2
        
        
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test001']
    unittest.main()