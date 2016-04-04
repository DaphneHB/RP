# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 15:05:12 2016

@author: daphnehb
"""

import gestIO as io
import time
import numpy as np
import matplotlib.pyplot as plt
import gestDict as dic

ITERATIONS = 5
LIGN_DEF = 5
LIGN_MIN = 3
LIGN_MAX = 7
PAS = 2
CASE_NOIRE_MIN = 0
CASE_NOIRE_MAX = 10

def time_it(functions, iterations, grid):
    time_log = np.empty((iterations,))
    for i in range(iterations):
        solver = io.Solver(grid, dic.DICTIONNAIRE, random=True)
        start = time.time()
        for f in functions:
            f(solver)
        time_log[i] = time.time() - start
        #print "time({}) = {:4}".format(i, time_log[i])
    return time_log #,np.mean(time_log), np.std(time_log)

def tpsAlgosUneGrid(grid,nbIter=ITERATIONS):
    # on recupere le dictionnaire
    dic.recupDictionnaire()
    tpsFC = []
    tpsFcAc3 = []
    tpsCbj = []
    tpsCbjAc3 = []
    if grid is None:
        grid = io.GrilleMots.genere_grid(LIGN_DEF,LIGN_DEF,CASE_NOIRE_MIN)
    solv = io.Solver(grid, dic.DICTIONNAIRE, random=True)
    # dans tous les cas, on calcule tous les tps
    for i in range(nbIter):
        # pour FC
        dt = time.time()
        solv.run(ac3=False,fc=True)
        ft = time.time()
        tpsFC.append(ft-dt)
        # on clear la grille
        grid.clearAllVariables()
        # pour FC avec AC3
        dt = time.time()
        solv.run(ac3=True,fc=True)
        ft = time.time()
        tpsFcAc3.append(ft-dt)
        # on clear la grille
        grid.clearAllVariables()
        
    return [tpsFC,tpsFcAc3]#,tpsCbj,tpsCbjAc3]

def boxPlotTabs(xlabels,ylabel,data):
    nbLbls = len(xlabels)
    for i in range(nbLbls):
        nbLign = nbLbls/2
        nbCol = nbLbls/nbLign+nbLbls%2
        plt.subplot(nbLign,nbCol,i)
        plt.boxplot(data[i])
    #    plt.title(xlabels[i])
        plt.xlabel(xlabels[i])
    plt.ylabel(ylabel)
    plt.save_fig(io.PLOT_PATH+'algos_diff.png')
    plt.show()
    
def plotsGridLength():
    # on recupere le dictionnaire
    dic.recupDictionnaire()
    tpsFC = []
    tpsFcAc3 = []
    tpsCbj = []
    tpsCbjAc3 = []
    # dans tous les cas, on calcule tous les tps
    for i in range(LIGN_MIN,LIGN_MAX,PAS):
        # recup grille
        grid = io.GrilleMots.genere_grid(i,i,CASE_NOIRE_MIN)
        solv = io.Solver(grid, dic.DICTIONNAIRE, random=True)
        # pour FC
        dt = time.time()
        solv.run(ac3=False,fc=True)
        ft = time.time()
        tpsFC.append(ft-dt)
        # on clear la grille
        grid.clearAllVariables()
        # pour FC avec AC3
        dt = time.time()
        solv.run(ac3=True,fc=True)
        ft = time.time()
        tpsFcAc3.append(ft-dt)
        # on clear la grille
        grid.clearAllVariables()
    
    times = [tpsFC,tpsFcAc3]#,tpsCbj,tpsCbjAc3]
    
    for i in range(len(times)):
        plt.plot(times[i])
    #plt.save_fig(io.PLOT_PATH+'tailles_grid_diff.png')
    # TODO : label tps en fct de la taille de la grille
    #plt.xlabel(np.arange(LIGN_MIN,LIGN_MAX,PAS))
    plt.show()
    
def plotsDiffDicos(grid):
    tpsFC = []
    tpsFcAc3 = []
    tpsCbj = []
    tpsCbjAc3 = []
    # TODO : recup liste dico
    dicos = ["850-mots-us.txt","22600-mots-fr.txt","58000-mots-us.txt","133000-mots-us.txt","135000-mots-fr.txt"]
    if grid is None:
        grid = io.GrilleMots.genere_grid(LIGN_DEF,LIGN_DEF,CASE_NOIRE_MIN)
    # dans tous les cas, on calcule tous les tps
    for d in dicos:
        # recup dicos
        dic.recupDictionnaire([d],clear=True)
        solv = io.Solver(grid, dic.DICTIONNAIRE, random=True)
        # pour FC
        dt = time.time()
        solv.run(ac3=False,fc=True)
        ft = time.time()
        tpsFC.append(ft-dt)
        # on clear la grille
        grid.clearAllVariables()
        # pour FC avec AC3
        dt = time.time()
        solv.run(ac3=True,fc=True)
        ft = time.time()
        tpsFcAc3.append(ft-dt)
        # on clear la grille
        grid.clearAllVariables()
    
    times = [tpsFC,tpsFcAc3]#,tpsCbj,tpsCbjAc3]
    
    for i in range(len(times)):
        plt.plot(times[i])
    #plt.save_fig(io.PLOT_PATH+'tailles_grid_diff.png')
    # TODO : label tps en fct de la taille de la grille
    #plt.xlabel(np.arange(LIGN_MIN,LIGN_MAX,PAS))
    plt.show()

def plotsNoiresDiff():
    dic.recupDictionnaire()
    tpsFC = []
    tpsFcAc3 = []
    tpsCbj = []
    tpsCbjAc3 = []
    # dans tous les cas, on calcule tous les tps
    for noires in range(CASE_NOIRE_MIN,CASE_NOIRE_MAX):
        # recup dicos
        grid = io.GrilleMots.genere_grid(LIGN_DEF,LIGN_DEF,noires)
        solv = io.Solver(grid, dic.DICTIONNAIRE, random=True)
        # pour FC
        dt = time.time()
        solv.run(ac3=False,fc=True)
        ft = time.time()
        tpsFC.append(ft-dt)
        # on clear la grille
        grid.clearAllVariables()
        # pour FC avec AC3
        dt = time.time()
        solv.run(ac3=True,fc=True)
        ft = time.time()
        tpsFcAc3.append(ft-dt)
        # on clear la grille
        grid.clearAllVariables()
    
    times = [tpsFC,tpsFcAc3]#,tpsCbj,tpsCbjAc3]
    
    for i in range(len(times)):
        plt.plot(times[i])
    #plt.save_fig(io.PLOT_PATH+'tailles_grid_diff.png')
    # TODO : label tps en fct de la taille de la grille
    #plt.xlabel(np.arange(LIGN_MIN,LIGN_MAX,PAS))
    plt.show()

### TESTS
# on recupere les 3 grilles exemples
A = io.read_file("grille1.txt")[0]
B = io.read_file("grille2.txt")[0]
C = io.read_file("grille3.txt")[0]

# sauvegarde et affichage des graphes  sur une grille selon l'algo
algos = ['FC sans AC3','FC avec AC3']#,'FC-CBJ sans AC3','FC-CBJ avec AC3']
#times = tpsAlgosUneGrid(A)
#boxPlotTabs(algos,'Temps',times)    

#plotsGridLength()

plotsDiffDicos(A)