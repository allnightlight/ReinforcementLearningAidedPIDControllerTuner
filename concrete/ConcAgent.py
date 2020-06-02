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
import numpy as np


class ConcAgent(Agent, tf.keras.Model):
    '''
    classdocs
    '''

    checkpointFolderPath = "./checkpoint"


    def __init__(self, nMv, sd, use_bias = True, fix_sd = True, fix_scale = True):
        '''
        Constructor
        '''
        super(ConcAgent, self).__init__()
        
        if fix_scale:
            self._logScale = tf.zeros(shape=(nMv,)) # (1, nMv)
        else:
            self._logScale = tf.Variable(tf.random.normal(shape=(nMv,))) # (1, nMv)
            
        self.nMv = nMv
        self.gainP = tf.keras.layers.Dense(nMv, use_bias = use_bias) # (*, nPv) -> (*, nMv)
        
        if fix_sd:
# This agent has the fixed standard deviation, sd, of the normal density function which represents the policy.
# It means that the policy is represented as like this:
# pi(a|s) = Normal(a|mu, sd), 
# where mu = a neural network(s) 
# and sd is the parameter given at the initialization.
            self._logSd = tf.ones(shape=(1, nMv)) * np.log(sd + 1e-16) # (1, nMv)
        else:        
# If fix_sd is True, this agent will output the Mv added by random values with the tunable standard deviation
# Precisely, pi(u|y), where pi,u,y are the probability of the agent, u: Mv and y: observation, respectively,
# pi(u|y) = Normal distribution(u; mu, sd), mu = Gain * y + bias, sd: variable(not fixed).
            self._logSd = tf.Variable(tf.random.normal(shape=(1, nMv))) # (1, nMv)
        
        self.use_bias = use_bias
        
    # <<private>>
    def getProbabilisticFunctionParameter(self, observationSequence):
        
        assert isinstance(observationSequence, ObservationSequence)
        obserbation = observationSequence.get(-1) # the latest observation
        y = obserbation.getValue() # (*, nPv)
        
        _mu = self.gainP(y) * tf.math.exp(self._logScale) # (*, nMv)
            
        _sd = tf.math.exp(self._logSd) # (1, nMv)
        _logSd = self._logSd # (1, nMv)
        
        return _mu, _sd, _logSd
    
    def sampleMvFromPi(self, observationSequence):
        _mu, _sd, _ = self.getProbabilisticFunctionParameter(observationSequence)
        # _mu: (*, nMv), _sd: (*, nMv)
        mu = _mu.numpy() # (*, nMv)
        sd = _sd.numpy() # (*, nMv)

        u = mu + np.random.randn(mu.shape[0], 1) * sd # (*, nMv)
        
        return u # (*, nMv)

        
    def call(self, observationSequence):
        # input: an instance of observationSequence is not used here.
        
        u = self.sampleMvFromPi(observationSequence) # (*, nMv)
                
        return ConcAction(u)
    
    def loglikelihood(self, observationSequence, action):
        
        _mu, _, _logSd = self.getProbabilisticFunctionParameter(observationSequence)

        u = action.getValue() # (*, nMv)

        _ll = tf.reduce_sum(-self._logSd - (u - _mu)**2/2 * tf.math.exp(-2 * _logSd), axis=-1, keepdims=True) # (*, 1)
            
        return _ll #(*, 1)
        
    
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
        
        
    def getParameters(self):
        
        _scale = tf.math.exp(self._logScale) # (1, nMv)
        
        param = dict()
        param["gain"] = (self.gainP.weights[0] * _scale).numpy() # (1, nMv)
        if self.use_bias:
            param["bias"] = (self.gainP.weights[1] * _scale).numpy() # (1, nMv)
        else:
            param["bias"] = np.nan * np.ones((1, self.nMv)) # (1, nMv)
        param["sd"] = (_scale * np.exp(self._logSd)).numpy()  # (1, nMv)
            
        return param
