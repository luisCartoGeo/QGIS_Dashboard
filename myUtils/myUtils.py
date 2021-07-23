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
from qgis.core import QgsProject
from qgis import PyQt
from qgis.PyQt.QtGui import QColor

def qcolorToStr(qcolor):
    if type(qcolor)==QColor:
        return 'rgb('+','.join([str(qcolor.red()),str(qcolor.green()),str(qcolor.blue())])+')'
    else:
        return qcolor

class utils:
    @staticmethod
    def splitText(cadena):
        resultado=[]
        lbr=[]
        for e,texto in enumerate(cadena):
            if len(texto)>10:
                l=[texto[i:i+10] for i in range(0,len(texto),10)]
                text=''
                br=0
                for e,i in enumerate(l):
                    if e<len(l)-1 and len(l[e+1])>4:
                        br=br+1
                        lbr.append(br)
                        if i[-1].isspace():
                            text=text+i[:-1]+'<br>'
                        else:
                            text=text+i+'<br>'
                    else:
                        text=text+i
                resultado.append(text)
            else:
                resultado.append(texto)
        return resultado
#        return (resultado,lbr)   
    
    @staticmethod
    def splitSentence(texto,max):
        if len(texto)>max:
            l=[texto[i:i+max] for i in range(0,len(texto),max)]
            text=''
            for e,i in enumerate(l):
                if e<len(l)-1 and len(l[e+1])>4:
                    if i[-1].isspace():
                        text=text+i[:-1]+'<br>'
                    else:
                        text=text+i+'<br>'
                else:
                    text=text+i
            return text
        else:
            return texto
    
    @staticmethod
    def writeTextPanel(tp):
        spatialOptions=['entid-selec-intersect','entid-selec-intersect-atrib','buffer-contains',\
        'buffer-contains-attrib','buffer-contains-sum','densidad','densidad valor']
        capa=tp.capa
        texto=''
        texto=''.join([texto,'panel:textPanel','\n'])
        texto=''.join([texto,'capa:'+capa.name(),'\n'])
        texto=''.join([texto,'rutaCapa:'+capa.source(),'\n'])
        texto=''.join([texto,'idCapa:'+capa.id(),'\n'])
        texto=''.join([texto,'x:'+str(tp.relativePosition().x()),'\n'])
        texto=''.join([texto,'y:'+str(tp.relativePosition().y()),'\n'])

        texto=''.join([texto,'title:'+str(tp.title),'\n'])
        texto=''.join([texto,'type:'+str(tp.tipo),'\n'])
        exp=','.join(tp.expresion)
        texto=''.join([texto,'expression:'+exp,'\n'])
        if tp.tipo in spatialOptions:
            pry=QgsProject.instance()
            capa2=pry.mapLayersByName(tp.expresion[0])[0]
            id=capa2.id()
            path=capa2.source()
            texto=texto+'capa2:'+id+','+path+'\n'
        else:
            texto=texto+'capa2:None'+'\n'
        ancho=tp.frameSizeMm().width()
        alto=tp.frameSizeMm().height()
        texto=''.join([texto,'anchoP:'+str(ancho),'\n'])
        texto=''.join([texto,'altoP:'+str(alto),'\n'])
        
        fondTit=qcolorToStr(tp.fondTit)
        texto=texto+'fondTit:'+fondTit+'\n'
        colorTextTit=qcolorToStr(tp.colorTextTit)
        texto=texto+'colorTextTit:'+colorTextTit+'\n'
        fondVal=qcolorToStr(tp.fondVal)
        texto=texto+'fondVal:'+fondVal+'\n'
        colorTextVal=qcolorToStr(tp.colorTextVal)
        texto=texto+'colorTextVal:'+colorTextVal+'\n'
        
        texto=''.join([texto,'suavizado:'+str(tp.suavizado),'\n'])
        texto=''.join([texto,'estilo:'+str(tp.estilo),'\n'])
        if tp.icono:
            texto=''.join([texto,'icono:True','\n'])
        else:
            texto=''.join([texto,'icono:False','\n'])
        if type(tp.rutaIcono)==str:
            texto=''.join([texto,'rutaIcono:'+tp.rutaIcono,'\n'])
        else:
            texto=''.join([texto,'rutaIcono: ','\n'])
        texto=''.join([texto,'direccionIcono:'+tp.direccionIcono,'\n'])
        texto=''.join([texto,'colorIcono:'+str(tp.colorIcono),'\n'])
        return texto
    
    @staticmethod
    def writeBarPanel(tp):
        capa=tp.capa
        texto=''
        texto=''.join([texto,'panel:barrasPanel','\n'])
        texto=''.join([texto,'capa:'+capa.name(),'\n'])
        texto=''.join([texto,'rutaCapa:'+capa.source(),'\n'])
        texto=''.join([texto,'idCapa:'+capa.id(),'\n'])
        texto=''.join([texto,'x:'+str(tp.relativePosition().x()),'\n'])
        texto=''.join([texto,'y:'+str(tp.relativePosition().y()),'\n'])

        texto=''.join([texto,'title:'+str(tp.titulo),'\n'])
        texto=''.join([texto,'type:'+str(tp.tipo),'\n'])
        expresion=tp.expresion
        if type(expresion[0])==str:
            exp=','.join(tp.expresion)
        else:
            exp=','.join(tp.expresion[0])
        texto=''.join([texto,'expression:'+exp,'\n'])
        
        
        colorBar=qcolorToStr(tp.colorBar)
        texto=''.join([texto,'colorBar:'+colorBar,'\n'])
        texto=''.join([texto,'typeColor:'+tp.typeColor,'\n'])
        texto=''.join([texto,'palette:'+tp.palette,'\n'])
        
        colorTit=qcolorToStr(tp.colorTit)
        texto=''.join([texto,'colorTit:'+colorTit,'\n'])
        texto=''.join([texto,'sizeTitle:'+str(tp.sizeTitle),'\n'])
        
        colorLabels=qcolorToStr(tp.colorLabels)
        texto=''.join([texto,'colorLabels:'+colorLabels,'\n'])
        texto=''.join([texto,'sizeLabels:'+str(tp.sizeLabels),'\n'])
        ancho=tp.frameSizeMm().width()
        alto=tp.frameSizeMm().height()
        texto=''.join([texto,'anchoP:'+str(ancho),'\n'])
        texto=''.join([texto,'altoP:'+str(alto),'\n'])
        if tp.wordBreak:
            texto=''.join([texto,'wordBreak:True','\n'])
        else:
            texto=''.join([texto,'wordBreak:False','\n'])
        return texto
    
    @staticmethod
    def writeSeriePanel(tp):
        capa=tp.capa
        texto=''
        texto=''.join([texto,'panel:seriesPanel','\n'])
        texto=''.join([texto,'capa:'+capa.name(),'\n'])
        texto=''.join([texto,'rutaCapa:'+capa.source(),'\n'])
        texto=''.join([texto,'idCapa:'+capa.id(),'\n'])
        texto=''.join([texto,'x:'+str(tp.relativePosition().x()),'\n'])
        texto=''.join([texto,'y:'+str(tp.relativePosition().y()),'\n'])
        campox=tp.expresion[1]
        camposy=','.join(tp.expresion[0])
        
        texto=''.join([texto,'title:'+str(tp.title),'\n'])
        texto=''.join([texto,'camposy:'+camposy,'\n'])
        texto=''.join([texto,'campox:'+campox,'\n'])
        if tp.wordBreak:
            texto=''.join([texto,'wordBreak:True','\n'])
        else:
            texto=''.join([texto,'wordBreak:False','\n'])
        
        colorTit=qcolorToStr(tp.colorTit)
        texto=''.join([texto,'colorTit:'+colorTit,'\n'])
        texto=''.join([texto,'sizeTitle:'+str(tp.sizeTitle),'\n'])
        
        colorLabels=qcolorToStr(tp.colorLabels)
        texto=''.join([texto,'colorLabels:'+colorLabels,'\n'])
        texto=''.join([texto,'sizeLabels:'+str(tp.sizeLabels),'\n'])
        texto=''.join([texto,'widthline:'+str(tp.widthline),'\n'])
        ancho=tp.frameSizeMm().width()
        alto=tp.frameSizeMm().height()
        texto=''.join([texto,'anchoP:'+str(ancho),'\n'])
        texto=''.join([texto,'altoP:'+str(alto),'\n'])
        if tp.fill:
            texto=''.join([texto,'fill:True','\n'])
        else:
            texto=''.join([texto,'fill:False','\n'])
        return texto
    
    @staticmethod
    def writeIndicadorPanel(tp):
        spatialOptions=['entid-selec-intersect','entid-selec-intersect-atrib','buffer-contains',\
        'buffer-contains-attrib','buffer-contains-sum','densidad','densidad valor']
        capa=tp.capa
        texto=''
        texto=''.join([texto,'panel:indicadorPanel','\n'])
        texto=''.join([texto,'capa:'+capa.name(),'\n'])
        texto=''.join([texto,'rutaCapa:'+capa.source(),'\n'])
        texto=''.join([texto,'idCapa:'+capa.id(),'\n'])
        texto=''.join([texto,'x:'+str(tp.relativePosition().x()),'\n'])
        texto=''.join([texto,'y:'+str(tp.relativePosition().y()),'\n'])
        ancho=tp.frameSizeMm().width()
        alto=tp.frameSizeMm().height()
        texto=''.join([texto,'anchoP:'+str(ancho),'\n'])
        texto=''.join([texto,'altoP:'+str(alto),'\n'])
        
        if type(tp.expresion[0])==str:
            exp=','.join(tp.expresion)
        else:
            exp=','.join(tp.expresion[0])
        texto=''.join([texto,'expression:'+exp,'\n'])
        
        texto=''.join([texto,'title:'+str(tp.title),'\n'])
        
        colorTit=qcolorToStr(tp.colorTit)
        texto=''.join([texto,'colorTit:'+colorTit,'\n'])
        
        colorBar=qcolorToStr(tp.colorBar)
        texto=''.join([texto,'colorBar:'+colorBar,'\n'])
        
        colorBackground=qcolorToStr(tp.colorBackground)
        texto=''.join([texto,'colorBackground:'+colorBackground,'\n'])
        
        colorBase=qcolorToStr(tp.colorBase)
        texto=''.join([texto,'colorBase:'+colorBase,'\n'])
        
        colorLine=qcolorToStr(tp.colorLine)
        texto=''.join([texto,'colorLine:'+colorLine,'\n'])
        
        colorFinal=qcolorToStr(tp.colorFinal)
        texto=''.join([texto,'colorFinal:'+colorFinal,'\n'])
        
        colorMark=qcolorToStr(tp.colorMark)
        texto=''.join([texto,'colorMark:'+colorMark,'\n'])
        
        colorValue=qcolorToStr(tp.colorValue)
        texto=''.join([texto,'colorValue:'+colorValue,'\n'])
        texto=''.join([texto,'sizeTitle:'+str(tp.sizeTitle),'\n'])
        texto=''.join([texto,'sizeLabel:'+str(tp.sizeLabel),'\n'])
        texto=''.join([texto,'relative:'+tp.relative,'\n'])
        texto=''.join([texto,'type:'+tp.tipo,'\n'])
        texto=''.join([texto,'estilo:'+tp.estilo,'\n'])
        min=tp.range[0]
        max=tp.range[1]
        texto=''.join([texto,'min:'+str(min),'\n'])
        texto=''.join([texto,'max:'+str(max),'\n'])
        texto=''.join([texto,'threshold:'+str(tp.threshold),'\n'])
        return texto
    
    @staticmethod
    def loadPanels(lista):
        panels=[]
        position=0
        for e,i in enumerate(lista):
            if i=='textPanel':
                position=e+23
                panels.append(lista[e+1:position])
                position=e
            elif i=='barrasPanel':
                position=e+20
                panels.append(lista[e+1:position])
                position=e
            elif i=='seriesPanel':
                position=e+19
                panels.append(lista[e+1:position])
                position=e
            elif i=='indicadorPanel':
                position=e+27
                panels.append(lista[e+1:position])
                position=e
            else:
                position=e
#        print('como lista ',textPanels)
        listDicPanels=[]
        if len(panels)>0:
            for i in panels:
                d={t[0:t.find(':')]:t[t.find(':')+1:len(t)] for t in i}
                listDicPanels.append(d)
        
        return listDicPanels
            
        
    
        
        
        