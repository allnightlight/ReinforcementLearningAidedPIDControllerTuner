'''
Created on 2020/05/05

@author: ukai
'''
import json
import os

from ConcAgentMemento import ConcAgentMemento
from ConcBuildOrder import ConcBuildOrder
from framework import Store, StoreField, TrainId


class ConcStore(Store):
    '''
    classdocs
    '''
    
    saveFolderPath = "./trainLog"


    def __init__(self):
        '''
        Constructor
        '''
                
    def load(self, trainId):
        assert isinstance(trainId, TrainId)
        
        savedFilePath = os.path.join(
            ConcStore.saveFolderPath,
            trainId.__str__(),
            )
        
        with open(savedFilePath, "r",  encoding = "utf-8") as fp:            
            savedData = json.load(fp)
        
        timeSimulation = savedData["body"]["timeSimulation"]
        agentMemento = ConcAgentMemento(**savedData["body"]["agentMemento"])
        buildOrder = ConcBuildOrder(**savedData["body"]["buildOrder"])
        timeStamp = savedData["body"]["timeStamp"]
        
        storeField = StoreField(timeSimulation, agentMemento, buildOrder, timeStamp)
        
        return storeField
    
    def save(self, trainId, storeField):
        
        assert isinstance(trainId, TrainId)
        assert isinstance(storeField, StoreField)
        
        if not os.path.exists(ConcStore.saveFolderPath):
            os.mkdir(ConcStore.saveFolderPath)
        
        saveFilePath = os.path.join(
            ConcStore.saveFolderPath,
            trainId.__str__(),
            )
        
        savedData = {
            "trainId": trainId.__str__(),
            "body":{
                "timeSimulation": storeField.getTimeSimulation(),
                "agentMemento": storeField.getAgentMemento().toDict(),
                "buildOrder": storeField.getBuildOrder().toDict(),
                "timeStamp": storeField.getTimeStamp(),            
                },
            }
        with open(saveFilePath, "w", encoding = "utf-8") as fp:
            json.dump(savedData, fp)
        