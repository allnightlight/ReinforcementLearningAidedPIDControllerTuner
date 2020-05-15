'''
Created on 2020/05/03

@author: ukai
'''

import numpy as np
from framework import Action

class ConcAction(Action):
    '''
    classdocs
    '''

    def __init__(self, _pLever):
        '''
        Constructor
        '''
        assert len(_pLever.shape) == 2 
        self._pLever = _pLever # (*, nLevers,)
        
        nBatch, nLevers = _pLever.shape
        
        threshold = np.cumsum(_pLever.numpy(), axis=-1) # (*, nLevers,)
        iSelected = np.sum(np.random.rand(nBatch, 1) < threshold, axis=-1) - 1 # (*,)
        assert np.all((iSelected >= 0) & (iSelected < nLevers)) 
        
        self.selectedAction = np.zeros((nBatch, nLevers,)).astype(np.float32) # (*, nLevers,)
        for i, j in enumerate(iSelected):
            self.selectedAction[i, j] = 1
        
    def getValue(self):
        return self._pLever # (*, nLevers,)
    
    def getSelectedAction(self):
        return self.selectedAction # (*, nLevers,)