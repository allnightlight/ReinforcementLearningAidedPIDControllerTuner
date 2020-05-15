'''
Created on 2020/05/03

@author: ukai
'''
import unittest
import numpy as np
from ConcAction import ConcAction
from ConcAgent import ConcAgent
import tensorflow as tf
from framework import ObservationSequence, AgentMemento
from ConcObservation import ConcObservation
import shutil
from ConcAgentFactory import ConcAgentFactory
from ConcBuildOrder import ConcBuildOrder
from ConcAgentMemento import ConcAgentMemento
import json


class Test(unittest.TestCase):


    def test001(self):
        nBatch = 2**5
        nLevers = 10
        _pLever = tf.random.uniform(shape=(nBatch, nLevers,))
        action = ConcAction(_pLever)
        assert isinstance(action, ConcAction)
        
    def test002(self):
        nLevers = 10
        agent = ConcAgent(nLevers)
        
        assert isinstance(agent, ConcAgent)
        
        action = agent(None)
        
        assert isinstance(action, ConcAction)
        
    def test003(self):
        nLevers = 3
        _pLever = tf.ones(shape=(1, nLevers,))
        _pLever = _pLever / tf.reduce_sum(_pLever) # (nLevers,)
        pLever = _pLever.numpy()
        
        A = []
        for _ in range(2**10):
            action = ConcAction(_pLever)        
            selectedAction = action.getSelectedAction() # (nLevers,)
            A.append(selectedAction)
        Aavg = np.mean(A, axis=0)
        # this assertion might be violated with a small probability.
        assert np.max(np.abs(Aavg - pLever)) < 0.1
        
    def test004(self):
        ConcAgent.checkpointFolderPath = "./test_checkpoints"
        
        nLevers = 10
        agent = ConcAgent(nLevers)
        
        assert isinstance(agent, ConcAgent)

        observationSequence = ObservationSequence()
        
        y = np.array(1., dtype=np.float32).reshape(1,1) # (*, Ny = 1)
        observationSequence.add(ConcObservation(y))
        
        agent(observationSequence)
        
        agentMemento = agent.createMemento()
        assert isinstance(agentMemento, AgentMemento)
        
        agent2 = ConcAgent(nLevers)
        
        agent2.loadFromMemento(agentMemento)
                
        for (w1, w2) in zip(agent.trainable_variables, agent2.trainable_variables):            
            assert np.all(w1.numpy() == w2.numpy())
            
        shutil.rmtree(ConcAgent.checkpointFolderPath)
        
    def test005(self):
        
        agentFactory = ConcAgentFactory()
        assert isinstance(agentFactory, ConcAgentFactory)
        
        buildOrder = ConcBuildOrder(100, 1, 2, 10, 32, 128, "test", 3)
        
        agent = agentFactory.create(buildOrder)
        assert isinstance(agent, ConcAgent)
        
    def test006(self):
        
        arg1 = dict(saveFilePath = "abcefg")
        agentMemento = ConcAgentMemento(**arg1)
        
        arg2 = agentMemento.toDict()
        
        assert arg1 == arg2
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test001']
    unittest.main()