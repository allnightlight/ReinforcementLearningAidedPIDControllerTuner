'''
Created on 2020/05/03

@author: ukai
'''
import numpy as np
from framework import Environment
from ConcObservation import ConcObservation

class ConcEnvironment(Environment):
    '''
    classdocs
    '''


    def __init__(self, nLevers):
        '''
        Constructor
        '''
        
        x = None
        p = np.zeros((nLevers,)) # (nLevers,)
        
        for k1 in range(nLevers):
            if k1 < nLevers - 1:
                p[k1] = 1/2**(k1+1)
            else:
                p[-1] = 1 - np.sum(p[:-1])
                
        self.p = p # (nLevers, )
        self.x = x # in {0, 1}
        
    def init(self):
        self.x = 0. # {0,1}
        
    def observe(self):
        y = self.x # {0, 1}        
        y_numpy = np.array(y, dtype=np.float32).reshape(1,-1)
        return ConcObservation(y_numpy)
    
    def update(self, action):
        # action as ConcAction
        
        selectedAction = action.getSelectedAction() # (nLevers,)
        pSelectedLever = np.sum(self.p * selectedAction) # (,)
        self.x = float(np.random.rand() < pSelectedLever) # (,)
        