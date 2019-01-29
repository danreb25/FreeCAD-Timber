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
__author__ = "Bernard Blockmans"
__url__ = "http://www.freecadweb.org"

import FreeCAD,Arch

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


def filterTaggedObjects(objs,taglist):
    '''
    BBL not used yet
    '''
    objs = [o for o in objs if ( o!=None  and  hasattr(o,"Tag") and o.Tag)]
    # vérifier si le tag de l'objet est bien présent dans la liste des tag sur lesquels on filtre
    if tagFilter:
        objs = [o for o in objs if (o.Tag in taglist )]
    return objs
