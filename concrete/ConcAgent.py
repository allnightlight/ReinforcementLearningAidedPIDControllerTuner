'''
Created on 2020/05/03

@author: ukai
'''
import os

from ConcAction import ConcAction
from ConcAgentMemento import ConcAgentMemento
from Utils import Utils
from framework import Agent, ObservationSequence
import tensorflow as tf


class ConcAgent(Agent, tf.keras.Model):
    '''
    classdocs
    '''

    checkpointFolderPath = "./checkpoint"


    def __init__(self, nMv):
        '''
        Constructor
        '''
        super(ConcAgent, self).__init__()
        
        self.gainP = tf.keras.layers.Dense(nMv) # (*, nPv) -> (*, nMv)
        
    def call(self, observationSequence):
        # input: an instance of observationSequence is not used here.
        
        assert isinstance(observationSequence, ObservationSequence)
        obserbation = observationSequence.get(-1) # the latest observation
        y = obserbation.getValue() # (*, nPv)
        
        _u = self.gainP(y) # (*, nMv)
        
        return ConcAction(_u)
    
    def createMemento(self):
        if not os.path.exists(ConcAgent.checkpointFolderPath):
            os.mkdir(ConcAgent.checkpointFolderPath)
        
        saveFilePath = os.path.join(ConcAgent.checkpointFolderPath,
                                    Utils.generateRandomString(16))  
        # save
        self.save_weights(saveFilePath)        
        agentMemento = ConcAgentMemento(saveFilePath)        
        return agentMemento
    
    def loadFromMemento(self, agentMemento):
        assert isinstance(agentMemento, ConcAgentMemento)
        # load        
        self.load_weights(agentMemento.saveFilePath)        
        
        
        