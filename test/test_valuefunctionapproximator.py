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
from ConcAction import ConcAction
from ConcEnvironment import ConcEnvironment


class Test(unittest.TestCase):


    def test001(self):
        
        nHiddenValueApproximator = 2**3
        nBatch = 2**5
        
        valueFunctionApproximator = ConcValueFunctionApproximator(nHiddenValueApproximator)
        
        assert isinstance(valueFunctionApproximator, ConcValueFunctionApproximator)
        
        observationSequence = ObservationSequence()
        
        y = np.random.randn(nBatch, ConcEnvironment.nPv).astype(np.float32) # (*, nPv)
        observation = ConcObservation(y)
        observationSequence.add(observation)

        u = np.random.randn(nBatch, ConcEnvironment.nMv) # (*, nMv)        
        action = ConcAction(u)

        value = valueFunctionApproximator(observationSequence, action)
        
        assert isinstance(value, ConcValue)
        
        _aValue, _sValue = value.getValue()
        assert _aValue.shape == (nBatch, 1)
        assert _sValue.shape == (nBatch, 1)
        
    def test002(self):
        
        valueFunctionApproximatorFactory = ConcValueFunctionApproximatorFactory()
        assert isinstance(valueFunctionApproximatorFactory, ConcValueFunctionApproximatorFactory)
        
        buildOrder = ConcBuildOrder(100, 1, 2, 10, 32, 128, "test", 100, 2**3, 0.01, 2**3)
        
        valueFunctionApproximator = valueFunctionApproximatorFactory.create(buildOrder)
        assert isinstance(valueFunctionApproximator, ConcValueFunctionApproximator)

    def test003(self):
        
        nHiddenValueApproximator = 2**3
        nBatch = 2**5
        
        valueFunctionApproximator = ConcValueFunctionApproximator(nHiddenValueApproximator, enable_i_component=True, enable_d_component=True)
        
        assert isinstance(valueFunctionApproximator, ConcValueFunctionApproximator)
        
        observationSequence = ObservationSequence()
        
        for _ in range(10):
            y = np.random.randn(nBatch, ConcEnvironment.nPv).astype(np.float32) # (*, nPv)
            observation = ConcObservation(y)
            observationSequence.add(observation)

        u = np.random.randn(nBatch, ConcEnvironment.nMv) # (*, nMv)        
        action = ConcAction(u)

        value = valueFunctionApproximator(observationSequence, action)
        
        assert isinstance(value, ConcValue)
        
        _aValue, _sValue = value.getValue()
        assert _aValue.shape == (nBatch, 1)
        assert _sValue.shape == (nBatch, 1)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test001']
    unittest.main()