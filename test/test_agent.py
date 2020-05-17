'''
Created on 2020/05/03

@author: ukai
'''
import shutil
import unittest

from ConcAction import ConcAction
from ConcAgent import ConcAgent
from ConcAgentFactory import ConcAgentFactory
from ConcAgentMemento import ConcAgentMemento
from ConcBuildOrder import ConcBuildOrder
from ConcObservation import ConcObservation
from framework import ObservationSequence, AgentMemento
import numpy as np


class Test(unittest.TestCase):


    def test001(self):
        nBatch = 2**5
        nMv = 10
        u = np.random.randn(nBatch, nMv)
        action = ConcAction(u)
        assert isinstance(action, ConcAction)

    def test002(self):
        nMv = 10
        nPv = 3
        nBatch = 2**5
        agent = ConcAgent(nMv, sd = 0.0)
        
        assert isinstance(agent, ConcAgent)
        
        observationSequence = ObservationSequence()
        y = np.random.randn(nBatch, nPv).astype(np.float32)  # (*, nPv)        
        observation = ConcObservation(y)
        observationSequence.add(observation)
        
        action = agent(observationSequence)
        
        assert isinstance(action, ConcAction)
        
    def test003(self):
        
        for _ in range(2**3):
            nMv, nBatch = np.random.randint(2**5, size=(2,))
            
            u = np.random.randn(nBatch, nMv)
            action = ConcAction(u)        
            actionOnEnvironment = action.getActionOnEnvironment() # (*, nMv)
            
            assert np.all((actionOnEnvironment >= -1.) & (actionOnEnvironment <= 1.))             
        
    def test004(self):
        ConcAgent.checkpointFolderPath = "./test_checkpoints"
        
        nMv = 10
        agent = ConcAgent(nMv, sd = 0.0)
        
        assert isinstance(agent, ConcAgent)

        observationSequence = ObservationSequence()
        
        y = np.array(1., dtype=np.float32).reshape(1,1) # (*, Ny = 1)
        observationSequence.add(ConcObservation(y))
        
        agent(observationSequence)
        agentMemento = agent.createMemento()
        assert isinstance(agentMemento, AgentMemento)
        
        agent2 = ConcAgent(nMv, 0.0)

        agent2.loadFromMemento(agentMemento)
        
        agent2(observationSequence)
        assert len(agent.trainable_variables) ==  len(agent2.trainable_variables)        
        for (w1, w2) in zip(agent.trainable_variables, agent2.trainable_variables):
            assert np.all(w1.numpy() == w2.numpy())
            
        shutil.rmtree(ConcAgent.checkpointFolderPath)
        
    def test005(self):
        
        agentFactory = ConcAgentFactory()
        assert isinstance(agentFactory, ConcAgentFactory)
        
        buildOrder = ConcBuildOrder(100, 1, 2, 10, 32, 128, "test", 100, 3, 0.0, 2**3)
        
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