# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 17:10:57 2016

@author: daphnehb
"""
from numpy import ndarray

def isString(value):
    return type(value) is str
    
def isList(value):
    return type(value) is list
    
def isTab(value):
    return type(value) is ndarray
    
isTab([])