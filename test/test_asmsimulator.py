'''
Created on 2020/05/25

@author: ukai
'''
import unittest
import numpy as np
from AsmSimulator import AsmSimulator
from AsmAction import AsmAction
from ConcObservation import ConcObservation


class Test(unittest.TestCase):

    def test001(self):
        
        DoMax = 3.0
        DoMin = 0.0
        for _ in range(2**3):
            u = np.random.randn(2**5, 1) # (*, 1)
            action = AsmAction(u, DoMax=DoMax, DoMin = DoMin)
            assert isinstance(action, AsmAction)
            Do = action.getActionOnEnvironment()
            assert np.all(Do >= DoMin - 1e-8)
            assert np.all(Do <= DoMax + 1e-8)

    def test002(self):
        
        asmSimulator = AsmSimulator()
        
        assert isinstance(asmSimulator, AsmSimulator)
        
        asmSimulator.init()
        
        assert asmSimulator.t is not None
        assert asmSimulator.x is not None
        
        assert np.all(asmSimulator.x > 0. - 1e-16)
        
        for _ in range(2**4):
            action = AsmAction(np.random.randn(1, 1)) # (1, nMv = 1)
            asmSimulator.update(action)
            
            assert not np.any(np.isnan(asmSimulator.x))
                        
            observation = asmSimulator.observe()            
            assert isinstance(observation, ConcObservation)
 

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test001']
    unittest.main()