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

class groupPanel():
    def __init__(self,canvas,listDash=[],ubicacion='top-left'):
        pry= QgsProject.instance()
        self.canvas = canvas
        self.manejador=pry.annotationManager()
        self.posicion=ubicacion #posicion por defecto de las disponibles
        self.paneles=listDash
        self.offset=40 #separación adicional entre paneles el 20.4% del canvas
        self.manejador.annotationAboutToBeRemoved.connect(self.desconecPanel)
        self.globalToolTip=False
        self.globalBordeMarco=True
        
    def desconecPanel(self,tp):
        try:
            self.paneles.remove(tp)
        except:
            pass
        if type(tp)== textPanel or type(tp)==indicadorPanel \
        or type(tp)==barrasPanel or type(tp)==seriesPanel:
            print('entro borrar html')
            tp.borrarHtml()
            
    #AÑADIR PANEL
    def addPanel(self, panel):
        self.paneles.append(panel)
        
    #DEFINIENDO LA POSICION, SE INTRODUCE DE 0 A 1
    def yp(self,valor,altoPantalla):
        if valor==0:
            return 0
        else:
            return float(valor/altoPantalla)
        print(yp)
    
    def xp(self,valor,anchoPantalla):
        if valor==0:
            return 0
        else:
            return float(valor/anchoPantalla)
    
    def configurarIndiceEspacial(self):
        if len(self.paneles)>0:
            #creamos un diccionario cuyas claves son las capas secundarias
            listCS={}   #inicializamos el diccionario
            #llenamos el diccionario con claves como capas2 y listas
            for i in self.paneles:
                if (type(i)==indicadorPanel or type(i)==textPanel) and type(i.capa2)==QgsVectorLayer:
                    listCS[i.capa2]=[]
            #Ahora llenamos el dic con los paneles
            print('candidatos para el indice espacial: ',len(listCS))
            if len(listCS)>0:
                for i in self.paneles:
                    if type(i)==indicadorPanel or type(i)==textPanel:
                        if type(i.capa2) is QgsVectorLayer:
                            capa=i.capa2
                            print(capa.name())
                            listCS[capa].append(i)
                for i in listCS.keys():
                    if i.featureCount()>=1000 and i.geometryType()!=QgsWkbTypes.PointGeometry:
                        index = QgsSpatialIndex() # Spatial index
                        index = QgsSpatialIndex(i.getFeatures())
                        print('evaluando importacion',index)
                        for j in listCS[i]:
                            j.asignarIndEspacial(index)
                            print('asignando indice')
                
    def ubicarPaneles(self):
        self.configurarIndiceEspacial()
        print(self.paneles)
        nPaneles=len(self.paneles)
        altoPanel=self.paneles[0].altop
        anchoPanel=self.paneles[0].anchop
        #Dimensiones pantalla
        anchoC= self.canvas.size().width()#-self.canvas.size().width()*self.offset
        altoC= self.canvas.size().height()#-self.canvas.size().height()*self.offset
        print(self.posicion)
        if self.posicion=='top-left':
            xi=0
            yi=0
            c=0
#            print(len(self.paneles),self.paneles,c)
            for i in self.paneles:
                #Quitando la linea del borde del marco
                if self.globalBordeMarco==False:
                    i.fillSymbol().setOpacity(0.0)
#                print(yi)
                capa=i.capa
#                print(i.capa.name())
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
                i.setRelativePosition(QtCore.QPointF(0, self.yp(yi,altoC)))
                yi=yi+i.altop+60
#                if type(i)==textPanel and i.estilo!='entero-tenue' and i.estilo!='tim':
#                    yi=yi+(i.altop+22)*2+self.offset
#                else:
#                    yi=yi+i.altop+40
                c=c+1 
        elif self.posicion=='top-right':
            c=0
            yi=0
            xi=0
            for i in self.paneles:
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
                    ai.setToolTip("<strong>nombre</strong>")
                i.setHasFixedMapPosition(False)
                xi=anchoC-(i.anchoF+self.offset)
                i.setRelativePosition(QtCore.QPointF(self.xp(xi,anchoC), self.yp(yi,altoC)))
                yi=yi+i.altop+60
#                if type(i)==textPanel and i.estilo!='entero-tenue' and i.estilo!='tim':
#                    yi=yi+(i.altop+22)*2+self.offset
#                else:
#                    yi=yi+i.altop+40
                c=c+1
        elif self.posicion=='bottom-left':
            c=0
            xi=0
            altoT=0
            for j in self.paneles:
                altoT=altoT+(j.altop+60)
#                if type(j)==textPanel and i.estilo!='entero-tenue' and i.estilo!='tim':
#                    altoT=altoT+(j.altop+22)*2+self.offset
#                else:
#                    altoT=altoT+(j.altop+40)
            yi=altoC-altoT
            print("yi",yi,", altoT ",altoT,", altoC ",altoC)
            for i in self.paneles:
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
                    ai.setToolTip("<strong>nombre</strong>")
                i.setHasFixedMapPosition(False)
                print(self.yp(yi,altoC))
                i.setRelativePosition(QtCore.QPointF(xi, self.yp(yi,altoC)))
                yi=yi+i.altop+60
