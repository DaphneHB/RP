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

ITERATIONS = 50
LIGN_DEF = 5
LIGN_MIN = 3
LIGN_MAX = 7
PAS = 2
CASE_NOIRE_MIN = 0
CASE_NOIRE_MAX = 10

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
        # pour CBJ
        dt = time.time()
        solv.run(ac3=False,cbj=True)
        ft = time.time()
        tpsCbj.append(ft-dt)
        # on clear la grille
        grid.clearAllVariables()
        # pour CBJ avec ac3
        dt = time.time()
        solv.run(ac3=True,cbj=True)
        ft = time.time()
        tpsCbjAc3.append(ft-dt)
        # on clear la grille
        grid.clearAllVariables()
        
    return [tpsFC,tpsFcAc3,tpsCbj,tpsCbjAc3]

def boxPlotTabs(xlabels,ylabel,data,title):
    nbLbls = len(xlabels)
    for i in range(1,nbLbls+1):
        nbLign = nbLbls/2
        nbCol = nbLbls/nbLign+nbLbls%2
        plt.subplot(nbLign,nbCol,i)
        plt.boxplot(data[i-1])
    #    plt.title(xlabels[i])
        plt.xlabel(xlabels[i-1])
    plt.ylabel(ylabel)
    plt.savefig(io.PLOT_PATH+'algos_diff_'+title+'.png')
    #plt.show()
    plt.close()
    
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
        # pour CBJ
        dt = time.time()
        solv.run(ac3=False,cbj=True)
        ft = time.time()
        tpsCbj.append(ft-dt)
        # on clear la grille
        grid.clearAllVariables()
        # pour CBJ avec ac3
        dt = time.time()
        solv.run(ac3=True,cbj=True)
        ft = time.time()
        tpsCbjAc3.append(ft-dt)
        # on clear la grille
        grid.clearAllVariables()
        
    
    times = [tpsFC,tpsFcAc3,tpsCbj,tpsCbjAc3]
    
    for i in range(len(times)):
        plt.plot(times[i])
    #plt.save_fig(io.PLOT_PATH+'tailles_grid_diff.png')
    # TODO : label tps en fct de la taille de la grille
    #plt.xlabel(np.arange(LIGN_MIN,LIGN_MAX,PAS))
    #plt.show()
    plt.close()
    
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
        # pour CBJ
        dt = time.time()
        solv.run(ac3=False,cbj=True)
        ft = time.time()
        tpsCbj.append(ft-dt)
        # on clear la grille
        grid.clearAllVariables()
        # pour CBJ avec ac3
        dt = time.time()
        solv.run(ac3=True,cbj=True)
        ft = time.time()
        tpsCbjAc3.append(ft-dt)
        # on clear la grille
        grid.clearAllVariables()
    times = [tpsFC,tpsFcAc3,tpsCbj,tpsCbjAc3]
    
    for i in range(len(times)):
        plt.plot(times[i])
    plt.save_fig(io.PLOT_PATH+'tailles_grid_diff.png')
    # TODO : label tps en fct de la taille de la grille
    #plt.xlabel(np.arange(LIGN_MIN,LIGN_MAX,PAS))
    #plt.show()
    plt.close()
    
def plotsNoiresDiff():
    dic.recupDictionnaire()
    tpsFC = []
    tpsFcAc3 = []
    tpsCbj = []
    tpsCbjAc3 = []
    taille = LIGN_DEF
    # dans tous les cas, on calcule tous les tps
    for noires in range(CASE_NOIRE_MIN,taille*taille):
        # recup dicos
        grid = io.GrilleMots.genere_grid(taille,taille,noires)
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
        # pour CBJ
        dt = time.time()
        solv.run(ac3=False,cbj=True)
        ft = time.time()
        tpsCbj.append(ft-dt)
        # on clear la grille
        grid.clearAllVariables()
        # pour CBJ avec ac3
        dt = time.time()
        solv.run(ac3=True,cbj=True)
        ft = time.time()
        tpsCbjAc3.append(ft-dt)
        # on clear la grille
        grid.clearAllVariables()
    
    times = [tpsFC,tpsFcAc3,tpsCbj,tpsCbjAc3]
    
    for i in range(len(times)):
        plt.plot(times[i])
    plt.save_fig(io.PLOT_PATH+'var_nb_cases_noires.png')
    # TODO : label tps en fct de la taille de la grille
    #plt.xlabel(np.arange(LIGN_MIN,LIGN_MAX,PAS))
    #plt.show()
    plt.close()

### TESTS
# on recupere les 3 grilles exemples
A = io.read_file("grille1.txt")[0]
B = io.read_file("grille2.txt")[0]
C = io.read_file("grille3.txt")[0]

# sauvegarde et affichage des graphes  sur une grille selon l'algo
algos = ['FC sans AC3','FC avec AC3','FC-CBJ sans AC3','FC-CBJ avec AC3']

# pour comparer les differents algos sur une meme instance
# grille A
times = tpsAlgosUneGrid(A)
boxPlotTabs(algos,'Temps',times,"grilleA")
# grille B
times = tpsAlgosUneGrid(B)
boxPlotTabs(algos,'Temps',times,"grilleB")
# grille C
times = tpsAlgosUneGrid(C)
boxPlotTabs(algos,'Temps',times,"grilleC")

# pour comparer selon des tailles de grilles differerentes
plotsGridLength()

# pour comparer selon des tailles de dicos
plotsDiffDicos(A)

# pour comparer selon le nombre de cases noires pour une grille fixee
plotsNoiresDiff()