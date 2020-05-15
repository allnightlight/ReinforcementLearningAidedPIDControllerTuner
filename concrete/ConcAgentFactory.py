'''
Created on 2020/05/05

@author: ukai
'''
from ConcAgent import ConcAgent
from ConcBuildOrder import ConcBuildOrder
from framework import AgentFactory


class ConcAgentFactory(AgentFactory):
    '''
    classdocs
    '''


    def __init__(self):
        super(ConcAgentFactory, self).__init__()

    def create(self, buildOrder):
        assert isinstance(buildOrder, ConcBuildOrder)
        
        return ConcAgent(buildOrder.getnLevers())