#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import time
import numpy as np
import gestIO as io
from PyQt4 import QtGui, QtCore

M_MIN = 5
M_MAX = 70
N_MIN = 5
N_MAX = 70

OBST_MIN = 0
OBST_MAX = 0
E_OBST = 15
VAL_MINMAX_OBST = M_MIN*N_MIN-E_OBST
VAL_MAX_OBST = 100

CONST_TAILLE = 200

FILE_PATH = './Grille'
COULEUR_PATH = "background-color: blue"
COULEUR_DEF = "background-color: white"

class CaractGrille(QtGui.QWidget):
    """
    Widget/Panel pour choisir M,N et le nom du fichier avant de determiner les obstacles
    """
    
    def __init__(self, statusBar,parent=None):
        super(CaractGrille, self).__init__(parent=parent)
        self.statusBar = statusBar
        self.M = 0
        self.N = 0
        self.nbObstacles = 0
        self.validButton = QtGui.QPushButton("Formulaire Valide")
        self.isCaract = True
        self.initUI()
        
    def initUI(self):
        
        vbox = QtGui.QVBoxLayout()

        nbLignesLbl = QtGui.QLabel('Nombre de lignes (M)')
        nbColsLbl = QtGui.QLabel('Nombre de colonnes (N)')
        self.nbObstLbl = QtGui.QLabel('Nombre d\'obstacles')
        
        nbLignesSlider = QtGui.QSlider(QtCore.Qt.Horizontal,self)
        nbLignesSlider.setToolTip("Entier compris entre {} et {}".format(M_MIN,M_MAX))
        nbColsSlider = QtGui.QSlider(QtCore.Qt.Horizontal,self)
        nbColsSlider.setToolTip("Entier compris entre {} et {}".format(N_MIN,N_MAX))
        self.nbObstSlider = QtGui.QSlider(QtCore.Qt.Horizontal,self)
        self.nbObstSlider.setToolTip("Entier compris entre {} et {}".format(0,OBST_MAX))
        
        nbColsSlider.valueChanged[int].connect(self.changeNValue)
        nbColsSlider.setRange(N_MIN,N_MAX)
        nbLignesSlider.valueChanged[int].connect(self.changeMValue)
        nbLignesSlider.setRange(M_MIN,M_MAX)
        self.nbObstSlider.valueChanged[int].connect(self.changeObstValue)
        self.nbObstSlider.setRange(0,OBST_MAX)
        
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(nbLignesLbl, 1, 0)
        grid.addWidget(nbLignesSlider, 1, 1)

        grid.addWidget(nbColsLbl, 2, 0)
        grid.addWidget(nbColsSlider, 2, 1)

        grid.addWidget(self.nbObstLbl, 3, 0)
        grid.addWidget(self.nbObstSlider, 3, 1)

        
        vbox.addLayout(grid)
        
        # genere aleatoirement
        okButton = QtGui.QPushButton("OK")
        okButton.setToolTip(u"Génère aléatoirement un problème")
        cancelButton = QtGui.QPushButton("Cancel")
        
        self.validButton = okButton
        cancelButton.clicked.connect(QtCore.QCoreApplication.instance().quit)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)
        
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        
        self.setWindowTitle(u'Caractéristiques de la grille')    
        self.show()
        
    def changeMValue(self,value):
        self.M = value
        global OBST_MAX        
        OBST_MAX = max(VAL_MINMAX_OBST,min(VAL_MAX_OBST,value*self.N-E_OBST))
        self.nbObstSlider.setToolTip("Entier compris entre {} et {}".format(0,OBST_MAX))
        self.nbObstSlider.setRange(0,OBST_MAX)
        self.statusBar.showMessage("M = {}, N = {}, {} obstacles".format(self.M,self.N,self.nbObstacles))
        
    def changeNValue(self,value):
        self.N = value
        global OBST_MAX        
        OBST_MAX = max(VAL_MINMAX_OBST,min(VAL_MAX_OBST,value*self.M-E_OBST))
        self.nbObstSlider.setToolTip("Entier compris entre {} et {}".format(0,OBST_MAX))
        self.nbObstSlider.setRange(0,OBST_MAX)
        self.statusBar.showMessage("M = {}, N = {}, {} obstacles".format(self.M,self.N,self.nbObstacles))

    def changeObstValue(self,value):
        self.nbObstacles = value
        self.statusBar.showMessage("M = {}, N = {}, {} obstacles".format(self.M,self.N,self.nbObstacles))
            
            
