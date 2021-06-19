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
from qgis import PyQt
from qgis.PyQt.QtGui import QColor
import os

class styleTextPanel():
    typeStyles=('Separate frames','United frames','One frame')
    def __init__(self,title='',fondTit='black',colorTextTit='white',fondVal='lightblue', colorTextVal='black',\
    estilo='Separate frames',icono=False,rutaIcono=None,suavizado=0,\
        direccionIcono='center',colorIcono=0):
        self.styles={'Separate frames':self.twoFrames,'United frames':self.tim,'One frame':self.oneFrame}
        self.title=title
        self.style=estilo
        self.html=''
        self.html0=''
        self.value='<p class='+'"valor"><strong>0</strong></p>'+'\n'
        self.colorTitle=fondTit
        self.colorFontTitle=colorTextTit
        self.colorValue=fondVal
        self.colorFontValue=colorTextVal
        self.suavizado=suavizado
        #Icon settings
        self.iconPath=rutaIcono
        self.icon=icono  #boolean
        self.iconDirection=direccionIcono
        self.iconColor=colorIcono
    
    @classmethod
    def getTypeStyles(estilo):
        tipos=estilo.typeStyles
        return tipos
        
    def assignStyle(self,estilo):
        if estilo in self.styles:
            self.style=estilo
            self.styles[estilo]()
            
    def twoFrames(self):
        self.evalColors()
        self.html0='<html lang='+"es"+'>'+'\n'+\
        '<style>'+'\n'+\
        '.titulo {'+'\n'+\
        'padding-top: 7vw;'+'\n'+\
        'margin-bottom: 1px;'+'\n'+\
        'margin-right: 5px;'+'\n'+\
        'word-wrap: 15;'+'\n'+\
        'overflow: hidden;'+'\n'+\
        'height: 37%;'+'\n'+\
        'width: 95%;'+'\n'+\
        'display: block;'+'\n'+\
        'border-left-style: solid;'+'\n'+\
        'border-width: thick;'+'\n'+\
        'border-color: blue;'+'\n'+\
        'box-shadow: 5px 5px gray;'+'\n'+\
        'border-radius: '+str(self.suavizado)+'px;'+'\n'+\
        'background-color: '+self.colorTitle+';'+'\n'+\
        'font-size: 8.7vw;'+'\n'+\
        'font-family:Arial,Sans-serif;'+'\n'+\
        'color: '+self.colorFontTitle+';'+'\n'+\
        'text-align: center;}'+'\n'+\
        '.valor {'+'\n'+\
        '  height: 39%;'+'\n'+\
        '  width: 95%;'+'\n'+\
        '  padding-top: 4vw;'+'\n'+\
        '  margin-top: 5px;'+'\n'+\
        '  margin-right: 5px;'+'\n'+\
        '  font-family:Arial Black,Sans-serif;'+'\n'+\
        '  font-size: 14vw;'+'\n'+\
        '  display: block;'+'\n'+\
        '  border-left-style: solid;'+'\n'+\
        '  border-width: thick;'+'\n'+\
        '  border-color: blue;'+'\n'+\
        '  box-shadow: 5px 5px gray;'+'\n'+\
        '  border-radius: '+str(self.suavizado)+'px;'+'\n'+\
        '  background-color: '+self.colorValue+';'+'\n'+\
        '  text-align: center;'+'\n'+\
        '  color: '+self.colorFontValue+';}'+'\n'+\
        '}'+'\n'+\
        '.paneli{'+'\n'+\
        '  height: 80%;'+'\n'+\
        '}'+'\n'+\
        '</style>'+'\n'+\
        '<body>'+'\n'+\
        '<div class="paneli" style=text-align:center>'
        self.html=self.html0
        self.defTitle()
        self.defValue()
        self.defCierre()
    
    def tim(self):
        self.evalColors()
        self.html0='<html lang='+"es"+'>'+'\n'+\
        '<head>'+'\n'+\
        '<style>'+'\n'+\
        '.titulo {'+'\n'+\
        '  height:35%;'+'\n'+\
        '  margin-top: 0px;'+'\n'+\
        '  margin-bottom: -4vw;'+'\n'+\
        '  word-wrap: 15;'+'\n'+\
        '  overflow: hidden;'+'\n'+\
        '  display: block;'+'\n'+\
        '  background-color: '+self.colorTitle+';'+'\n'+\
        '  font-size: 8vw;'+'\n'+\
        '  font-family:Arial,Sans-serif;'+'\n'+\
        '  color: '+self.colorFontTitle+';'+'\n'+\
        '  text-align: center;}'+'\n'+\
        '.valor {'+'\n'+\
        '  height:50%;'+'\n'+\
        '  padding-top: 4px;'+'\n'+\
        '  margin-top: 0px;'+'\n'+\
        '  font-family:Arial Black,Sans-serif;'+'\n'+\
        '  font-size: 15vw;'+'\n'+\
        '  display: block;'+'\n'+\
        '  background-color: '+self.colorValue+';'+'\n'+\
        '  text-align: center;'+'\n'+\
        '  color: '+self.colorFontValue+';}'+'\n'+\
        '.imagen{'+'\n'+\
        '  padding-top: -2px;'+'\n'+\
        '  margin-bottom: 0px;'+'\n'+\
        '  text-align: center;'+'\n'+\
        '  height:24%;'+'\n'+\
        '  background-color: '+self.colorTitle+';}'+'\n'+\
        '.paneli{'+'\n'+\
        '  height:100%;'+'\n'+\
        '  font-size: 5vw;'+'\n'+\
        '  text-align: center;'+'\n'+\
        '  overflow: hidden;'+'\n'+\
        '  background-color: '+self.colorTitle+';'+'\n'+\
        '  display: block;}'+'\n'
        self.html=self.html0
        self.closeDIV()
        self.defTitle()
        self.defValue()
        self.defCierre()   
    
    def oneFrame(self):
        self.evalColors()
        self.html0='<html lang='+"es"+'>'+'\n'+\
        '<head>'+'\n'+\
        '<style>'+'\n'+\
        '.paneli {'+'\n'+\
        '  margin-top: 0px;'+'\n'+\
        '  overflow: hidden;'+'\n'+\
        '  padding-top: 10px;'+'\n'+\
        '  padding-bottom: 2px;'+'\n'+\
        '  height:90%;'+'\n'+\
        '  width:100%;'+'\n'+\
        '  background-color: '+self.colorTitle+';'+'\n'+\
        '  font-family:Arial,Sans-serif;'+'\n'+\
        '  display: block;}'+'\n'+\
        '.valor{'+'\n'+\
        '  font-size:18vw;'+'\n'+\
        '  padding-top: 5px;'+'\n'+\
        '  margin-top:0px;'+'\n'+\
        '  margin-left:7px;'+'\n'+\
        '  color: '+self.colorFontTitle+';'+'\n'+\
        '  align:left;}'+'\n'+\
        '.titulo{'+'\n'+\
        '  word-wrap: 15;'+'\n'+\
        '  font-size:10vw;'+'\n'+\
        '  margin-top:-30px;'+'\n'+\
        '  margin-left:7px;'+'\n'+\
        '  height:30%;'+'\n'+\
        '  color: '+self.colorFontTitle+';'+'\n'+\
        '  align:left;}'+'\n'+\
        '.imagen{'+'\n'+\
        '  margin-top: -5px;'+'\n'+\
        '  margin-bottom: -2px;'+'\n'+\
        '  height:35%;}'+'\n'
        self.html=self.html0
        self.closeDIV()
        self.defValue()
        self.defTitle()
        self.defCierre()
          
    def defTitle(self):
        if self.title== None or self.title=='':
            tit='<p class='+'"titulo"><strong>Panel de texto</strong></p>'+'\n'
        else:
            tit='<p class='+'"titulo"><strong>'+self.title+'</strong></p>'+'\n'
        self.html=self.html+tit
    
    def defValue(self):
        self.html=self.html+self.value
    
    def defCierre(self):
        cierre= '</div>'+'\n'+\
        '</body>'+'\n'+\
        '</html>'
        self.html=self.html+cierre
    
    def setTitle(self,texto):
        self.title=texto
        self.update()
    
    def closeDIV(self):
        if self.style=='United frames' and self.icon==True and os.path.exists(self.iconPath):
            print('entrp a cierre div',self.iconColor)
            textIm='.r{filter:invert('+str(self.iconColor)+');'+'\n'+\
            'padding-top: 2px;'+'\n'+\
            'margin-top: 0px;'+'\n'+\
            'margin-bottom: 0px;'+'\n'+\
            'height:100%;'+'\n'+\
            '}'+'\n'+\
            '</style>'+'\n'+\
            '<body>'+'\n'+\
            '<div class="paneli" >'+'\n'+\
            '<div class="imagen" style=text-align:'+self.iconDirection+'>'+\
            '<img class='+"'r'"+' src=file:///'+self.iconPath+' alt='+'"icono"'+\
            'height='+'"27"'+'></div>'
        elif self.style=='One frame' and\
        self.icon==True and os.path.exists(self.iconPath):
            print('entro cierre div entero')
            textIm='.r{filter:invert('+str(self.iconColor)+');'+'\n'+\
            'height:100%;}'+'\n'+\
            '</style>'+'\n'+\
            '<body>'+'\n'+\
            '<div class="paneli" >'+'\n'+\
            '<div class="imagen" style=text-align:'+self.iconDirection+'>'+\
            '<img class='+"'r'"+' src=file:///'+self.iconPath+' alt='+'"icono"'+\
            'height='+'"27"'+'></div>'
        else:
            textIm='</style>'+'\n'+\
            '<body>'+'\n'+\
            '<div class="paneli" >'+'\n'+\
            '<div class="imagen"></div>'
        self.html=self.html+textIm
        
    def update(self):
        self.styles[self.style]()
        
    def evalColors(self):
        colors=[self.colorTitle,self.colorFontTitle,self.colorValue,self.colorFontValue]
        lc=map(lambda x:'rgb('+str(x.red())+','+str(x.green())+','+str(x.blue())+')'\
        if type(x)==QColor else x,colors)
        self.colorTitle,self.colorFontTitle,self.colorValue,self.colorFontValue=lc
        
#    def colorTextTitle(self,color):
#        self.colFontTitulo=color
#        self.update()
#        
#    def colorBackTitle(self,color):
#        self.colorTitulo=color
#        self.update()
#        
#    def colorTextValue(self,color):
#        self.colFontValor=color
#        self.update()
#            
#    def colorBackValue(self,color):
#        self.colorValor=color
#        self.update()
        
    
    