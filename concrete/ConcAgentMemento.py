'''
Created on 2020/05/03

@author: ukai
'''
from framework import AgentMemento
import json

class ConcAgentMemento(AgentMemento):
    '''
    classdocs
    '''


    def __init__(self, saveFilePath):
        '''
        Constructor
        '''
        self.saveFilePath = saveFilePath
        
    def toDict(self):
        
        return dict(saveFilePath = self.saveFilePath) 