# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 17:23:58 2015

@author: daphne
"""

from classes import *
#import algos
import os


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