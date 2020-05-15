'''
Created on 2020/05/03

@author: ukai
'''
import os

from ConcAction import ConcAction
from ConcAgentMemento import ConcAgentMemento
from Utils import Utils
from framework import Agent
import tensorflow as tf


class ConcAgent(Agent, tf.keras.Model):
    '''
    classdocs
    '''

    checkpointFolderPath = "./checkpoint"


    def __init__(self, nLevers):
        '''
        Constructor
        '''
        super(ConcAgent, self).__init__()
        
        self._q = tf.Variable(tf.random.normal(shape=(1, nLevers,))) # (1, nLevers,)
        
    def call(self, _):
        # input: an instance of observationSequence is not used here.
        
        _pLever = tf.math.softmax(self._q, axis=-1) # (1, nLevers,)
        
        return ConcAction(_pLever)
    
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
        
        
        