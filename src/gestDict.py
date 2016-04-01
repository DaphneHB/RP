# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 10:50:17 2016

@author: daphnehb
"""

from error_tools import FinProgException
from tools import ABS_PATH_PRINC,OUT_STREAM

DICO_PATH = ABS_PATH_PRINC+"/data/Dicos/"
# DICT_DEF = "850-mots-us.txt"
# DICT_FNAME = "850-mots-us.txt"
DICT_DEF = "133000-mots-us.txt"
DICT_FNAME = "133000-mots-us.txt"
################# LECTURE D'UN FICHIER DICTIONNAIRE ##########

# le dictionnaire de mots utilisé pour lancer l'algo
# de la forme {length : {set de mots de cette length}}
DICTIONNAIRE = dict()

"""
    Lit le fichier filename
    et rempli le dico DICTIONNAIRE contenant tous les mots
"""
def recupDictionnaire(liste_fname=None, clear=True):
    if clear:
        # on vide le dictionnaire courant
        clearDico()
    # si le fichier à charger est le fichier par defaut
    if liste_fname is None or liste_fname==[]:
        remplirDico()
    # sinon on remplit le dico avec tous les nom de fichier de la liste
    else:
        global DICT_FNAME, DICTIONNAIRE
        for name in liste_fname:
            DICT_FNAME = name
            try:
                remplirDico()
            except FinProgException:
                OUT_STREAM.write("Le fichier {} n'a pu etre chargé...\n".format(name))
        #end for
    # end if
    # si aucun fichier n'était valide, le dico reste vide
    if DICTIONNAIRE == {}:
        raise FinProgException(u"Aucun fichier ne correspondait a un dictionnaire.\n")
    # end if

def remplirDico():
    # on récuère le dictionnaire global
    global DICTIONNAIRE

    monfile = None

    filename = DICO_PATH+DICT_FNAME
    try :
        monfile = open(filename,"r")
    except IOError:
        raise FinProgException('Fichier {} inexitant!\n'.format(DICO_PATH+DICT_FNAME))

    OUT_STREAM.write("Récupération du dictionnaire contenu dans {}\n".format(DICO_PATH+DICT_FNAME))
    line = "\n"
    # tant que ce n'est pas la fin du fichier
    while line!="":
        # getting the next word
        line = monfile.readline()
        # tant que ce sont des lignes vides
        while line=="\n":
            line = monfile.readline()
        # si la dernière ligne non vide est la fin du fichier
        if line=="":
            break;
        # removing the last \n
        line = line.rstrip().upper()
        # sinon on recupere la taille du mot
        taille = len(line)
        # on l'ajoute à la liste du dictionnaire correspondante
        if not DICTIONNAIRE.has_key(taille):
            DICTIONNAIRE[taille] = {line}
        else:
            DICTIONNAIRE[taille].add(line)
        # end if
    # end while
    monfile.close()
    # en fonction

def clearDico():
    global DICTIONNAIRE
    DICTIONNAIRE = dict()

def afficheDico():
    global DICTIONNAIRE
    OUT_STREAM.write("\Dictionnaire: \n")
    for t in sorted(DICTIONNAIRE.keys()):
        OUT_STREAM.write("Mots de taille {} : \n\t{}\n".format(t,DICTIONNAIRE[t]))
    # end for
    # end
