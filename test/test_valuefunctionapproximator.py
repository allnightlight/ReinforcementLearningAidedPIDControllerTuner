'''
Created on 2020/05/03

@author: ukai
'''

import unittest

from ConcObservation import ConcObservation
from ConcValueFunctionApproximator import ConcValueFunctionApproximator
import numpy as np
from framework import ObservationSequence
from ConcValue import ConcValue
from ConcValueFunctionApproximatorFactory import ConcValueFunctionApproximatorFactory
from ConcBuildOrder import ConcBuildOrder


class Test(unittest.TestCase):


    def test001(self):
        
        nLevers = 10
        
        valueFunctionApproximator = ConcValueFunctionApproximator(nLevers)
        
        assert isinstance(valueFunctionApproximator, ConcValueFunctionApproximator)
        
        observationSequence = ObservationSequence()
        
        y = np.array(1.0, np.float32).reshape(1,1)
        observation = ConcObservation(y)
        observationSequence.add(observation)

        value = valueFunctionApproximator(observationSequence)
        
        assert isinstance(value, ConcValue)
        
        _qValue = value.getValue()
        assert _qValue.shape == (1, nLevers)
        
    def test002(self):
        
        valueFunctionApproximatorFactory = ConcValueFunctionApproximatorFactory()
        assert isinstance(valueFunctionApproximatorFactory, ConcValueFunctionApproximatorFactory)
        
        buildOrder = ConcBuildOrder(100, 1, 2, 10, 32, 128, "test", 3)
        
        valueFunctionApproximator = valueFunctionApproximatorFactory.create(buildOrder)
        assert isinstance(valueFunctionApproximator, ConcValueFunctionApproximator)

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test001']
    unittest.main()