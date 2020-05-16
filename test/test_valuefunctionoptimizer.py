'''
Created on 2020/05/03

@author: ukai
'''
import unittest

from ConcAction import ConcAction
from ConcAgent import ConcAgent
from ConcObservation import ConcObservation
from ConcRewardGiver import ConcRewardGiver
from ConcValueFunctionApproximator import ConcValueFunctionApproximator
from ConcValueFunctionOptimizer import ConcValueFunctionOptimizer
from MyArray import MyArray
from framework import ObservationSequence
import numpy as np
from ConcEnvironment import ConcEnvironment


class Test(unittest.TestCase):


    def test001(self):
        
        nHiddenValueApproximator = 2**3
        nHorizonValueOptimization = 3
        sdPolicy = 0.1
        
        valueFunctionApproximator = ConcValueFunctionApproximator(nHiddenValueApproximator)
        agent = ConcAgent(ConcEnvironment.nMv, sd = sdPolicy)
        
        valueFunctionOptimizer = ConcValueFunctionOptimizer(valueFunctionApproximator, agent, nHorizonValueOptimization)
        
        assert isinstance(valueFunctionOptimizer, ConcValueFunctionOptimizer)
        
        observationSequences = MyArray()
        actions = MyArray()
        rewards = MyArray()
        
        nStep= 10
        nBatch = 2**5
        
        observationSequence = ObservationSequence()
        for _ in range(nStep + 1):
            y = np.random.randn(nBatch, ConcEnvironment.nPv).astype(np.float32) # (*, nPv)
            observationSequence.add(ConcObservation(y))
            observationSequences.add(observationSequence)
            
        for _ in range(nStep):
            u = np.random.randn(nBatch, ConcEnvironment.nMv).astype(np.float32) # (*, nMv)
            action = ConcAction(u)
            actions.add(action)
        
        for observationSequence, action in zip(observationSequences, actions):
            reward = ConcRewardGiver().evaluate(observationSequence, action)
            rewards.add(reward)


        agent(observationSequence)
        valueFunctionApproximator(observationSequence, action)

        param0_policy = [elm.numpy()  for elm in agent.trainable_variables]
        param0_valfunc = [elm.numpy()  for elm in valueFunctionApproximator.trainable_variables]                        
        valueFunctionOptimizer.train(observationSequences, actions, rewards)
        param1_policy = [elm.numpy()  for elm in agent.trainable_variables]
        param1_valfunc = [elm.numpy()  for elm in valueFunctionApproximator.trainable_variables]                        

        for (elm0, elm1) in zip(param0_valfunc, param1_valfunc):
            assert not np.all(elm0 == elm1)
        
        for (elm0, elm1) in zip(param0_policy, param1_policy):
            assert np.all(elm0 == elm1)

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test001']
    unittest.main()