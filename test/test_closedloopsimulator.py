'''
Created on 2020/05/03

@author: ukai
'''
import unittest
import numpy as np
from ConcEnvironment import ConcEnvironment
from ConcAgent import ConcAgent
from framework import ClosedLoopSimulator, BuildOrder


class Test(unittest.TestCase):


    def test001(self):
        
        nLevers = 5
        environment = ConcEnvironment(nLevers)
        agent = ConcAgent(nLevers)
        
        nSeq = 3
        
        closedLoopSimulator = ClosedLoopSimulator(environment, agent, nSeq)
        
        assert isinstance(closedLoopSimulator, ClosedLoopSimulator)
        
        closedLoopSimulator.init()
        assert len(closedLoopSimulator.observationSequenceLast) == 1
        assert len(closedLoopSimulator.observationSequencePrev) == 0
        
        for k1 in range(nSeq * 2):
            y = closedLoopSimulator.observationSequenceLast[-1].getValue()
            assert not np.any(np.isnan(y))

            closedLoopSimulator.update()
            assert len(closedLoopSimulator.observationSequenceLast) == min(nSeq, k1+2)
            assert len(closedLoopSimulator.observationSequencePrev) == min(nSeq, k1+1)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test001']
    unittest.main()