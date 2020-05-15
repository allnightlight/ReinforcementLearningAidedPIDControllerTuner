'''
Created on 2020/05/05

@author: ukai
'''
from ConcPolicyOptimizer import ConcPolicyOptimizer
from ConcValueFunctionOptimizer import ConcValueFunctionOptimizer
from framework import TrainerFactory, ClosedLoopSimulator, Trainer


class ConcTrainerFactory(TrainerFactory):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        super(ConcTrainerFactory, self).__init__()
        
    def create(self, agent, environment, valueFunctionApproximator, rewardGiver, buildOrder):
        closedLoopSimulator = ClosedLoopSimulator(environment, agent, buildOrder.getnSeq())
        valueFunctionOptimizer = ConcValueFunctionOptimizer(valueFunctionApproximator, agent, buildOrder.getnHorizonValueOptimization())
        policyOptimizer = ConcPolicyOptimizer(agent, valueFunctionApproximator, buildOrder.getnIntervalPolicyOptimization(), buildOrder.getnBatchPolicyOptimization())
        return Trainer(closedLoopSimulator, valueFunctionOptimizer, policyOptimizer, rewardGiver, buildOrder.getnIteration(), buildOrder.getnSaveInterval())
