# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 17:23:58 2015

@author: daphne
"""

from classes import *
import algos
import os

PATH_FILE = "./Grille/"
################# LECTURE D'UN FICHIER ##########
# on fait confiance à l'utilisateur: le fichier est conforme au format attendu
def read_bloc(M,N, Mlignes) :
    """
    Lecture du fichier contenant les données dun problème
    
    """
    obstacles = Obstacles()
    # on construit la grille de taille M*N
    grille = np.zeros((M,N),int)
    # on remplit la grille
    for i in range(M) :
        grille[i] = np.array(map(int,Mlignes[i].split()))
        # on ajoute les obstacles au probleme
        for j in range(N):
            if (grille[i][j]==1):
                obstacles.addObstacle(i,j)
            # end if
        # end for j
    # end for i
    # on recupere les points de depart et d'arrive ainsi que l'orientation initiale
    XD, YD, XA, YA, o = Mlignes[M].split()
    pointDep = (int(XD),int(YD))
    pointArr = (int(XA),int(YA))
    orient = Orientations[o]
    
    # (grille, point_depart, point_arrivee, orientation)
    prob = Problem(grille, pointDep,pointArr,orient,obstacles)
    return prob

def read_file(filename) :
    """
    Lit le fichier filename
    et renvoie la liste des problemes y étant
    """
    monfile = None
    try:
        monfile = open(filename,'r')
    except IOError:
        try:
            monfile = open(PATH_FILE+filename,'r')
        except:
            #QtGui.QMessageBox.critical(QtGui.QApplication(),u"Fichier inexistant", u"Le fichier {} n'existe pas et n'est pas dans {}".format(filename,PATH_FILE))
            print "Fichiers {} et {} inexistants".format(filename,PATH_FILE+filename)
            return None
            
    print "File {} exite".format(filename)
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
            M,N = map(int,(line.split()))
            Mlignes = []
            for j in range(M+1) :
                Mlignes.append(monfile.readline().rstrip())
            # on recupere le probleme correspondant a ce bloc
            blocProb.append(read_bloc(M,N,Mlignes))
            i += 1
            line = monfile.readline().rstrip()
        # fin tant que
    except ValueError:
        # TODO
        #QtGui.QMessageBox.critical(QtGui.QApplication(),u"Fichier invalide", u"Le fichier {} ne correspond pas à une grille".format(filename))
        print "Fichier {} invalide : ce n'est pas une grille".format(filename)
        return None
    return blocProb
        
# Lecture du fichier
def selctProb(filename):
    """
    Lit le fichier filename et affiche les probleme y étant
    """
    probs = read_file(filename)
    if probs is None:
        return None
    # affichage des probleme du fichier filename
    for k in probs :
        print k

################# ECRITURE D'UN PROBLEME DANS UN FICHIER ##########
    
def write_EntryFile(filename,listeTuple, pathOk = False) :
    """
    Genere autant de problemes qu'il y a de tuple dans la liste
    et les ecrit dans un fichier filename écrasé
    """
    
    if not os.path.exists(PATH_FILE) and not pathOk: 
        os.makedirs(PATH_FILE) 

    path = PATH_FILE+""+filename if not pathOk else filename
    # on ecrase le precedent contenu du fichier
    with open(path,'w') as monfile:
        for tuplet in listeTuple :
            # on genere le probleme correspondant
            M,N,nb = tuplet
            prob = Problem.genere_prob(M,N,nb)
            # on ajoute son affichage file au file en question
            monfile.write(prob.str_writeEntryFile())
    
        # on declare la fin du fichier
        monfile.write("\n0 0")
        
def write_ProblemFile(filename,prob,pathOk=False) :
    """
    Genere autant de problemes qu'il y a de tuple dans la liste
    et les ecrit dans un fichier filename écrasé
    """
    if not os.path.exists(PATH_FILE) and not pathOk: 
        os.makedirs(PATH_FILE) 

    path = PATH_FILE+""+filename if not pathOk else filename
    # on ecrase le precedent contenu du fichier
    monfile = None
    try:
        monfile = open(path,'w')
    except:
        try:
            monfile = open(filename,'w')
        except:
            print "Nom de fichier ou arborescence choisie invalide\nVeuillez essayer de sauvegarder le fichier avant tout"
            return None

    # on ajoute son affichage file au file en question
    monfile.write(prob.str_writeEntryFile())

    # on declare la fin du fichier
    monfile.write("\n0 0")
    monfile.close()

################# ECRITURE DE LA SOLUTION D'UN PROBLEME DANS UN FICHIER ##########
    
def write_SolutionFile(filename,problemes,pathOk=False) :
    """
    Prend un liste de probleme en parametre
    Genere autant de bloc solution que de problemes s'il n'y en a pas deja
    et les ecrit dans un fichier solution_filename écrasé
    Renvoie la liste des temps d'execution de la resolution pour chaque probleme
    """
    tabTps = list()
    if not os.path.exists(PATH_FILE) and not pathOk: 
        os.makedirs(PATH_FILE) 

    path = PATH_FILE+"solution_"+filename if not pathOk else filename
    # on ecrase le precedent contenu du fichier
    monfile = None
    try:
        monfile = open(path,'w')
    except:
        try:
            monfile = open("solution_"+filename,'w')
        except:
            print "Nom de fichier ou arborescence choisie invalide\nVeuillez essayer de sauvegarder le fichier avant tout"
            return None
    if problemes is None:
        return None
        
    for prob in problemes :
        # si la solution du probleme n'a pas deja eté générée            
        if prob.solutionFile is None:
            # on lance la resolution du probleme correspondant
            algos.Algorithm(prob)
        # on ajoute son affichage file au file en question
        monfile.write(prob.str_writeSolutionFile())
        tabTps.append(prob.tpsSolution)
        # fin du fichier
        monfile.write("\n")
    # end for
    monfile.close()    
    return tabTps