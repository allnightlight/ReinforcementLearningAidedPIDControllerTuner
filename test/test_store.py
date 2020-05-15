'''
Created on 2020/05/05

@author: ukai
'''
import unittest

from ConcAgent import ConcAgent
from ConcAgentFactory import ConcAgentFactory
from ConcAgentMemento import ConcAgentMemento
from ConcBuildOrder import ConcBuildOrder
from ConcStore import ConcStore
from framework import TrainId, StoreField
import shutil
import os


class Test(unittest.TestCase):
    
    def setUp(self):
        
        ConcAgent.checkpointFolderPath = "testCheckPointFolder"
        ConcStore.saveFolderPath = "testSaveFolder"
        
    def tearDown(self):

        for path in [ConcAgent.checkpointFolderPath, ConcStore.saveFolderPath]:
            if os.path.exists(path):
                shutil.rmtree(path)


    def test001(self):
        
        concStore = ConcStore()
        
        isinstance(concStore, ConcStore)
        
        trainId = TrainId.generateTrainId()
            
        timeSimulation  = 123
        agentMemento = ConcAgentMemento(saveFilePath = "saveFilePathTEST")        
        buildOrder = ConcBuildOrder(100, 1, 2, 10, 32, 128, "test", 2)
        timeStamp = "2020-05-05 16:23:59"
        
        storeField = StoreField(timeSimulation, agentMemento, buildOrder, timeStamp);
        
        concStore.save(trainId, storeField)
        
        storeField2 = concStore.load(trainId)
        
        assert storeField.timeSimulation == storeField2.timeSimulation
        assert storeField.timeStamp == storeField2.timeStamp
        assert storeField.agentMemento.toDict() == storeField2.agentMemento.toDict() 
        assert storeField.buildOrder.toDict() == storeField2.buildOrder.toDict()
        
        
    def test002(self): 
        
        N = 2**10
        X = set([TrainId.generateTrainId().__str__()  for _ in range(N)])
        assert len(X) == N
        
    def test003(self):

        concStore = ConcStore()
        agentFactory = ConcAgentFactory()
                
        N = 2**3
        for _ in range(N):
                
            trainId = TrainId.generateTrainId()
            buildOrder = ConcBuildOrder(100, 1, 2, 10, 32, 128, "test", 2)
            
            agent = agentFactory.create(buildOrder)
                
            timeSimulation  = 123
            agentMemento = agent.createMemento()        
            timeStamp = "2020-05-05 16:23:59"
            
            storeField = StoreField(timeSimulation, agentMemento, buildOrder, timeStamp);
            
            concStore.save(trainId, storeField)
            
            storeField2 = concStore.load(trainId)
            
            agent2 = agentFactory.create(storeField2.getBuildOrder())
            agent2.loadFromMemento(storeField2.getAgentMemento())
                        
                        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test001']
    unittest.main()