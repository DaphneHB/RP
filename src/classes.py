# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 12:55:22 2016

@author: ppti
"""

import numpy as np
import random
from enum import Enum
import tools
import error_tools as err

class Orientation(Enum):
    """
    Enumération des orientation possible d'un mot (en ligne:horizontal ou en colonne:vertical)

    """
    HORIZONTAL = 0
    VERTICAL = 1

    def __str__(self):
        return str(self.name)


class GrilleMots:

    def __init__(self,grille, nbLignes, nbCols):
        self.height = nbLignes
        self.width = nbCols
        self.nbMots = 0
        # un dictionnaire de listes {numX: [(numLigne,numColonne),taille,orientation,valeur]}
        # où (numLigne,numColonne) sont les coordonnees du début du mot
        self.variables = dict()
        # on crée l'objet contrainte, lui indiquant qu'il y a nbMots Mots
        self.contraintes = Contraintes(self.height,self.width)
        self.solution = False
        # récupération de la grille suivant son type
        # la grille en int np.ndarray sera alors enregistrée dans self.grille
        # et la string dans self.str_grille
        self.recupGrid(grille)
        self.constructGrille()


    def recupGrid(self, grille):
        # si c'est une liste de string
        if tools.isList(grille):
            grille = ''.join(grille)
        # si la grille donnée au constructeur est une string
        if tools.isString(grille):
            self.str_grille = grille
            str_grille = grille.split()
            # on convertit la liste de string en liste d'int
            try:
                str_grille = map(int,str_grille)
            except (ValueError, TypeError):
                print "Grille non valide"
            #on recupere le tableau correspondant et aux bonnes dimensions
            self.grille = np.asarray(str_grille).reshape((self.height,self.width))
        elif tools.isTab(grille):
            # on fait de la grille une liste de liste
            griList = map(list,list(grille))
            # on la transforme en liste de string
            griList = map(lambda x:' '.join(map(lambda y:" ".join(str(y)),x)),griList)
            self.str_grille = '\n'.join(griList)
            self.grille = grille
        else:
            raise err.FinProgException("La grille a mal ete lue")

    def constructGrille(self):
        grille = self.grille
        nouvMot = True
        numMot = 1
        tailleMot = 0
        iMot = jMot = 0
        self.horiz_var = dict()
        self.vertic_var = dict()
        ### on itere dans un sens: les mots en ligne
        for i in range(self.height):
            nouvMot = True
            for j in range(self.width):
                # case noire
                if grille[i,j]==1:
                    # si la case precedente etait un un ou on est passé a la ligne -> nouveau mot
                    nouvMot = True
                    continue
                elif grille[i,j]==0: # case blanche
                    # si c'est un nouveau mot, on ecrase la taille precedente
                    # et si ce n'est pas le premier mot (donc que la taille est non nulle, ie il y a un mot)
                    if nouvMot and tailleMot!=0:
                        self.enregistreNouvMot(iMot,jMot,numMot,tailleMot,Orientation.HORIZONTAL)
                        # on remet la taille du mot a 0
                        tailleMot = 0
                        iMot = i
                        jMot = j
                        # on passe au mot suivant:
                        numMot += 1
                    # si la taille est a 0 le debut du mot est a marquer
                    elif tailleMot==0:
                        iMot = i
                        jMot = j
                    # end if
                    # si c'est le premier mot
                    # ou apres avoir stocké le mot precedent : on continue
                    # numLettre = len actuelle du mot
                    tailleMot+=1
                    nouvMot = False
                # end if
            #end for
        #end for
        ### on enregistre le dernier mot de sortie de boucle s'il existe
        if tailleMot!=0:
            self.enregistreNouvMot(iMot,jMot,numMot,tailleMot,Orientation.HORIZONTAL)
        # on remet la taille du mot a 0
        tailleMot = 0
        # on passe au mot suivant:
        numMot += 1
        ### on itere dans l'autre sens: les mots en colonne
        for j in range(self.width):
            nouvMot = True
            for i in range(self.height):
                if grille[i,j]==1:
                    nouvMot = True
                    continue
                elif grille[i,j]==0:
                    # si c'est un nouveau mot, on ecrase la taille precedente
                    # et si ce n'est pas le premier mot (donc que la taille est non nulle, ie il y a un mot)
                    if nouvMot and tailleMot!=0:
                        self.enregistreNouvMot(iMot,jMot,numMot,tailleMot,Orientation.VERTICAL)
                        # on remet la taille du mot a 0
                        tailleMot = 0
                        iMot = i
                        jMot = j
                        # on passe au mot suivant:
                        numMot += 1
                    # si la taille est a 0 le debut du mot est a marquer
                    elif tailleMot==0:
                        iMot = i
                        jMot = j
                    # end if
                    # si c'est le premier mot
                    # ou apres avoir stocké le mot precedent : on continue
                    # numLettre = len actuelle du mot
                    tailleMot+=1
                    nouvMot = False
                # end if
            #end for
        #end for
        ### on enregistre le dernier mot de sortie de boucle s'il existe
        if tailleMot!=0:
            self.enregistreNouvMot(iMot,jMot,numMot,tailleMot,Orientation.VERTICAL)
        ## on recupere les contraintes de croisement de toutes les variables
        self.buildConstraints()

    """
    Enregistre le mot numMot de taille tailleMot et ajoute la contrainte correspondante
    """
    def enregistreNouvMot(self,x,y,numMot,tailleMot,orientMot):
        # on ajoute la contrainte taille du mot
        self.contraintes.addLengthConstraint(numMot,tailleMot)
        # on crée le tableau de taille tailleMot à l'indice numMot-1: représentera le mot
        # on ajoute la variable aux autres
        var = [(x,y),tailleMot,orientMot,None]
        self.variables.update({numMot:var})
        if orientMot is Orientation.HORIZONTAL:
            self.horiz_var.update({numMot:var})
        else:
            self.vertic_var.update({numMot:var})
        # on incremente le nombre de mots
        self.nbMots += 1

    def buildConstraints(self):
        # pour chaque variable on sauvegarde les contraintes qui lui sont liées
        # les variables horizontales ne croisant que les variables verticales et inversement
        # il n'est besoin que de regarder dans toutes leur longueur que les variables dans un sens (ici Horizontales)
        for numH,varH in self.horiz_var.iteritems():
            iH,jH = varH[0]
            lenH = varH[1]
            for numV,varV in self.vertic_var.iteritems():
                iV,jV = varV[0]
                lenV = varV[1]
                # si les mots se croisent
                if iH in range(iV,iV+lenV) and jV in range(jH,jH+lenH):
                    # croisement au point (iH,jV) de la matrice grille
                    # => (jV-jH) ème lettre de numH et (iH-iV)ème lettre de numV
                    indH = jV-jH
                    indV = iH-iV
                    self.contraintes.addCommonIndexConstraint(numH,indH,numV,indV)
                    self.contraintes.addCommonIndexConstraint(numV,indV,numH,indH)
                # end if
            # end for
        # end for
        #end

    """
    Vérifie que ce mot est imaginable pour le mot numMot
    """
    def verifyMot(self,numVar,str_mot):
        if self.variables.has_key(numVar) :
            if self.variables[numVar][3] is None:
                return self.contraintes.areConstraintsVerified(numVar,str_mot,self.variables)
            else :
                raise err.NameAlreadyDefinedException(numVar,self.variables[numVar][3])
        else:
            raise err.UnknownVarNbException(numVar)

    def setVarValue(self,numVar,str_mot):
        if self.verifyMot(numVar,str_mot):
            self.variables[numVar][3] = str_mot
            return True
        else:
            return False

    def recupSolution(self):
        pass

    def __str__(self):
        print self.str_grille
        string = "Grille {}*{} avec {} mots\n".format(self.height,self.width,self.nbMots)

        # pour chaque variable on affiche ses caracteristiques
        #for num,val in self.variables.iteritems():
        #    string+= "\tMot {} commençant en {}, avec {} lettres et en direction {}\n".format(num,val[0],val[1],val[2])
        return str(string)

    def str_writeEntryFile(self):
        string = "\n{} {}\n".format(self.height,self.width)
        string+=self.str_grille+"\n"
        return string

    def str_writeSolutionFile(self):
        matrix = np.empty([self.height, self.width], dtype="S1")
        # on initialise la matrice à # -> case noire partout
        matrix[:] = "#"
        # fichier solution au format
        # taille grille lignes*colonnes
        # nbVars contenues dans la grille
        # grille de lettres et de # pour les cases noires
        string = "\nSize: {}, {}".format(self.height,self.width)
        string += "\n{} words\n".format(self.nbMots)
        # pour chaque variable horizontale
        # on place les lettres correspondantes
        for num,((iv,jv),taille,orient,val) in self.variables.items():
            # si la variable est verticale on arrete
            if orient==Orientation.VERTICAL:
                break
            # on ecrit lettre par lettre la valeur en string de la variable
            for ind in range(taille):
                # TODO : cas inimaginable?!
                if val is None:
                    matrix[iv][jv+ind]="_"
                    continue
                matrix[iv][jv+ind] = val[ind]
                # end if
            # end for
             # end if
        # end for
        string+="\n".join([" ".join(x) for x in matrix])
        string+="\n"
        return string

    def fillGrid(self, instance):
        for numVar, str_mot in instance.items():
            self.setVarValue(numVar,str_mot)

    def clearAllVariables(self):
        for num,var in self.variables.items():
            var[3] = None
        self.solution = False

    """
    To backtrack a value defined for a var
    For the algo to change his mind
    """
    def backValueVar(self,numVar,otherVal):
        val = self.variables[numVar]
        if val[3]==otherVal:
            raise err.NameAlreadyDefinedException(numVar,otherVal)
        else:
            val[3] = otherVal

    ##################### GENERATION ALEATOIRE D'UNE GRILLE #################
    @staticmethod
    def genere_grid(lignes,colonnes,nbCasesNoires) :
        """
        Genere aléatoirement une grille avec nbCasesNoires
        et de taille lignes*colonnes
        """
         # on genere la grille  de zeros
        grille = np.zeros((lignes,colonnes), int)
        # on place les cases noires
        if nbCasesNoires>=lignes*colonnes :
            print("ERREUR : {} cases noires ≥ {} (taille de la grille)".format(nbCasesNoires,lignes*colonnes))
            return None
        for i in range(nbCasesNoires) :
            # tant qu'aucun x, y n'est valide
            while True :
                x = random.randint(0,lignes-1)
                y = random.randint(0,colonnes-1)
                if (grille[x][y]!=1) :
                    # si ce x, y sont valides
                    # on assigne un nouvel obstacle a la grille
                    grille[x][y] = 1
                    break;
        grille_mots = GrilleMots(grille,lignes,colonnes)
        return grille_mots

class Contraintes:

    def __init__(self, nbLignes,nbColonnes):
        # un dictionnaire de dict {numX: {numVarY : (indX,indY), numVarZ : (indX,indZ)}}
        self.valeurCommuneVars = dict()
        # pour les contraintes de tailles
        # a chaque indices -> un int correspondant a la taille max de la var au num de l'ind
        # dico car accès en O(1)
        self.tailleFixeVars = dict()
        #self.matrixConst = ContrainteMatrix(nbLignes,nbColonnes)
        self.intersectIndexes = dict()

    def areConstraintsVerified(self,num_var,str_mot,variables):
        if not self.tailleFixeVars.has_key(num_var):
            raise err.UnknownVarNbException(num_var)
        return self.isLengthVerified(num_var,len(str_mot)) and self.allDiffVars(num_var,str_mot,variables) and self.areLettersVerified(num_var,str_mot,variables)

    def isLengthVerified(self,num_var,length):
        if self.tailleFixeVars[num_var]==length:
            return True
        else:
            raise err.WrongLengthException(num_var,length)

    def areLettersVerified(self,num_var,str_mot,variables):
        # s'il n'y a aucune contrainte d'intersection avec ce mot c'est ok
        if not self.valeurCommuneVars.has_key(num_var):
            return True
        else:
            # sinon pour chaque contrainte d'intersection liee à ce mot
            # on verifie si pour l'autre variable, un mot a déja été placé
            # et donc si la contrainte d'egalite convient
            for numY, indXY in self.valeurCommuneVars[num_var].items():
                varY = variables[numY]
                motY = varY[3]
                # on verifie que la val[indX]-ème lettre ==val[indY]-ème lettre
                indX = indXY[0]
                indY = indXY[1]
                if not motY is None and str_mot[indX]!=motY[indY]:
                    raise err.DifferentLetterException(num_var,indX,numY,indY)
                # end if
            # end for
        return True

    def addLengthConstraint(self,num_var,length):
        self.tailleFixeVars[num_var] = length

    def addCommonIndexConstraint(self,num_varX, indX, num_varY,indY):
        # si la case de dictionnaire existe deja
        if self.valeurCommuneVars.has_key(num_varX):
            # on la recupere
            dictX = self.valeurCommuneVars[num_varX]
        else: # sinon on la cree
            dictX = dict()
        # on ajoute l'intersection
        dictX[num_varY] = (indX, indY)
        # on update le dictionnaire de contraintes
        self.valeurCommuneVars.update({num_varX:dictX})
        sorted_tuple = tuple(sorted((num_varX, num_varY)))
        if not sorted_tuple in self.intersectIndexes:
            if num_varX < num_varY:
                self.intersectIndexes[sorted_tuple] = (indX, indY)
            else:
                self.intersectIndexes[sorted_tuple] = (indY, indX)


    def allDiffVars(self,num_var,str_mot,variables):
        #print str_mot
        for num,var in variables.items():
            if num==num_var:
                continue
            #sinond
            #print var[3]
            if var[3]==str_mot:
                raise err.SimilarWordException(num_var,num,str_mot)
        return True

    def __str__(self):
        string = "Contraintes de la grille:\n"
        # on affiche les contraintes joliment et dans l'ordre croissant
        for num in sorted(self.tailleFixeVars.keys()):
            string +="\tVariable {} de taille {} ".format(num,self.tailleFixeVars[num])
            # si cette variable est en contrainte avec d'autres
            if self.valeurCommuneVars.has_key(num):
                string+="telle que "
                for numX, indXY in self.valeurCommuneVars[num]:
                    string+="X{}[{}]==X{}[{}]   ".format(num,indXY[0],numX,indXY[1])
            string+="\n"
        return string
