'''
Created on 2020/05/03

@author: ukai
'''

from framework import Action
import numpy as np


class ConcAction(Action):
    '''
    classdocs
    '''

    def __init__(self, u, uMin = -1, uMax = 1, limitBy = "tanh"):
        '''
        Constructor
        '''
        assert len(u.shape) == 2
        assert type(u) is np.ndarray 
        self.u = u.astype(np.float32) # (*, nMv,)

        # u is not used as a manipulated value for the environment,
        # instead, what should be used is the value ceiling u   
        # after having converted as numpy.ndarray         
        if limitBy == "tanh":
            self.actionOnEnvironment = np.tanh(u).astype(np.float32) # (*, nMv,)
            
        if limitBy == "clamp":            
            actionOnEnvironment = u.copy() * (uMax - uMin)/2 + (uMax + uMin)/2 # (*, nMv)
            actionOnEnvironment[u < -1.] = uMin
            actionOnEnvironment[u > 1.] = uMax
            self.actionOnEnvironment = actionOnEnvironment.astype(np.float32) # (*, nMv,)

        
    def getValue(self):
        return self.u # (*, nMv,)
    
    def getActionOnEnvironment(self):
        return self.actionOnEnvironment # (*, nMv,)