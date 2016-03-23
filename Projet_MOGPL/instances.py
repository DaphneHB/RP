# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 23:51:51 2015

@author: daphne
"""

from gestIO import *
import numpy as np
import matplotlib.pyplot as plt

N_MIN = 10
N_MAX = 50
N_STEP = 10

N_FIX = 20
NB_OBST_MIN = 10
NB_OBST_MAX = 50
NB_OBST_STEP = 10

def instances_questC(filename,nbInst, N) :
    """
    Creation du fichier contenant les instances entree des problemes
    Permet de tester l'influence de la taille de la grille
    NbInst instances de problemes avec comme plus petit probleme N=M=10
    """
    listTuple = list()
    for i in range(1,nbInst+1):
        listTuple.append((N,N,N))
    write_EntryFile(filename,listTuple)


def instances_questD(filename,nbInst,nbObst) :
    """
    Creation du fichier contenant les instances entree des problemes
    Permet de tester l'influence du nombre d'obstacles dans la grille
    NbInst instances de problemes avec comme plus petit probleme N=M=10
    """
    if (nbObst>N_FIX*N_FIX):
        raise(ValueError(nbObst))
    listTuple = list()
    for i in range(1,nbInst+1):
        listTuple.append((N_FIX,N_FIX,nbObst))

    write_EntryFile(filename,listTuple)


def resQC(N, nbInst) :
    """
    Essai numérique de l'algo en fct de la taille
    Fichier entree: EntreesQuestC.txt
    Retourne la moyenne des tps d'execution pour cett tail
    """
    strFile = "EntreesQuestC"+str(N)+".txt"
    # on genere aleatoirement les nbInst problemes dans strFile
    instances_questC(strFile,nbInst,N)
    # onn recupere la liste de probleme a resoudre
    probsC = read_file(strFile)
    # on resout les problemes et on genere le fichier resultat
    tps = write_SolutionFile(strFile,probsC)
    # renvoie la moyenne des tps de resolutions
    if tps is None:
        print (u"Il y a eu une erreur. Aucun temps n'a pu être calculé.")
        return None
    tps = np.array(tps)
    return tps.mean()



def resQD(nbObst,nbInst) :
    """
    Essai numérique de l'algo en fct du nb d'obstacles
    Fichier entree: EntreesQuestD.txt
    """
    strFile = "EntreesQuestD"+str(nbObst)+".txt"
    # on genere aleatoirement les nbInst problemes dans strFile
    instances_questD(strFile,nbInst,nbObst)
    # onn recupere la liste de probleme a resoudre
    probsD = read_file(strFile)
    # on resout les problemes et on genere le fichier resultat
    tps = write_SolutionFile(strFile,probsD)
    # renvoie la moyenne des tps de resolutions
    if tps is None:
        print (u"Il y a eu une erreur. Aucun temps n'a pu être calculé.")
        return None
    tps = np.array(tps)
    return tps.mean()
    
def questionC(nbInst):
    """
    Affiche et sauvegarde le plot des temps moyens d'execution
    avec nbInst iteration pour N=M=10,20,30,40,50
    """
    rangeN = range(N_MIN,N_MAX+N_STEP,N_STEP)
    listTps =  list()
    for N in rangeN:
        tps = resQC(N, nbInst)
        if not tps is None:
            listTps.append(tps)
    if listTps == []:
        return None
    tabTps = np.array(listTps)
    
    plt.plot(rangeN,tabTps,'ro-')
    # on donne un titre
    plt.title("Temps en fonction de N")
    # on attribut des labels au axes
    plt.xlabel("Taille de la grille (N,N=M)")
    plt.ylabel("Temps d'execution (secondes)")
    plt.grid()
    # on sauvegarde la figure dans un dossier plot
    plt.savefig("Plots/plotQuestC.png")
    plt.show()
    
        
def questionD(nbInst):
    """
    Affiche et sauvegarde le plot des temps moyens d'execution
    avec nbInst iteration pour N=M=20
    et nbObstacles=10,20,30,40,50
    """
    rangeNbO = range(NB_OBST_MIN,NB_OBST_MAX+NB_OBST_STEP,NB_OBST_STEP)
    listTps =  list()
    for nbObst in rangeNbO:
        tps = resQD(nbObst, nbInst)
        if not tps is None:
            listTps.append(tps)
    if listTps == []:
        print (u"Aucun plot généré")
        return None
    tabTps = np.array(listTps)
    plt.plot(rangeNbO,tabTps,'gD-')
    # on donne un titre
    plt.title("Temps en fonction du nombre d'obstacle avec N=M=20")
    # on attribut des labels au axes
    plt.xlabel("Nombre d'obstacles")
    plt.ylabel("Temps d'execution (secondes)")
    plt.grid()
    # on sauvegarde la figure dans un dossier plot
    plt.savefig("Plots/plotQuestD.png")
    plt.show()