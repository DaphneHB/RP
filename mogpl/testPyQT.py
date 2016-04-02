#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore

class HighlightSquare(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent=None)
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                                       QtGui.QSizePolicy.Expanding))                  
        self.setMinimumSize(self.minimumSizeHint()) 
        layout = QtGui.QGridLayout()
        layout.addItem(QtGui.QSpacerItem(10,10), 0, 0)
        layout.addItem(QtGui.QSpacerItem(10,10), 0, 1)
        layout.addItem(QtGui.QSpacerItem(10,10), 1, 0)
        layout.addItem(QtGui.QSpacerItem(10,10), 1, 1)       
        self.setLayout(layout)
        self.resize(150, 150)
        self.update()

    def paintEvent(self, event = None):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        winHeight=self.size().height(); heightStep=winHeight/2
        winWidth=self.size().width(); widthStep=winWidth/2

        #Draw lines
        painter.setPen(QtCore.Qt.black)
        for i in range(4):
            #vertical lines
            painter.drawLine(QtCore.QPoint(i*widthStep,0), QtCore.QPoint(i*widthStep, winHeight))
            #horizontal lines
            painter.drawLine(QtCore.QPoint(0,heightStep*i), QtCore.QPoint(winWidth, heightStep*i))

        #Draw blue outline around box 1,1
        highlightCoordinate=(1,1)
        pen=QtGui.QPen(QtCore.Qt.blue, 3)        
        painter.setPen(pen)
        coordHighlight=[QtCore.QPoint(highlightCoordinate[1]*heightStep, highlightCoordinate[0]*widthStep),\
                        QtCore.QPoint(highlightCoordinate[1]*heightStep, (highlightCoordinate[0]+1)*widthStep),\
                        QtCore.QPoint((highlightCoordinate[1]+1)*heightStep, (highlightCoordinate[0]+1)*widthStep),\
                        QtCore.QPoint((highlightCoordinate[1]+1)*heightStep, highlightCoordinate[0]*widthStep),\
                        QtCore.QPoint(highlightCoordinate[1]*heightStep, highlightCoordinate[0]*widthStep)]
        #print coordHighlight
        painter.drawPolyline(coordHighlight)

    def minimumSizeHint(self):
        return QtCore.QSize(120,120)


if __name__=="__main__":
    import sys
    app=QtGui.QApplication(sys.argv)
    myLight = HighlightSquare()
    myLight.show()
    sys.exit(app.exec_())