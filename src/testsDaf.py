# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 13:30:31 2016

@author: 3200234
"""

#import classes as cl
import gestDict as dic
import gestIO as io
#from classes import Solver
import error_tools as err

########### charging the dico
# to charge it multiple dictionnaires
dic.recupDictionnaire()
#dic.recupDictionnaire(["133000-mots-us.txt","850-mots-us.txt"])
#dic.afficheDico()
# to clear the dico
#dic.clearDico()



######### getting the grid
grid = io.read_file("grilles1.txt")[2]
#grid = io.GrilleMots.genere_grid(7,7,4)
grid = io.write_EntryFile("aleatoire7-7-10.txt",[(7,7,10),(7,7,10),(7,7,10)])[0]
grid = io.write_XGridEntryFile("3aleatoire5-5-1.txt",3,(5,5,1))[0]

solv = io.Solver(grid, dic.DICTIONNAIRE,random=True)
#solv.run()
#io.write_SolutionFile("grille1.txt",[grid])
