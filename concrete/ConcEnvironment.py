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

    nPv = 1
    nMv = 1

    def __init__(self, tConstant, amplitudeDv = 0.1):
        '''
        Constructor
        '''
        
        self.x = None
        self.alpha = 1 - 1/tConstant # e.g. 0.99 = 1 - 1/100 with tConstant = 100
        self.beta = 1/np.sqrt(1 - self.alpha**2)
        # to normalize the amplitude of disturbance 
        # so that the influence on x equal to 1.
        self.gamma = amplitudeDv
        # the influence of disturbance on x is controlled by gamma
        
    def init(self):
        self.x = np.zeros((1,1)) # (1, nState = 1)
        
    def observe(self):
        y = self.x # (1, nState = nPv = 1)
        return ConcObservation(y.astype(np.float32))
    
    def update(self, action):
        # action as ConcAction
        
        u = action.getActionOnEnvironment() # (1, nMv)
        w = np.random.randn(1, 1) # (1, nDv = 1)
        self.x = self.alpha * self.x + (1-self.alpha) * u[:,0,None] + self.gamma * self.beta * w # (1, nState = 1)
        