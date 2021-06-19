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
import random
import numpy as np

contrast=['red','blue','green','lightblue','magenta','orange','cyan','gray','darkblue','lightgray',
            'purple','cyan','pink','rgb(229,245,249)','yellow','rgb(217,95,14)','rgb(255,247,188)',
            'rgb(201,148,199)','rgb(127,205,187)','rgb(117,107,177)','rgb(199,233,180)','rgb(0,109,44)',
            'rgb(55,250,188)']
        
breBlues=['rgb(230,242,255)','rgb(198,247,247)','rgb(247,252,240)','rgb(224,243,219)','rgb(204,235,197)',
           'rgb(168,221,181)','rgb(0, 204, 255)','rgb(77, 136, 255)','rgb(102, 179, 255)','rgb(123,204,196)',
           'rgb(78,179,211)','rgb(51, 153, 255)','rgb(77, 136, 255)','rgb(0, 184, 230)','rgb(43,140,190)',    
           'rgb(8,104,172)','rgb(0, 143, 179)','rgb(0, 122, 153)','rgb(0, 102, 128)','rgb(8,64,129)']

whiteRed=['rgb(255,255,255)','rgb(255,230,240)','rgb(255,179,209)','rgb(255,179,209)','rgb(255,153,194)',
              'rgb(255,128,179)','rgb(255,102,163)','rgb(255,77,148)','rgb(255,51,133)','rgb(255,26,117)',
              'rgb(255,0,102)','rgb(230,0,92)','rgb(rgb(204,0,82)','rgb(179,0,71)','rgb(153,0,61)','rgb(128,0,51)',
              'rgb(102,0,41)','rgb(77,0,31)','rgb(51,0,20)','rgb(26,0,10)']
palettes={'contrast':contrast,'breBlues':breBlues,'whiteRed':whiteRed}

class dashColors:
    def __init__(self):
        self.v=0
    @staticmethod
    def returnPalette(paleta=palettes):
        return paleta.keys()
        
    @staticmethod
    def getPalette(name,nclasses,paleta=palettes):
        palettes=paleta
        if name in palettes:
            palet=palettes[name]
        else:
            palet=palettes['contrast']
        ncolors=len(palet)
        if nclasses<ncolors:
            div=ncolors//nclasses
            listc=[palet[i] for i in range(0,ncolors,div)]
            return "['"+"','".join(listc)+"']"
        else:
            nmissing=nclasses-ncolors
            if palet==self.breBlues:
                red=np.random.randint(0,255,nmissing)
                green=np.random.randint(0,255,nmissing)
                l1=",255)','rgb(".join(str(i[0])+','+str(i[1]) for i in zip(red,green))
                olist="','".join(breBlues)
                return "['"+olist+",rgb('"+l1+",255)'"+"]"
            else:
                red=np.random.randint(0,255,nmissing)
                green=np.random.randint(0,255,nmissing)
                blue=np.random.randint(0,255,nmissing)
                lista=[]
                for i in red:
                    for z in zip(green,blue):
                        t="'rgb("+str(i)+','
                        t2=','.join(str(e) for e in z)+")'"
                        lista.append(t+t2)
                olist="','".join(contrast)
                return "['"+olist+','.join(lista)+']'
        

