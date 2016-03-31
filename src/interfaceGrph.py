#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import gestDict as dic
import gestIO as io
import os
from tools import ABS_PATH_PRINC
from PyQt4 import QtGui, QtCore

WINDOW_DEF_SIZE = 600

M_MIN = 3
M_MAX = 20
N_MIN = 3
N_MAX = 20

NOIRES_MIN = 0
NOIRES_MAX = 0
E_OBST = 20
VAL_MINMAX_OBST = M_MIN*N_MIN-4
VAL_MAX_OBST = 30

GRID_PATH = ABS_PATH_PRINC+'/data/Grilles'

COULEUR_PATH = "background-color: blue"
COULEUR_NOIRE = "background-color: black"
COULEUR_DEF = "background-color: white"

class CaractGrille(QtGui.QWidget):
    """
    Widget/Panel pour choisir M,N et le nom du fichier avant de determiner les obstacles
    """
    
    def __init__(self, statusBar,parent=None):
        super(CaractGrille, self).__init__(parent=parent)
        self.statusBar = statusBar
        self.lignes = M_MIN
        self.colonnes = M_MAX
        self.nbCasesNoires = NOIRES_MIN
        self.validButton = QtGui.QPushButton("Formulaire Valide")
        self.isCaract = True
        # Taille par defaut
        MaWindow.HEIGHT = MaWindow.WIDTH = WINDOW_DEF_SIZE
        self.initUI()
        
    def initUI(self):
        
        vbox = QtGui.QVBoxLayout()

        nbLignesLbl = QtGui.QLabel('Nombre de lignes')
        nbColsLbl = QtGui.QLabel('Nombre de colonnes')
        self.nbNoiresLbl = QtGui.QLabel('Nombre de cases noires')
        
        nbLignesSlider = QtGui.QSlider(QtCore.Qt.Horizontal,self)
        nbLignesSlider.setToolTip("Entier compris entre {} et {}".format(M_MIN,M_MAX))
        nbColsSlider = QtGui.QSlider(QtCore.Qt.Horizontal,self)
        nbColsSlider.setToolTip("Entier compris entre {} et {}".format(N_MIN,N_MAX))
        self.nbNoiresSlider = QtGui.QSlider(QtCore.Qt.Horizontal,self)
        self.nbNoiresSlider.setToolTip("Entier compris entre {} et {}".format(0,NOIRES_MAX))
        
        nbColsSlider.valueChanged[int].connect(self.changeColsValue)
        nbColsSlider.setRange(N_MIN,N_MAX)
        nbLignesSlider.valueChanged[int].connect(self.changeLignsValue)
        nbLignesSlider.setRange(M_MIN,M_MAX)
        self.nbNoiresSlider.valueChanged[int].connect(self.changeNbNoiresValue)
        self.nbNoiresSlider.setRange(NOIRES_MIN,NOIRES_MAX)
        
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(nbLignesLbl, 1, 0)
        grid.addWidget(nbLignesSlider, 1, 1)

        grid.addWidget(nbColsLbl, 2, 0)
        grid.addWidget(nbColsSlider, 2, 1)

        grid.addWidget(self.nbNoiresLbl, 3, 0)
        grid.addWidget(self.nbNoiresSlider, 3, 1)

        
        vbox.addLayout(grid)
        
        # genere aleatoirement
        okButton = QtGui.QPushButton("OK")
        okButton.setToolTip(u"Génère aléatoirement un une grille de mots croisés")
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
        
    def changeLignsValue(self,value):
        self.lignes = value
        global NOIRES_MAX        
        NOIRES_MAX = max(VAL_MINMAX_OBST,min(VAL_MAX_OBST,value*self.colonnes-E_OBST))
        self.nbNoiresSlider.setToolTip("Entier compris entre {} et {}".format(NOIRES_MIN,NOIRES_MAX))
        self.nbNoiresSlider.setRange(NOIRES_MIN,NOIRES_MAX)
        self.statusBar.showMessage("{} lignes, {} colonnes, {} cases noires".format(self.lignes,self.colonnes,self.nbCasesNoires))

    def changeColsValue(self,value):
        self.colonnes = value
        global NOIRES_MAX        
        NOIRES_MAX = max(VAL_MINMAX_OBST,min(VAL_MAX_OBST,value*self.lignes-E_OBST))
        self.nbNoiresSlider.setToolTip("Entier compris entre {} et {}".format(NOIRES_MIN,NOIRES_MAX))
        self.nbNoiresSlider.setRange(NOIRES_MIN,NOIRES_MAX)
        self.statusBar.showMessage("{} lignes, {} colonnes, {} cases noires".format(self.lignes,self.colonnes,self.nbCasesNoires))

    def changeNbNoiresValue(self,value):
        self.nbCasesNoires  = value
        self.statusBar.showMessage("{} lignes, {} colonnes, {} cases noires".format(self.lignes,self.colonnes,self.nbCasesNoires))

