'''
Created on 2020/05/02

@author: ukai
'''
from datetime import datetime
import unittest

from MyArray import MyArray
from Utils import Utils
from framework import BuildOrder, Builder, UseCases


class Test(unittest.TestCase):

    def test001(self):

        UseCases().case001()
        
    def test002(self):
        UseCases().case002()
        
    def test003(self):
        datetime.strptime(Utils.generateCurrentDatetimeAsString(), "%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test001']
    unittest.main()