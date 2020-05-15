'''
Created on 2020/05/05

@author: ukai
'''
import unittest

from ConcAgentFactory import ConcAgentFactory
from ConcBuildOrder import ConcBuildOrder
from ConcEnvrionmentFactory import ConcEnvironmentFactory
from ConcRewardGiverFactory import ConcRewardGiverFactory
from ConcTrainerFactory import ConcTrainerFactory
from ConcValueFunctionApproximatorFactory import ConcValueFunctionApproximatorFactory
from framework import Trainer


class Test(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        
        buildOrder = ConcBuildOrder(nIteration=100
                                    , nSeq=2
                                    , nHorizonValueOptimization=1
                                    , nIntervalPolicyOptimization=10
                                    , nBatchPolicyOptimization=2**5
                                    , nSaveInterval=2**5
                                    , description="test"
                                    , nLevers=3)
        
        agent = ConcAgentFactory().create(buildOrder)
        environment = ConcEnvironmentFactory().create(buildOrder)
        valueFunctionApproximator = ConcValueFunctionApproximatorFactory().create(buildOrder)
        rewardGiver = ConcRewardGiverFactory().create(buildOrder)
        
        trainerFactory = ConcTrainerFactory()
        trainer = trainerFactory.create(agent, environment, valueFunctionApproximator, rewardGiver, buildOrder)
        
        self.buildOrder = buildOrder
        self.trainer = trainer
        
        

    def test001(self):
        
        trainer = self.trainer
        assert isinstance(trainer, Trainer)
        
    def test002(self):
        
        trainer = self.trainer
        
        trainer.init()
        
        assert trainer.timeLastUpdate == -1
        assert trainer.timeSimulation == -1

        assert len(trainer.historyActions) == 0
        assert len(trainer.historyObservationSequences) == 1
        assert len(trainer.historyRewards) == 0
        
    def test003(self):
        
        trainer = self.trainer
        
        trainer.init()
        trainer.train(1)
        
        assert trainer.timeLastUpdate == -1
        assert trainer.timeSimulation == 0
        
        assert len(trainer.historyActions) == 1
        assert len(trainer.historyObservationSequences) == 2
        assert len(trainer.historyRewards) == 1
        
        assert trainer.valueFunctionOptimizer.countUpdate == 1

    def test004(self):
        
        trainer = self.trainer
        buildOrder = self.buildOrder
        
        trainer.init()
        trainer.train(buildOrder.getnIntervalPolicyOptimization())
        
        assert trainer.policyOptimizer.countUpdate == 1

    def test005(self):
        
        trainer = self.trainer
        
        trainer.init()
        trainer.train(2**10)
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test001']
    unittest.main()