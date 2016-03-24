# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:04:04 2016

@author: daphnehb
"""

import sys

"""
Write a message on the error stream of the system
"""
def print_err(str_error):
    sys.stderr.write(str_error+"\n")
    
"""
Exception raised for any launching error that occured
"""
class FinProgException(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)