# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 12:41:41 2015

@author: daphne
"""

from classes import *
from monTas import *
import time

class Algorithm :
    COEFF_IT = 4
    """
    Represente l'application de l'algorithme du plus court chemin sur le graphe des roseNodes
    """
    
    def __init__(self, prob):
        self.prob = prob
        self.nodesATraiter = MyHeap()
        self.tpsAlgo = 0
        self.nbNoeuds = (prob.nbLigne)*(prob.nbCol)-prob.obstacles.nbObstacles()
        # matrice correspondant au probleme pour la recuperation des roseNode
        print u"\nRésolution problème {}*{}".format(prob.nbLigne,prob.nbCol)
        # on lance le chrono d'execution de l'algorithme        
        startTime = time.time()
        self.initAlgo()
        self.boucleAlgo()
        stopTime = time.time()
        # fin du chrono
        # on recupere la duree d'execution
        self.tpsAlgo = stopTime-startTime
        # on sauvegarde aussi dans le probleme la duree de la generation de cette solution
        self.prob.tpsSolution = self.tpsAlgo
        print self.tpsAlgo
        
    def initAlgo(self):
        """
        Initialise les listes de nodes traites et a traiter selon le probleme
        """
        xd,yd = self.prob.depart
        roseInit = self.prob.roses[xd][yd]
        orientation = self.prob.orientation
        # on cree le seul et unique node de la rose initiale avec un cout nul et l'orientation initiale
        #node = roseInit.betterSolutionUntil(orientation, 0, None)
        node = roseInit.boussole[orientation.name] = Node(0,None,orientation,(xd,yd))
        self.nodesATraiter.push(node)
        
        
    def boucleAlgo(self):
        """
        Initialise la solution dans prob avec le tuple (cout,sequence)
        Application de l'algo
        """
        xfin,yfin = self.prob.arrivee
        roses = self.prob.roses
        roseNodeFin = roses[xfin][yfin]
        roseNodeFin.isSolution = True
        node = self.nodesATraiter.pop()
        # variable locale pour verifier si a traiter est empty
        aTraiterEmpty = False
        i = 0
        # tant que ce n'est pas le noeud final
        # ou qu'on n'a pas depassé un certain nombre d'iterations (nbNoeuds a traiter *4)
        # ou que la liste de noeuds a traiter est vide
        # -> not self.nodesTraites.contains(?) and  ?
        # -> and not node.rose.isSolution ?
        while (not node is None and i<=self.nbNoeuds*Algorithm.COEFF_IT and not roseNodeFin.marque):
            
           # print self.strAvancee(node.rose.coord.x,node.rose.coord.y, i)
            # on remplit les rose Nodes voisins de node
            # et on les ajoute a la liste des noeuds a traiter
            # vers chaque (les 4) orientations possibles
            for o in Orientations:
                # on genere les points des avancees 1,2 et 3 pas
                for dist in 1,2,3 :
                    # dans point : def avance(self,dist,orient,prob):
                    point = node.avance(dist,o,self.prob)
                    # si le point n'est pas realisable
                    if (point==None):
                        # on ne teste pas les points plus loin
                        # e.g: si a1 impossible alors a2 et a3 impossibles
                        break
                    # sinon : le point est atteignable
                    else:
                        xn,yn = point
                        # on recupere le cout de node a ce point
                        orientInit = node.orientation
                        cout = Etats.calcCout(orientInit,dist ,o)
                        # on recupere la roseNode correspondant a ce point
                        roseNode = roses[xn][yn]
                        # puis on cree le node correspondant a cette orientation avec ce cout
                        newnode = roseNode.betterSolutionUntil(o,cout,node)
                        # si ce noeud n'a pas deja ete traité :
                        if (not newnode.isMarked and not newnode.aTraiter):
                            # on ajoute le node crée au tas des nodes a traiter
                            self.nodesATraiter.push(newnode)
                            newnode.aTraiter = True
                    # end if
                # end for avance
            # end for orientations
            # on marque ce noeud comme traite
            node.isMarked = True
            # on lui retire l'etat a traiter
            node.aTraiter = False
            # on recupere ses coordonnees
            x, y = node.coordonnees
            # on marque la rose correspondant si elle n'est pas deja marquee
            # ne veut pas pour autant dire que toutes les orientations ont été visitées
            roses[x][y].marque = True
            # s'il n'y a plus aucun noeud a tester alors il n'y a pas de solution
            if (self.nodesATraiter.isEmpty()):
                aTraiterEmpty = True
                break;
            # on recupere le prochain noeud sur lequel iterer
            node = self.nodesATraiter.pop()
            i+=1
        # end while
        ################ FIN ALGO
        # cas pas de solution
        # si on a deja trop iterer
        if (i>self.nbNoeuds*Algorithm.COEFF_IT 
            # ou que le prochain noeud est vide
            or node is None 
            # ou qu'il n'y a plus de noeud a traiter et qu'on a pas encore atteint l'arrivee
            or (aTraiterEmpty and not roseNodeFin.marque)) :
            # alors il n'y a pas de solution possible
            self.prob.solutionFile = (-1,list())
            self.prob.solutionNoeuds = None
            print "Pas de solution"
        # cas ou il y a une solution
        else:
            self.prob.solutionFile,self.prob.solutionNoeud = self.remonteAlgo()
            print "Solution trouvée"
            
        
            
    def remonteAlgo(self):
        """
        Retourne le tuple cout,sequence pour la solution
        Renvoie la sequence (si elle existe) de trajet du robot
        sinon renvoie None
        """
        xfin,yfin = self.prob.arrivee
        # on recupere le noeud d'arrivee
        node = self.prob.roses[xfin][yfin].getBestSolution() 
        # on applique la recursion
        solFile,solNoeud = node.calcBestSolution()
        return ((node.cout,solFile),solNoeud)
    
    def strAvancee(self,x,y,i):
        """
        Affiche graphiquement quel point on etudie par rapport a l'arrivee et au depart
        """
        rails = self.rails
        xd,yd = self.depart
        xf,yf = self.fin
        string = "Grille it {} \n".format(i)
        strGrille = np.where(rails==1,"X ","0 ")
        # la grille
        for i in range(len(rails)):
            for j in range(len(rails[0])):
                if(xd==i and yd==j):
                    string += "D "
                elif(xf==i and yf==j):
                    string += "A "
                elif(x==i and y==j):
                    string += "R "                    
                else :
                    string += strGrille[i][j]
                # end if
            # end for
            string += "\n"
        # end for
        string += "\n"
        return string
    
