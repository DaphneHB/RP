# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 17:10:57 2016

@author: daphnehb
"""
from numpy import ndarray
import sys
import os

# getting the output stream to print thing on
OUT_STREAM = sys.stdout
# se base sur le fait que le fichier est lancé de src
ABS_PATH_PRINC = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

def isString(value):
    return type(value) is str
    
def isList(value):
    return type(value) is list
    
def isTab(value):
    return type(value) is ndarray
    

def deepish_copy(org):
    '''
    much, much faster than deepcopy, for a dict of the simple python types.
    '''
    out = dict().fromkeys(org)
    for k,v in org.iteritems():
        try:
            out[k] = v.copy()   # dicts, sets
        except AttributeError:
            try:
                out[k] = v[:]   # lists, tuples, strings, unicode
            except TypeError:
                out[k] = v      # ints

    return out
    