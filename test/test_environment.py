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
import tensorflow as tf
from ConcEnvrionmentFactory import ConcEnvironmentFactory
from ConcBuildOrder import ConcBuildOrder


class Test(unittest.TestCase):


    def test001(self):
        
        nLevers = 3
        environment = ConcEnvironment(nLevers)
        
        assert isinstance(environment, ConcEnvironment)
        
        environment.init()        
        observation = environment.observe()
        assert isinstance(observation, ConcObservation)
        
        _pLever = tf.random.uniform(shape=(1, nLevers,)) # (nLevers,)
        action = ConcAction(_pLever)
        action.selectedAction[:, 1:] = 0
        action.selectedAction[:, 0] = 1
        
        Y = []
        for _ in range(2**10):    
            environment.update(action)        
            observation = environment.observe()
            Y.append(observation.getValue())
        
        yAvg = np.mean(Y)
        # this assertion might be violated with a small probability.        
        assert np.abs(yAvg - 0.5) < 0.1, "y(average) = %.2f" % yAvg
        
    def test002(self):
        
        environmentFactory = ConcEnvironmentFactory()
        assert isinstance(environmentFactory, ConcEnvironmentFactory)
        
        buildOrder = ConcBuildOrder(100, 1, 2, 10, 32, 128, "test", 3)
        
        environment = environmentFactory.create(buildOrder)
        assert isinstance(environment, ConcEnvironment)

        
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test001']
    unittest.main()