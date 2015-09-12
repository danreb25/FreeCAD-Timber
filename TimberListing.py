# -*- coding: utf-8 -*-
# FreeCAD init script of the Timber module
# (c) 2015 Jonathan Wiedemann

#***************************************************************************
#*   (c) Jonathan Wiedemann (jonatan@wiedemann.fr) 2015                    *
#*                                                                         *
#*   This file is part of the FreeCAD CAx development system.              *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   FreeCAD is distributed in the hope that it will be useful,            *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Lesser General Public License for more details.                   *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with FreeCAD; if not, write to the Free Software        *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#*   Jonathan Wiedemann 2015                                               *
#***************************************************************************/

__title__="FreeCAD Timber API"
__author__ = "Jonathan Wiedemann"
__url__ = "http://www.freecadweb.org"

import FreeCAD, FreeCADGui
import Arch, Draft, Part
import math, DraftGeomUtils, DraftVecUtils
from FreeCAD import Vector, Rotation, Placement, Console
from PySide import QtCore, QtGui

import os
__dir__ = os.path.dirname(__file__)

def makeTimberListing(display=True):
    tb = Listing()
    tb.makeTimberList()
    if display:
        tb.printTimberList()
    #return tb.getTimberList()

def getTagList():
    taglist = []
    for obj in FreeCAD.ActiveDocument.Objects :
        try :
            if obj.Tag:
                if taglist.count(str(obj.Tag)) == 0:
                    taglist.append(str(obj.Tag))
        except AttributeError:
            pass
    return taglist

class _CommandListing:
        "the Timber Listing command definition"
        def GetResources(self):
           return {'Pixmap'  : __dir__ + '/icons/Timber_Listing.svg',
                    'MenuText': QtCore.QT_TRANSLATE_NOOP("Timber_Listing","Make listing"),
                    'ToolTip': QtCore.QT_TRANSLATE_NOOP("Timber_Listing","List objects")}

        def IsActive(self):
            return True

        def Activated(self):
            panel = _ListingTaskPanel()
            FreeCADGui.Control.showDialog(panel)

class _ListingTaskPanel:
    def __init__(self):
        self.form = QtGui.QWidget()
        self.form.setObjectName("TaskPanel")
        self.grid = QtGui.QGridLayout(self.form)
        self.grid.setObjectName("grid")
        self.title = QtGui.QLabel(self.form)
        self.grid.addWidget(self.title, 1, 0)
        self.taglistwidget = QtGui.QListWidget(self.form)
        self.grid.addWidget(self.taglistwidget, 2, 0)
        for tag in getTagList():
            self.taglistwidget.addItem(tag)
        self.infoText =  QtGui.QLabel(self.form)
        self.grid.addWidget(self.infoText, 3, 0)
        self.combobox = QtGui.QComboBox()
        self.combobox.setCurrentIndex(0)
        self.grid.addWidget(self.combobox, 3, 1)
        #self.linedit = QtGui.QLineEdit()
        #self.combobox.setCurrentIndex(0)
        #self.grid.addWidget(self.linedit, 3, 1)
        #self.taglistwidget.itemClicked.connect(self.setTag)
        #QtCore.QObject.connect(self.taglistwidget,QtCore.SIGNAL("itemClicked(item)"),self.setTag)
        #self.previewObj = FreeCAD.ActiveDocument.addObject("Part::Feature", str(translate("Arch", "PreviewCutVolume")))
        self.retranslateUi(self.form)
        #self.previewCutVolume(self.combobox.currentIndex())

    def setTag(self,item):
        #print "setText"
        self.linedit.setText(str(item.text()))

    #def printTimberList(self):
        #pass

    def accept(self):
        #FreeCAD.ActiveDocument.removeObject(self.previewObj.Name)
        #destination = str(self.combobox.currentItem.text())
        #tag = self.linedit.text()
        #print makeTimberListing(tag,destination)
        makeTimberListing()
        #FreeCAD.ActiveDocument.recompute()
        return True

    def reject(self):
        FreeCAD.Console.PrintMessage("Cancel Listing\n")
        return True

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel)

    def retranslateUi(self, TaskPanel):
        TaskPanel.setWindowTitle(QtGui.QApplication.translate("Timber", "Listing", None, QtGui.QApplication.UnicodeUTF8))
        self.title.setText(QtGui.QApplication.translate("Timber", "Choose tag to list", None, QtGui.QApplication.UnicodeUTF8))
        self.infoText.setText(QtGui.QApplication.translate("Timber", "Destination", None, QtGui.QApplication.UnicodeUTF8))
        self.combobox.addItems([QtGui.QApplication.translate("Timber", "Window", None, QtGui.QApplication.UnicodeUTF8),
                                    QtGui.QApplication.translate("Timber", "Report View", None, QtGui.QApplication.UnicodeUTF8),
                                    QtGui.QApplication.translate("Timber", "Spreadsheet", None, QtGui.QApplication.UnicodeUTF8),
                                    QtGui.QApplication.translate("Timber", "CuttingStock .dat", None, QtGui.QApplication.UnicodeUTF8)])

