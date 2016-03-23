# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 12:55:22 2016

@author: ppti
"""

import numpy as np
from enum import Enum  

class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class GrilleMots:
    
    def __init__(self,str_grille, nbLignes, nbCols):
        self.height = nbLignes
        self.width = nbCols
        self.grille = str_grille
        self.nbMots = 0
        # un dictionnaire tuple {numX: ((x,y),taille,orientation,valeur)}
        self.variables = dict()
        self.contraintes = Contraintes()
        #self.constructGrille()
        
        
    def constructGrille(self):
        str_grille = self._grille.split()
        # on convertit la liste de string en liste d'int
        try:
            str_grille = map(int,str_grille)
        except ValueError:
            print "Grille non valide"
        #on recupere le tableau correspondant et aux bonnes dimensions
        self.grille = grille = np.asarray(str_grille).reshape((self.height,self.width))
        # si la case precedente etait un zero ou on est passé a la ligne -> nouveau mot
        nouvMot = True
        numMot = 1
        tailleMot = 0
        ### on itere dans un sens: les mots en ligne
        for i in range(self.height):
            nouvMot = True
            tailleMot = 0
            for j in range(self.width):
                if grille[i,j]==1:
                    nouvMot = True
                    continue
                else:
                    # si c'est un nouveau mot, on ecrase la taille precedente
                    # et si ce n'est pas le premier mot (donc que la taille est non nulle, ie il y a un mot)
                    if nouvMot and tailleMot!=0:
                        self.enregistreNouvMot(i,j,numMot,tailleMot,Orientation.HORIZONTAL)
                        # on remet la taille du mot a 0
                        tailleMot = 0
                        # on passe au mot suivant:
                        numMot += 1
                    # end if
                    # si c'est le premier mot
                    # ou apres avoir stocké le mot precedent : on continue
                    # numLettre = len actuelle du mot
                    tailleMot+=1
                    nouvMot = False
                # end if
            #end for
        #end for
        ### on enregistre le dernier mot de sortie de boucle
        self.enregistreNouvMot(i,j,numMot,tailleMot,Orientation.HORIZONTAL)
        # on remet la taille du mot a 0
        tailleMot = 0
        # on passe au mot suivant:
        numMot += 1
        ### on itere dans l'autre sens: les mots en colonne
        for j in range(self.width):
            nouvMot = True
            tailleMot = 0
            for i in range(self.height):
                if grille[i,j]==1:
                    nouvMot = True
                    continue
                else:
                    # si c'est un nouveau mot, on ecrase la taille precedente
                    # et si ce n'est pas le premier mot (donc que la taille est non nulle, ie il y a un mot)
                    if nouvMot and tailleMot!=0:
                        self.enregistreNouvMot(i,j,numMot,tailleMot,Orientation.VERTICAL)
                        # on remet la taille du mot a 0
                        tailleMot = 0
                        # on passe au mot suivant:
                        numMot += 1
                    # end if
                    # si c'est le premier mot
                    # ou apres avoir stocké le mot precedent : on continue
                    # numLettre = len actuelle du mot
                    tailleMot+=1
                    nouvMot = False
                # end if
            #end for
        #end for
        ### on enregistre le dernier mot de sortie de boucle
        self.enregistreNouvMot(i,j,numMot,tailleMot,Orientation.VERTICAL)

        
    """
    Enregistre le mot numMot de taille tailleMot et ajoute la contrainte correspondante
    """
    def enregistreNouvMot(self,x,y,numMot,tailleMot,orientMot):
        # on ajoute la contrainte taille du mot
        self.contraintes.addLengthConstraint(numMot,tailleMot)
        # on crée le tableau de taille tailleMot à l'indice numMot-1: représentera le mot
        # on ajoute la variable aux autres
        var = ((x,y),tailleMot,orientMot,None)
        self.variables.update({numMot:var})
        # on incremente le nombre de mots
        self.nbMots += 1
        
    
    """
    Vérifie que ce mot est imaginable pour le mot numMot
    """
    def verifyMot(self,str_mot,numMot):
        return self.contraintes.isLengthVerified(numMot,len(str_mot)) and self.contraintes.areLettersVerified(numMot,str_mot,self.mots)
    
        
class Contraintes:
    
    def __init__(self, nbLignes,nbColonnes):
        # un dictionnaire tuple {numX: ((num varX,indX), (num autre varY,indY))}
        self.valeurCommuneVars = dict()
        # pour les contraintes de tailles
        # a chaque indices -> un int correspondant a la taille max de la var au num de l'ind
        self.tailleFixeVars = list()
        self.matrixConst = ContrainteMatrix(nbLignes,nbColonnes)
    
    def isConstraintVerified(self,num_var,str_mot,mots):
        return self.isLengthVerified(num_var,len(str_mot)) and self.areLettersVerified(num_var,str_mot,mots)
    
    def isLengthVerified(self,num_var,length):
        return self.tailleFixeVars[num_var]==length
        
    def areLettersVerified(self,num_var,str_mot,mots):
        pass
        
    def addLengthConstraint(self,num_var,length):
        self.tailleFixeVars[num_var] = length
    
    def addCommonIndexConstraint(self,num_varX, indX, num_varY,indY):
        self.valeurCommuneVars.append((num_varX,indX,num_varY,indY))
        

class ContrainteMatrix:
    
    def __init__(self, nbLignes, nbColonnes):
        # la matrice grille
        self.matrix = [[ None for x in range(nbColonnes)] for y in range(nbLignes)]
        
    def __str__(self):
        string = ""
        for lign in self.matrix:
            for val in lign:
                if val is None:
                    string = string+"None  "
                else:
                    string = string+val+"  "
            string+="\n"
        return string