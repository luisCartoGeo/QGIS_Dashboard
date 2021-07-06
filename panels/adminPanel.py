# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QGISDashboard
                                 A QGIS plugin
 This plugin allows the construction and management of Dashboards on screen.
                              -------------------
        begin                : 2021-06-14
        git sha              : https://github.com/luisCartoGeo/QGIS_Dashboard
        copyright            : (C) 2021 by Luis Eduardo Perez https://www.linkedin.com/in/luisedpg/
        email                : luis3176@yahoo.com
 ***************************************************************************/
 """
#PERMITIR AGREGAR PANELES PAULATINAMENTE
#CREA UN INDICE ESPACIAL DE SER NECESARIO
from qgis.core import *
from qgis.gui import *
import qgis.utils
from .textPanel import textPanel
from .indicadorPanel import indicadorPanel
from .seriesPanel import seriesPanel
from .barrasPanel import barrasPanel
from .stylesTextPanel import styleTextPanel
from ..calculations.dataQuery import queriesData
from ..calculations.spatialQuery import spatialQueries
from ..register import logControl
import glob
import tempfile
import os

class adminPanel():
    def __init__(self,ubicacion='topLeft'):
        pry= QgsProject.instance()
        self.canvas = None
        self.manejador=pry.annotationManager()
        self.posicion=ubicacion #posicion por defecto de las disponibles
        self.paneles=[]
        self.tempPanels=[]
        self.manejador.annotationAboutToBeRemoved.connect(self.desconecPanel)
        pry.cleared.connect(self.delClose)
        self.globalToolTip=False
        self.globalBordeMarco=True
        
        self.listpositions={'topLeft':self.topLeft,'topRight':self.topRight,'bottomLeft':self.bottomLeft,\
            'bottomRight':self.bottomRight,'horizontalTop':self.horizontalTop,'horizontalBottom':self.horizontalBottom}
        #Dimensiones de los paneles
        self.anchoP=None
        self.altoP=None
        
        self.log=logControl()
        print('log es ',self.log)
        self.logAcces=self.log.canWriteLog()
        
    def init(self,canvas):
        self.canvas=canvas
        self.extentCan=self.canvas.extent()
        self.altoScreen=self.canvas.height()
        self.anchoScreen=self.canvas.width()
        self.dpi=self.canvas.mapSettings().outputDpi ()
    
    def initPlacePanels(self,anchop,altop):
        #Dimensiones de los paneles
        self.anchoP=anchop
        self.altoP=altop
        print(self.dpi)
        self.altomm=round((self.altoScreen*25)/self.dpi,2)
        self.anchomm=round((self.anchoScreen*25)/self.dpi,2)
        print('ancho mm',self.anchomm)
        print('ancho p',self.xp(self.anchoP))
    
    def desconecPanel(self,tp):
        try:
            self.paneles.remove(tp)
            try:
                self.paneles.remove(tp)
            except:
                print('segundo intento de borrar')
        except Exception as e:
            if self.logAcces:
                self.log.writeLog('No se pudieron remover los paneles de la lista ')
        if type(tp)==textPanel or type(tp)==indicadorPanel \
        or type(tp)==barrasPanel or type(tp)==seriesPanel:
            tp.borrarHtml()
        try:
            if os.path.exists(tp.tempf.name):
                os.remove(tp.tempf.name)
        except Exception as e:
            if self.logAcces:
                self.log.writeLog('Archivo persistente a borrar '+str(e))
            
    #AÑADIR PANEL
    def addPanels(self, lista):
        self.tempPanels.clear()
        if len(lista)>0:
            for i in lista:
                self.tempPanels.append(i)
        
    #DEFINIENDO LA POSICION, SE INTRODUCE DE 0 A 1
    def yp(self,valor):
        return float(valor/self.altomm)

    def xp(self,valor):
        return float(valor/self.anchomm)
    
    def placePanels(self):
        try:
            if len(self.tempPanels)>0:
                print('en ubicar paneles ',self.posicion)
                print(self.posicion in self.listpositions)
                print(self.listpositions[self.posicion])
                self.listpositions[self.posicion]()
                self.tempPanels.clear()
                return True
            else:
                return False
        except Exception as e:
            if self.logAcces:
                self.log.writeLog('Error al ubicar panel en admin '+str(e))
        
    def topLeft(self):
        x=0
        for e,i in enumerate(self.tempPanels):
            if e==0:
                y=e
            else:
                y=round(self.yp(e*self.altoP),4)
            print(x,y)
            #Quitando la linea del borde del marco
            if self.globalBordeMarco==False:
                i.fillSymbol().setOpacity(0.0)
            capa=i.capa
            geo=capa.getFeature(0).geometry()
            rec=geo.boundingBox()
            punto=rec.center()
            i.setMapPosition(punto)
            i.setMapPositionCrs(QgsCoordinateReferenceSystem(capa.crs()))
            self.manejador.addAnnotation(i)
            ai=QgsMapCanvasAnnotationItem(i, self.canvas)
            if self.globalToolTip==True:
                nombre=i.capa.name()
                ai.setToolTip("<strong>"+nombre+"</strong>")
            i.setHasFixedMapPosition(False)
            i.setRelativePosition(QtCore.QPointF(x, y))
            self.paneles.append(i)
            #self.paneles.append(ai)
    
    def topRight(self):
        xi=self.anchomm-self.anchoP
        x=round(self.xp(xi),4)
        y=0
        for e,i in enumerate(self.tempPanels):
            if e==0:
                y=e
            else:
                y=round(self.yp(e*self.altoP),4)
            capa=i.capa
            geo=capa.getFeature(0).geometry()
            rec=geo.boundingBox()
            punto=rec.center()
            i.setMapPosition(punto)
            i.setMapPositionCrs(QgsCoordinateReferenceSystem(capa.crs()))
            self.manejador.addAnnotation(i)
            ai=QgsMapCanvasAnnotationItem(i, self.canvas)
            if self.globalToolTip==True:
                nombre=i.capa.name()
                ai.setToolTip("<strong>"+nombre+"</strong>")
            i.setHasFixedMapPosition(False)
            i.setRelativePosition(QtCore.QPointF(x, y))
            self.paneles.append(i)
    
    def bottomLeft(self):
        x=0
        print('bottom left',x)
        for e,i in enumerate(self.tempPanels,1):
            y=1-round(self.yp(e*self.altoP),4)
            capa=i.capa
            geo=capa.getFeature(0).geometry()
            rec=geo.boundingBox()
            punto=rec.center()
            i.setMapPosition(punto)
            i.setMapPositionCrs(QgsCoordinateReferenceSystem(capa.crs()))
            self.manejador.addAnnotation(i)
            ai=QgsMapCanvasAnnotationItem(i, self.canvas)
            if self.globalToolTip==True:
                nombre=i.capa.name()
                ai.setToolTip("<strong>"+nombre+"</strong>")
            i.setHasFixedMapPosition(False)
            i.setRelativePosition(QtCore.QPointF(x, y))
            self.paneles.append(i)
            
    def bottomRight(self):
        xi=self.xp(self.anchoP)
        x=1-xi
        for e,i in enumerate(self.tempPanels,1):
            y=1-abs(round(self.yp(e*self.altoP),4))
            capa=i.capa
            geo=capa.getFeature(0).geometry()
            rec=geo.boundingBox()
            punto=rec.center()
            i.setMapPosition(punto)
            i.setMapPositionCrs(QgsCoordinateReferenceSystem(capa.crs()))
            self.manejador.addAnnotation(i)
            ai=QgsMapCanvasAnnotationItem(i, self.canvas)
            if self.globalToolTip==True:
                nombre=i.capa.name()
                ai.setToolTip("<strong>"+nombre+"</strong>")
            i.setHasFixedMapPosition(False)
            i.setRelativePosition(QtCore.QPointF(x, y))
            self.paneles.append(i)
            
    def horizontalBottom(self):
        print('horizonatla bottom')
        y=1-round(self.yp(self.altoP),4)
        for e,i in enumerate(self.tempPanels):
            if e==0:
                x=e
            else:
                x=round(self.xp(e*self.anchoP),4)
            capa=i.capa
            geo=capa.getFeature(0).geometry()
            rec=geo.boundingBox()
            punto=rec.center()
            i.setMapPosition(punto)
            i.setMapPositionCrs(QgsCoordinateReferenceSystem(capa.crs()))
            self.manejador.addAnnotation(i)
            ai=QgsMapCanvasAnnotationItem(i, self.canvas)
            if self.globalToolTip==True:
                nombre=i.capa.name()
                ai.setToolTip("<strong>"+nombre+"</strong>")
            i.setHasFixedMapPosition(False)
            i.setRelativePosition(QtCore.QPointF(x, y))
            self.paneles.append(i)
        
    def horizontalTop(self):
        y=0
        for e,i in enumerate(self.tempPanels):
            if e==0:
                x=e
            else:
                x=round(self.xp(e*self.anchoP),5)
            capa=i.capa
            geo=capa.getFeature(0).geometry()
            rec=geo.boundingBox()
            punto=rec.center()
            i.setMapPosition(punto)
            i.setMapPositionCrs(QgsCoordinateReferenceSystem(capa.crs()))
            self.manejador.addAnnotation(i)
            ai=QgsMapCanvasAnnotationItem(i, self.canvas)
            if self.globalToolTip==True:
                nombre=i.capa.name()
                ai.setToolTip("<strong>"+nombre+"</strong>")
            i.setHasFixedMapPosition(False)
            i.setRelativePosition(QtCore.QPointF(x, y))
            self.paneles.append(i)
            
    def delClose(self):
        if len(self.paneles)>0:
            for a in self.paneles:
                a.borrarHtml()
                try:
                    self.manejador.removeAnnotation(a)
                except:
                    pass
        dir=tempfile.gettempdir()
        lista=[]
        for f in glob.glob(os.path.join(dir,"qd*html")):
            print(f)
            lista.append(f)
        if len(lista)>0:
            for f in lista:
                try:
                    os.remove(f)
                except:
                    print('error en borrar en admin')