class BoutonGrille(QtGui.QPushButton):
    SIZE = 40
    MIN_SIZE = 20
    def __init__(self,coord,parent=None):
        super(BoutonGrille,self).__init__(parent)
        self.coordonnees = coord
        self.isObstacle = False
        self.isArrivee = False
        self.isDepart = False
        self.setStyleSheet(COULEUR_DEF)
        self.initUI()
        
    def initUI(self):
        self.setMinimumSize(BoutonGrille.MIN_SIZE,BoutonGrille.MIN_SIZE)
        self.setMaximumSize(BoutonGrille.SIZE,BoutonGrille.SIZE)
        """        
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy)
        """
        pass
                
    def stateChange(self,etat):
        """
        Definit si la case est l'arrivee, le depart, un ostacle ou une simple case
        etat = 1 pour obstacle, 2 pour depart, 3 pour arrivee
        """
        if etat>3 or etat<0:
            exit
        obstacle = self.isObstacle
        arrivee = self.isArrivee
        depart = self.isDepart
        if etat==2 and not arrivee and not obstacle:
            self.isDepart = not depart
        elif etat==1 and not depart and not arrivee:
            self.isObstacle = not obstacle
        elif etat==3 and not depart and not obstacle:
            self.isArrivee = not arrivee
        elif etat==0 :
            self.isArrivee = False
            self.isDepart = False
            self.isObstacle = False
        else:
            # cas ou on a deja attribué un etat a la case
            exit
        
        # si c'est un obstacle 
        if self.isObstacle :
            self.setFlat(True)
            self.setIcon(QtGui.QIcon('IMG/mur.jpg'))
            self.setIconSize(QtCore.QSize(BoutonGrille.SIZE,BoutonGrille.SIZE))
        elif self.isArrivee :
            self.setFlat(True)
            self.setIcon(QtGui.QIcon('IMG/arrivee.png'))
            self.setIconSize(QtCore.QSize(BoutonGrille.SIZE,BoutonGrille.SIZE))
        elif self.isDepart :
            self.setFlat(True)
            self.setIcon(QtGui.QIcon('IMG/robot.png'))
            self.setIconSize(QtCore.QSize(BoutonGrille.SIZE,BoutonGrille.SIZE))            
        else:
            self.setIcon(QtGui.QIcon())
        self.setFlat(False)
        
            
    def __str__(self):
        string = ""
        if self.isObstacle :
            string+= "Obstacle : "
        elif self.isArrivee :
            string+= u"Arrivée : "
        elif self.isDepart :
            string+= u"Départ : "
        else :
            string+= "Case : "
        i,j = self.coordonnees
        string+="(ligne={},colonne={})".format(i,j)
        return string
        
    
