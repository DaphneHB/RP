# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 13:30:31 2016

@author: 3200234
"""

import gestDict as dic
import gestIO as io

dic.recupDictionnaire()

grid = io.GrilleMots.genere_grid(5,5,0)
#grid = io.read_file("grille3.txt")[0]
solver = io.Solver(grid, dic.DICTIONNAIRE, random=True)
solver.run(ac3=False, cbj=True, heuristic=3, verbose=1)
print grid.str_writeSolutionFile()
