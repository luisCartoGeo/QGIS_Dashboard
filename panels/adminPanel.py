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
    def __init__(self,iface,ubicacion='topLeft'):
        self.iface=iface
        self.pry= QgsProject.instance()
        self.canvas=self.iface.mapCanvas()
        self.manejador=self.pry.annotationManager()
        self.posicion=ubicacion #posicion por defecto de las disponibles
        self.paneles=[]
        self.tempPanels=[]
        self.manejador.annotationAboutToBeRemoved.connect(self.desconecPanel)
        self.pry.cleared.connect(self.delClose)
        self.globalToolTip=False
        self.globalBordeMarco=True
        
        self.listpositions={'topLeft':self.topLeft,'topRight':self.topRight,'bottomLeft':self.bottomLeft,\
            'bottomRight':self.bottomRight,'horizontalTop':self.horizontalTop,'horizontalBottom':self.horizontalBottom}
        #Dimensiones de los paneles
        self.anchoP=None
        self.altoP=None
        
        self.log=logControl()
        self.logAcces=self.log.canWriteLog()
        
    def init(self,canvas):
        self.extentCan=self.canvas.extent()
        self.altoScreen=self.canvas.height()
        self.anchoScreen=self.canvas.width()
        self.dpi=self.canvas.mapSettings().outputDpi ()
    
    def initPlacePanels(self,anchop,altop):
        #Dimensiones de los paneles
        self.anchoP=anchop
        self.altoP=altop
        self.altomm=round((self.altoScreen*25)/self.dpi,2)
        self.anchomm=round((self.anchoScreen*25)/self.dpi,2)
    
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
    
    def removePanels(self):
        self.tempPanels.clear()
        self.delClose()    
        
    #DEFINIENDO LA POSICION, SE INTRODUCE DE 0 A 1
    def yp(self,valor):
        return float(valor/self.altomm)

    def xp(self,valor):
        return float(valor/self.anchomm)
    
    def placePanels(self):
        try:
            if len(self.tempPanels)>0:
                self.listpositions[self.posicion]()
                self.tempPanels.clear()
                return True
            else:
                return False
        except Exception as e:
            if self.logAcces:
                self.log.writeLog('Error al ubicar panel en admin '+str(e))
    
    def loadByList(self,listaPaneles):
        spatialOptions=['entid-selec-intersect','entid-selec-intersect-atrib','buffer-contains',\
        'buffer-contains-attrib','buffer-contains-sum','densidad','densidad valor']
        pry=QgsProject.instance()
        for lista in listaPaneles:
            ncapa=lista['capa']
            lcapas=pry.mapLayersByName(ncapa)
            capa=''
            if len(lcapas)>0:
                for c in lcapas:
                    if c.source()==lista['rutaCapa']:
                        capa=lcapas[0]
                        break
                    else:
                        capa=lcapas[0]
