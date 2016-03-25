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
        
        
########## USEFULL EXCEPTIONS FOR IHM
"""
Exception raised when the tested word length is wrong
"""
class WrongLengthException(Exception):
    def __init__(self, num_var, taille_var):
        self.num_var = num_var
        self.taille_var = taille_var
    
    def __str__(self):
        return repr("Le variable {} attend un mot de taille {}".format(self.num_var,self.taille_var))

"""
Exception raised when the tested word isn't ok for its mutual constraint
"""
class DifferentLetterException(Exception):
    def __init__(self, numX,indX,numY,indY):
        self.numX = numX
        self.numY = numY
        self.indX = indX
        self.indY = indY
    
    def __str__(self):
        return repr("La contrainte X{}[{}]==X{}[{}] n'est pas validée".format(self.numX,self.indX,self.numY,self.indY))

"""
Exception raised when a non-number-variable is tested
"""
class UnknownVarNbException(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr("La variable {} n'existe pas dans cette grille".format(self.value))

"""
Exception raised when trying to put word for different vars
"""
class SimilarWordException(Exception):
    def __init__(self, numX,numY,str_mot):
        self.numX = numX
        self.numY = numY
        self.str_mot = str_mot
    
    def __str__(self):
        return repr("Deux variables dans la grille ne peuvent avoir la même valeur, ici X{}=X{}={}".format(self.numX,self.numY,self.str_mot))

"""
Exception raised when the var num_var already got a string value
"""
class NameAlreadyDefinedException(Exception):
    def __init__(self, num_var, str_var):
        self.num_var = num_var
        self.str_mot = str_var
    
    def __str__(self):
        return repr("La variable {} a déjà une valeur {}".format(self.num_var,self.str_mot))
