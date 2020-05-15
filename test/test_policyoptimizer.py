'''
Created on 2020/05/03

@author: ukai
'''

import unittest

from ConcAgent import ConcAgent
from ConcObservation import ConcObservation
from ConcValueFunctionApproximator import ConcValueFunctionApproximator
from ConcValueFunctionOptimizer import ConcValueFunctionOptimizer
from MyArray import MyArray
from framework import ObservationSequence, PolicyOptimizer
import numpy as np
from ConcPolicyOptimizer import ConcPolicyOptimizer


class Test(unittest.TestCase):


    def test001(self):
        
        nLevers = 10
        nHorizonValueOptimization = 3
        
        valueFunctionApproximator = ConcValueFunctionApproximator(nLevers)
        agent = ConcAgent(nLevers)
        
        valueFunctionOptimizer = ConcValueFunctionOptimizer(valueFunctionApproximator, agent, nHorizonValueOptimization)
        
        assert isinstance(valueFunctionOptimizer, ConcValueFunctionOptimizer)
        
        observationSequences = MyArray()
        
        Nstep = 10
        Ny = 1
        observationSequence = ObservationSequence()
        for _ in range(Nstep + 1):
            y = np.random.randn(1, Ny).astype(np.float32)
            observationSequence.add(ConcObservation(y))
            observationSequences.add(observationSequence)

        nIntervalPolicyOptimization = 10
        nBatchPolicyOptimization = 2**5
        policyOptimizer = ConcPolicyOptimizer(agent, valueFunctionApproximator, nIntervalPolicyOptimization, nBatchPolicyOptimization)
        
        policyOptimizer.train(observationSequences)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test001']
    unittest.main()