from datetime import datetime
import random
import string

from MyArray import MyArray
import numpy as np


class Utils(object):

    @classmethod
    def generateRandomString(cls, length):
        
        randomString = "".join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=length))
        
        return randomString        
        

    @classmethod
    def myRandomRrandint(cls, nLow, nHigh, nSize):
        
        return np.random.randint(low=nLow, high=nHigh, size=nSize) # (*,)

    @classmethod
    def generateCurrentDatetimeAsString(cls):
        return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
