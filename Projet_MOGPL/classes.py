# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 23:28:45 2015

@author: daphne
"""
import math
import random
import numpy as np
from enum import Enum


# Orientation du robot
class Orientations (Enum) :
    """
    Enumération des orientation possible du robot (nord/sud/est/ouest)

    """    
    nord = 0
    est = 1
    sud = 2
    ouest = 3
    
    def __str__(self):
        return str(self.name)
        
class Etats (Enum) :
    """
    Enumeration des differents états qui apparaitront dans le fichier de sortie
    Chaque etat ayant un cout de 1
    """
    D = 0
    G = 1
    A1 = 2
    A2 = 3
    A3 = 4
    
    def __str__(self):
        if (self.value==0 or self.value==1):
            return str(self.name)
        else :
            return str(self.name).lower()
    
    @staticmethod
    def calcCout(orientInit, dist, orientArr):
        """
        Calcule le cout entre 2 points ecartés de dist entre 1 et 3
        avec deux orientations depart orientInit et arrivee orientArr
        """
        if(dist<1 or dist>3):
            return -1
        # cas ou on avance de 1, 2 ou 3 sans tourner
        if (orientInit==orientArr) :
            return 1
        # cas ou on tourne
        else :
            # somme des rotation + un d'avancée
            return (len(Etats.seqTourne(orientInit,orientArr))+1)
        
    @staticmethod
    def seqTourne(orientInit,orientArr):
        """
        Genere l'enchainement/la sequence necessaire au passage de l'orientInit a l'orientArr
        """
        # on recupere les valeurs numerales des orientations
        vInit = orientInit.value
        vArr = orientArr.value
        # si l'orientation d'arrivee et celle de depart sont identiques
        if (vInit==vArr):
            return []
        # cas demi-tour
        if ((vInit+vArr)%2==0):
            # demi-tour : equivalent a [Etats.G,Etats.G]
            return [Etats.D,Etats.D]
        # sinon
        # cas 1 a droite
        if (((vArr-vInit)%4)==1):
            return [Etats.D]
        # cas 1 a gauche
        else:
            return [Etats.G]
            
    @staticmethod
    def seqAvance(pointDep, pointArr):
        """
        Renvoie la sequence necessaire pour avancer du point pointDep a pointArr
        """
        xdep,ydep = pointDep
        xarr,yarr = pointArr
        # calcul de la distance de l'un a l'autre
        dist = math.sqrt(((xdep-xarr)**2+(ydep-yarr)**2))
        # si dist est negative ou nulle ou >3 : probleme
        if (dist<1 or dist>3):
            return []
        # sinon
        # A1 = 2;A2 = 3;A3 = 4
        return [Etats(dist+1)]

# correspond au probleme d'un fichier donné
class Problem :
    """
    Représentation du probleme avec sa grille d'intersection de rail,
    son point de depart, son point d'arrivee,
    et son orientation
    entrees: 
    @param grille -> la grille des cases du fichier a transformer en grille de rails
    @param depart -> le point de depart (x,y)
    @param arrivee -> le point d'arrivee (x,y)
    @param orientation -> l'orientation de depart
    """
    def __init__(self,grille,depart,arrivee,orientation, obstacles):
        self.grille = grille
        # transformation en grille de parcours du robot
        self.rails = None
        # matrice des roses pour lancer l'algo, chaque rose etant associee a un point
        self.roses = None
        self.depart = depart
        self.arrivee = arrivee
        self.obstacles =  obstacles
        self.orientation = orientation
        self.tpsSolution = -1
        # nblignes : nb de cases par lignes
        self.nbLigne = len(grille)
        # nbColonnes : nb de cases par colonnes
        self.nbCol = len(grille[0])
        # correspond au tuple (cout,liste d'etats) solution
        self.solutionNoeud = None
        self.solutionFile = None
        self.initP()
    
    def initP(self):
        """
        Initialise la grille de rails utilisables par le robot
        et la matrice des roses nodes de l'algorithme
        """
        M = self.nbLigne
        N = self.nbCol
        # rails : matrice des rails 
        self.rails = np.zeros((M,N), int)
        # matrice des roses non obstacles
        self.roses = []        
        # pour chaque valeur de la grille en entree
        for x in range(M) :
            for y in range(N) :
                # si le point est un obstacle
                # rails : on l'ajoute a la liste des obstacles
                if (x<M and y<N and self.grille[x][y]==1):
                    # rails : on ajoute l'obstacle comme point nord-ouest d'un bloc de 4 obstacles
                    self.obstacles.addObstacle(x,y)
                    self.rails[x][y]= 1
                    self.roses.append(None)
                # cas: si le point est un des autres coins d'un obstacle,
                # rails : on l'ajoute a la liste des obstacles
                elif (self.obstacles.isObstacle(x,y)):
                    self.rails[x][y]= 1
                    self.roses.append(None)
                # sinon on laisse a zero dans rails
                # on cree un rose Node dans roses pour le point x,y
                else :
                    self.roses.append(RoseNodes((x,y)))
                # end if
            # end for
        # end for
        # transformation de la liste de roses en tableau 2D de taille (M,N)
        self.roses = np.asarray(self.roses)
        self.roses.shape = (M,N)
        
  
    def __str__(self):
        """
        Override du toString de la grille entree
        """
        string = "Taille de la grille : "+str(self.nbLigne)+"*"+str(self.nbCol)+"\n"
        # orientation de départ
        string += "Orientation de départ : "+str(self.orientation.name)+"\n"
        string += "Grille \n"
        strGrille = np.where(self.grille==0,"O","X")
        xd,yd = self.depart
        xf,yf = self.arrivee
        # la grille
        for i in range(self.nbLigne):
            for j in range(self.nbCol):
                if(xd==i and yd==j):
                    string += "D "
                elif(xf==i and yf==j):
                    string += "A "
                else :
                    string += strGrille[i][j]+" "
                # end if
            # end for
            string += "\n"
        # end for
        string += "\n"
        return string
        
    #################### STRING du fichier entre ############
    def str_writeEntryFile(self) :
        """
        Retourne la string de ce qui sera dans un fichier d'entree contenant ce probleme
        """
        stringFile = "\n"
        stringFile += "{} {}\n".format(self.nbLigne,self.nbCol)
        
        # on ecrit la grille generée avec les obstacles
        for val in self.grille :
            val = " ".join(map(str,val))
            stringFile += "{}\n".format(val)
        # on ecrit les point de depart et darrivee et l'orientation de depart
        XD,YD = self.depart
        XA,YA = self.arrivee
        orient = self.orientation
        stringFile += "{} {} {} {} {}\n".format(XD, YD, XA, YA, orient)
        return stringFile

    #################### STRING du fichier solution ############
    def str_writeSolutionFile(self) :
        """
        Retourne la string de ce qui sera dans un fichier solution contenant la solution de ce probleme
        """
        stringFile = "\n"
        # si pas de solution genere
        if self.solutionFile is None :
            return "\nSolution non generee"
        cout, listEtats = self.solutionFile
        # on ecrit le cout
        stringFile += "{} ".format(cout)
        stringFile += " ".join(map(str,listEtats))
        stringFile += "\n"
        return stringFile
        
    ##################### GENERATION ALEATOIRE D'UN PROBLEME #################
    @staticmethod
    def genere_prob(M,N,nbObs) :
        """
        Genere aléatoirement un  probleme avec nbObs
        et un grille de taille M*N
        """
        obst = Obstacles()
         # on genere la grille  de zeros
        grille = np.zeros((M,N), int)
        # on place les obstacles
        if nbObs>=M*N :
            print("ERREUR : {} obstacles ≥ {} (taille de la grille)".format(nbObs,M*N))
            return None           
        for i in range(nbObs) :
            # tant qu'aucun x, y n'est valide
            while True :
                x = random.randint(0,M-1)
                y = random.randint(0,N-1)
                if (grille[x][y]!=1) :
                    # si ce x, y sont valides
                    obst.addObstacle(x,y)
                    break;
            # on assigne un nouvel obstacle a la grille
            grille[x][y] = 1
        # on genere un point de depart, un point d'arrivee et un orientation
        lA = []
        lD = []
        # XA!=XD && YA!=YD && (XA,YA)!=1 && (XD,YD)!=1
        while True:
            XD = random.randint(0,M-1)
            YD = random.randint(0,N-1)
            if lD.__contains__((XD,YD)):
                continue
            # si le depart n'est pas un obstacle au robot
            if (not obst.isObstacle(XD,YD)):
                break
            else :
                lD.append((XD,YD))
        while True :
            XA = random.randint(0,M-1)
            YA = random.randint(0,N-1)
            if lA.__contains__((XD,YA)):
                continue
            # si l'arrivee n'est pas un obstacle et n'est pas le depart
            if (not obst.isObstacle(XA,YA) and (XD!=XA or YD!=YA)):
                break
            else:
                lA.append((XA,YA))
        orient = Orientations(random.randint(0,3))
        
        prob = Problem(grille, (XD,YD), (XA,YA), orient, obst)
        return prob
      
class Obstacles():
    def __init__(self):
        """
        Recupere la liste des coordonnees (x,y) d'intersection rails de la grille en entree
        """
        self.liste = list()
        
        
    def addObstacle(self,xp,yp):
        """
        A partir du point point de coordonnees (x,y)
        enregistre les quatres points correspondants comme obstacles
        (x,y),(x+1,y),(x,y+1),(x+1,y+1)
        """
        # si le point n'est pas deja dans la liste
        if (not self.liste.__contains__((xp,yp))) :
            # on l'ajoute
            self.liste.append((xp,yp))
            # sinon on le laisse tel quel
        # on ajoute de la meme maniere les 3 points sud, est,sud-est
        self.addVal(xp+1,yp)
        self.addVal(xp,yp+1)
        self.addVal(xp+1,yp+1)
        
    def addVal(self,xp,yp):
        """
        Ajoute un point a la liste s'il n'y ai pas
        Sinon ne fait rien
        """
        # si le point n'est pas deja dans la liste
        if (not self.liste.__contains__((xp,yp))) :
            # on l'ajoute
            self.liste.append((xp,yp))
        
        
    def isObstacle(self, xp,yp):
        """
        Renvoie True si le point de la grille de rails de coordonnees xp,yp est un obstacle au robot
        """
        return self.liste.__contains__((xp,yp))
        
    def nbObstacles(self):
        """
        Retourne le nombre d'obstacles du probleme auquel le robot fait face
        """
        return len(self.liste)
    
    @staticmethod
    def findObstacles(grille):
        """
        Renvoie pour la grille en parametre une instance d'obstacle
        """
        obs = Obstacles()
        listObs = list(map(tuple,np.argwhere(grille==1)))
        for x,y in listObs:
            obs.addObstacle(x,y)
        return obs

class RoseNodes : # nom tiré de la rose des vents pour les 4 orientations
    """
    RoseNodes[orient, node] : arrivee au point 4 orientations max differentes => par orientation d'arrivee 12 etats possible
    (ie 12couts differents sachant qu'on vient du sud, de l'est, du nord ou de l'ouest)
    Rose de noeuds correspondant a un point et contenant pour chaque orientation possible un Node
    """
    def __init__(self, point):
        # point actuel tuple (x,y)
        self.coord = point
        # boussole : dictionnaire donnant pour une orientation un "meilleur" noeud (avec son parent et son cout)
        # initialisée a vide pour chaque orientation
        self.boussole = {"nord":None,"est":None,"sud":None,"ouest":None}
        # node minimum pour atteindre ces coordonnees
        self.minNode = None
        self.marque = False
        self.isSolution = False
        
    def betterSolutionUntil(self, orient, cout, papa):
        """
        Pour l'orientation d'arrivee donnée, 
        verifie si c'est un meilleur solution que celle deja enregistree
        si aucune n'a ete deja ete enregistree, alors enregistre celle la
        """
        # on recupere le node de l'orientation recherchee
        n = self.boussole[orient.name]
        # si il en existe deja un
        if (n!=None):
            # on choisit le meilleur
            n.betterSolution(cout,papa)
        else:
            n = Node(cout,papa, orient, self.coord)
            self.boussole[orient.name] = n
            
        # on recupere le noeud min de cette rose
        # possibilité trop longue : dependant du nombre total de noeuds qui seront créés
        #if (self.minNode is None or self.minNode.cout>=n.cout) :
        #    self.minNode = n
        return n
        
    def getBestSolution(self):
        """
        Meilleure solution que de tester a chaque fois car ne fait que 4 grosses comparaisons plutot que N*M*4 petites au max
        Retourne le meilleur noeud et son orientation, ie le moindre cout de la rose
        """
        # on recupere les couts des noeuds (non nuls) pour chaque orientation
        if (not self.boussole["nord"] is None):
            nord = self.boussole["nord"].cout
        else :
            nord = float('inf')
        if (not self.boussole["est"] is None):
            est = self.boussole["est"].cout
        else :
            est = float('inf')
        if (not self.boussole["sud"] is None):
            sud = self.boussole["sud"].cout
        else :
            sud = float('inf')
        if (not self.boussole["ouest"] is None):
            ouest = self.boussole["ouest"].cout
        else :
            ouest = float('inf')
            
        if (nord<=est and nord<=sud and nord<=ouest):
            # le nord est le mieux
            self.minNode = self.boussole["nord"]
        elif (sud<=est and sud<=nord and sud<=ouest):
            # le sud est le mieux
            self.minNode = self.boussole["sud"]
        elif (est<=nord and est<=sud and est<=ouest):
            # l'est est le mieux
            self.minNode = self.boussole["est"]
        elif (ouest<=est and ouest<=sud and ouest<=nord):
            # l'ouest est le mieux
            self.minNode = self.boussole["ouest"]
                
        
        return self.minNode
        
    def __str__(self):
        return self.coord.__str__()
        
        
class Node :
    """
    Node : depart du point 4orientations et 3 etats (a1,a2,a3) pour chaque orientation => 12 etats max
    Noeud de la rose du graphe, contenant comme attribut :
    -le noeud parent (Node)
    -le cout jusque là (avec cette orientation)
    -les chemins possibles jusqu'a l'arrivee si ce n'est pas le bon point
    - l'orientation par laquelle on y est arrive
    - les coordonnees du point tuple x,y
    """
    def __init__(self,cout, papa, orientation, coordonnees):
        # cout jusque la
        if (papa is None):
            self.cout = 0
        else:
            self.cout = cout+papa.cout
        # node parent
        self.parent = papa
        self.orientation = orientation
        self.coordonnees = coordonnees
        # pour l'algo
        self.isMarked = False
        self.aTraiter = False
        
    def betterSolution(self, cout, papa):
        """
        Modifie le noeud si l'optimisation est meilleure
        Traite le cas d'arrivee par sauts (a1,a2,a3) donc le parent peut etre different
        Compare les couts d'arrivée a ces coord
        SI cout meilleur alors le sauvegarder
        """
        coutTot = cout+papa.cout
        if (self.cout>=coutTot) :
            self.cout = coutTot
            self.parent = papa
           
        # endif
        # sinon on ne traite pas et on oublie cette solution
    
    def calcBestSolution(self):
        """
        Retourne la sequence du meilleur itinéraire pour venir jusque la depuis l'arrivee
        """
        # pour le cas ou c'est le premier noeud du graphe
        if (self.parent is None):
            return [],[self.coordonnees]
        # sinon pour tous les autres noeuds
        sequenceFile = []
        sequenceNoeuds = []
        # on recupere d'abord la sequence precedente
        solFilePapa,solNoeudPapa = self.parent.calcBestSolution()
        sequenceFile.extend(solFilePapa)
        sequenceNoeuds.extend(solNoeudPapa)
        ### on recupere la sequence entre le parent et self
        ## sequence de rotation au niveau du parent
        # on recupere l'orientation initiale du parent
        oPapa = self.parent.orientation
        oMoi = self.orientation
        sequenceFile.extend(Etats.seqTourne(oPapa,oMoi))
        ## sequence d'avancement du parent a self
        sequenceFile.extend(Etats.seqAvance(self.parent.coordonnees,self.coordonnees))
        sequenceNoeuds.append(self.coordonnees)
        return sequenceFile,sequenceNoeuds
            
    def avance(self,dist,orient,prob):
        """
        Renvoie le tuple point (x,y) correspondant en avancant de dist rails
        Verifie que ce point est dans la grille du robot et n'est pas un obstacle
        """
        x,y = self.coordonnees
        # on recupere le point d'arrivee
        if (dist<1 or dist>3):
            return None
        if (orient.value == Orientations.sud.value) :
            xn = x+dist
            yn = y
        elif (orient.value == Orientations.nord.value) :
            xn = x-dist
            yn = y
        elif (orient.value == Orientations.est.value) :
            xn = x
            yn = y+dist
        else : # cas orientation ouest
            xn = x
            yn = y-dist
        # on verifie qu'il est dans la grille
        Mr = prob.nbLigne
        Nr = prob.nbCol
        if (xn>=Mr or yn>=Nr or xn<0 or yn<0):
            return None
        # on verifie que ce point n'est pas un obstacle
        if (prob.obstacles.isObstacle(xn,yn)):
            return None
        # on retourne un tuple point valide            
        return (xn,yn)
        
    def __str__(self):
        """
        Override du toString
        """
        orient = self.orientation
        string = "Node {} (cout = {})\n".format(orient, self.cout)
        string += "\tChemin : {}".format(self.calcBestSolution())
        return string
        
    def __eq__(self,other):
        """
        Override de l'egalite entre deux noeuds
        """
        return (not other is None and other.cout==self.cout and other.coordonnees==self.coordonnees)
        