class Grille(QtGui.QWidget):
    """
    Représente l'affichage de la grille
    soit d'un probleme genere aleatoirement soit d'un probleme lu dans un fichier
    """
    def __init__(self,M,N,nbObst, parent=None,prob=None):
        super(Grille,self).__init__(parent=parent)
        self.prob = prob
        # nb de lignes de la grille
        self.M = M
        # nb de colonnes de la grille
        self.N = N
        # point d'arrivee
        self.arrivee = (2,2)
        # point de depart
        self.depart = (0,0)
        # orientation de depart
        self.orientation = "Nord"
        # nombre d'obstacles à générer aléatoirement
        self.nbObstacles = nbObst
        # grille sauvegardée dans le fichier
        self.grille = None
        # solution generee pour la grille actuellement affichée
        self.solutionAffichee = None
        self.initUI()
        
    def initUI(self):
        # generation de la grille        
        if self.prob is None:
            # on genere aléatoirement une grille avec les parametres precedemment entres
            # le nombre d'obstacles, le depart et l'arrivee pourront etre modifiés a tout moment
            self.genereGrille()
        else:
            self.affichProblem(self.prob)
            
        # s'il y a eu un soucis a la generation/creation du pb
        if self.prob is None:
            self.parent().parent().nouvFile()
            return None

        # layout compliqués pour que les point de la grille se serrent entre eux
        vLayout = QtGui.QVBoxLayout()
        hLayout = QtGui.QHBoxLayout()
        self.setLayout(vLayout)
        # on centre la grille dans son espace
        hLayout.addStretch(1)
        hLayout.addLayout(self.gridLay)
        hLayout.addStretch(1)
        vLayout.addLayout(hLayout)
        # on pousse la grille en haut de la fenetre
        vLayout.addStretch(1)
        # fin layout compliqué
        self.setMinimumSize(BoutonGrille.MIN_SIZE*self.M,BoutonGrille.MIN_SIZE*self.N)
        self.show()
    
    def genereGrille(self):
        # on genere un probleme aleatoirement
        prob = io.Problem.genere_prob(self.M,self.N,self.nbObstacles)
        self.prob = prob
        # s'il ya un soucis avec M et N
        if prob is None:
            QtGui.QMessageBox.critical(self,u"Génération impossible",u"Impossible de générer un nouveau problème avec ces données")
            return None
        # on recupere le depart et l'arrivee et la grille
        self.grille = prob.grille
        self.depart = prob.depart
        self.arrivee = prob.arrivee
        
        # remplissage du gridLayout
        grid = QtGui.QGridLayout()
        butt = []
        for i in range(self.M):
            l = []
            for j in range(self.N):
                button = BoutonGrille((i,j),self)
                button.setMaximumSize(BoutonGrille.SIZE,BoutonGrille.SIZE)
                button.setBaseSize(20,20)    
                grid.setColumnMinimumWidth(j,BoutonGrille.SIZE)
                grid.addWidget(button, i,j)
                button.clicked.connect(self.clicked)
                button.setStatusTip(button.__str__())
                
                # si ce point est l'arrivee
                if (i,j)==self.arrivee:
                    button.stateChange(3)
                # si ce point est le depart
                elif (i,j)==self.depart:
                    button.stateChange(2)
                # si ce point est un obstacle
                elif self.grille[i,j]==1:
                    button.stateChange(1)
                # end if
                l.append(button)
            # end first for
            butt.append(l)
            grid.setRowMinimumHeight(i,BoutonGrille.SIZE)
        # end 2e for
        grid.setSpacing(0)
        self.gridLay = grid
            
    def affichProblem(self,prob):
        # on recupere le depart et l'arrivee et la grille
        self.prob = prob
        self.grille = prob.grille
        self.depart = prob.depart
        self.arrivee = prob.arrivee
        self.M = prob.nbLigne
        self.N = prob.nbCol
        papaOrient =  self.parent().orientCombo
        papaOrient.setCurrentIndex(papaOrient.findText(prob.orientation.name,QtCore.Qt.MatchFixedString))
        self.orientation = prob.orientation.name
        self.nbObstacles = 0
        # remplissage du gridLayout
        grid = QtGui.QGridLayout()
        butt = []
        for i in range(self.M):
            l = []
            for j in range(self.N):
                button = BoutonGrille((i,j),self)
                button.setMaximumSize(BoutonGrille.SIZE,BoutonGrille.SIZE)
                button.setBaseSize(20,20)    
                grid.setColumnMinimumWidth(j,BoutonGrille.SIZE)
                grid.addWidget(button, i,j)
                button.clicked.connect(self.clicked)
                button.setStatusTip(button.__str__())
                
                # si ce point est l'arrivee
                if (i,j)==self.arrivee:
                    button.stateChange(3)
                # si ce point est le depart
                elif (i,j)==self.depart:
                    button.stateChange(2)
                # si ce point est un obstacle
                elif self.grille[i,j]==1:
                    button.stateChange(1)
                    self.nbObstacles+=1
                # end if
                l.append(button)
            # end first for
            butt.append(l)
            grid.setRowMinimumHeight(i,BoutonGrille.SIZE)
        # end 2e for
        grid.setSpacing(0)
        self.gridLay = grid
        
    
    def resoutProblem(self):
        # si une solution a été générée 
        # on l'efface
        if not self.solutionAffichee is None:
            self.effaceResolution()
        obs = io.Obstacles.findObstacles(self.grille)
        orientName =  self.orientation.lower()
        orient = io.Orientations[orientName]
        prob = io.Problem(self.grille,self.depart,self.arrivee,orient,obs)
        # generation de la solution
        io.algos.Algorithm(prob)
        ####### recuperation de la solution
        filename = self.parent().parent().filename
        # si aucune sauvegarde n'a été faite
        # sauvegarde de la solution dans un fichier
        reply = QtGui.QMessageBox.question(self,u"Sauvegarde",u"Voulez-vous sauvegarder la solution?".format(filename),QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No|QtGui.QMessageBox.Cancel, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            # si ce probleme n'a pas de fichier correspondant
            if filename is None:
                # recuperation du nom de fichier solution
                dialog = QtGui.QInputDialog()
                filename, ok = dialog.getText(self, 'Fichier Sauvegarde', 
                                                          'Nom du fichier sauvergarde')
            ok=True
        elif reply == QtGui.QMessageBox.Cancel:
            QtGui.QMessageBox.information(self,u'Résolution annulée',u'La résolution du problème {} a été annulée'.format(filename))
            return None
        else:
            ok=False
        # on traite la reponse
        if ok:
            io.write_SolutionFile(filename,[prob])
            self.parent().parent().filename = filename
        solution = prob.solutionNoeud
        self.solutionAffichee = solution
        self.parent().solutionAffichee = solution
        self.affichResolution()
        return solution
        
    def clicked(self):
        """
        Fonction appelée au clic sur un bouton de la grille
        """
        # si une solution a été générée 
        # on l'efface
        if not self.solutionAffichee is None:
            self.effaceResolution()
        sender = self.sender()
        # on notifie au bouton d'aparaitre tel que l'etat le suggere
        # et on recupere les coordonnees de ce bouton pour changer la self.grille        
        x,y = sender.coordonnees
        
        etat = self.parent().etat
        arrivee = sender.isArrivee
        depart = sender.isDepart
        obstacle = sender.isObstacle
        # c'est un obstacle
        if etat==1 and not arrivee and not depart:
            # si un obstacle peut etre poser ici alors on le pose
            if self.verifObstacle(x,y) :
                # on verifie qu'aucun n'est déja arrivee ou depart
                if not obstacle:
                    self.grille[x][y] = 1
                    self.nbObstacles += 1
                else:
                    self.grille[x][y] = 0
                    self.nbObstacles -= 1
                sender.stateChange(etat)
            else:
                QtGui.QMessageBox.warning(self,"Mouvement impossible",u"Un obstacle ne peut être posé en ({},{})".format(x,y))
        elif etat==3 and not depart and not obstacle and not arrivee:
            # on verifie si l'arrivee peut etre posée ici (ie les case alentours ne sont pas bloquées)
            if self.verifCaseRobot(x,y):
                # c'est l'arrivee
                xa,ya = self.arrivee
                self.arrivee = (x,y)
                # on retire l'ancien arrivee de l'affichage
                exArr = self.gridLay.itemAtPosition(xa,ya).widget()
                exArr.stateChange(0)
                sender.stateChange(etat)
            else:
                QtGui.QMessageBox.warning(self,"Mouvement impossible",u"L'arrivée ne peut être posé en ({},{})\nIl y a un/des obstacle(s) à l'intersection concernée".format(x,y))
        elif etat==2 and not depart and not arrivee and not obstacle:
            # on verifie si le depart peut etre posée ici (ie les case alentours ne sont pas bloquées)
            if self.verifCaseRobot(x,y):
                # c'est le depart
                xd,yd = self.depart
                self.depart = (x,y)
                # on retire l'ancien depart de l'affichage
                exDep = self.gridLay.itemAtPosition(xd,yd).widget()
                exDep.stateChange(0)
                sender.stateChange(etat)
            else:
                QtGui.QMessageBox.warning(self,"Mouvement impossible",u"Le départ ne peut être posé en ({},{})\nIl y a un/des obstacle(s) à l'intersection concernée".format(x,y))
            # end if
        # end if
        self.parent().updateData()
                
    def verifObstacle(self,x,y):
        """
        Permet de verfier si on peut reellement poser un obstacle a cet endroit
        Verifie qu'aucun des 4 points n'est déjà l'arrivee ou le depart
        Return true si le mouvement est possible, false sinon
        """
        wEst = (x,y+1)
        wSud = (x+1,y)
        wSudEst = (x+1,y+1)
        # on recupere l'arrivee et le depart courant
        depart = self.depart
        arrivee =  self.arrivee
        # si l'est n'est ni l'arrivee, ni un obstacle ou est vide
        if ((wEst != arrivee and wEst != depart)
            # et le sud non plus
            and (wSud != arrivee and wSud != depart)
            # et l'ouest non plus
            and (wSudEst != arrivee and wSudEst != depart)
           ):
            # alors x,y peut etre un obstacle
            return True
        else:
            return False
            
    def verifCaseRobot(self,x,y):
        """
        Verifie que la case x,y est une où le robot peut se poser
        Ie x-1,y; x,y-1 et x-1,y-1 ne sont pas des obstcles
        """
        wNord = (x,y-1)
        wOuest = (x-1,y)
        wNordOuest = (x-1,y-1)
        listObs = list(map(tuple,np.argwhere(self.grille==1)))
        return (not 
                (listObs.__contains__(wNord)
                or listObs.__contains__(wOuest)
                or listObs.__contains__(wNordOuest)))
                
    
        
    def affichResolution(self):
        """
        Affiche sur l'interfaceChoixGrille actuelle le chemin en colorant les case en bleu
        """
        chemin = self.solutionAffichee
        if chemin is None:
            exit
        else:
            widgGrille = self.gridLay
            precPt = chemin[0]
            # cas du premier point
            # TODO border right does not work
            Sicolor = "border-right:5px dotted red;"+COULEUR_DEF
            Sjcolor = "border-top: 5px dotted red;"+COULEUR_DEF
            Sicolor = Sjcolor = COULEUR_PATH
#            widgGrille.itemAtPosition(*precPt).widget().setStyleSheet(Scolor)
            for point in chemin :
                if point == precPt:
                    # on zappe le premier point
                    continue
                # pour chaque point ou le robot tourne
                # on reconstruit l'itineraire entre les point
                xprec,yprec = precPt
                xp,yp = point
                # cas ou on avance sur la colonne : j constant
                if xprec!=xp:
                    rangeX = range(xprec,xp) if xp>xprec else range(xp,xprec)
                    for i in rangeX :
                        widgGrille.itemAtPosition(i,yp).widget().setStyleSheet(Sicolor)
                # cas ou on avance sur la ligne : i constant
                elif yprec!=yp:
                    rangeY = range(yprec,yp) if yp>yprec else range(yp,yprec)
                    for j in rangeY :
                        widgGrille.itemAtPosition(xp,j).widget().setStyleSheet(Sjcolor)
                    # end for
                # on prevoit le passage au point suivant
                precPt = point
            #widgGrille.itemAtPosition(*point).widget().setStyleSheet(Scolor)
            
    def effaceResolution(self):
        """
        Retire de l'interfaceChoixGrille actuelle le chemin en colorant les case en bleu
        """
        chemin = self.solutionAffichee
        if chemin is None:
            exit
        else:
            widgGrille = self.gridLay
            precPt = chemin[0]
            # cas du premier point
            Scolor = COULEUR_DEF
            widgGrille.itemAtPosition(*precPt).widget().setStyleSheet(Scolor)
            for point in chemin :
                
                if point == precPt:
                    # on zappe le premier point
                    continue
                # pour chaque point ou le robot tourne
                # on reconstruit l'itineraire entre les point
                xprec,yprec = precPt
                xp,yp = point
                # cas ou on avance sur la ligne : i constant
                if yprec!=yp:
                    rangeY = range(yprec,yp) if yp>yprec else range(yp,yprec)
                    for j in rangeY :
                        widgGrille.itemAtPosition(xp,j).widget().setStyleSheet(Scolor)
                    # end for
                # cas ou on avance sur la colonne : j constant
                elif xprec!=xp:
                    rangeX = range(xprec,xp) if xp>xprec else range(xp,xprec)
                    for i in rangeX :
                        widgGrille.itemAtPosition(i,yp).widget().setStyleSheet(Scolor)
                # on prevoit le passage au point suivant
                precPt = point
            widgGrille.itemAtPosition(*point).widget().setStyleSheet(Scolor)
            self.solutionAffichee = None
            self.parent().solutionAffichee = None
        
    def sauvegardeInFile(self, sous=False):
        filename = self.parent().parent().filename
        # si aucune sauvegarde n'a été faite
        if filename is None or sous:
            fname = str(QtGui.QFileDialog(self).getSaveFileName(self, "Sauvegarder la grille",FILE_PATH)) 
            if fname=="":
                return filename
            else :
                filename = fname
            # end if
        # end if
        pbs = self.probs
        # TODO modifier pour que a la sauvegarde d'une ancienne grille avec un ensemble de grille
        # le fichier conserve autant de grilles
        obs = io.Obstacles.findObstacles(self.grille)
        orientName =  self.orientation.lower()
        orient = io.Orientations[orientName]
        prob = self.prob#io.Problem(self.grille,self.depart,self.arrivee,orient,obs)
        io.write_ProblemFile(filename,prob,True)
        self.parent().parent().isSavedFile = True
        return filename
    """
    # TODO gerer paint event pour dessiner la solution
    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()
        
    def drawLines(self, qp):
      
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)

        qp.setPen(pen)
        qp.drawLine(20, 40, 250, 40)

        pen.setStyle(QtCore.Qt.DashLine)
        qp.setPen(pen)
        qp.drawLine(20, 80, 250, 80)

        pen.setStyle(QtCore.Qt.DashDotLine)
        qp.setPen(pen)
        qp.drawLine(20, 120, 250, 120)

        pen.setStyle(QtCore.Qt.DotLine)
        qp.setPen(pen)
        qp.drawLine(20, 160, 250, 160)

        pen.setStyle(QtCore.Qt.DashDotDotLine)
        qp.setPen(pen)
        qp.drawLine(20, 200, 250, 200)

        pen.setStyle(QtCore.Qt.CustomDashLine)
        pen.setDashPattern([1, 4, 5, 4])
        qp.setPen(pen)
        qp.drawLine(20, 240, 250, 240)
    """
              
class ChoixGrille(QtGui.QWidget):
    
    def __init__(self, M, N, nbObst,parent=None, prob = None):
        super(ChoixGrille, self).__init__(parent=parent)
        self.prob = prob
        # nb de lignes de la grille
        self.M = M
        # nb de colonnes de la grille
        self.N = N
        # etat actuel selectionné pour modifier la grille
        self.etat = 0
        # point d'arrivee
        self.arrivee = (2,2)
        # point de depart
        self.depart = (0,0)
        # orientation des choix
        self.orientation = "Nord"
        # nombre d'obstacles à générer aléatoirement
        self.nbObstacles = nbObst
        # grille sauvegardée dans le fichier
        self.grille = None
        # savoir dans quel widget on est
        self.isCaract = False
        # solution generee pour la grille actuellement affichée
        self.solutionAffichee = None
        #print self.parentWidget.truc
        self.initUI()
        
    def initUI(self):
        # bouton d'obstacle, d'arrivee et de depart
        vbox = QtGui.QVBoxLayout()
        # ligne avec la grille et les bouton
        hboxGrille = QtGui.QHBoxLayout()  
        principal_box = QtGui.QVBoxLayout()

        self.setLayout(principal_box)
        
        # on cree la liste de possibilites: obstacle, arrivee ou depart
        obstBut = QtGui.QPushButton('Obstacle',self)
        obstBut.setCheckable(True)
        obstBut.setIcon(QtGui.QIcon('IMG/mur.jpg'))
        obstBut.setIconSize(QtCore.QSize(BoutonGrille.SIZE,BoutonGrille.SIZE))
        obstBut.clicked[bool].connect(self.changeEtat)
        obstBut.setToolTip(u"Obstacle : bloque le robot aux quatres intersections avec cette case")
        # depart
        depBut = QtGui.QPushButton(u'Départ',self)
        depBut.setCheckable(True)
        depBut.setIcon(QtGui.QIcon('IMG/robot.png'))
        depBut.setIconSize(QtCore.QSize(BoutonGrille.SIZE,BoutonGrille.SIZE))
        depBut.clicked[bool].connect(self.changeEtat)
        depBut.setToolTip(u"Départ : coin supérieur gauche de la case")
        # arrive
        arrBut = QtGui.QPushButton(u'Arrivée',self)
        arrBut.setCheckable(True)
        arrBut.setIcon(QtGui.QIcon('IMG/arrivee.png'))
        arrBut.setIconSize(QtCore.QSize(BoutonGrille.SIZE,BoutonGrille.SIZE))
        arrBut.clicked[bool].connect(self.changeEtat)
        arrBut.setToolTip(u"Arrivée : coin supérieur gauche de la case")
        # orientation
        combo = QtGui.QComboBox(self)
        combo.addItem("Nord")
        combo.addItem("Sud")
        combo.addItem("Est")
        combo.addItem("Ouest")
        combo.setCurrentIndex(combo.findText(self.orientation))
        combo.activated[str].connect(self.orientationChanged)
        # regeneration d'un probleme pour les memes valeurs
        generBut = QtGui.QPushButton(u'Re-Générer',self)
        generBut.setIcon(QtGui.QIcon('IMG/refresh.png'))
        generBut.setIconSize(QtCore.QSize(BoutonGrille.SIZE,BoutonGrille.SIZE))
        generBut.clicked.connect(self.regenerePb)
        generBut.setToolTip(u"Re-Génère une grille avec M={}, N={} et {} obstacles".format(self.M,self.N,self.nbObstacles))
        
        # choix du probleme parmi ceux du fichier SI ouverture
        listPBs = QtGui.QComboBox(self)
        listPBs.activated[int].connect(self.changePb)
        listPBs.hide()
        
        self.listPBs = listPBs
        self.orientCombo = combo
        self.depBut = depBut
        self.obsBut = obstBut
        self.arrBut = arrBut
        
        vbox.addStretch(1)
        vbox.addWidget(obstBut)
        vbox.addWidget(depBut)
        vbox.addWidget(arrBut)
        vbox.addWidget(combo)
        vbox.addStretch(1)
        vbox.addWidget(generBut)
        vbox.addWidget(listPBs)
        vbox.addStretch(1)

        # creation de la grille probleme
        self.grille = Grille(self.M,self.N,self.nbObstacles, self, self.prob)

        hboxGrille.addLayout(vbox)
        hboxGrille.addStretch(1)        
        hboxGrille.addWidget(self.grille)
        hboxGrille.addStretch(1)        
        
        # on suit le layout de la grille
        # pour modifications futures
        self.grilleLayout = hboxGrille
        
        principal_box.addStretch(1)
        principal_box.addLayout(hboxGrille)
        principal_box.addStretch(1)
        
        self.updateData()
        self.setMinimumSize(BoutonGrille.MIN_SIZE*self.M+30,BoutonGrille.MIN_SIZE*self.N+50)
        self.setWindowTitle('Grille')
        self.show()
        
    def changeEtat(self,pressed):
        sender = self.sender()
        
        txt = sender.text()
        if txt=='Obstacle':
            # on desactive les autres boutons
            self.arrBut.setEnabled(not pressed)
            self.depBut.setEnabled(not pressed)
            # on change l'etat courant
            val = 1 
        elif txt==u'Départ':
            # on desactive les autres boutons
            self.arrBut.setEnabled(not pressed)
            self.obsBut.setEnabled(not pressed)
            val = 2
        elif txt==u'Arrivée':
            # on desactive les autres boutons
            self.obsBut.setEnabled(not pressed)
            self.depBut.setEnabled(not pressed)
            val = 3
        
        if pressed :
            self.etat = val
        else:
            self.etat = 0
            
    def orientationChanged(self,text): 
        # si une solution a été générée 
        # on l'efface
        if not self.solutionAffichee is None:
            self.grille.effaceResolution()
        self.grille.orientation = str(text)
        self.orientation = str(text)
        
    def openedFile(self,probs):
        """
        Sauvegarde les autres problemes qui etaient contenus dans le file lors de l'ouverture dun file precis
        """
        # on enregistre les problemes
        self.probs = probs
        for i in range(len(probs)):
            self.listPBs.addItem(u"Grille n°{}".format(i+1))
        self.listPBs.show()
        
        
    def sauvegarde(self,sous=False):
        return self.grille.sauvegardeInFile(sous=sous)
        
    def resoudre(self):
        return self.grille.resoutProblem()
        
    def changePb(self, nbPb):
        # on change le probleme courant
        self.prob = self.probs[nbPb]
        # on genere l'affichage
        self.setPb()
        
        
    def regenerePb(self):
        self.prob = None
        self.setPb()
        
    def setPb(self):        
        # on supprime l'ancienne grille
        self.grilleLayout.removeWidget(self.grille)
        self.grille.deleteLater()
        self.grille = Grille(self.M,self.N,self.nbObstacles, self, self.prob)
        self.grilleLayout.addWidget(self.grille)
        self.updateData()
        self.update()
        
    def updateData(self):
        grille = self.grille
        self.M = grille.M
        self.N = grille.N
        self.nbObstacles = grille.nbObstacles
        self.depart = grille.depart
        self.arrivee = grille.arrivee
        
        
        
class MaWindow(QtGui.QMainWindow):
    
    def __init__(self,parent=None):
        super(MaWindow, self).__init__()
        self.M = 0
        self.N = 0
        self.nbObstacles = 0
        self.depart = None
        self.arrivee = None
        self.filename = None
        self.isSavedFile = False
        choice_widget = CaractGrille(self.statusBar(),self)
        choice_widget.validButton.clicked.connect(self.validCaract)        
        self.setCentralWidget(choice_widget)
        self.initUI()
        
    def initUI(self):  
        wMax = QtGui.QDesktopWidget().availableGeometry().width()-200
        hMax = QtGui.QDesktopWidget().availableGeometry().height()-200
        self.setMaximumSize(wMax,hMax)
        # menu nouvelle grille
        newAction = QtGui.QAction('&Nouveau', self)        
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('Nouvelle grille aléatoire')
        newAction.triggered.connect(self.nouvFile)
        
        # menu ouvrir probleme
        openAction = QtGui.QAction('&Ouvrir',self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip(u'Ouvre une grille déjà existante')
        openAction.triggered.connect(self.openGrille)
        
        # mmenu exit
        exitAction = QtGui.QAction('&Quitter', self)        
        exitAction.setShortcut(QtCore.Qt.Key_Escape)
        exitAction.setStatusTip('Quitte l\'application')
        exitAction.triggered.connect(QtGui.qApp.quit)
        
        # menu sauvegarde
        sauvAction = QtGui.QAction('&Sauver',self)
        sauvAction.setShortcut('Ctrl+S')
        sauvAction.setStatusTip("Sauvegarde la grille")
        sauvAction.triggered.connect(self.sauvegarderGrille)
        # menu sauvegarde sous
        sauvSousAction = QtGui.QAction('&Sauver sous',self)
        sauvSousAction.setShortcut('Ctrl+Shift+S')
        sauvSousAction.setStatusTip("Sauvegarde la grille sous")
        sauvSousAction.triggered.connect(self.sauvegarderGrilleSous)
        
        # menu generation de la solution
        resoutAction = QtGui.QAction(u'&Résoudre',self)
        resoutAction.setShortcut(QtCore.Qt.Key_F4)
        resoutAction.setToolTip(u'Résout la grille avec sauvegarde de la grille et de la solution')
        resoutAction.triggered.connect(self.resoudreGrille)
        
        # menu
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)
        
        optionGrille = menubar.addMenu('&Options')
        optionGrille.addAction(sauvAction)
        optionGrille.addAction(sauvSousAction)
        optionGrille.addAction(resoutAction)
        
        # on force la taille max a celle de l'ecran
        screen = QtGui.QDesktopWidget().screenGeometry()
        wScr = screen.width()
        hScr = screen.height()
        self.setMaximumSize(wScr,hScr)
        # on force la taille actuelle
        self.resize(400,400)
        self.setWindowTitle('Fenetre Principale')
        self.show()
        self.center()
         
    def updateDatas(self):
        grille = self.centralWidget()        
        self.M = grille.M
        self.N = grille.N
        self.nbObstacles = grille.nbObstacles
        self.depart = grille.depart
        self.arrivee = grille.arrivee
        
    def validCaract(self):
        # on recupere M,N et filename du children CaractGrille
        self.M = self.centralWidget().M
        self.N = self.centralWidget().N
        # on verifie que le nombre d'obstacles choisi n'est pas trop grand
        self.nbObstacles = self.centralWidget().nbObstacles
        # on cree le prochain panel (ChoixGrille) avec les M et N entrés précédemment
        grille_widget = ChoixGrille(self.M,self.N,self.nbObstacles,self)
        self.setCentralWidget(grille_widget)
        self.updateDatas()
        self.resizeEvent(QtCore.QEvent(QtCore.QEvent.Resize))
        
    def sauvegarderGrille(self):
        widg = self.centralWidget()
        if widg.isCaract:
            QtGui.QMessageBox.critical(self,"Sauvegarde impossible",u"Pas de sauvegarde possible.\nAucune grille entrée")
            exit
        # sinon
        else:
            self.filename = widg.sauvegarde()
            self.statusBar().showMessage(u"Sauvegarde de {} effectuée".format(self.filename))

    def sauvegarderGrilleSous(self):
        widg = self.centralWidget()
        if widg.isCaract:
            QtGui.QMessageBox.critical(self,"Sauvegarde impossible",u"Pas de sauvegarde possible.\nAucune grille entrée")
            exit
        # sinon
        else:
            self.filename = widg.sauvegarde(True)
            self.isSavedFile = not self.filename is None
            self.statusBar().showMessage(u"Sauvegarde de {} effectuée".format(self.filename))

    def resoudreGrille(self):
        widg = self.centralWidget()
        if widg.isCaract:
            exit
        # sinon
        else :
            self.statusBar().showMessage(u"Résolution de la grille en cours")
            # on recupere le chemin generé
            resolu = widg.resoudre()
            if resolu is None:
                self.statusBar().showMessage(u"Aucune solution trouvée")
                QtGui.QMessageBox.information(self,u'Solution',u'<font color=\"red\">Aucune solution trouvée</font>')
            else:
                self.statusBar().showMessage(u"Grille résolue : {}".format(resolu))
                QtGui.QMessageBox.information(self,u'Solution',u'<font color=\"green\">Solution trouvée : {}</font>'.format(resolu))
        
    def nouvFile(self):
        choice_widget = CaractGrille(self.statusBar(),self)
        choice_widget.validButton.clicked.connect(self.validCaract)        
        self.setCentralWidget(choice_widget)

    def openGrille(self):
        # on recupere le nom de la grille avec un QInputDialog
        fname = str(QtGui.QFileDialog.getOpenFileName(self, 'Ouvrir Fichier', 
                FILE_PATH))
        # si aucun nom sélectionné
        if fname=="":
            return None
        
        # on genere la grille
        probs = io.read_file(fname)
        if probs is None:
            QtGui.QMessageBox.critical(self,u"Fichier {} invalide".format(fname),u"Le fichier entré génère des erreurs et ne renvoie rien de bon")
            return None
        #for p in probs:
        # on cree le prochain panel (ChoixGrille) avec les M et N entrés précédemment
        chgrille_widget = ChoixGrille(probs[0].nbLigne,probs[0].nbCol,0,self, probs[0])
        self.setCentralWidget(chgrille_widget)
        chgrille_widget.openedFile(probs)
        self.filename = fname
        self.updateDatas()
        
    def keyPressEvent(self, e):
        
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        # si l'utilisateur appuie sur entrée alors qu'on est dans CaractGrille
        elif e.key() == QtCore.Qt.Key_Return and self.centralWidget().isCaract:
            self.validCaract()
        
    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
    def closeEvent(self, event):
        # si on etait sur le Widget CaractGrille, rien a faire
        if not self.centralWidget().isCaract and not self.isSavedFile:
            # sinon il faut PEUT ETRE sauvegarder la grille
            reply = QtGui.QMessageBox.question(self, 'Message',
                "Voulez vous sauvegarder la grille en cours?", QtGui.QMessageBox.Yes | 
                QtGui.QMessageBox.No|QtGui.QMessageBox.Cancel, QtGui.QMessageBox.No)
    
            # on lance la sauvegarde si l'utilisateur a cliqué oui
            if reply == QtGui.QMessageBox.Yes:
                self.sauvegarderGrille()
                # puis on quitte
                event.accept()
            # on annule si l'utilisateur a cliqué cancel
            if reply == QtGui.QMessageBox.Cancel:
                event.ignore()
        else:
            # sinon on quitte sans soucis
            event.accept()
            
    def resizeEvent(self,resizeEvent):
        if self.centralWidget().isCaract :
            self.resize(400,400)
        else:
            self.setMinimumSize(BoutonGrille.MIN_SIZE*self.M+CONST_TAILLE,BoutonGrille.MIN_SIZE*self.N+CONST_TAILLE)
        self.center()
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    w = MaWindow()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
