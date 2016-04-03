# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 13:30:31 2016

@author: 3200234
"""

import gestDict as dic
import gestIO as io

dic.recupDictionnaire()

# grid = io.read_file("grille1.txt")[0]
# solver = io.olver(grid, dic.DICTIONNAIRE)
# print solver.ac3()

grid = io.read_file("grille3.txt")[0]
print grid.variables
solver_x = io.Solver(grid, dic.DICTIONNAIRE, random=True)
#solver_x.ac3()
#solver_x.forwardChecking(first=True)
solver_x.run(ac3=False, verbose=1)
print grid.variables