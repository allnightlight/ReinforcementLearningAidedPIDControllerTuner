'''
Created on 2020/05/05

@author: ukai
'''
from ConcAgent import ConcAgent
from ConcBuildOrder import ConcBuildOrder
from framework import AgentFactory
from ConcEnvironment import ConcEnvironment
from AsmSimulator import AsmSimulator
from AsmAgent import AsmAgent


class ConcAgentFactory(AgentFactory):
    '''
    classdocs
    '''


    def __init__(self):
        super(ConcAgentFactory, self).__init__()

    def create(self, buildOrder):
        assert isinstance(buildOrder, ConcBuildOrder)
        
        if buildOrder.environmentName == "ConcEnvironment":
            return ConcAgent(ConcEnvironment.nMv, buildOrder.sdPolicy, use_bias = buildOrder.agentUseBias)
        
        if buildOrder.environmentName == "AsmSimulator":
            return AsmAgent(AsmSimulator.nMv, buildOrder.sdPolicy, use_bias = buildOrder.agentUseBias)
