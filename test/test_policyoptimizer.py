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
from ConcAction import ConcAction
from ConcEnvironment import ConcEnvironment


class Test(unittest.TestCase):


    def test001(self):
        
        nHiddenValueApproximator = 2**3
        sdPolicy = 0.01
                
        valueFunctionApproximator = ConcValueFunctionApproximator(nHiddenValueApproximator)
        agent = ConcAgent(ConcEnvironment.nMv, sdPolicy)        
        
        observationSequences = MyArray()
        
        Nstep = 10
        observationSequence = ObservationSequence()
        for _ in range(Nstep + 1):
            y = np.random.randn(1, ConcEnvironment.nPv).astype(np.float32) # (1, nPv)
            observationSequence.add(ConcObservation(y))
            observationSequences.add(observationSequence)
            
        u = np.random.randn(1, ConcEnvironment.nMv) # (1, nMv)
        action = ConcAction(u)
            
        # to initialize the internal parameters
        agent(observationSequence)
        valueFunctionApproximator(observationSequence, action)

        nIntervalPolicyOptimization = 10
        nBatchPolicyOptimization = 2**5
        nActionsSampledFromPolicy = 2**3
        
        policyOptimizer = ConcPolicyOptimizer(agent, valueFunctionApproximator, nIntervalPolicyOptimization, nBatchPolicyOptimization, nActionsSampledFromPolicy)
        
        param0_policy = [elm.numpy()  for elm in agent.trainable_variables]
        param0_valfunc = [elm.numpy()  for elm in valueFunctionApproximator.trainable_variables]
        policyOptimizer.train(observationSequences)                        
        param1_policy = [elm.numpy()  for elm in agent.trainable_variables]
        param1_valfunc = [elm.numpy()  for elm in valueFunctionApproximator.trainable_variables]                        

        for (elm0, elm1) in zip(param0_valfunc, param1_valfunc):
            assert np.all(elm0 == elm1)
        
        for (elm0, elm1) in zip(param0_policy, param1_policy):
            assert not np.all(elm0 == elm1)

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test001']
    unittest.main()