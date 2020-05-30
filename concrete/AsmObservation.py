'''
Created on 2020/05/27

@author: ukai
'''
from ConcObservation import ConcObservation

class AsmObservation(ConcObservation):
    '''
    classdocs
    '''


    def __init__(self, e, S_NH4, SvNh4):
        '''
        Constructor
        '''
        
        super(AsmObservation, self).__init__(e)
        
        self.S_NH4 = S_NH4 # (,)
        self.SvNh4 = SvNh4 # (,)
        