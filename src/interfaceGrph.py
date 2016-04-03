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

class TaskThread(QtCore.QThread):
    taskFinished = QtCore.pyqtSignal()
    def __init__(self,solv,ac3=False,fc=True,cbj=False):
        QtCore.QThread.__init__(self)
        self.solv=solv
        self.ac3 = ac3
        self.fc = fc
        self.cbj = cbj
    
    def run(self):
        self.solv.run(ac3=self.ac3,fc=self.fc,cbj=self.cbj)

        self.taskFinished.emit()  


class ChoixSolverDialog(QtGui.QDialog):
    def __init__(self,parent=None):
        super(ChoixSolverDialog, self).__init__(parent=parent)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Dialog")
        vbox = QtGui.QVBoxLayout()
        # choix avec ou sans ac3
        self.groupAc3 = QtGui.QGroupBox("AC3",self)
        self.ravecAc3 = QtGui.QCheckBox('Avec AC3', self)
        self.ravecAc3.setChecked(False)
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(self.ravecAc3)
        hbox1.addStretch(1)
        self.groupAc3.setLayout(hbox1)
        
        # choix de l'algo:
        self.groupAlgo = QtGui.QGroupBox("Algorithme",self)
        self.rfc = QtGui.QRadioButton("Forward Checking")
        self.rcbj = QtGui.QRadioButton("Conflict Back Jumping")
        self.rfc.setChecked(True)
        vbox2 = QtGui.QVBoxLayout()
        vbox2.addStretch(1)
        vbox2.addWidget(self.rfc)
        vbox2.addWidget(self.rcbj)
        vbox2.addStretch(1)
        self.groupAlgo.setLayout(vbox2)
        
        # valid button
        self.valid = QtGui.QPushButton("Valider")
        self.valid.connect(self.valid, QtCore.SIGNAL('clicked()'), self.choixSolver)
        self.cancel = QtGui.QPushButton("Annuler")
        self.cancel.connect(self.cancel, QtCore.SIGNAL('clicked()'), self.close)
        hbox3 = QtGui.QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(self.valid)
        hbox3.addWidget(self.cancel)
        hbox3.addStretch(1)
        vbox.addStretch(1)
        vbox.addWidget(self.groupAc3)
        vbox.addWidget(self.groupAlgo)
        vbox.addLayout(hbox3)
        vbox.addStretch(1)
        self.setLayout(vbox)
        return None
        
    def choixSolver(self):
        if self.sender()==self.valid:
            self.with_ac3 = self.ravecAc3.isChecked()
            self.with_cbj = self.rcbj.isChecked()
            self.with_fc = self.rfc.isChecked()
            self.close()
            self.parent().genereResolution(self)
            
   
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
        
