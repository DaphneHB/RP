# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 22:18:40 2016

@author: daphnehb
"""

from classes import *
#import algos
from tools import OUT_STREAM,ABS_PATH_PRINC


GRID_PATH = ABS_PATH_PRINC+"/data/Grilles/"


def read_file(filename) :
    """
    Lit le fichier filename
    et renvoie la liste des grilles y étant
    """
    monfile = None
    try:
        monfile = open(filename,'r')
    except IOError:
        try:
            monfile = open(GRID_PATH+filename,'r')
        except:
            #QtGui.QMessageBox.critical(QtGui.QApplication(),u"Fichier inexistant", u"Le fichier {} n'existe pas et n'est pas dans {}".format(filename,PATH_FILE))
            OUT_STREAM.write("Fichiers {} et {} inexistants".format(filename,PATH_FILE+filename))
            return None
            
    OUT_STREAM.write("\nLe fichier {} existe\n".format(filename))
    line = ""
    # liste des problemes
    # 1 probleme correspondant a un bloc
    blocProb = []
    i=0
    try:
        # tant qu'on est pas à la fin du fichier 0 0
        while line!="0 0" :
            # tant que ce sont des lignes vides
            while line=="" :
                line = monfile.readline().rstrip()
            # la derniere ligne lue n'étant pas vide si ce n'est pas 0 0 (la fin du fichier)
            if line=="0 0" :
                break
            # sinon il s'agit d'encore un bloc à sauvegarder
            # on recupere la taille de la grille du prochain bloc en int
            lignes,colonnes = map(int,(line.split()))
            Mlignes = ""
            for j in range(lignes+1) :
                Mlignes+=monfile.readline()
            # on recupere le probleme correspondant a ce bloc
            #blocProb.append(read_bloc(lignes,colonnes,Mlignes))
            blocProb.append(GrilleMots(Mlignes,lignes,colonnes))
            i += 1
            line = monfile.readline().rstrip()
        # fin tant que
    except ValueError:
        # TODO
        #QtGui.QMessageBox.critical(QtGui.QApplication(),u"Fichier invalide", u"Le fichier {} ne correspond pas à une grille".format(filename))
        OUT_STREAM.write("Fichier {} invalide : ce n'est pas une grille".format(filename))
        monfile.close()
        return blocProb
    monfile.close()
    return blocProb
        
# Lecture du fichier
def selectProb(filename):
    """
    Lit le fichier filename et affiche les grilles y étant enregistrées
    """
    grilles = read_file(filename)
    if grilles is []:
        return None
    # affichage des probleme du fichier filename
    for k in grilles :
        # TODO : not working -> OUT_STREAM.write(k)
        print k
        print k.contraintes