#Evaluar si existe capa2 para operaciones espaciales
#            if lista['estilo'] in spatialOptions:
#                ncapa2=lista['expresion']
                x=float(lista['x'])
                y=float(lista['y'])
                ancho=float(lista['anchoP'])
                alto=float(lista['altoP'])
                if lista['panel']=='textPanel':
                    if ',' in lista['expression']:
                        expresion=lista['expression'].rsplit(",")
                    else:
                        expresion=[lista['expression']]
                    if lista['icono']=='True':
                        icono=True
                    else:
                        icono=False
                    try:
                        tp=textPanel(capa, lista['type'], lista['title'],expresion,fondTit=lista['fondTit'],\
                        colorTextTit=lista['colorTextTit'],fondVal=lista['fondVal'],colorTextVal=lista['colorTextVal'],\
                        suavizado=lista['suavizado'],estilo=lista['estilo'],\
                        icono=icono,rutaIcono=lista['rutaIcono'],direccionIcono=lista['direccionIcono'],\
                        colorIcono=lista['colorIcono'],anchoP=ancho,altoP=alto)
                        tp.fillSymbol().setOpacity(0.0)
                    except:
                        self.iface.messageBar().pushMessage('ERROR',\
                        'Error in panel creation, check that the layers linked to the field structure when'+ 
                        ' the panel was created exist',level=Qgis.Warning, duration=7)
                    if type(tp)==textPanel:
                        self.manejador.addAnnotation(tp)
                        tp.setHasFixedMapPosition(False)
                        tp.setRelativePosition(QtCore.QPointF(x, y))
                        self.paneles.append(tp)
                elif lista['panel']=='indicadorPanel':
                    if ',' in lista['expression']:
                        expresion=lista['expression'].rsplit(",")
                    else:
                        expresion=[lista['expression']]
                    range=[float(lista['min']),float(lista['max'])]
                    
                    try:
                        tp=indicadorPanel(capa,lista['type'],lista['title'],expresion,float(lista['threshold']),range=range,\
                        estilo=lista['estilo'],anchoP=ancho,altoP=alto,colorBar=lista['colorBar'],\
                        colorBackground=lista['colorBackground'],colorTit=lista['colorTit'],\
                        sizeTitle=lista['sizeTitle'],colorBase=lista['colorBase'],colorLine=lista['colorLine'],\
                        sizeLabel=lista['sizeLabel'],colorFinal=lista['colorFinal'],colorValue=lista['colorValue'],\
                        colorMark=lista['colorMark'],relative=lista['relative'])
                    except:
                        self.iface.messageBar().pushMessage('ERROR',\
                        'Error in panel creation, check that the layers linked to the field structure when'+ 
                        ' the panel was created exist',level=Qgis.Warning, duration=7)
                    if type(tp)==indicadorPanel:
                        tp.fillSymbol().setOpacity(0.0)
                        self.manejador.addAnnotation(tp)
                        tp.setHasFixedMapPosition(False)
                        tp.setRelativePosition(QtCore.QPointF(x, y))
                        self.paneles.append(tp)
                elif lista['panel']=='barrasPanel':
                    if lista['type']=='atributo-sum':
                        expresion=lista['expression'].rsplit(",")
                    else:
                        expresion=[lista['expression'].rsplit(",")]
                    if lista['wordBreak']=='True':
                        wordbreak=True
                    else:
                        wordbreak=False
                    try:
                        tp=barrasPanel(capa,lista['type'],lista['title'],expresion,\
                        colorBar=lista['colorBar'],colorTit=lista['colorTit'],typeColor=lista['typeColor'],\
                        wordBreak=wordbreak,sizeTitle=lista['sizeTitle'],sizeLabels=lista['sizeLabels'],\
                        colorLabels=lista['colorLabels'],palette=lista['palette'],\
                        anchoP=ancho,altoP=alto)
                    except:
                        self.iface.messageBar().pushMessage('ERROR',\
                        'Error in panel creation, check that the layers linked to the field structure when'+ 
                        ' the panel was created exist',level=Qgis.Warning, duration=7)
                    if type(tp)==barrasPanel:
                        tp.fillSymbol().setOpacity(0.0)
                        self.manejador.addAnnotation(tp)
                        tp.setHasFixedMapPosition(False)
                        tp.setRelativePosition(QtCore.QPointF(x, y))
                        self.paneles.append(tp)
                elif lista['panel']=='seriesPanel':
                    campox=lista['campox']
                    camposy=lista['camposy'].rsplit(",")
                    if lista['wordBreak']=='True':
                        wordbreak=True
                    else:
                        wordbreak=False
                    if lista['fill']=='True':
                        fill=True
                    else:
                        fill=False
                    try:
                        tp=seriesPanel(capa,[camposy,campox],title=lista['title'],fill=fill,wordBreak=wordbreak,\
                        widthline=int(lista['widthline']),colorTit=lista['colorTit'],\
                        sizeTitle=lista['sizeTitle'],colorLabels=lista['colorLabels'],\
                        sizeLabels=lista['sizeLabels'],anchoP=ancho,altoP=alto)
                    except:
                        self.iface.messageBar().pushMessage('ERROR',\
                        'Error in panel creation, check that the layers linked to the field structure when'+ 
                        ' the panel was created exist',level=Qgis.Warning, duration=7)
                    if type(tp)==seriesPanel:
                        tp.fillSymbol().setOpacity(0.0)
                        self.manejador.addAnnotation(tp)
                        tp.setHasFixedMapPosition(False)
                        tp.setRelativePosition(QtCore.QPointF(x, y))
                        self.paneles.append(tp)
            else:
                self.iface.messageBar().pushMessage('ERROR',\
                'layer '+ncapa+' for '+lista['panel']+' not in project', level=Qgis.Warning, duration=2)
                continue
    
    def topLeft(self):
        crs=self.pry.crs()
        x=0
        for e,i in enumerate(self.tempPanels):
            if e==0:
                y=e
            else:
                y=round(self.yp(e*self.altoP),4)
            #Quitando la linea del borde del marco
            if self.globalBordeMarco==False:
                i.fillSymbol().setOpacity(0.0)
            self.manejador.addAnnotation(i)
            i.setHasFixedMapPosition(False)
            i.setRelativePosition(QtCore.QPointF(x, y))
            ai=QgsMapCanvasAnnotationItem(i, self.canvas)
            if self.globalToolTip==True:
                nombre=i.capa.name()
                ai.setToolTip("<strong>"+nombre+"</strong>")
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
            lista.append(f)
        if len(lista)>0:
            for f in lista:
                try:
                    os.remove(f)
                except:
                    print('error en borrar en admin')