class BoutonGrille(QtGui.QPushButton):
    SIZE = 25
    def __init__(self,coord,parent=None):
        super(BoutonGrille,self).__init__(parent)
        self.coordonnees = coord
        # c'est une case noire
        self.isBlack = False
        self.setFixedSize(self.SIZE,self.SIZE)
        self.setStyleSheet(COULEUR_DEF)
        self.initUI()
        
    def initUI(self):
        """        
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy)
        """
        pass
                
    def stateChange(self,noire):
        """
        Definit si la case est l'arrivee, le depart, un ostacle ou une simple case
        etat = 1 pour une case noire
        """
        self.isBlack = noire
        if noire:
            self.setStyleSheet(COULEUR_NOIRE)
        else:
            self.setStyleSheet(COULEUR_DEF)
            
    def __str__(self):
        string = ""
        if self.isBlack :
            string+= "Black : "
        else :
            string+= "Case : "
        i,j = self.coordonnees
        string+="(ligne={},colonne={});".format(i,j)
        return string
        
class ChoixGrille(QtGui.QWidget):
    
    def __init__(self, lign, cols, nbNoires, wordGrid = None, parent=None):
        super(ChoixGrille, self).__init__(parent=parent)
        self.dico = parent.dico
        # objet GrilleMots
        self.wordGrid = wordGrid
        # nb de lignes de la grille
        self.lignes = lign
        # nb de colonnes de la grille
        self.colonnes = cols
        # etat actuel selectionné pour modifier la grille (0:blanc;1:noire)
        self.etat = 0
        # nombre de cases noires à générer aléatoirement
        self.nbCasesNoires = nbNoires
        # grille de 0 et de 1 sauvegardée dans le fichier
        self.grille = None
        # savoir dans quel widget on est
        self.isCaract = False
        # solution generee pour la grille actuellement affichée
        self.solutionAffichee = None
        # options pour lire des multi-grid-file
        self.nbGridz = 0
        self.numGrid = 0
        self.gridz = None
        # on resize le parent pour recuperer les bonnes tailles
        self.resizeParent()
        self.initUI()
        
    def initUI(self):
        principal_box = QtGui.QHBoxLayout(self)

        topleft = QtGui.QFrame(self)
        topleft.setFrameShape(QtGui.QFrame.StyledPanel)
 
        bottomleft = QtGui.QFrame(self)
        bottomleft.setFrameShape(QtGui.QFrame.StyledPanel)

        right = QtGui.QFrame(self)
        right.setFrameShape(QtGui.QFrame.StyledPanel)

        splitter1 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter1.addWidget(topleft)
        splitter1.addWidget(bottomleft)
        
        splitter2 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(right)
        
        splitter1.setSizes([self.parent().height()/4.,self.parent().height()*3/4.])
        splitter2.setSizes([self.parent().width()/3.,self.parent().width()*2/3.])
        
        
        principal_box.addWidget(splitter2,1)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        
        # bouton d'obstacle, d'arrivee et de depart
        vbox = QtGui.QVBoxLayout()
        
        self.setLayout(principal_box)
        
        # on cree la liste de possibilites: case noire ou résolution
        noireBut = QtGui.QPushButton('Case Noire',self)
        noireBut.setCheckable(True)
        noireBut.setIconSize(QtCore.QSize(BoutonGrille.SIZE,BoutonGrille.SIZE))
        noireBut.clicked[bool].connect(self.changeEtat)
        noireBut.setToolTip(u"Case Noire : ne peut contenir aucune lettre")
        
        self.noireBut = noireBut
        
        vbox.addWidget(noireBut)
        topleft.setLayout(vbox)
        
        # generation de la grille        
        if self.wordGrid is None:
            # on genere aléatoirement une grille avec les parametres precedemment entres
            # le nombre d'obstacles, le depart et l'arrivee pourront etre modifiés a tout moment
            self.genereGrille()
        else:
            # on recupere le 1er objet grille de la liste
            self.gridz = self.wordGrid
            self.wordGrid = self.wordGrid[0]
            self.numGrid = 0
            self.nbGridz = len(self.gridz)
            self.affichGrille(self.wordGrid)

        # layout compliqués pour que les point de la grille se serrent entre eux
        vLayout = QtGui.QVBoxLayout()
        hLayout = QtGui.QHBoxLayout()
        # on centre la grille dans son espace
        hLayout.addStretch(1)
        hLayout.addLayout(self.gridLay)
        hLayout.addStretch(1)
        vLayout.addStretch(1)
        vLayout.addLayout(hLayout)
        vLayout.addStretch(1)
        # fin layout compliqué

        right.setLayout(vLayout)
        
        wmax = self.parent().width()
        hmax = self.parent().height()
        self.setMaximumSize(wmax,hmax)
        self.setWindowTitle('Grille')
        self.show()
        
    def genereGrille(self):
        # on genere une grille de mots aleatoirement
        self.grilleMots = io.GrilleMots.genere_grid(self.lignes,self.colonnes,self.nbCasesNoires)
        # on recupere la grille
        self.grille = self.grilleMots.grille
        
        # une seule grille => pas d'option multi
        self.nbGridz = 1
        self.numGrid = 0
        # remplissage du gridLayout
        grid = QtGui.QGridLayout()
        butt = []
        for i in range(self.lignes):
            l = []
            for j in range(self.colonnes):
                button = BoutonGrille((i,j),self)
                button.setMaximumSize(BoutonGrille.SIZE,BoutonGrille.SIZE)
                button.setBaseSize(20,20)    
                grid.setColumnMinimumWidth(j,BoutonGrille.SIZE)
                grid.addWidget(button, i,j)
                button.clicked.connect(self.clicked)
                button.setStatusTip(button.__str__())
                
                # si ce point est un obstacle
                if self.grille[i,j]==1:
                    button.stateChange(1)
                # end if
                l.append(button)
            # end first for
            butt.append(l)
            grid.setRowMinimumHeight(i,BoutonGrille.SIZE)
        # end 2e for
        grid.setSpacing(0)
        self.gridLay = grid
        
    def resizeParent(self):
        caseCols = self.colonnes
        caseLigns = self.lignes
        tailleBut = BoutonGrille.SIZE
        # on recupere la nouvelle taille
        MaWindow.WIDTH = MaWindow.MARGE + caseCols*tailleBut
        MaWindow.HEIGHT = MaWindow.MARGE + caseLigns*tailleBut
         
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
        
        etat = self.etat
        caseNoire = sender.isBlack
        # c'est une case noire
        if etat==1:
            # si une case noire peut etre posee ici alors on la pose
            # si x ne vaut pas ligne max et y ne vaut pas colonnes max
            # ie si on n'est pas sur une des cases contenant un rail mais pas d'obstacle
            if (x<self.lignes and y<self.colonnes):
                # on met la case en noire ou blanche selon son etat precedent
                if caseNoire:
                    self.grille[x][y] = 0
                else:
                    self.grille[x][y] = 1
                    sender.stateChange(self.grille[x,y]==1)
            else:
                QtGui.QMessageBox.warning(self,"Mouvement impossible",u"Une case noire ne peut être posé en ({},{})".format(x,y))

    def changeEtat(self,pressed):
        sender = self.sender()
        
        txt = sender.text()
        if txt==u'Case Noire':
            # on change l'etat courant
            if pressed :
                self.etat = 1
            else:
                self.etat = 0
        
    def sauvegardeInFile(self, sous=False):
        filename = self.parent().filename
        # si aucune sauvegarde n'a été faite
        if filename is None or sous:
            filename = str(QtGui.QFileDialog(self).getSaveFileName(self, "Sauvegarder la grille")) 
        if filename=="":
            return self.parent().filename
        self.grilleMots = io.GrilleMots(self.grille,self.lignes,self.colonnes)
        # TODO write file grille
        if self.nbGridz==1:
            io.write_GrilleFile(filename,[self.grilleMots],True)
        else:
            io.write_GrilleFile(filename,self.gridz,True)
        self.parent().isSavedFile = True
        return filename
        
    def resoutProblem(self):
        # si une solution a été générée 
        # on l'efface
        if not self.solutionAffichee is None:
            self.effaceResolution()
        # recuperation d'un nouvel objet grille car il y a peut etre eu des modif
        self.grilleMots = io.GrilleMots(self.grille,self.lignes,self.colonnes)
        # recuperation du dictionnaire
        if self.dico == {}:
            self.chooseDico()
        return None
        
        # resolution de la grille
        # generation de la solution
        # TODO : io.algos.Algorithm(prob)
        ####### recuperation de la solution
        filename = self.parent().filename
        # si aucune sauvegarde n'a été faite
        # sauvegarde de la solution dans un fichier
        if filename is None:
            # recuperation du nom de fichier solution
            dialog = QtGui.QInputDialog()
            filename, ok = dialog.getText(self, 'Fichier Sauvegarde', 
                                                      'Nom du fichier sauvergarde')             
        else:
            reply = QtGui.QMessageBox.question(self,u"Sauvegarde",u"Voulez-vous écraser l'ancienne grille {} et sauvegarder la solution?".format(filename),QtGui.QMessageBox.Yes | 
                QtGui.QMessageBox.No|QtGui.QMessageBox.Cancel, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                ok=True
            elif reply == QtGui.QMessageBox.Cancel:
                QtGui.QMessageBox.information(self,u'Résolution annulée',u'La résolution du problème {} a été annulée'.format(filename))
                return None
            else:
                ok=False
        # on traite la reponse
        # TODO : resoudre + write solution file
        return None
        if ok:
            io.write_ProblemFile(filename,prob)
            io.write_SolutionFile(filename,[prob])
            self.parent().isSavedFile = True
            self.parent().filename = filename
        solution = prob.solutionNoeud
        self.solutionAffichee = solution
        self.affichResolution()
        return solution
        
    def affichResolution(self):
        """
        Affiche sur l'interfaceChoixGrille actuelle le chemin en colorant les case en bleu
        """
        # TODO : resoudre
        return None
        
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
        # TODO : resoudre
        return None
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
    
    def affichGrille(self,grid):
        # on recupere la grille
        self.grille = grid.grille
        self.lignes = grid.height
        self.colonnes = grid.width
        # remplissage du gridLayout
        grid = QtGui.QGridLayout()
        butt = []
        for i in range(self.lignes):
            l = []
            for j in range(self.colonnes):
                button = BoutonGrille((i,j),self)
                button.setMaximumSize(BoutonGrille.SIZE,BoutonGrille.SIZE)
                button.setBaseSize(20,20)    
                grid.setColumnMinimumWidth(j,BoutonGrille.SIZE)
                grid.addWidget(button, i,j)
                button.clicked.connect(self.clicked)
                button.setStatusTip(button.__str__())
                
                # si ce point est une case noire
                if i<self.lignes and j<self.colonnes and self.grille[i,j]==1:
                    button.stateChange(1)
                # end if
                l.append(button)
            # end first for
            butt.append(l)
            grid.setRowMinimumHeight(i,BoutonGrille.SIZE)
        # end 2e for
        grid.setSpacing(0)
        self.gridLay = grid
     
    def chooseDico(self):
        # on recupere le nom de la grille avec un QInputDialog
        fname = str(QtGui.QFileDialog.getOpenFileName(self, 'Choisir Dictionnaire',dic.DICO_PATH))
        fname =  os.path.basename(fname)
        # si aucun nom sélectionné
        if fname=="":
            QtGui.QMessageBox.critical(self,u"truc Fichier {} invalide".format(fname),u"Le fichier choisi est le fichier par défaut {}".format(dic.DICT_FNAME))
            fname = None
        # on recupere le dico
        try:
            dic.recupDictionnaire([fname])
        except Exception:
            dic.recupDictionnaire([dic.DICT_DEF])
            QtGui.QMessageBox.critical(self,u"Fichier {} invalide".format(fname),u"Le fichier choisi est le fichier par défaut {}".format(dic.DICT_FNAME))
        self.dico = dic.DICTIONNAIRE
        #print self.dico
        
                 
class MaWindow(QtGui.QMainWindow):
    MARGE = 200
    WIDTH = WINDOW_DEF_SIZE
    HEIGHT = WINDOW_DEF_SIZE
    
    def __init__(self,parent=None):
        super(MaWindow, self).__init__()
        self.dico = dic.DICTIONNAIRE
        self.lignes = 0
        self.colonnes = 0
        self.nbCasesNoires  = 0
        self.nbVariables = 0
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
        
        # menu changement de dictionnaire
        changeDicAction = QtGui.QAction('&Changer le dictionnaire courant',self)
        changeDicAction.setShortcut('Ctrl+Shift+D')
        changeDicAction.setStatusTip("Change le dictionnaire courant")
        changeDicAction.triggered.connect(self.changeDico)
        
        # menu changement de dictionnaire
        addDicAction = QtGui.QAction('&Sauve sous',self)
        addDicAction.setShortcut('Ctrl+Shift+S')
        addDicAction.setStatusTip("Change le dictionnaire courant")
        addDicAction.triggered.connect(self.addDico)
        
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
        
        # TODO : choix du dictionnaire
        toolGrille = menubar.addMenu('&Outils')
        toolGrille.addAction(changeDicAction)
 #       toolGrille.addAction(sauvSousAction)
        toolGrille.addAction(resoutAction)
        
        self.setWindowTitle(u'Mes Mots Croisés')
        self.show()
        self.resizing()
        self.center()
         
    def validCaract(self):
        # on recupere M,N et filename du children CaractGrille
        self.lignes = self.centralWidget().lignes
        self.colonnes = self.centralWidget().colonnes
        # on verifie que le nombre d'obstacles choisi n'est pas trop grand
        self.nbCasesNoires  = self.centralWidget().nbCasesNoires
        # on cree le prochain panel (ChoixGrille) avec les nb lignes et nb colonnes entrés précédemment
        grille_widget = ChoixGrille(self.lignes,self.colonnes,self.nbCasesNoires, None, self)
        self.setCentralWidget(grille_widget)
        self.resizing()
        self.center()
        sys.stdout.write("grille {}*{} avec {} cases noires".format(self.lignes,self.colonnes,self.nbCasesNoires))
        
    def changeDico(self):
        pass
    
    def addDico(self):
        pass
    
    def sauvegarderGrille(self):
        widg = self.centralWidget()
        if widg.isCaract:
            QtGui.QMessageBox.critical(self,"Sauvegarde impossible",u"Pas de sauvegarde possible.\nAucune grille entrée")
            exit
        # sinon
        else:
            self.filename = widg.sauvegardeInFile()
            self.statusBar().showMessage(u"Sauvegarde de {} effectuée".format(self.filename))

    def sauvegarderGrilleSous(self):
        widg = self.centralWidget()
        if widg.isCaract:
            QtGui.QMessageBox.critical(self,"Sauvegarde impossible",u"Pas de sauvegarde possible.\nAucune grille entrée")
            exit
        # sinon
        else:
            self.filename = widg.sauvegardeInFile(True)
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
            resolu = widg.resoutProblem()
            if resolu is None:
                self.statusBar().showMessage(u"Aucune solution trouvée")            
            else:
                self.statusBar().showMessage(u"Grille résolue : {}".format(resolu))
        
    def nouvFile(self):
        choice_widget = CaractGrille(self.statusBar(),self)
        choice_widget.validButton.clicked.connect(self.validCaract)        
        self.setCentralWidget(choice_widget)
        self.resizing()
        self.center()
        
    def openGrille(self):
        # on recupere le nom de la grille avec un QInputDialog
        fname = str(QtGui.QFileDialog.getOpenFileName(self, 'Ouvrir Fichier',io.GRID_PATH))
        # si aucun nom sélectionné
        if fname=="":
            return None
        
        # on genere la grille
        try:
            gridz = io.read_file(fname)
        except:
            gridz = None
        if gridz is None:
            QtGui.QMessageBox.critical(self,u"Fichier {} invalide".format(fname),u"Le fichier entré génère des erreurs et ne renvoie rien de bon")
            return None
        #for p in probs:
        # on cree le prochain panel (ChoixGrille) avec les M et N entrés précédemment
        grille_widget = ChoixGrille(self.lignes,self.colonnes,self.nbCasesNoires, gridz, self)
        self.setCentralWidget(grille_widget)
        self.filename = fname
        self.resizing()
        self.center()

    def keyPressEvent(self, e):
        
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        # si l'utilisateur appuie sur entrée alors qu'on est dans CaractGrille
        elif e.key() == QtCore.Qt.Key_Return and self.centralWidget().isCaract:
            self.validCaract()
           
    def resizing(self):
        # on resize si la taille doit changer selon la grille
        self.setFixedSize(self.WIDTH,self.HEIGHT)
            
    def center(self):
        self.move(QtGui.QDesktopWidget().availableGeometry().center() - self.frameGeometry().center())
        
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

def main():
    
    app = QtGui.QApplication(sys.argv)
    w = MaWindow()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
