'''
Created on 2020/05/05

@author: ukai
'''
import os
import shutil
import unittest

from ConcAgent import ConcAgent
from ConcAgentFactory import ConcAgentFactory
from ConcBuildOrder import ConcBuildOrder
from ConcEnvrionmentFactory import ConcEnvironmentFactory
from ConcMyLogger import ConcMyLogger
from ConcRewardGiverFactory import ConcRewardGiverFactory
from ConcStore import ConcStore
from ConcTrainerFactory import ConcTrainerFactory
from ConcValueFunctionApproximatorFactory import ConcValueFunctionApproximatorFactory
from MyArray import MyArray
from framework import Builder


class Test(unittest.TestCase):
    
    def setUp(self):
                
        builder = Builder(ConcStore()
                , ConcAgentFactory()
                , ConcEnvironmentFactory()
                , ConcTrainerFactory()
                , ConcValueFunctionApproximatorFactory()
                , ConcRewardGiverFactory()
                , ConcMyLogger())
        
        self.builder = builder
        
        ConcAgent.checkpointFolderPath = "testCheckPointFolder"
        ConcStore.saveFolderPath = "testSaveFolder"
        
    def tearDown(self):
        
        for path in [ConcAgent.checkpointFolderPath, ConcStore.saveFolderPath]:
            if os.path.exists(path):
                shutil.rmtree(path)


    def test001(self):
        builder = self.builder
        assert isinstance(builder, Builder)

    def test002(self):
        
        builder = self.builder        
        
        buildOrders = MyArray()
            
        for k1 in range(1):
            buildOrder = ConcBuildOrder(nIteration=100
                        , nSeq=2
                        , nHorizonValueOptimization=1
                        , nIntervalPolicyOptimization=10
                        , nBatchPolicyOptimization=2**5
                        , nSaveInterval=2**5
                        , description="test %d/3" % (k1+1)
                        , tConstant = 10
                        , nHiddenValueApproximator = 2**5
                        , sdPolicy = 0.1
                        , nActionsSampledFromPolicy = 2**1
                        , amplitudeDv = 0.0
                        )
            
            buildOrders.add(buildOrder)
            
        for k1 in range(1):
            buildOrder = ConcBuildOrder(nIteration=100
                        , nSeq=2
                        , nHorizonValueOptimization=1
                        , nIntervalPolicyOptimization=10
                        , nBatchPolicyOptimization=2**5
                        , nSaveInterval=2**5
                        , description="test %d/3" % (k1+1)
                        , tConstant = 10
                        , nHiddenValueApproximator = 2**5
                        , sdPolicy = 0.1
                        , nActionsSampledFromPolicy = 2**1
                        , amplitudeDv = 0.0
                        , valueFunctionOptimizer = "RMSprop"
                        , policyOptimizer = "RMSprop"
                        )
            
            buildOrders.add(buildOrder)
            
        buildOrder = ConcBuildOrder(nIteration=100
                    , nSeq=2
                    , nHorizonValueOptimization=1
                    , nIntervalPolicyOptimization=10
                    , nBatchPolicyOptimization=2**5
                    , nSaveInterval=2**5
                    , description="test 3"
                    , tConstant = 10
                    , nHiddenValueApproximator = 2**5
                    , sdPolicy = 0.1
                    , nActionsSampledFromPolicy = 2**1
                    , amplitudeDv = 0.0
                    , valueFunctionOptimizer = "RMSprop"
                    , policyOptimizer = "RMSprop"
                    , returnType = "SumOfInfiniteRewardSeries"
                    , gamma = 0.9
                    )
        
        buildOrders.add(buildOrder)
            
        builder.build(buildOrders)
   
    def test003(self):
        
        builder = self.builder        
        
        buildOrders = MyArray()            
        buildOrder = ConcBuildOrder(nIteration=100
                    , nSeq=2
                    , nHorizonValueOptimization=1
                    , nIntervalPolicyOptimization=10
                    , nBatchPolicyOptimization=2**5
                    , nSaveInterval=2**5
                    , description="test"
                    , tConstant = 10
                    , nHiddenValueApproximator = 2**5
                    , sdPolicy = 0.1
                    , nActionsSampledFromPolicy = 2**1
                    , amplitudeDv = 0.0
                    , environmentName = "AsmSimulator"
                    , asmPenaltyType = 0
                    , asmWeightOnCost = 0.9
                    , amplitudePeriodicDv= 2.0                    
                    )
        
        buildOrders.add(buildOrder)
        
        builder.build(buildOrders)
        
        
    def test004(self):
        
        builder = self.builder        
        
        buildOrders = MyArray()            
        buildOrder = ConcBuildOrder(nIteration=100
                    , nSeq=2
                    , nHorizonValueOptimization=1
                    , nIntervalPolicyOptimization=10
                    , nBatchPolicyOptimization=2**5
                    , nSaveInterval=2**5
                    , description="test"
                    , tConstant = 10
                    , nHiddenValueApproximator = 2**5
                    , sdPolicy = 0.1
                    , nActionsSampledFromPolicy = 2**1
                    , amplitudeDv = 0.0
                    , environmentName = "AsmSimulator"
                    , asmPenaltyType = 0
                    , asmWeightOnCost = 0.9
                    , amplitudePeriodicDv= 2.0
                    , agentEnableDcomponent = True
                    , agentEnableIcomponent = True                    
                    )
        
        buildOrders.add(buildOrder)
        
        builder.build(buildOrders)

    def test005(self):
        
        builder = self.builder        
        
        buildOrders = MyArray()            
        buildOrder = ConcBuildOrder(nIteration=100
                    , nSeq=2
                    , nHorizonValueOptimization=1
                    , nIntervalPolicyOptimization=10
                    , nBatchPolicyOptimization=2**5
                    , nSaveInterval=2**5
                    , description="test"
                    , tConstant = 10
                    , nHiddenValueApproximator = 2**5
                    , sdPolicy = 0.1
                    , nActionsSampledFromPolicy = 2**1
                    , amplitudeDv = 0.0
                    , environmentName = "AsmSimulator"
                    , asmPenaltyType = 0
                    , asmWeightOnCost = 0.9
                    , amplitudePeriodicDv= 2.0
                    , agentEnableDcomponent = True
                    , agentEnableIcomponent = True
                    , agentLimitBy = "clamp"                    
                    )
        
        buildOrders.add(buildOrder)
        
        builder.build(buildOrders)

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test001']
    unittest.main()