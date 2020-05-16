'''
Created on 2020/05/03

@author: ukai
'''
import unittest

from ConcAction import ConcAction
from ConcEnvironment import ConcEnvironment
from ConcObservation import ConcObservation
from framework import EnvironmentFactory
import numpy as np
from ConcEnvrionmentFactory import ConcEnvironmentFactory
from ConcBuildOrder import ConcBuildOrder


class Test(unittest.TestCase):


    def test001(self):
        
        tConstant = 10
        environment = ConcEnvironment(tConstant)
        environment.gamma = 0.0
        
        assert isinstance(environment, ConcEnvironment)
        
        environment.init()        
        observation = environment.observe()
        assert isinstance(observation, ConcObservation)
        
        Y = []
        for _ in range(2**10):
            u = np.random.randn(1, ConcEnvironment.nMv) # (1, nMv = 1)
            action = ConcAction(u)
    
            environment.update(action)        
            observation = environment.observe()
            Y.append(observation.getValue())

        Ynumpy = np.concatenate(Y, axis=0) # (2**10, nPv = 1)
        assert np.all((Ynumpy >= -1.) & (Ynumpy <= 1.)) 
        
    def test002(self):
        
        environmentFactory = ConcEnvironmentFactory()
        assert isinstance(environmentFactory, ConcEnvironmentFactory)
        
        buildOrder = ConcBuildOrder(100, 1, 2, 10, 32, 128, "test", 3, 100, 0.01)
        
        environment = environmentFactory.create(buildOrder)
        assert isinstance(environment, ConcEnvironment)

        
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test001']
    unittest.main()