class Listing:
    def __init__(self):
        doc = FreeCAD.ActiveDocument
        objs = FreeCAD.ActiveDocument.Objects
        self.objlist=[]
        #print("Il y a "+str(len(objs))+" objets dans le document.")
        for obj in objs:
            #a = obj.Name
            #print("Objet : " + str(a))
            #b = obj.Label
            if hasattr(obj,"Proxy"):
                #print(" - hasattr Proxy : ok")
                if hasattr(obj.Proxy,"Type"):
                    #print(" - hasattr Type : ok")
                    if FreeCADGui.ActiveDocument.getObject(obj.Name).Visibility :
                        #print(" - Visibility : True")
                        try:
                            if obj.Tag:
                                self.objlist.append(obj)
                        except AttributeError:
                            pass
                        #Listing()
                        #objectAnalyse(obj)
                    else:
                        #print(" - Visibility : False")
                        pass
                else:
                    #print(" - hasattr Type : no")
                    pass
            else:
                #print(" - hasattr Proxy : no")
                pass

        parms = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Units")
        self.timberlist=[]

    def makeTimberList(self):
        for tag in getTagList():
            timberlistbytag = []
            for obj in self.objlist:
                if obj.Tag == tag:
                    if obj.Proxy.Type in ["Structure", "Panel", "StructuralSystem", "Frame"]:
                        for solid in obj.Shape.Solids:
                            name = str("Aligned_"+str(obj.Name))
                            timber_part = self.shapeAnalyse(name,solid,)
                            timberlistbytag = self.addListe(timberlistbytag, timber_part[0], timber_part[1], timber_part[2])
                    else :
                        print("Type structurel non pris en charge")
            self.timberlist.append([tag,timberlistbytag])
        return self.timberlist

    def getTimberList():
        makeTimberList()
        return self.timberlist

    def printTimberList(self):
        for listbytag in self.timberlist:
            print("Tag : " + str(listbytag[0]))
            for section in listbytag[1]:
                print("Section : " + str(section[0])+"x"+str(section[1]))
                print("Qte    Longueur")
                for debit in section[2]:
                    print(str(debit[1])+"      "+str(debit[0]))
            print("")
        if hasattr(FreeCAD.ActiveDocument,"TimberSpeadsheet"):
            mySheet = FreeCAD.ActiveDocument.TimberSpreadsheet
        else :
            mySheet = FreeCAD.ActiveDocument.addObject('Spreadsheet::Sheet','TimberSpreadsheet')
        mySheet.clearAll()
        FreeCAD.ActiveDocument.recompute()
        mySheet.set('A1', 'Liste')
        n=1
        for listbytag in self.timberlist:
            n += 1
            mySheet.set('A'+str(n), str(listbytag[0]))
            #print("Tag : " + str(listbytag[0]))
            n += 1
            mySheet.set('A'+str(n), "Base : ")
            #mySheet.set('B'+str(n), str(section[0])+"x"+str(section[1]))
            mySheet.set('B'+str(n), "Hauteur : ")
            mySheet.set('C'+str(n), "Longueur : ")
            mySheet.set('D'+str(n), "Quantite : ")
            for section in listbytag[1]:
                partBase = str(section[0])
                partHeight = str(section[1])
                #print("Section : " + str(section[0])+"x"+str(section[1]))
                #print("Qte    Longueur")
                #n += 1
                #mySheet.set('A'+str(n), "Quantite")
                #mySheet.set('B'+str(n), "Longueur")
                for debit in section[2]:
                    n += 1
                    mySheet.set('A'+str(n), partBase)
                    mySheet.set('B'+str(n), partHeight)
                    mySheet.set('C'+str(n), str(debit[0]))
                    mySheet.set('D'+str(n), str(debit[1]))
                    #print(str(debit[1])+"      "+str(debit[0]))
            #print("")
            FreeCAD.ActiveDocument.recompute()

    def addListe(self, listbytag, base, hauteur, longueur):
        #precision = parms.GetInt('Decimals')
        precision = 0
        base = round(base,precision)
        hauteur = round(hauteur,precision)
        longueur = round(longueur,precision)
        base = int(base)
        hauteur = int(hauteur)
        longueur = int(longueur)
        liste =  sorted([base, hauteur, longueur])
        base = liste[0]
        hauteur = liste[1]
        longueur = liste[2]
        #print "self.timberlist : ,",self.timberlist
        added = False
        if len(listbytag) > 0 :
            #print "self.timberlist est > 0"
            for x in listbytag :
                if x[0]==base and x[1]==hauteur :
                    #print "la section existe"
                    for qte in x[2]:
                        if qte[0] == longueur :
                            #print "la longueur existe"
                            #print "ajout une unite a longueur"
                            qte[1] += 1
                            added = True
                    if not added:
                        #print "ajout une longueur et une unite"
                        x[2].append([longueur,1])
                        added = True
            if not added:    #else:
                #print "la section existe pas"
                #print "ajout section , longueur, qte"
                listbytag.append([base, hauteur,[[longueur,1],],])
        else:
            #print "la liste est vide"
            #print "ajout section , longueur, qte"
            listbytag.append([base, hauteur,[[longueur,1],],])
        return listbytag
        #print "self.timberlist : ,",self.timberlist

    def getArea(self, face):
        return face.Area

    def getFacesMax(self, faces):
        faces = sorted(faces,key=self.getArea, reverse = True)
        facesMax = faces[0:4]
        return facesMax

    def getCoupleFacesEquerre(self, faces):
        listeCouple = []
        lenfaces = len(faces)
        faces.append(faces[0])
        for n in range(lenfaces):
            norm2 = faces[n+1].normalAt(0,0)
            norm1 = faces[n].normalAt(0,0)
            norm0 = faces[n-1].normalAt(0,0)
            if abs(round(math.degrees(DraftVecUtils.angle(norm1,norm0)))) == 90.:
                listeCouple.append([faces[n],faces[n-1]])
            if abs(round(math.degrees(DraftVecUtils.angle(norm1,norm2)))) == 90.:
                listeCouple.append([faces[n],faces[n+1]])
        return listeCouple

    def shapeAnalyse(self, name, shape):
        ## Create a new object with the shape of the current arch object
        ## His placment is set to 0,0,0
        obj = FreeCAD.ActiveDocument.addObject('Part::Feature',name)
        obj.Shape=shape
        obj.Placement.Base = FreeCAD.Vector(0.0,0.0,0.0)
        obj.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0.0,0.0,1.0),0.0)
        FreeCAD.ActiveDocument.recompute()
        ## Get the face to align with XY plane
        faces = obj.Shape.Faces
        facesMax = self.getFacesMax(faces)
        coupleEquerre = self.getCoupleFacesEquerre(facesMax)
        ## Get the normal of this face
        nv1 = coupleEquerre[0][0].normalAt(0,0)
        ## Get the goal normal vector
        zv = Vector(0,0,1)
        ## Find and apply a rotation to the object to align face
        pla = obj.Placement
        rot = pla.Rotation
        rot1 = Rotation(nv1, zv)
        newrot = rot.multiply(rot1)
        pla.Rotation = newrot
        ## Get the face to align with XY plane
        faces = obj.Shape.Faces
        facesMax = self.getFacesMax(faces)
        coupleEquerre = self.getCoupleFacesEquerre(facesMax)
        ## Get the longest edge from aligned face
        maxLength = 0.
        for e in coupleEquerre[0][0].Edges:
            if e.Length > maxLength:
                maxLength = e.Length
                edgeMax = e
        ## Get the angle between edge and X axis and rotate object
        vec = DraftGeomUtils.vec(edgeMax)
        vecZ = FreeCAD.Vector(vec[0],vec[1],0.0)
        pos2 = obj.Placement.Base
        rotZ = math.degrees(DraftVecUtils.angle(vecZ,FreeCAD.Vector(1.0,0.0,0.0),zv))
        Draft.rotate([obj],rotZ,pos2,axis=zv,copy=False)
        FreeCAD.ActiveDocument.recompute()
        ## Get the boundbox
        return [obj.Shape.BoundBox.YLength, obj.Shape.BoundBox.ZLength, obj.Shape.BoundBox.XLength]

if FreeCAD.GuiUp:
    FreeCADGui.addCommand('Timber_Listing',_CommandListing())