class GridObject(QtGui.QWidget):
    MARGE = 100
    def __init__(self, wordGrid,papa=None, parent=None):
        super(GridObject, self).__init__(parent=parent)
        # objet GrilleMots
        self.wordGrid = wordGrid
        # nb de lignes de la grille
        self.lignes = wordGrid.height
        # nb de colonnes de la grille
        self.colonnes = wordGrid.width
        # grille de 0 et de 1 sauvegardée dans le fichier
        self.grille = wordGrid.grille
        # on recupere l'objet choixgrille parent
        self.papaWidg = papa
        
        self.initUI()
        
    def initUI(self):
        self.gridLay = QtGui.QGridLayout()
        
        # generation de la grille        
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
        
        self.setLayout(vLayout)
        width = self.colonnes*BoutonGrille.SIZE+self.MARGE
        height = self.lignes*BoutonGrille.SIZE+self.MARGE

        self.setFixedSize(width,height)
        self.show()
        
    def affichGrille(self,gridO):
        self.lignes = gridO.height
        self.colonnes = gridO.width
        # on recupere la grille
        self.grille = gridO.grille
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
                if self.grille[i,j]==1:
                    button.stateChange(1)
                # end if
                l.append(button)
            # end first for
            butt.append(l)
            grid.setRowMinimumHeight(i,BoutonGrille.SIZE)
        # end 2e for
        grid.setSpacing(0.5)
        self.buttons = butt
        self.gridLay = grid
     
    def clicked(self):
        self.papaWidg.clicked(self.sender())
    
    def afficheResolution(self):
        """
        Affiche sur l'interfaceChoixGrille actuelle le chemin en colorant les case en bleu
        """
            
        if not self.wordGrid.solution:
            return False
        # sinon on recupere les variables generees par la solution
        solutions = self.wordGrid.variables
        for num,((iv,jv),taille,orient,val) in solutions.items():
            # si la variable est verticale on arrete
            if orient==io.Orientation.VERTICAL:
                break
            # on ecrit lettre par lettre la valeur en string de la variable
            for ind in range(taille):
                # TODO : cas inimaginable?!
                if val is None:
                    return False
                self.buttons[iv][jv+ind].setText(val[ind])
                # end if
            # end for
        # end for
        return True
         
    def effaceResolution(self):
        print self.buttons
        # on remet les cases blanches en blanc (ie sans lettre dessus)
        for butt in self.buttons:
            # si ce n'est pas une case noire
            if not butt.isBlack:
                # on le met a blanc
                butt.setText("")
        
        
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
        self.modifiee = False
        self.initUI()
        
    def initUI(self):
        principal_box = QtGui.QHBoxLayout(self)
        self.gridLayout = QtGui.QGridLayout()
        topleft = QtGui.QFrame(self)
        topleft.setFrameShape(QtGui.QFrame.StyledPanel)
 
        bottomleft = QtGui.QFrame(self)
        bottomleft.setFrameShape(QtGui.QFrame.StyledPanel)
        
        ### liste des dico a utiliser
        dicsLay = QtGui.QHBoxLayout()
        bottomleft.setLayout(dicsLay)
        self.listDicsWidg = QtGui.QListWidget()
        self.listDicsWidg.itemActivated.connect(self.removeAction)
        dicsLay.addWidget(self.listDicsWidg)
        for f in self.parent().listDics:
            item = QtGui.QListWidgetItem(f)
            self.listDicsWidg.addItem(item)
        
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
            # on recupere la grille correspondante:
            self.grille = self.wordGrid.grille.copy()
            self.lignes = self.wordGrid.height
            self.colonnes = self.wordGrid.width

        # dans les deux cas on affiche la grille
        self.gridWidget = GridObject(self.wordGrid,papa=self,parent=self)
        
        # on liste toutes les grilles du fichier ouvert ou creees
        combo = QtGui.QComboBox(self)
        for i in range(self.nbGridz):
            combo.addItem('Grille {}'.format(i+1))
        #combo.setCurrentIndex(combo.findText(self.numGrid))
        combo.activated[str].connect(self.changeGridView)
        
        self.gridCombo = combo
        vbox.addWidget(self.gridCombo)
        
        self.gridLayout.addWidget(self.gridWidget)

        right.setLayout(self.gridLayout)
        
        wmax = self.parent().width()
        hmax = self.parent().height()
        self.setMaximumSize(wmax,hmax)
        self.setWindowTitle('Grille')
        self.show()
        
    def removeAction(self):
        self.parent().removeDico()
        
    def genereGrille(self):
        # on genere une grille de mots aleatoirement
        self.wordGrid = io.GrilleMots.genere_grid(self.lignes,self.colonnes,self.nbCasesNoires)
        # on recupere la grille
        self.grille = self.wordGrid.grille.copy()
        
        # une seule grille => pas d'option multi
        self.gridz = [self.wordGrid]
        self.nbGridz = 1
        self.numGrid = 0
        return None        
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
        self.gridLayout = grid
        
    def resizeParent(self):
        caseCols = self.colonnes
        caseLigns = self.lignes
        tailleBut = BoutonGrille.SIZE
        # on recupere la nouvelle taille
        MaWindow.WIDTH = MaWindow.MARGE + caseCols*tailleBut
        MaWindow.HEIGHT = MaWindow.MARGE + caseLigns*tailleBut
         
    def clicked(self,sender):
        """
        Fonction appelée au clic sur un bouton de la grille
        """
        # si une solution a été générée 
        # on l'efface
        
        if self.solutionAffichee :
            self.effaceResolution()
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
            # on met la case en noire ou blanche selon son etat precedent
            if caseNoire:
                self.grille[x][y] = 0
            else:
                self.grille[x][y] = 1
            self.modifiee=True
            sender.stateChange(self.grille[x,y]==1)
                
    def changeGridView(self,text):
        text = str(text).split()
        num = int(text[1])-1
        # si c'est le meme numero, on ne change rien
        # ou s'il y a un soucis et que la grille num n'existe pas on ne fait rien
        if num!=self.numGrid and num<self.nbGridz:
            self.switchGrille(num)
        
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
            filename = str(QtGui.QFileDialog(self).getSaveFileName(self, "Sauvegarder les grilles")) 
        if filename=="":
            QtGui.QMessageBox.warning(self,u'Sauvegarde annuléee',u"Aucune sauvegarde n'a pu être effectuée")
            return self.parent().filename
        self.gridz[self.numGrid] = io.GrilleMots(self.grille,self.lignes,self.colonnes)
        io.write_GrilleFile(filename,self.gridz,True)
        QtGui.QMessageBox.information(self,u'Sauvegarde effectuée',u'Sauvegarde effectuée dans le fichier {}'.format("solution_"+filename))
        self.parent().isSavedFile = True
        return filename
        
    def resoutGrille(self):
        # si une solution a été générée 
        # on l'efface
        if self.solutionAffichee:
            self.effaceResolution()
        # on charge les dicos
        self.chargeDicos()
        # recuperation d'un nouvel objet grille car il y a peut etre eu des modif
        self.wordGrid = io.GrilleMots(self.grille,self.lignes,self.colonnes)
        self.gridz[self.numGrid] = self.wordGrid
        # resolution de la grille
        # generation de la solution
        dialog = ChoixSolverDialog(parent=self)
        dialog.show()
        
    def sauveResolution(self,isSolution=True):
        ok = False
        if not isSolution:
            QtGui.QMessageBox.information(self,u'Aucune solution',u'Pas de solution pour cette grille avec ce dictionnaire là.')
        else:
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
                filename = os.path.basename(filename)
                reply = QtGui.QMessageBox.question(self,u"Sauvegarde",u"Voulez-vous écraser l'ancienne résolution {}/solution_{} et sauvegarder la solution?".format(io.SOLUTION_PATH,filename),QtGui.QMessageBox.Yes | 
                    QtGui.QMessageBox.No|QtGui.QMessageBox.Cancel, QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    ok=True
                elif reply == QtGui.QMessageBox.Cancel:
                    QtGui.QMessageBox.information(self,u'Sauvegarde annulée',u'La sauvegarde de la grille a été annulée')
                    return None
                else:
                    ok=False
        # on traite la reponse
        if ok and isSolution:
            io.write_GrilleFile(filename,self.gridz)
            io.write_SolutionFile(filename,self.gridz)
            self.parent().isSavedFile = True
            self.parent().filename = filename
        else:
            self.solutionAffichee = False
        
    def genereResolution(self,dialog):
        # on recupere l'algo voulu par l'utilisateur
        solveur = io.Solver(self.wordGrid,dic.DICTIONNAIRE,random=True)
        # on applique l'AC3 si c'est voulu par l'utilisateur
        ac3 = dialog.with_ac3
        # on applique l'algo choisi par l'utilisateur
        FC = dialog.with_fc
        CBJ = dialog.with_cbj
     
        # launching resolution    
        self.progress = QtGui.QProgressDialog("Algorithme en cours","Cancel",0,0,self) 
        self.progress.setWindowTitle('...')
        self.progress.setWindowModality(QtCore.Qt.WindowModal)
        self.progress.canceled.connect(self.progress.close)
        self.progress.show()
        
        self.TT = TaskThread(solveur,ac3=ac3,fc=FC,cbj=CBJ)
        self.TT.finished.connect(self.TT_Finished)
        self.progress.canceled.connect(self.progress.close)
        self.progress.show()
        self.TT.start()

    def TT_Finished(self):
        self.progress.close()
        self.afficheResolution()
        
    def afficheResolution(self):
        # le gridWidget recupere la grille et ses caracteristiques
        widg = self.gridWidget
        self.wordGrid.solution = self.solutionAffichee = True
        widg.lignes = self.lignes
        widg.colonnes = self.colonnes
        widg.wordGrid = self.wordGrid
        widg.nbCasesNoires = self.nbCasesNoires
        # TODO : not working?
        if widg.afficheResolution():
            # on demande a sauver/ou non la resolution generee
            self.sauveResolution()
        else :
            self.sauveResolution(isSolution=False)
                     
    def effaceResolution(self):
        """
        Retire de l'interfaceChoixGrille actuelle le chemin en effacant toutes les lettres des cases blanches
        """
        self.gridWidget.effaceResolution()
    
    def affichGrille(self,grid):
        self.lignes = grid.height
        self.colonnes = grid.width
        # on recupere la grille
        self.grille = grid.grille
        self.lignes = grid.height
        self.colonnes = grid.width
        # remplissage du gridLayout
        return None        
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
                if self.grille[i,j]==1:
                    button.stateChange(1)
                # end if
                l.append(button)
            # end first for
            butt.append(l)
            grid.setRowMinimumHeight(i,BoutonGrille.SIZE)
        # end 2e for
        grid.setSpacing(0.5)
        self.gridLayout = grid
     
    def switchGrille(self,nouv_num):
        if self.modifiee:
            reply = QtGui.QMessageBox.question(self,u"Enregistrement",u"Voulez-vous écraser l'ancienne grille {} et enregistrer la nouvelle grille à la place?".format(self.numGrid+1),QtGui.QMessageBox.Yes | 
                QtGui.QMessageBox.No|QtGui.QMessageBox.Cancel, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                ok=True
            elif reply == QtGui.QMessageBox.Cancel:
               return None
            else:
                ok=False
            if ok:
                # on enregistre la grille courante si l'utilisateur le veut
                self.gridz[self.numGrid] = io.GrilleMots(self.grille,self.lignes,self.colonnes)
        # on change le panel courant
        # on recupere le i-eme objet grille de la liste
        self.wordGrid = self.gridz[nouv_num]
        self.numGrid = nouv_num
        nWidget = GridObject(self.wordGrid,papa=self,parent=self)
        self.grille = self.wordGrid.grille.copy()
        self.lignes = self.wordGrid.height
        self.colonnes = self.wordGrid.width
        self.setNewPanel(nWidget)
        self.modifiee = False
        
    def setNewPanel(self, npanel):
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().deleteLater()
        self.gridWidget = npanel
        self.gridLayout.addWidget(self.gridWidget)
        
    def chargeDicos(self):
        # on recupere le dico
        try:
            dic.recupDictionnaire(self.parent().listDics)
        except :
            dic.recupDictionnaire([dic.DICT_DEF])
            QtGui.QMessageBox.critical(self,u"Fichier invalide",u"Le fichier choisi est le fichier par défaut {}".format(dic.DICT_FNAME))
        self.dico = dic.DICTIONNAIRE

        
class MaWindow(QtGui.QMainWindow):
    MARGE = 200
    WIDTH = WINDOW_DEF_SIZE
    HEIGHT = WINDOW_DEF_SIZE
    
    def __init__(self,parent=None):
        super(MaWindow, self).__init__()
        self.dico = dic.DICTIONNAIRE
        self.listDics = []
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
        # super look?
        #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        
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
        removeDicAction = QtGui.QAction('&Supprimer dictionnaire',self)
        removeDicAction.setStatusTip("Supprime un dictionnaire")
        removeDicAction.triggered.connect(self.removeDico)
        
        # menu changement de dictionnaire
        addDicAction = QtGui.QAction('&Ajouter un dictionnaire',self)
        addDicAction.setShortcut('Ctrl+Shift+A')
        addDicAction.setStatusTip("Ajoute un dictionnaire")
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
        
        toolGrille = menubar.addMenu('&Outils')
        toolGrille.addAction(addDicAction)
        toolGrille.addAction(removeDicAction)
        
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
        sys.stdout.write("\n\t----> Grille {}*{} avec {} cases noires\n".format(self.lignes,self.colonnes,self.nbCasesNoires))
     
    def modifDicsList(self,filename,add=True):
        if filename is None or filename=="":
            return None
        if add:
            self.listDics.append(filename)
            item = QtGui.QListWidgetItem(filename)
            #item.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
            #item.addAction(self.remAction)
            if not self.centralWidget().isCaract:
                self.centralWidget().listDicsWidg.addItem(item)
        else:
            # on retire un dico de la liste
            self.listDics.remove(filename)
            if not self.centralWidget().isCaract:
                self.centralWidget().listDicsWidg.takeItem(self.centralWidget().listDicsWidg.currentRow())
                
    def chooseDico(self):
        # on recupere le nom du dico avec un QInputDialog
        fname = str(QtGui.QFileDialog.getOpenFileName(self, 'Choisir Dictionnaire',dic.DICO_PATH))
        fname =  os.path.basename(fname)
        # si aucun nom sélectionné
        if fname=="":
            QtGui.QMessageBox.critical(self,u"Fichier invalide",u"Aucun fichier choisi")
            fname = dic.DICT_DEF
        return fname
    
    def addDico(self):
        filename = self.chooseDico()
        self.modifDicsList(filename,add=True)

    def removeDico(self):
        fname = self.centralWidget().listDicsWidg.currentItem().text()
        self.modifDicsList(fname,add=False)
    
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
            self.isSavedFile = widg.isSavedFile
            if not self.isSavedFile:
                QtGui.QMessageBox.warning(self,"Sauvegarde impossible",u"Nom de fichier nécessaire")
            self.statusBar().showMessage(u"Sauvegarde de {} effectuée".format(self.filename))

    def resoudreGrille(self):
        widg = self.centralWidget()
        if widg.isCaract:
            exit
        # sinon
        else :
            self.statusBar().showMessage(u"Résolution de la grille en cours")
            # on recupere le chemin generé
            # si le dico est vide on en charge un
            if self.listDics == []:
                self.addDico()
            widg.resoutGrille()
            if not widg.solutionAffichee:
                self.statusBar().showMessage(u"Aucune solution trouvée")            
            else:
                self.statusBar().showMessage(u"Grille résolue")
        
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
        self.WIDTH = max(self.WIDTH,WINDOW_DEF_SIZE)
        self.HEIGHT = max(self.HEIGHT,WINDOW_DEF_SIZE)
        # on resize si la taille doit changer selon la grille
        self.setFixedSize(self.WIDTH,self.HEIGHT)
            
    def center(self):
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))
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
