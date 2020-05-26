'''
Created on 2020/05/05

@author: ukai
'''
from framework import BuildOrder

class ConcBuildOrder(BuildOrder):
    '''
    classdocs
    '''


    def __init__(self, nIteration, nSeq, nHorizonValueOptimization, nIntervalPolicyOptimization, nBatchPolicyOptimization, nSaveInterval, description, nHiddenValueApproximator, sdPolicy, nActionsSampledFromPolicy, tConstant = 10, amplitudeDv = 0.1, amplitudePeriodicDv = 1.0, cyclePeriodicDv = 30, agentUseBias = True, policyOptimizer = "Adam", valueFunctionOptimizer = "Adam", learningRatePolicyOptimizer = 1e-3, learningRateValueFunctionOptimizer = 1e-3, weightOnError = 0.5, returnType = "SumOfFiniteRewardSeries", gamma = None, environmentName = "ConcEnvironment"):
        '''
        Constructor
        '''
        
        super(ConcBuildOrder, self).__init__(nIteration, nSeq, nHorizonValueOptimization, nIntervalPolicyOptimization, nBatchPolicyOptimization, nSaveInterval, description)
        
        self.tConstant = tConstant
        self.nHiddenValueApproximator = nHiddenValueApproximator
        self.sdPolicy = sdPolicy
        self.nActionsSampledFromPolicy = nActionsSampledFromPolicy
        self.amplitudeDv = amplitudeDv
        self.amplitudePeriodicDv = amplitudePeriodicDv
        self.cyclePeriodicDv = cyclePeriodicDv
        self.agentUseBias = agentUseBias
        self.learningRatePolicyOptimizer = learningRatePolicyOptimizer 
        self.learningRateValueFunctionOptimizer = learningRateValueFunctionOptimizer
        self.weightOnError = weightOnError        
        self.policyOptimizer = policyOptimizer
        self.valueFunctionOptimizer = valueFunctionOptimizer
        self.returnType = returnType
        self.gamma = gamma
        self.environmentName = environmentName

                
    def toDict(self):
        
        return dict(
            nIteration=self.nIteration,
            nSeq=self.nSeq,
            nHorizonValueOptimization=self.nHorizonValueOptimization,
            nIntervalPolicyOptimization=self.nIntervalPolicyOptimization,
            nBatchPolicyOptimization=self.nBatchPolicyOptimization,
            nSaveInterval=self.nSaveInterval,
            description=self.description,
            tConstant=self.tConstant,
            nHiddenValueApproximator = self.nHiddenValueApproximator,
            sdPolicy = self.sdPolicy,
            nActionsSampledFromPolicy = self.nActionsSampledFromPolicy,
            amplitudeDv = self.amplitudeDv,
            amplitudePeriodicDv = self.amplitudePeriodicDv,
            cyclePeriodicDv = self.cyclePeriodicDv,
            agentUseBias = self.agentUseBias, 
            learningRatePolicyOptimizer = self.learningRatePolicyOptimizer,  
            learningRateValueFunctionOptimizer = self.learningRateValueFunctionOptimizer,
            weightOnError = self.weightOnError,            
            policyOptimizer = self.policyOptimizer,
            valueFunctionOptimizer = self.valueFunctionOptimizer,
            returnType = self.returnType,
            gamma = self.gamma,
            environmentName = self.environmentName, 
            )