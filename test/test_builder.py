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
            
        for k1 in range(3):
            buildOrder = ConcBuildOrder(nIteration=100
                        , nSeq=2
                        , nHorizonValueOptimization=1
                        , nIntervalPolicyOptimization=10
                        , nBatchPolicyOptimization=2**5
                        , nSaveInterval=2**5
                        , description="test %d/3" % (k1+1)
                        , nLevers=3)
            
            buildOrders.add(buildOrder)
            
        builder.build(buildOrders)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test001']
    unittest.main()