#                if type(i)==textPanel:
#                    yi=yi+(i.altop+22)*2+self.offset
#                else:
#                    yi=yi+i.altop+40
                c=c+1
        elif self.posicion=='bottom-right':
            c=0
            altoT=0
            for j in self.paneles:
                altoT=altoT+(j.altop+60)
#                if type(j)==textPanel and j.estilo!='entero-tenue' and j.estilo!='tim':
#                    altoT=altoT+(j.altop+22)*2+self.offset
#                else:
#                    altoT=altoT+(j.altop+40)
            yi=altoC-altoT
            print("yi",yi,", altoT ",altoT,", altoC ",altoC)
            for i in self.paneles:
                #Quitando la linea del borde del marco
                if self.globalBordeMarco==False:
                    i.fillSymbol().setOpacity(0.0)
                capa=i.capa
                geo=list(capa.getFeatures())[c].geometry()
                rec=geo.boundingBox()
                punto=rec.center()
                i.setMapPosition(punto)
                i.setMapPositionCrs(QgsCoordinateReferenceSystem(capa.crs()))
                self.manejador.addAnnotation(i)
                ai=QgsMapCanvasAnnotationItem(i, self.canvas)
                if self.globalToolTip==True:
                    nombre=i.capa.name()
                    ai.setToolTip("<strong>nombre</strong>")
                i.setHasFixedMapPosition(False)
                xi=anchoC-(i.anchoF+self.offset+10)
#                print(self.yp(yi,altoC))
                i.setRelativePosition(QtCore.QPointF(self.xp(xi,anchoC), self.yp(yi,altoC)))
#                if type(i)==textPanel and i.estilo!='entero-tenue' and i.estilo!='tim':
#                    yi=yi+(i.altop+22)*2+self.offset
#                else:
#                    yi=yi+i.altop+40
                yi=yi+i.altop+60
                c=c+1 
        if self.posicion=='dtop-left':
            if len(self.paneles)%2==0: #devuelve el resto, para un numero par es 0
                iteracion=int(len(self.paneles)/2)
                xi=0
                yi=0
                c=0
                for i in range(iteracion):
                    #Quitando la linea del borde del marco
                    if self.globalBordeMarco==False:
                        self.paneles[i].fillSymbol().setOpacity(0.0)
                    capa=self.paneles[i].capa
                    geo=list(capa.getFeatures())[c].geometry()
                    rec=geo.boundingBox()
                    punto=rec.center()
                    self.paneles[i].setMapPosition(punto)
                    self.paneles[i].setMapPositionCrs(QgsCoordinateReferenceSystem(capa.crs()))
                    self.manejador.addAnnotation(self.paneles[i])
                    ai=QgsMapCanvasAnnotationItem(self.paneles[i], self.canvas)
                    if self.globalToolTip==True:
                        nombre=i.capa.name()
                        ai.setToolTip("<strong>nombre</strong>")
                    self.paneles[i].setHasFixedMapPosition(False)
                    self.paneles[i].setRelativePosition(QtCore.QPointF(0, self.yp(yi,altoC)))
#                    if type(i)==textPanel and i.estilo!='entero-tenue' and i.estilo!='tim':
#                        yi=yi+(self.paneles[i].altop+22)*2+self.offset
#                    else:
#                        yi=yi+(self.paneles[i].altop+40)
                    yi=yi+(self.paneles[i].altop+60)
                    c=c+1
                xi=0
                yi=0
                c=0
                v=iteracion*2
                for j,i in enumerate(range(iteracion,v)):
                    #Quitando la linea del borde del marco
                    if self.globalBordeMarco==False:
                        self.paneles[i].fillSymbol().setOpacity(0.0)
                    capa=self.paneles[i].capa
                    geo=list(capa.getFeatures())[c].geometry()
                    rec=geo.boundingBox()
                    punto=rec.center()
                    self.paneles[i].setMapPosition(punto)
                    self.paneles[i].setMapPositionCrs(QgsCoordinateReferenceSystem(capa.crs()))
                    self.manejador.addAnnotation(self.paneles[i])
                    ai=QgsMapCanvasAnnotationItem(self.paneles[i], self.canvas)
                    if self.globalToolTip==True:
                        nombre=i.capa.name()
                        ai.setToolTip("<strong>nombre</strong>")
                    self.paneles[i].setHasFixedMapPosition(False)
                    self.paneles[i].setRelativePosition(QtCore.QPointF(\
                    self.xp(self.paneles[i].anchop+1.55*self.offset,anchoC), self.yp(yi,altoC)))
#                    if type(i)==textPanel and i.estilo!='entero-tenue' and i.estilo!='tim':
#                        yi=yi+(self.paneles[i].altop+22)*2+self.offset
#                    else:
#                        yi=yi+(self.paneles[i].altop+40)
                    yi=yi+(self.paneles[i].altop+60)
                    c=c+1
            else:
                self.posicion='top-left'
                self.ubicarPaneles()
            
    def separarY(self, valor):
        if self.posicion=='top-left' or self.posicion=='top-right':
            for i in range(1,len(self.paneles)):
                psInicial=self.paneles[i].relativePosition()
                self.paneles[i].setRelativePosition(QPointF(psInicial.x(),psInicial.y()+valor*i))
          