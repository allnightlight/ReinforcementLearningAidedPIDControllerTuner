'''
Created on 2020/05/25

@author: ukai
'''

import numpy as np
from ConcAction import ConcAction

class AsmAction(ConcAction):
    '''
    classdocs
    '''

    def __init__(self, u, DoMax = 3, DoMin = 0):
        '''
        Constructor
        '''
        assert len(u.shape) == 2
        assert type(u) is np.ndarray 
        self.u = u.astype(np.float32) # (*, nMv,)
        
        # u is not used as a manipulated value for the environment,
        # instead, what should be used is the value ceiling u   
        # after having converted as numpy.ndarray 
        self.actionOnEnvironment = DoMin + (DoMax - DoMin) * 1./(1.+np.exp(-u)).astype(np.float32) # (*, nMv,)
        
    def getValue(self):
        return self.u # (*, nMv,)
    
    def getActionOnEnvironment(self):
        return self.actionOnEnvironment # (*, nMv,)

    