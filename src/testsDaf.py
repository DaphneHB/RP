# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 13:30:31 2016

@author: 3200234
"""

#import classes as cl
import gestDict as dic
import gestIO as io
import classes as cl
import error_tools as err

########### charging the dico
# to charge it multiple dictionnaires
dic.recupDictionnaire()
#dic.recupDictionnaire(["133000-mots-us.txt","850-mots-us.txt"])
#dic.afficheDico()
# to clear the dico
#dic.clearDico()



######### getting the grid
grid = io.read_file("grille1.txt")[0]
print grid.contraintes
print grid.setVarValue(1,"TRE")
try:
    print grid.setVarValue(5,"TRE")
except err.UnknownVarNbException:
    err.print_err("ERROR")
gr = cl.GrilleMots.genere_grid(5,5,9)
print gr.contraintes

