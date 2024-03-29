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
from qgis.PyQt import uic
import os
from qgis import PyQt
from qgis.PyQt import*
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtCore import *
from qgis.core import *
from qgis.gui import QgsSvgSelectorWidget
from .panels.stylesIndicadorPanel import styleIndicadorPanel
from .panels.stylesTextPanel import styleTextPanel
from .panels.stylesBarPanel import styleBarPanel
from .panels.operations import operations
from .panels.textPanel import textPanel
from .panels.indicadorPanel import indicadorPanel
from .panels.seriesPanel import seriesPanel
from .panels.barrasPanel import barrasPanel
#from .panels.groupPanel6 import groupPanel
from .myUtils.dashColors import dashColors
from .panels.adminPanel import adminPanel

from .calculations import *
from .register import logControl

DialogUi, DialogType=uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'QGIS_Dashboard_dialog_base.ui'))

class dashDialog(DialogUi, DialogType):
    """Construction and management of the panel creation wizard """
    def __init__(self,iface,manager):
        """Constructor.

        :param mapCanvas Represents a drawing window, it is where the 
        layers are displayed (raster, vector, ..)..
        :type canvas: QgsMapCanvas
        """
        super().__init__()
        self.setupUi(self)   #initializes everything done in QtDesigner
        self.dir = os.path.dirname(__file__)
        self.posicion='topLeft'
        self.setWindowTitle("-----Builder of  Dashboard----")
        self.npaneles=0
        #gestor de paneles
        self.manager=manager
        self.listaPaneles=[]
        #Predefined panel sizes
        self.sizesPanels={'Medium':(40,30),'Small':(35,25),'Large':(45,35)}
        #iface
        self.iface=iface
        #MapCanvas
        self.canvas=self.iface.mapCanvas()
#        self.adminDash=groupPanel(canvas)
        #REFERENCE TO THE PROJECT
        self.pry=QgsProject.instance()
        #MAXIMIZE AND MINIMIZE BUTTON
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        #VARIABLES ICON
        self.icono=False
        self.ruta_icono=''
        
        #septup dialog Box
        #updates the label when changing the number of panels
        self.cbnPaneles.currentTextChanged.connect(self.cambioNPaneles)
        self.labelNp.textChanged.connect(self.cambioLabel)
        #---------------------------------------
        self.paginador.setCurrentIndex(0)
        self.siguiente.setFlat(False)
        self.siguiente.clicked.connect(self.cambiarPagina)
        #Set up the Series field list for multiple selections.
        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget2.setSelectionMode(QAbstractItemView.ExtendedSelection)
        
        #LOADING LOGOS AND ICONS
        icoTop= QtGui.QPixmap(os.path.join(self.dir,'images','iconTop.png'))
        self.l0.setPixmap(icoTop)
        self.l0.resize(icoTop.width(),icoTop.height())
        self.l0.setSizePolicy(QtWidgets.QSizePolicy\
        (QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding))
        icoBar= QtGui.QPixmap(os.path.join(self.dir,'images','barras.png'))
        self.lbar.setPixmap(icoBar)
        self.lbar.resize(icoBar.width(),icoBar.height())
        self.lbar.setSizePolicy(QtWidgets.QSizePolicy\
        (QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding))
        icoIndi= QtGui.QPixmap(os.path.join(self.dir,'images','indicador.png'))
        self.lindicador.setPixmap(icoIndi)
        self.lindicador.resize(icoIndi.width(),icoIndi.height())
#        self.lindicador.setSizePolicy(QtWidgets.QSizePolicy\
#        (QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding))
        icoPanel= QtGui.QPixmap(os.path.join(self.dir,'images','panel.png'))
        self.lpanel.setPixmap(icoPanel)
        self.lpanel.resize(icoPanel.width(),icoPanel.height())
        icoSerie= QtGui.QPixmap(os.path.join(self.dir,'images','serie.png'))
        self.lserie.setPixmap(icoSerie)
        self.lserie.resize(icoSerie.width(),icoSerie.height())
        self.lserie.setSizePolicy(QtWidgets.QSizePolicy\
        (QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding))
        icoCenter= QtGui.QPixmap(os.path.join(self.dir,'images','iconCenter.png'))
#        self.lcenter.setPixmap(icoCenter)
#        self.lcenter.resize(icoCenter.width(),icoCenter.height())
#        self.lcenter.setSizePolicy(QtWidgets.QSizePolicy\
#        (QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding))
        
        #error log
        self.log=logControl()
        self.logAcces=self.log.canWriteLog()
        
        #GENERAL DASHBOARD SETTINGS
        self.checkBoxToolTip.setChecked(False)
        self.checkBoxMarco.setChecked(True)
        #SETTINGS checkbox of bar, line
        self.optColor.setChecked(True)
        self.opPalette.setChecked(False)
        self.splitTextBar.setChecked(False)
        self.opLineStyle.setChecked(True)
        self.opAreaStyle.setChecked(False)
        self.splitTextLine.setChecked(False)
        #Initializing predefined panel sizes
        self.cbSizePanel.addItems(self.sizesPanels.keys())
        
        #TOOLBOX BAR PANEL SETTINGS
        self.barToolBox.setCurrentIndex(0)
        self.modBarras.clear()
        self.modBarras.addItems(['Values of a field (Attribute)','Multiple fields'])
        self.colorBar.setColor(QColor(111,158,235))
        self.colorTitleBar.setColor(QColor('black'))
        self.colorLabelBar.setColor(QColor('black'))
        self.spTitleSizeBar.setValue(12)
        self.spLabelSizeBar.setValue(9)
        self.paletteBar.addItems(dashColors.returnPalette())
        self.paletteBar.setEnabled(False)
        if self.optColor.isChecked()==False:
            self.optColor.setChecked(True)
        #CONECT EVENTS
        self.optColor.toggled.connect(self.cambiarColorBar)
        self.opPalette.toggled.connect(self.cambiarColorBar)
        
        #TOOLBOX LINE PANEL SETTINGS
        self.lineToolBox.setCurrentIndex(0)
        self.colorTitleline.setColor(QColor('black'))
        self.labelColorLine.setColor(QColor('black'))
        self.spTitleSizeLine.setValue(12)
        self.spLabelSizeLine.setValue(9)
        if self.opLineStyle.isChecked()==False:
            self.opLineStyle.setChecked(True)
        
        #TOOLBOX OF TEXTPANEL SETTINGS
        self.tptoolBox.setCurrentIndex(0)#colocamos en modalidad de calculo
        self.cbTextPestilo.clear()
        self.cbTextPestilo.addItems(styleTextPanel.getTypeStyles())
        self.cbTextPestilo.setCurrentIndex(0)
        #colores de panel text. Fondos
        self.ctitPanelText.setColor(QColor("black"))
        self.cconPanelText.setColor(QColor(254,196,79))
        #colores de panel text. Textos
        self.cTextTitPT.setColor(QColor("white"))
        self.cTextConPT.setColor(QColor("black"))
        #Colocar icono en panel-------
        self.checkBoxIcono.setChecked(False)
        self.ubiIcono.setCurrentIndex(0)#por defecto ubica el icono en el centro
        self.color_icono.setCurrentIndex(1)#por defecto color invertido
        #UBICAR Y CONFIGURAR EL SELECTOR DE ICONOS SVG
        self.svg_selector_widget = QgsSvgSelectorWidget()
        #EVENTO AL SELECCIONAR UN ICONO
        self.svg_selector_widget.svgSelected.connect(self.svg_seleccionado)
        self.scrollArea.setWidget(self.svg_selector_widget)
        self.svg_selector_widget.show()
        #Configuraciones dependiendo del estilo seleccionado
        self.cbTextPestilo.currentTextChanged.connect(self.cambioPanelTextEstilo)
        self.cbTextPestilo.setCurrentIndex(0)
        self.cambioPanelTextEstilo()
        #EVENTO CAMBIO CAPA SECUNDARIA
        self.cap2PanelTexto.currentTextChanged.connect(self.cambioCapaSecundTextP)
        
        #TOOLBOX INDICATOR PANEL SETTINGS
        self.indToolBox.setCurrentIndex(0)
        self.cbIndEstilo.clear()
        self.cbIndEstilo.addItems(styleIndicadorPanel.getTypeStyles())
        self.cbIndEstilo.setCurrentIndex(0)
        self.indTitleColor.setColor(QColor("black"))
        self.indBaseColor.setColor(QColor("lightGray"))
        self.indLineColor.setColor(QColor("red"))
        self.indFinalColor.setColor(QColor("darkGray"))
        self.indMarkColor.setColor(QColor("red"))
        self.indBarColor.setColor(QColor("blue"))
        self.indBackColor.setColor(QColor("white"))
        self.indColorValue.setColor(QColor("black"))
        
        #BOTONES PARA DEFINIR POSICION
        self.posi1=QPushButton('')
        self.posi2=QPushButton('')
        self.posi3=QPushButton('')
        self.posi4=QPushButton('')
        self.posi5=QPushButton('')
        self.posi6=QPushButton('')
        self.configurarPosiciones()
        self.cargarCapasCampos()
        self.capaSecundariaInd()
        self.iniciarModalidad()
        self.iniciarModalidadInd()
        self.iniciarModalidadBarras()
        #Capa secudnaria text panel
        self.capaSecundariaTextP()
        #---------------------
        #EVENTO PROCESAR PANEL
        self.procPanelT.clicked.connect(self.procesarTextPanel)
        #EVENTO PROCESAR INDICADOR
        self.procIndicador.clicked.connect(self.procesarIndicador)
        #EVENTO PROCESAR BARRAS
        self.procBarras.clicked.connect(self.procesarBarras)
        #EVENTO PROCESAR SERIES
        self.procSeries.clicked.connect(self.procesarSeries)
        #EVENTO ACEPTAR CANCELAR
        self.accepted.connect(self.aceptar)
        self.rejected.connect(self.cancelar)
        #EVENTOS DEL PROYECTO
        self.pry.layersWillBeRemoved.connect(self.capaRemovida)
        self.pry.layersAdded.connect(self.capaAdicionada)
    
    #TEXT PANEL: configuracion de los tool dependiendo del estilo
    def cambioPanelTextEstilo(self):
        if self.cbTextPestilo.currentText()=='Separate frames':
            self.checkBoxIcono.setEnabled(False)
            self.ubiIcono.setEnabled(False)
            self.color_icono.setEnabled(False)
            self.svg_selector_widget.setEnabled(False)
            self.roundFrame.setEnabled(True)
            self.cTextTitPT.setEnabled(True);self.cconPanelText.setEnabled(True);self.cTextConPT.setEnabled(True)
        elif self.cbTextPestilo.currentText()=='One frame':
            self.cTextTitPT.setEnabled(True);self.cconPanelText.setEnabled(False);self.cTextConPT.setEnabled(False)
            self.checkBoxIcono.setEnabled(True)
            self.ubiIcono.setEnabled(True)
            self.color_icono.setEnabled(True)
            self.roundFrame.setEnabled(False)
            self.svg_selector_widget.setEnabled(True)
        elif self.cbTextPestilo.currentText()=='United frames':
            self.checkBoxIcono.setEnabled(True)
            self.ubiIcono.setEnabled(True)
            self.svg_selector_widget.setEnabled(True)
            self.color_icono.setEnabled(True)
            self.roundFrame.setEnabled(False)
            self.cTextTitPT.setEnabled(True);self.cconPanelText.setEnabled(True);self.cTextConPT.setEnabled(True)
            
    #ALMACENA LA RUTA DEL ICONO SELECCIONADO
    def svg_seleccionado(self,path):
        self.ruta_icono=path
    
    #CUANDO EL NUMERO DE PANELES SEA 0, BLOQUEA PROCESAR
    def cambioLabel(self,e):
        if int(e)==0:
            self.procPanelT.setEnabled(False)
            self.procIndicador.setEnabled(False)
            self.procBarras.setEnabled(False)
            self.procSeries.setEnabled(False)
            
    def aceptar(self):
        if len(self.listaPaneles) >0:
            try:
                self.manager.posicion=self.posicion
                self.manager.init(self.canvas)
                ancho= self.sizesPanels[self.cbSizePanel.currentText()][0]
                alto= self.sizesPanels[self.cbSizePanel.currentText()][1]
                self.manager.initPlacePanels(ancho,alto)
                self.manager.addPanels(self.listaPaneles)
                #Verificamos si el check del borde esta checkeado o no
                if self.checkBoxMarco.isChecked()==False:
                    self.manager.globalBordeMarco=False
                if self.checkBoxToolTip.isChecked()==True:
                    self.manager.globalToolTip=True
                self.manager.placePanels()
            except Exception as e:
                if self.logAcces:
                    self.log.writeLog(str(e))
    
    def cancelar(self):
        self.listaPaneles.clear()
#        print('cancelar')
    
    def procesarSeries(self):
        #CREAMOS EL GRAFICO
        titulo=self.lineEdit.text()
        if titulo=='':
            titulo='Serie of data'
        items=self.listWidget.selectedItems()
        camposn=[i.text() for i in items]
        campox=self.camXSeries.currentText()
        ancho= self.sizesPanels[self.cbSizePanel.currentText()][0]
        alto= self.sizesPanels[self.cbSizePanel.currentText()][1]
        if len(camposn)>1:
            #Disminuimos el numero de paneles disponibles
            np=int(self.labelNp.text())-1
            self.labelNp.setText(str(np))
            if self.opLineStyle.isChecked():
                fill=False
            else:
                fill=True
            if self.splitTextLine.isChecked():
                wordBreak=True
            else:
                wordBreak=False
#            try:
            tp=seriesPanel(self.capa,[camposn,campox],title=titulo,fill=fill,wordBreak=wordBreak,\
                    widthline=self.widthLine.value(),colorTit=self.colorTitleline.color(),\
                    sizeTitle=self.spTitleSizeLine.value(),colorLabels=self.labelColorLine.color(),\
                    sizeLabels=self.spLabelSizeLine.value(),anchoP=ancho,altoP=alto)
#            except Exception as e:
#                if self.logAcces:
#                    self.log.writeLog(str(e))
#            try:
            self.listaPaneles.append(tp)
#            except Exception as e:
#                print(str(e))
#                if self.logAcces:
#                    self.log.writeLog(str(e))
    
    def procesarBarras(self):
        #CREAMOS EL GRAFICO
        titulo=self.lineEdit.text()
        if self.opPalette.isChecked():
            typeColor='palette'
        else:
            typeColor='unicolor'
        if self.splitTextBar.isChecked():
            wordBreak=True
        else:
            wordBreak=False
        if titulo=='':
            titulo='Bar Graphic'
        #Dimensiones
        ancho= self.sizesPanels[self.cbSizePanel.currentText()][0]
        alto= self.sizesPanels[self.cbSizePanel.currentText()][1]
        try:
            if self.modBarras.currentText()=='Values of a field (Attribute)':
                campox=self.camXBar.currentText()
                campoy=self.camYBar.currentText()
                print('value a field',campox,campoy)
                if len(campox)>0 and len(campoy)>0:
                    tp=barrasPanel(self.capa,'atributo-sum',titulo,[campox,campoy],\
                    colorBar=self.colorBar.color(),colorTit=self.colorTitleBar.color(),typeColor=typeColor,\
                    wordBreak=wordBreak,sizeTitle=self.spTitleSizeBar.value(),sizeLabels=self.spLabelSizeBar.value(),\
                    colorLabels=self.colorLabelBar.color(),palette=self.paletteBar.currentText(),\
                    anchoP=ancho,altoP=alto)
            elif self.modBarras.currentText()=='Multiple fields':
                items=self.listWidget2.selectedItems()
                campos=[i.text() for i in items]
                print('en multiple fields',campos)
                if len(campos)>1:
                    tp=barrasPanel(self.capa,'multiple_fields',titulo,[campos],\
                    colorBar=self.colorBar.color(),colorTit=self.colorTitleBar.color(),typeColor=typeColor,\
                    wordBreak=wordBreak,sizeTitle=self.spTitleSizeBar.value(),sizeLabels=self.spLabelSizeBar.value(),\
                    colorLabels=self.colorLabelBar.color(),palette=self.paletteBar.currentText(),\
                    anchoP=ancho,altoP=alto)
        except Exception as e:
            print(str(e))
            if self.logAcces:
                self.log.writeLog(str(e))
        try:
            self.listaPaneles.append(tp)
            #Disminuimos el numero de paneles disponibles
            np=int(self.labelNp.text())-1
            self.labelNp.setText(str(np))
        except Exception as e:
            if self.logAcces:
                self.log.writeLog(str(e))
    
    def cambiarColorBar(self):
        if self.sender()==self.optColor:
            self.colorBar.setEnabled(True)
            self.paletteBar.setEnabled(False)
        elif self.sender()==self.opPalette:
            self.colorBar.setEnabled(False)
            self.paletteBar.setEnabled(True)
    
    def procesarTextPanel(self):
        #CREAMOS EL PANEL
        titulo=self.lineEdit.text()
        if titulo=='':
            titulo='Text Panel'
        capa=self.capa.name()
        modo=self.cbModoPanelT.currentText()
        estilot=self.cbTextPestilo.currentText()
        #Verifcamos el icono
        if self.ubiIcono.currentText()=='Right':
            direcIcono='right'
        elif self.ubiIcono.currentText()=='Left':
            direcIcono='left'
        else:
            direcIcono='center'
        if self.color_icono.currentText()=='Normal':
            self.colorIcono=0
        else:
            self.colorIcono=1
        #Dimensiones
        ancho= self.sizesPanels[self.cbSizePanel.currentText()][0]
        alto= self.sizesPanels[self.cbSizePanel.currentText()][1]
        try:
            if modo=='Total selected entities':
                if self.checkBoxIcono.isChecked()==True and os.path.exists(self.ruta_icono) and\
                self.cbTextPestilo.currentText()!='Separate frames':
                    tp=textPanel(self.capa, 'entid_seleccionadas', titulo,[],\
                    fondTit=self.ctitPanelText.color(),colorTextTit=self.cTextTitPT.color(),\
                    fondVal=self.cconPanelText.color(),colorTextVal=self.cTextConPT.color(),\
                    estilo=estilot,icono=True,rutaIcono=self.ruta_icono,\
                    direccionIcono=direcIcono,colorIcono=str(self.colorIcono),anchoP=ancho,altoP=alto)
                else:
                    tp=textPanel(self.capa, 'entid_seleccionadas', titulo,[],\
                    fondTit=self.ctitPanelText.color(),colorTextTit=self.cTextTitPT.color(),\
                    fondVal=self.cconPanelText.color(),colorTextVal=self.cTextConPT.color(),\
                    suavizado=self.roundFrame.value(),estilo=estilot,anchoP=ancho,altoP=alto)
            elif modo=='Percentage':
                campo=self.cam1PanelTexto.currentText()
                if self.checkBoxIcono.isChecked()==True and os.path.exists(self.ruta_icono) and\
                self.cbTextPestilo.currentText()!='Separate frames':
                    tp=textPanel(self.capa,'Porcentaje',titulo,[campo],\
                    fondTit=self.ctitPanelText.color(),colorTextTit=self.cTextTitPT.color(),\
                    fondVal=self.cconPanelText.color(),colorTextVal=self.cTextConPT.color(),\
                    estilo=estilot,icono=True,rutaIcono=self.ruta_icono,\
                    direccionIcono=direcIcono,colorIcono=str(self.colorIcono),anchoP=ancho,altoP=alto)
                else:
                    tp=textPanel(self.capa,'Porcentaje',titulo,[campo],\
                    fondTit=self.ctitPanelText.color(),colorTextTit=self.cTextTitPT.color(),\
                    fondVal=self.cconPanelText.color(),colorTextVal=self.cTextConPT.color(),\
                    suavizado=self.roundFrame.value(),estilo=estilot,anchoP=ancho,altoP=alto)
            elif modo=='Sum of an attribute':
                campo=self.cam1PanelTexto.currentText()
                if self.checkBoxIcono.isChecked()==True and os.path.exists(self.ruta_icono) and\
                self.cbTextPestilo.currentText()!='Separate frames':
                    tp=textPanel(self.capa,'atributo',titulo,[campo],\
                    fondTit=self.ctitPanelText.color(),colorTextTit=self.cTextTitPT.color(),\
                    fondVal=self.cconPanelText.color(),colorTextVal=self.cTextConPT.color(),\
                    estilo=estilot,icono=True,rutaIcono=self.ruta_icono,\
                    direccionIcono=direcIcono,colorIcono=str(self.colorIcono),anchoP=ancho,altoP=alto)
                else:
                    tp=textPanel(self.capa,'atributo',titulo,[campo],\
                    fondTit=self.ctitPanelText.color(),colorTextTit=self.cTextTitPT.color(),\
                    fondVal=self.cconPanelText.color(),colorTextVal=self.cTextConPT.color(),\
                    suavizado=self.roundFrame.value(),estilo=estilot,anchoP=ancho,altoP=alto)
            elif modo=='Statistics. Selected entities':
                campo=self.cam1PanelTexto.currentText()
                operador=self.operadorPanelT.currentText()
                if self.checkBoxIcono.isChecked()==True and os.path.exists(self.ruta_icono) and\
                self.cbTextPestilo.currentText()!='Separate frames':
                    tp=textPanel(self.capa,'math-atributo',titulo,[campo,operador],
                    fondTit=self.ctitPanelText.color(),colorTextTit=self.cTextTitPT.color(),\
                    fondVal=self.cconPanelText.color(),colorTextVal=self.cTextConPT.color(),\
                    estilo=estilot,icono=True,rutaIcono=self.ruta_icono,\
                    direccionIcono=direcIcono,colorIcono=str(self.colorIcono),anchoP=ancho,altoP=alto)
                else:
                    tp=textPanel(self.capa,'math-atributo',titulo,[campo,operador],\
                    fondTit=self.ctitPanelText.color(),colorTextTit=self.cTextTitPT.color(),\
                    fondVal=self.cconPanelText.color(),colorTextVal=self.cTextConPT.color(),\
                    suavizado=self.roundFrame.value(),estilo=estilot,anchoP=ancho,altoP=alto)
            elif modo=='Statistics. Selection that coincides with':
                campo=self.cam1PanelTexto.currentText()
                operador=self.operadorPanelT.currentText()
                campos=self.cam2PanelTexto.currentText()
                atrib=self.lineE1.text()
                if self.checkBoxIcono.isChecked()==True and os.path.exists(self.ruta_icono) and\
                self.cbTextPestilo.currentText()!='Separate frames':
                    tp=textPanel(capa,'math-atributo',titulo,[campo,operador,campos,atrib],\
                    fondTit=self.ctitPanelText.color(),colorTextTit=self.cTextTitPT.color(),\
                    fondVal=self.cconPanelText.color(),colorTextVal=self.cTextConPT.color(),\
                    estilo=estilot,icono=True,rutaIcono=self.ruta_icono,\
                    direccionIcono=direcIcono,colorIcono=str(self.colorIcono),anchoP=ancho,altoP=alto)
                else:
                    tp=textPanel(self.capa,'math-atributo',titulo,[campo,operador,campos,atrib],\
                    fondTit=self.ctitPanelText.color(),colorTextTit=self.cTextTitPT.color(),\
                    fondVal=self.cconPanelText.color(),colorTextVal=self.cTextConPT.color(),\
                    suavizado=self.roundFrame.value(),estilo=estilot,anchoP=ancho,altoP=alto)
            elif modo=='Entities contained in selection':
                capa2=self.cap2PanelTexto.currentText()
                if self.capa==self.cap2PanelTexto.currentData():
                    self.iface.messageBar().pushMessage('ERROR',\
                    'Select a different layer than the main layer', level=Qgis.Warning, duration=7)
                else:
                    if self.checkBoxIcono.isChecked()==True and os.path.exists(self.ruta_icono) and\
                    self.cbTextPestilo.currentText()!='Separate frames':
                        tp=textPanel(self.capa, 'entid-selec-intersect', titulo,[capa2],\
                        fondTit=self.ctitPanelText.color(),colorTextTit=self.cTextTitPT.color(),\
                        fondVal=self.cconPanelText.color(),colorTextVal=self.cTextConPT.color(),\
                        estilo=estilot,icono=True,rutaIcono=self.ruta_icono,\
                        direccionIcono=direcIcono,colorIcono=str(self.colorIcono),anchoP=ancho,altoP=alto)
                    else:
                        tp=textPanel(self.capa, 'entid-selec-intersect', titulo,[capa2],\
                        fondTit=self.ctitPanelText.color(),colorTextTit=self.cTextTitPT.color(),\
                        fondVal=self.cconPanelText.color(),colorTextVal=self.cTextConPT.color(),\
                        suavizado=self.roundFrame.value(),estilo=estilot,anchoP=ancho,altoP=alto)
            elif modo=='Entities contained. count by attribute that coincides with':
                capa2=self.cap2PanelTexto.currentText()
                campo2=self.cam3PanelTexto.currentText()
                valor=self.lineE1.text()
                if self.capa==self.cap2PanelTexto.currentData():
                    self.iface.messageBar().pushMessage('ERROR',\
                    'Select a different layer than the main layer', level=Qgis.Warning, duration=7)
                else:
                    if self.checkBoxIcono.isChecked()==True and os.path.exists(self.ruta_icono) and\
                    self.cbTextPestilo.currentText()!='Separate frames':
                        tp=textPanel(self.capa,'entid-selec-intersect-atrib', titulo,\
                        [capa2,campo2,valor],fondTit=self.ctitPanelText.color(),colorTextTit=self.cTextTitPT.color(),\
                        fondVal=self.cconPanelText.color(),colorTextVal=self.cTextConPT.color(),\
                        estilo=estilot,icono=True,rutaIcono=self.ruta_icono,anchoP=ancho,altoP=alto,\
                        direccionIcono=direcIcono,colorIcono=str(self.colorIcono))
                    else:
                        tp=textPanel(self.capa, 'entid-selec-intersect-atrib', titulo,[capa2,campo2,valor],\
                        fondTit=self.ctitPanelText.color(),colorTextTit=self.cTextTitPT.color(),\
                        fondVal=self.cconPanelText.color(),colorTextVal=self.cTextConPT.color(),\
                        suavizado=self.roundFrame.value(),estilo=estilot,anchoP=ancho,altoP=alto)
            elif modo=='Number of entities in the area. Density':
                capa2=self.cap2PanelTexto.currentText()
                crs=self.capa.crs()
                if self.capa==self.cap2PanelTexto.currentData():
                    self.iface.messageBar().pushMessage('ERROR',\
                    'Select a different layer than the main layer', level=Qgis.Warning, duration=7)
                else:
                    if crs.isGeographic():
                        self.iface.messageBar().pushMessage('Layer in geographic coordinates',\
                        'The main layer is in geographic coordinates. Lat/Long The value will be processed in degrees', level=Qgis.Info, duration=7)
                        unidad=1
                    else:
                        if crs.mapUnits() != QgsUnitTypes.DistanceMeters:
                            self.iface.messageBar().pushMessage('Coordinate units will be considered in meters',\
                            'For now, only units of the coordinate system in meters are considered', level=Qgis.Info, duration=7)
                        unidad=self.tpUnit.currentText()   
                    if self.checkBoxIcono.isChecked()==True and os.path.exists(self.ruta_icono) and\
                        self.cbTextPestilo.currentText()!='Separate frames':
                        tp=textPanel(self.capa,'densidad', titulo,\
                        [capa2,unidad],fondTit=self.ctitPanelText.color(),colorTextTit=self.cTextTitPT.color(),\
                        fondVal=self.cconPanelText.color(),colorTextVal=self.cTextConPT.color(),\
                        estilo=estilot,icono=True,rutaIcono=self.ruta_icono,anchoP=ancho,altoP=alto,\
                        direccionIcono=direcIcono,colorIcono=str(self.colorIcono))
                    else:
                        tp=textPanel(self.capa, 'densidad', titulo,[capa2,unidad],\
                        fondTit=self.ctitPanelText.color(),colorTextTit=self.cTextTitPT.color(),\
                        fondVal=self.cconPanelText.color(),colorTextVal=self.cTextConPT.color(),\
                        suavizado=self.roundFrame.value(),estilo=estilot,anchoP=ancho,altoP=alto)
            elif modo=='Sum of attribute between area. Density':
                capa2=self.cap2PanelTexto.currentText()
                campo2=self.cam3PanelTexto.currentText()
                crs=self.capa.crs()
                if self.capa==self.cap2PanelTexto.currentData():
                    self.iface.messageBar().pushMessage('ERROR',\
                    'Select a different layer than the main layer', level=Qgis.Warning, duration=7)
                else:
                    if crs.isGeographic():
                        self.iface.messageBar().pushMessage('Layer in geographic coordinates',\
                        'The main layer is in geographic coordinates. Lat/Long The value will be processed in degrees', level=Qgis.Info, duration=7)
                        unidad=1
                    else:
                        if crs.mapUnits() != QgsUnitTypes.DistanceMeters:
                            self.iface.messageBar().pushMessage('Coordinate units will be considered in meters',\
                            'For now, only units of the coordinate system in meters are considered', level=Qgis.Info, duration=7)
                        unidad=self.tpUnit.currentText()
                    if self.checkBoxIcono.isChecked()==True and os.path.exists(self.ruta_icono) and\
                        self.cbTextPestilo.currentText()!='Separate frames':
                        tp=textPanel(self.capa,'densidad valor', titulo,\
                        [capa2,unidad,campo2],fondTit=self.ctitPanelText.color(),colorTextTit=self.cTextTitPT.color(),\
                        fondVal=self.cconPanelText.color(),colorTextVal=self.cTextConPT.color(),\
                        estilo=estilot,icono=True,rutaIcono=self.ruta_icono,anchoP=ancho,altoP=alto,\
                        direccionIcono=direcIcono,colorIcono=str(self.colorIcono))
                    else:
                        tp=textPanel(self.capa, 'densidad valor', titulo,[capa2,unidad,campo2],\
                        fondTit=self.ctitPanelText.color(),colorTextTit=self.cTextTitPT.color(),\
                        fondVal=self.cconPanelText.color(),colorTextVal=self.cTextConPT.color(),\
                        suavizado=self.roundFrame.value(),estilo=estilot,anchoP=ancho,altoP=alto)
            elif modo=='Entities contained at a distance. Buffer':
                capa2=self.cap2PanelTexto.currentText()
                dist=self.bufferDistance.value()
                crs=self.capa.crs()
                if self.capa==self.cap2PanelTexto.currentData():
                    self.iface.messageBar().pushMessage('ERROR',\
                    'Select a different layer than the main layer', level=Qgis.Warning, duration=7)
                else:
                    if crs.isGeographic():
                        self.iface.messageBar().pushMessage('Layer in geographic coordinates',\
                        'The main layer is in geographic coordinates. Lat/Long The value will'+\
                        'be processed in degrees', level=Qgis.Info, duration=7)
                    if self.checkBoxIcono.isChecked()==True and os.path.exists(self.ruta_icono) and\
                        self.cbTextPestilo.currentText()!='Separate frames':
                        tp=textPanel(self.capa,'buffer-contains', titulo,\
                        [capa2,dist],fondTit=self.ctitPanelText.color(),colorTextTit=self.cTextTitPT.color(),\
                        fondVal=self.cconPanelText.color(),colorTextVal=self.cTextConPT.color(),\
                        estilo=estilot,icono=True,rutaIcono=self.ruta_icono,anchoP=ancho,altoP=alto,\
                        direccionIcono=direcIcono,colorIcono=str(self.colorIcono))
                    else:
                        tp=textPanel(self.capa, 'buffer-contains', titulo,[capa2,dist],\
                        fondTit=self.ctitPanelText.color(),colorTextTit=self.cTextTitPT.color(),\
                        fondVal=self.cconPanelText.color(),colorTextVal=self.cTextConPT.color(),\
                        suavizado=self.roundFrame.value(),estilo=estilot,anchoP=ancho,altoP=alto)
            elif modo=='Entities contained at a distance that coincides with':
                capa2=self.cap2PanelTexto.currentText()
                dist=self.bufferDistance.value()
                campo2=self.cam3PanelTexto.currentText()
                valor=self.lineE1.text()
                crs=self.capa.crs()
                if self.capa==self.cap2PanelTexto.currentData():
                    self.iface.messageBar().pushMessage('ERROR',\
                    'Select a different layer than the main layer', level=Qgis.Warning, duration=7)
                else:
                    if crs.isGeographic():
                        self.iface.messageBar().pushMessage('Layer in geographic coordinates',\
                        'The main layer is in geographic coordinates. Lat/Long The value will'+\
                        'be processed in degrees', level=Qgis.Info, duration=7)
                    if self.checkBoxIcono.isChecked()==True and os.path.exists(self.ruta_icono) and\
                        self.cbTextPestilo.currentText()!='Separate frames':
                        tp=textPanel(self.capa,'buffer-contains-attrib', titulo,\
                        [capa2,dist,campo2,valor],fondTit=self.ctitPanelText.color(),colorTextTit=self.cTextTitPT.color(),\
                        fondVal=self.cconPanelText.color(),colorTextVal=self.cTextConPT.color(),\
                        estilo=estilot,icono=True,rutaIcono=self.ruta_icono,anchoP=ancho,altoP=alto,\
                        direccionIcono=direcIcono,colorIcono=str(self.colorIcono))
                    else:
                        tp=textPanel(self.capa,'buffer-contains-attrib', titulo,[capa2,dist,campo2,valor],\
                        fondTit=self.ctitPanelText.color(),colorTextTit=self.cTextTitPT.color(),\
                        fondVal=self.cconPanelText.color(),colorTextVal=self.cTextConPT.color(),\
                        suavizado=self.roundFrame.value(),estilo=estilot,anchoP=ancho,altoP=alto)    
            elif modo=='Sum of attributes of entities contained at a distance':
                capa2=self.cap2PanelTexto.currentText()
                dist=self.bufferDistance.value()
                campo2=self.cam3PanelTexto.currentText()
                layer2=self.cap2PanelTexto.currentData()
                fields=layer2.fields()
                field=fields.field(campo2)
                crs=self.capa.crs()
                if self.capa==self.cap2PanelTexto.currentData():
                    self.iface.messageBar().pushMessage('ERROR',\
                    'Select a different layer than the main layer', level=Qgis.Warning, duration=7)
                elif field.isNumeric() == False:
                    self.iface.messageBar().pushMessage('ERROR',\
                    'Select a numeric field', level=Qgis.Warning, duration=7)
                else:
                    if crs.isGeographic():
                        self.iface.messageBar().pushMessage('Layer in geographic coordinates',\
                        'The main layer is in geographic coordinates. Lat/Long The value will'+\
                        'be processed in degrees', level=Qgis.Info, duration=7)
                    if self.checkBoxIcono.isChecked()==True and os.path.exists(self.ruta_icono) and\
                        self.cbTextPestilo.currentText()!='Separate frames':
                        tp=textPanel(self.capa,'buffer-contains-sum', titulo,\
                        [capa2,dist,campo2,''],fondTit=self.ctitPanelText.color(),colorTextTit=self.cTextTitPT.color(),\
                        fondVal=self.cconPanelText.color(),colorTextVal=self.cTextConPT.color(),\
                        estilo=estilot,icono=True,rutaIcono=self.ruta_icono,anchoP=ancho,altoP=alto,\
                        direccionIcono=direcIcono,colorIcono=str(self.colorIcono))
                    else:
                        tp=textPanel(self.capa,'buffer-contains-sum', titulo,[capa2,dist,campo2,''],\
                        fondTit=self.ctitPanelText.color(),colorTextTit=self.cTextTitPT.color(),\
                        fondVal=self.cconPanelText.color(),colorTextVal=self.cTextConPT.color(),\
                        suavizado=self.roundFrame.value(),estilo=estilot,anchoP=ancho,altoP=alto)   
            
            if type(tp)==textPanel:
                self.listaPaneles.append(tp)
                #Disminuimos el numero de paneles disponibles
                np=int(self.labelNp.text())-1
                self.labelNp.setText(str(np))
        except Exception as e:
            print(str(e))
            if self.logAcces:
                self.log.writeLog(str(e))
            
#Modalidades en PANEL TEXT: Total entidades seleccionadas,
#Suma de un atributo,Estadistica. Entidades seleccionadas,
#Estadistica selección que coincide con
    def iniciarModalidad(self):
        indice=self.cbModoPanelT.findText('Total selected entities')
        self.cbModoPanelT.setCurrentIndex(indice)
        self.cam1PanelTexto.setEnabled(False)
        self.cam2PanelTexto.setEnabled(False)
        self.cam3PanelTexto.setEnabled(False)
        self.cap2PanelTexto.setEnabled(False)
        self.lineE1.setEnabled(False)
        self.operadorPanelT.setEnabled(False)
        self.bufferDistance.setEnabled(False)
        self.tpUnit.setEnabled(False)
        #EVENTOS
        self.cbModoPanelT.currentTextChanged.connect(self.cambioModo)

#INICIAR Modalidades en GRAFICO BARRAS 
    def iniciarModalidadBarras(self):
        indice=self.modBarras.findText('Values of a field (Attribute)')
        self.modBarras.setCurrentIndex(indice)
        self.listWidget2.setEnabled(False)
        #EVENTOS
        self.modBarras.currentTextChanged.connect(self.cambioModoBarras)
#Evento cambio de modalidad Grafico de Barras
    def cambioModoBarras(self):
        modo=self.modBarras.currentText()
        if modo=='Values of a field (Attribute)':
            self.listWidget2.setEnabled(False)
            self.camXBar.setEnabled(True)
            self.camYBar.setEnabled(True)
        elif modo=='Multiple fields':
            self.listWidget2.setEnabled(True)
            self.camXBar.setEnabled(False)
            self.camYBar.setEnabled(False)
    
    def cargarCapasCampos(self):
        #Cargamos las capas presentes en el mapa
        listacapas= self.pry.mapLayers().values()  #Lista de capas
        #------Filtramos y guardamos solo las capas Vector--------
        #------Utilizaremos las listas para cargar los combo Box--------
        self.listC=[] #Lista de capas vectoriales
        for i in listacapas:
            try:
                if  i.type()==QgsMapLayer.VectorLayer or isinstance(i,QgsVectorLayer):
                    if i.featureCount()>0:
                        self.listC.append(i)
            except Exception as e:
                if self.logAcces:
                    self.log.writeLog(e)
        #Si no hay capas cerrar
        if len(self.listC)==0:
            self.cierre()
        else:
            for i in self.listC:
                self.lc.addItem(i.name(),i)
            #Llenamos las listas de campos
            self.capa= self.lc.currentData()
            qfields=self.capa.fields()
            if qfields.count()>0:
                for i in qfields.toList():
                    if i.isNumeric():
                        self.cam1Ind.addItem(i.name()) #indicador
                        self.cam1PanelTexto.addItem(i.name())#panel texto
                        self.camYBar.addItem(i.name()) #campo categorico grafico barras
                        self.listWidget.addItem(i.name())#lista de campos numericos para grafico series
                        self.listWidget2.addItem(i.name())#lista de campos numericos para grafico Barras
                    else:
                        self.cam2Ind.addItem(i.name())#campo2 indicador
                        self.cam2PanelTexto.addItem(i.name())#panel texto
                        self.camXBar.addItem(i.name())
                        self.camXSeries.addItem(i.name())#campo categorico grafico series
                        
            #CONECTAR EVENTOS
            self.lc.currentTextChanged.connect(self.cambioCapa)
            self.updateOperations()
        
    def cambioCapa(self):
        if self.lc.count()==0 or self.lc.currentText()is "":
            self.cierre()
        else:
            self.capa=self.lc.currentData()
            self.cam1PanelTexto.clear()#vaciamos el listado de campos principal
            self.cam2PanelTexto.clear()#vaciamos el listado de campos secundario
            self.listWidget.clear()
            self.listWidget2.clear()
            self.camXSeries.clear()
            self.cam1Ind.clear()
            self.cam2Ind.clear()
            self.camYBar.clear()
            self.camXBar.clear()
            qfields=self.capa.fields()
            if qfields.count()>0:
                for i in qfields.toList():
                    if i.isNumeric():
                        self.cam1PanelTexto.addItem(i.name())#indicador
                        self.cam1Ind.addItem(i.name())#panel texto
                        self.camYBar.addItem(i.name())
                        self.listWidget.addItem(i.name())
                        self.listWidget2.addItem(i.name())
                    else:
                        self.cam2Ind.addItem(i.name())#campo2 indicador
                        self.cam2PanelTexto.addItem(i.name())
                        self.camXBar.addItem(i.name())
                        self.camXSeries.addItem(i.name())
            self.updateOperations()
    
    #ACTUALIZAMOS EL LISTADO DE OPERACIONES DE TEXT PANEL DEACUERDO AL TIPO DE CAPA
    def updateOperations(self):
        capa=self.capa
        tipoGeom=capa.geometryType()
        try:
            if capa.isSpatial()==False:
                self.cbModoPanelT.clear()
                self.cbModoInd.clear()
                listaFunciones=operations.getOperation('no spatial')
                self.cbModoPanelT.addItems(listaFunciones)
                listaFunInd=operations.getOperation('ind no spatial')
                self.cbModoInd.addItems(listaFunInd)
            else:
                if tipoGeom==QgsWkbTypes.PointGeometry or tipoGeom==QgsWkbTypes.LineGeometry:
                    self.cbModoPanelT.clear()
                    self.cbModoInd.clear()
                    listaFunciones=operations.getOperation('line or point')
                    self.cbModoPanelT.addItems(listaFunciones)
                    listaFunInd=operations.getOperation('ind line or point')
                    self.cbModoInd.addItems(listaFunInd)
                elif tipoGeom==QgsWkbTypes.PolygonGeometry:
                    self.cbModoPanelT.clear()
                    self.cbModoInd.clear()
                    listaFunciones=operations.getOperation('polygon')
                    self.cbModoPanelT.addItems(listaFunciones)
                    listaFunInd=operations.getOperation('ind polygon')
                    self.cbModoInd.addItems(listaFunInd)
                    
        except Exception as e:
            if self.logAcces:
                self.log.writeLog(e)
            #enviar un message bar capa no reconocida
                        
    #DEFINIMOS LA CAPA SECUNDARIA DE TEXT PANEL. LA CAPA QUE INTERSECTA
    def capaSecundariaTextP(self):
        if self.lc.count()>0 or self.lc.currentText()!= "":
            self.cap2PanelTexto.clear()
            capaPrincipal=self.lc.currentData()
            for i in self.listC:
    #            if i!=capaPrincipal:
                try:
                    if i.isSpatial():
                        self.cap2PanelTexto.addItem(i.name(),i)
                except:
                    pass
            capa2=self.cap2PanelTexto.currentData()
            qfields=capa2.fields()
            self.cam3PanelTexto.clear()
            if qfields.count()>0:
                for i in qfields.toList():
                    self.cam3PanelTexto.addItem(i.name())
    
    #Evento cuando seleccionamos otra capa secundaria.Text Panel
    def cambioCapaSecundTextP(self):
        if self.cap2PanelTexto.count()>0:
    #        print('n lista capas2 ',self.cap2PanelTexto.count())
            capa2=self.cap2PanelTexto.currentData()
    #        print(capa2)
            qfields=capa2.fields()
            self.cam3PanelTexto.clear()
            if qfields.count()>0:
                for i in qfields.toList():
                    self.cam3PanelTexto.addItem(i.name())
    
    #DEFINIMOS LA CAPA SECUNDARIA DE INDICADOR. LA CAPA QUE INTERSECTA
    def capaSecundariaInd(self):
        if self.lc.count()>0 or self.lc.currentText()!= "":
            self.capa2ind.clear()
            for i in self.listC:
    #            if i!=capaPrincipal:
                try:
                    if i.isSpatial():
                        self.capa2ind.addItem(i.name(),i)
                except:
                    pass
            #Llenamos las listas de campos
            capa2=self.capa2ind.currentData()
            qfields=capa2.fields()
            self.cam2Ind.clear()
            if qfields.count()>0:
                for i in qfields.toList():
                    self.cam2Ind.addItem(i.name())
            self.capa2ind.currentTextChanged.connect(self.cambioCapaSecund)
    
    #Evento cuando seleccionamos otra capa secundaria.indicador
    def cambioCapaSecund(self):
        if self.capa2ind.count()>0:
            capa=self.capa2ind.currentData()
            self.cam2Ind.clear()#vaciamos el listado de campos principal
            qfields=capa.fields()
            if qfields.count()>0:
                for i in qfields.toList():
                    self.cam2Ind.addItem(i.name())#indicador

    def nombreCapaCambio(self):
        pass
    
    def cierre(self):
        self.close()
        
    def cambiarPagina(self,e):
        self.paginador.setCurrentIndex(1)
        self.npaneles=self.cbnPaneles.currentText()
        self.labelNp.setText(str(self.npaneles))
    
    def cambioNPaneles(self):
        self.npaneles=self.cbnPaneles.currentText()
        self.labelNp.setText(str(self.npaneles))
        
    def configurarPosiciones(self):
        css = """
        QGroupBox{
            color:white;}"""
        self.posiciones.setStyleSheet(css) 
        grid = QGridLayout()
        grid.setContentsMargins(2,2,2,2)
        self.iupposi1=QIcon(os.path.join(self.dir,'images','b1.png'))
        self.idposi1=QIcon(os.path.join(self.dir,'images','b1a.png'))
        self.posi1.setIcon(self.idposi1)
        self.posi1.setIconSize(QSize(100,70))
        self.posi1.setSizePolicy(QtWidgets.QSizePolicy\
        (QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding))
        grid.addWidget(self.posi1,0,0)
        self.iupposi2=QIcon(os.path.join(self.dir,'images','b2.png'))
        self.idposi2=QIcon(os.path.join(self.dir,'images','b2a.png'))
        self.posi2.setIcon(self.iupposi2)
        self.posi2.setIconSize(QSize(100,70))
        self.posi2.setSizePolicy(QtWidgets.QSizePolicy\
        (QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding))
        grid.addWidget(self.posi2,0,1)
        self.iupposi3=QIcon(os.path.join(self.dir,'images','b3.png'))
        self.idposi3=QIcon(os.path.join(self.dir,'images','b3a.png'))
        self.posi3.setIcon(self.iupposi3)
        self.posi3.setIconSize(QSize(100,70))
        self.posi3.setSizePolicy(QtWidgets.QSizePolicy\
        (QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding))
        grid.addWidget(self.posi3,1,0)
        self.iupposi4=QIcon(os.path.join(self.dir,'images','b4.png'))
        self.idposi4=QIcon(os.path.join(self.dir,'images','b4a.png'))
        self.posi4.setIcon(self.iupposi4)
        self.posi4.setIconSize(QSize(100,70))
        self.posi4.setSizePolicy(QtWidgets.QSizePolicy\
        (QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding))
        grid.addWidget(self.posi4,1,1)
        self.iupposi5=QIcon(os.path.join(self.dir,'images','b5.png'))
        self.idposi5=QIcon(os.path.join(self.dir,'images','b5a.png'))
        self.posi5.setIcon(self.iupposi5)
        self.posi5.setIconSize(QSize(100,70))
        self.posi5.setSizePolicy(QtWidgets.QSizePolicy\
        (QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding))
        grid.addWidget(self.posi5,2,0)
        self.iupposi6=QIcon(os.path.join(self.dir,'images', 'b6.png'))
        self.idposi6=QIcon(os.path.join(self.dir,'images', 'b6a.png'))
        self.posi6.setIcon(self.iupposi6)
        self.posi6.setIconSize(QSize(100,70))
        self.posi6.setSizePolicy(QtWidgets.QSizePolicy\
        (QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding))
        grid.addWidget(self.posi6,2,1)
        self.posiciones.setLayout(grid)
        self.posiciones.setAutoFillBackground(True)
        palette = self.posiciones.palette()
        palette.setColor(QPalette.Window, QColor('black'))
        self.posiciones.setPalette(palette)
        #EVENTOS DE LOS BOTONES
        self.posi1.clicked.connect(self.defPosi1)
        self.posi2.clicked.connect(self.defPosi2)
        self.posi3.clicked.connect(self.defPosi3)
        self.posi4.clicked.connect(self.defPosi4)
        self.posi5.clicked.connect(self.defPosi5)
        self.posi6.clicked.connect(self.defPosi6)
    
    def defPosi1(self,e):
        if self.posicion!='topLeft':
            self.posicion='topLeft'
            self.posi1.setIcon(self.idposi1)
            self.posi2.setIcon(self.iupposi2)
            self.posi3.setIcon(self.iupposi3)
            self.posi4.setIcon(self.iupposi4)
            self.posi5.setIcon(self.iupposi5)
            self.posi6.setIcon(self.iupposi6)
    
    def defPosi2(self,e):
        if self.posicion!='topRight':
            self.posicion='topRight'
            self.posi1.setIcon(self.iupposi1)
            self.posi2.setIcon(self.idposi2)
            self.posi3.setIcon(self.iupposi3)
            self.posi4.setIcon(self.iupposi4)
            self.posi5.setIcon(self.iupposi5)
            self.posi6.setIcon(self.iupposi6)
    
    def defPosi3(self,e):
        if self.posicion!='bottomLeft':
            self.posicion='bottomLeft'
            self.posi1.setIcon(self.iupposi1)
            self.posi2.setIcon(self.iupposi2)
            self.posi3.setIcon(self.idposi3)
            self.posi4.setIcon(self.iupposi4)
            self.posi5.setIcon(self.iupposi5)
            self.posi6.setIcon(self.iupposi6)
    
    def defPosi4(self,e):
        if self.posicion!='bottomRight':
            self.posicion='bottomRight'
            self.posi1.setIcon(self.iupposi1)
            self.posi2.setIcon(self.iupposi2)
            self.posi3.setIcon(self.iupposi3)
            self.posi4.setIcon(self.idposi4)
            self.posi5.setIcon(self.iupposi5)
            self.posi6.setIcon(self.iupposi6)
    
    def defPosi5(self,e):
        if self.posicion!='horizontalTop':
            self.posicion='horizontalTop'
            self.posi1.setIcon(self.iupposi1)
            self.posi2.setIcon(self.iupposi2)
            self.posi3.setIcon(self.iupposi3)
            self.posi4.setIcon(self.iupposi4)
            self.posi5.setIcon(self.idposi5)
            self.posi6.setIcon(self.iupposi6)
    
    def defPosi6(self,e):
        if self.posicion!='horizontalBottom':
            self.posicion='horizontalBottom'
            self.posi1.setIcon(self.iupposi1)
            self.posi2.setIcon(self.iupposi2)
            self.posi3.setIcon(self.iupposi3)
            self.posi4.setIcon(self.iupposi4)
            self.posi5.setIcon(self.iupposi5)
            self.posi6.setIcon(self.idposi6)
    
    def cambioModo(self):
        modo=self.cbModoPanelT.currentText()
        if modo=='Total selected entities':
            self.cam1PanelTexto.setEnabled(False)
            self.cam2PanelTexto.setEnabled(False)
            self.lineE1.setEnabled(False)
            self.operadorPanelT.setEnabled(False)
            self.cap2PanelTexto.setEnabled(False)
            self.cam3PanelTexto.setEnabled(False)
            self.bufferDistance.setEnabled(False)
            self.tpUnit.setEnabled(False)
        elif modo=='Percentage':
            self.cam1PanelTexto.setEnabled(True)
            self.cam2PanelTexto.setEnabled(False)
            self.lineE1.setEnabled(False)
            self.operadorPanelT.setEnabled(False)
            self.cap2PanelTexto.setEnabled(False)
            self.cam3PanelTexto.setEnabled(False)
            self.bufferDistance.setEnabled(False)
            self.tpUnit.setEnabled(False)
        elif modo=='Sum of an attribute':
            self.cam1PanelTexto.setEnabled(True)
            self.cam2PanelTexto.setEnabled(False)
            self.lineE1.setEnabled(False)
            self.operadorPanelT.setEnabled(False)
            self.cap2PanelTexto.setEnabled(False)
            self.cam3PanelTexto.setEnabled(False)
            self.bufferDistance.setEnabled(False)
            self.tpUnit.setEnabled(False)
        elif modo=='Statistics. Selected entities':
            self.cam1PanelTexto.setEnabled(True)
            self.cam2PanelTexto.setEnabled(False)
            self.lineE1.setEnabled(False)
            self.cap2PanelTexto.setEnabled(False)
            self.cam3PanelTexto.setEnabled(False)
            self.operadorPanelT.setEnabled(True)
            self.bufferDistance.setEnabled(False)
            self.tpUnit.setEnabled(False)
        elif modo=='Statistics. Selection that coincides with':
            self.cam1PanelTexto.setEnabled(True)
            self.cam2PanelTexto.setEnabled(True)
            self.lineE1.setEnabled(True)
            self.operadorPanelT.setEnabled(True)
            self.cap2PanelTexto.setEnabled(False)
            self.cam3PanelTexto.setEnabled(False)
            self.bufferDistance.setEnabled(False)
            self.tpUnit.setEnabled(False)
        elif modo=='Entities contained in selection':
            self.cap2PanelTexto.setEnabled(True)
            self.cam3PanelTexto.setEnabled(False)
            self.cam1PanelTexto.setEnabled(False)
            self.cam2PanelTexto.setEnabled(False)
            self.lineE1.setEnabled(False)
            self.operadorPanelT.setEnabled(False)
            self.bufferDistance.setEnabled(False)
            self.tpUnit.setEnabled(False)
        elif modo=='Entities contained. count by attribute that coincides with':
            self.cap2PanelTexto.setEnabled(True)
            self.cam3PanelTexto.setEnabled(True)
            self.cam1PanelTexto.setEnabled(False)
            self.cam2PanelTexto.setEnabled(False)
            self.lineE1.setEnabled(True)
            self.operadorPanelT.setEnabled(False)
            self.bufferDistance.setEnabled(False)
            self.tpUnit.setEnabled(False)
        elif modo=='Entities contained at a distance. Buffer':
            self.cap2PanelTexto.setEnabled(True)
            self.cam3PanelTexto.setEnabled(False)
            self.cam1PanelTexto.setEnabled(False)
            self.cam2PanelTexto.setEnabled(False)
            self.lineE1.setEnabled(False)
            self.operadorPanelT.setEnabled(False)
            self.bufferDistance.setEnabled(True)
            self.tpUnit.setEnabled(True)
        elif modo=='Entities contained at a distance that coincides with':
            self.cap2PanelTexto.setEnabled(True)
            self.cam3PanelTexto.setEnabled(True)
            self.cam1PanelTexto.setEnabled(False)
            self.cam2PanelTexto.setEnabled(False)
            self.lineE1.setEnabled(True)
            self.operadorPanelT.setEnabled(False)
            self.bufferDistance.setEnabled(True)
            self.tpUnit.setEnabled(True)
        elif modo=='Sum of attributes of entities contained at a distance':
            self.cap2PanelTexto.setEnabled(True)
            #update cam3 only numeric field
            self.cam3PanelTexto.setEnabled(True)
            self.cam1PanelTexto.setEnabled(False)
            self.cam2PanelTexto.setEnabled(False)
            self.lineE1.setEnabled(False)
            self.operadorPanelT.setEnabled(False)
            self.bufferDistance.setEnabled(True)
            self.tpUnit.setEnabled(True)
        elif modo=='Number of entities in the area. Density':
            self.cap2PanelTexto.setEnabled(True)
            self.cam3PanelTexto.setEnabled(False)
            self.cam1PanelTexto.setEnabled(False)
            self.cam2PanelTexto.setEnabled(False)
            self.lineE1.setEnabled(False)
            self.operadorPanelT.setEnabled(False)
            self.bufferDistance.setEnabled(False)
            self.tpUnit.setEnabled(True)
        elif modo=='Sum of attribute between area. Density':
            self.cap2PanelTexto.setEnabled(True)
            #update cam3 only numeric field
            self.cam3PanelTexto.setEnabled(True)
            self.cam1PanelTexto.setEnabled(False)
            self.cam2PanelTexto.setEnabled(False)
            self.lineE1.setEnabled(False)
            self.operadorPanelT.setEnabled(False)
            self.bufferDistance.setEnabled(False)
            self.tpUnit.setEnabled(True)
    
#Modalidades en Indicador: Valor en tabla de atributos,Densidad 
#Entidades contenidas en seleccion,Entidades contenidas en seleccion con valor,
    def iniciarModalidadInd(self):
        self.cbModoInd.setCurrentIndex(0)
        self.cam1Ind.setEnabled(True)
        self.cam2Ind.setEnabled(False)
        self.capa2ind.setEnabled(False)
        self.valorInd.setEnabled(False)
        self.unidadInd.setEnabled(False)
        self.indBufferDistance.setEnabled(False)
        #EVENTOS
        self.cbModoInd.currentTextChanged.connect(self.cambioModoInd)
    
    def procesarIndicador(self):
        modo=self.cbModoInd.currentText()
        min=self.indMin.value()
        max=self.indMax.value()
        umbral=self.indUmbral_2.value()
        titulo=self.lineEdit.text()
        estilo=self.cbIndEstilo.currentText()
        campo=self.cam1Ind.currentText()
        if self.cbIndThreshold.currentText()=='Value difference':
            formatValue='false'
        else:
            formatValue='true'
        
        if titulo=='':
            titulo='Indicador'
        #Dimensiones
        ancho= self.sizesPanels[self.cbSizePanel.currentText()][0]
        alto= self.sizesPanels[self.cbSizePanel.currentText()][1]
       
        if max==min:
            self.iface.messageBar().pushMessage('ERROR',\
            'Assign a different value to the maximum and minimum value', level=Qgis.Warning, duration=7)
        else:
            try:
                if modo=='Sum of an attribute':
                    indp=indicadorPanel(self.capa,'atributo',titulo,[campo],umbral,[min,max],estilo=estilo,\
                        anchoP=ancho,altoP=alto,colorBar=self.indBarColor.color(),colorBackground=self.indBackColor.color(),\
                        colorTit=self.indTitleColor.color(),sizeTitle=self.indTitleSize.value(),\
                        colorBase=self.indBaseColor.color(),colorLine=self.indLineColor.color(),\
                        sizeLabel=self.indLabelSize.value(),colorFinal=self.indFinalColor.color(),\
                        colorValue=self.indColorValue.color(),colorMark=self.indMarkColor.color(),relative=formatValue)

                elif modo=='Entities contained in selection':
                    capa2=self.capa2ind.currentText()
                    if self.capa==self.capa2ind.currentData():
                        self.iface.messageBar().pushMessage('ERROR',\
                        'Select a different layer than the main layer', level=Qgis.Warning, duration=7)
                    else:
                        indp=indicadorPanel(self.capa,'entid-selec-intersect',titulo,[capa2],umbral,[min,max],estilo=estilo,\
                        anchoP=ancho,altoP=alto,colorBar=self.indBarColor.color(),colorBackground=self.indBackColor.color(),\
                        colorTit=self.indTitleColor.color(),sizeTitle=self.indTitleSize.value(),\
                        colorBase=self.indBaseColor.color(),colorLine=self.indLineColor.color(),\
                        sizeLabel=self.indLabelSize.value(),colorFinal=self.indFinalColor.color(),\
                        colorValue=self.indColorValue.color(),colorMark=self.indMarkColor.color(),relative=formatValue)

                elif modo=='Entities contained. count by attribute that coincides with':
                    capa2=self.capa2ind.currentText()
                    campo2=self.cam2Ind.currentText()
                    valor=self.valorInd.text()
                    if self.capa==self.capa2ind.currentData():
                        self.iface.messageBar().pushMessage('ERROR',\
                        'Select a different layer than the main layer', level=Qgis.Warning, duration=7)
                    else:
                        indp=indicadorPanel(self.capa,'entid-selec-intersect-atrib',titulo,[capa2,campo2,valor],umbral,[min,max],estilo=estilo,\
                        anchoP=ancho,altoP=alto,colorBar=self.indBarColor.color(),colorBackground=self.indBackColor.color(),\
                        colorTit=self.indTitleColor.color(),sizeTitle=self.indTitleSize.value(),\
                        colorBase=self.indBaseColor.color(),colorLine=self.indLineColor.color(),\
                        sizeLabel=self.indLabelSize.value(),colorFinal=self.indFinalColor.color(),\
                        colorValue=self.indColorValue.color(),colorMark=self.indMarkColor.color(),relative=formatValue)

                elif modo=='Number of entities in the area. Density':
                    capa2=self.capa2ind.currentText()
                    crs=self.capa.crs()
                    if self.capa==self.capa2ind.currentData():
                        self.iface.messageBar().pushMessage('ERROR',\
                        'Select a different layer than the main layer', level=Qgis.Warning, duration=7)
                    else:
                        if crs.isGeographic():
                            self.iface.messageBar().pushMessage('Layer in geographic coordinates',\
                            'The main layer is in geographic coordinates. Lat/Long The value will be processed in degrees', level=Qgis.Info, duration=7)
                            unidad=1
                        else:
                            if crs.mapUnits() != QgsUnitTypes.DistanceMeters:
                                self.iface.messageBar().pushMessage('Coordinate units will be considered in meters',\
                                'For now, only units of the coordinate system in meters are considered', level=Qgis.Info, duration=7)
                            unidad=self.unidadInd.currentText()
                        indp=indicadorPanel(self.capa,'densidad',titulo,[capa2,unidad],umbral,[min,max],estilo=estilo,\
                        anchoP=ancho,altoP=alto,colorBar=self.indBarColor.color(),colorBackground=self.indBackColor.color(),\
                        colorTit=self.indTitleColor.color(),sizeTitle=self.indTitleSize.value(),\
                        colorBase=self.indBaseColor.color(),colorLine=self.indLineColor.color(),\
                        sizeLabel=self.indLabelSize.value(),colorFinal=self.indFinalColor.color(),\
                        colorValue=self.indColorValue.color(),colorMark=self.indMarkColor.color(),relative=formatValue)

                elif modo=='Sum of attribute between area. Density':
                    capa2=self.capa2ind.currentText()
                    campo2=self.cam2Ind.currentText()
                    crs=self.capa.crs()
                    if self.capa==self.capa2ind.currentData():
                        self.iface.messageBar().pushMessage('ERROR',\
                        'Select a different layer than the main layer', level=Qgis.Warning, duration=7)
                    else:
                        if crs.isGeographic():
                            self.iface.messageBar().pushMessage('Layer in geographic coordinates',\
                            'The main layer is in geographic coordinates. Lat/Long The value will be processed in degrees', level=Qgis.Info, duration=7)
                            unidad=1
                        else:
                            if crs.mapUnits() != QgsUnitTypes.DistanceMeters:
                                self.iface.messageBar().pushMessage('Coordinate units will be considered in meters',\
                                'For now, only units of the coordinate system in meters are considered', level=Qgis.Info, duration=7)
                            unidad=self.unidadInd.currentText()
                        indp=indicadorPanel(self.capa,'densidad',titulo,[capa2,unidad,campo2],umbral,[min,max],estilo=estilo,\
                        anchoP=ancho,altoP=alto,colorBar=self.indBarColor.color(),colorBackground=self.indBackColor.color(),\
                        colorTit=self.indTitleColor.color(),sizeTitle=self.indTitleSize.value(),\
                        colorBase=self.indBaseColor.color(),colorLine=self.indLineColor.color(),\
                        sizeLabel=self.indLabelSize.value(),colorFinal=self.indFinalColor.color(),\
                        colorValue=self.indColorValue.color(),colorMark=self.indMarkColor.color(),relative=formatValue)

                elif modo=='Entities contained at a distance. Buffer':
                    capa2=self.capa2ind.currentText()
                    dist=self.indBufferDistance.value()
                    crs=self.capa.crs()
                    if self.capa==self.capa2ind.currentData():
                        self.iface.messageBar().pushMessage('ERROR',\
                        'Select a different layer than the main layer', level=Qgis.Warning, duration=7)
                    else:
                        if crs.isGeographic():
                            self.iface.messageBar().pushMessage('Layer in geographic coordinates',\
                            'The main layer is in geographic coordinates. Lat/Long The value will'+\
                            'be processed in degrees', level=Qgis.Info, duration=7)
                        indp=indicadorPanel(self.capa,'buffer-contains',titulo,[capa2,dist],umbral,[min,max],estilo=estilo,\
                        anchoP=ancho,altoP=alto,colorBar=self.indBarColor.color(),colorBackground=self.indBackColor.color(),\
                        colorTit=self.indTitleColor.color(),sizeTitle=self.indTitleSize.value(),\
                        colorBase=self.indBaseColor.color(),colorLine=self.indLineColor.color(),\
                        sizeLabel=self.indLabelSize.value(),colorFinal=self.indFinalColor.color(),\
                        colorValue=self.indColorValue.color(),colorMark=self.indMarkColor.color(),relative=formatValue)

                elif modo=='Entities contained at a distance that coincides with':
                    capa2=self.capa2ind.currentText()
                    dist=self.indBufferDistance.value()
                    campo2=self.cam2Ind.currentText()
                    valor=self.valorInd.text()
                    crs=self.capa.crs()
                    if self.capa==self.capa2ind.currentData():
                        self.iface.messageBar().pushMessage('ERROR',\
                        'Select a different layer than the main layer', level=Qgis.Warning, duration=7)
                    else:
                        if crs.isGeographic():
                            self.iface.messageBar().pushMessage('Layer in geographic coordinates',\
                            'The main layer is in geographic coordinates. Lat/Long The value will'+\
                            'be processed in degrees', level=Qgis.Info, duration=7)
                        indp=indicadorPanel(self.capa,'buffer-contains-attrib',titulo,[capa2,dist,campo2,valor],umbral,[min,max],estilo=estilo,\
                        anchoP=ancho,altoP=alto,colorBar=self.indBarColor.color(),colorBackground=self.indBackColor.color(),\
                        colorTit=self.indTitleColor.color(),sizeTitle=self.indTitleSize.value(),\
                        colorBase=self.indBaseColor.color(),colorLine=self.indLineColor.color(),\
                        sizeLabel=self.indLabelSize.value(),colorFinal=self.indFinalColor.color(),\
                        colorValue=self.indColorValue.color(),colorMark=self.indMarkColor.color(),relative=formatValue)

                elif modo=='Sum of attributes of entities contained at a distance':
                    capa2=self.capa2ind.currentText()
                    dist=self.indBufferDistance.value()
                    campo2=self.cam2Ind.currentText()
                    fields=self.capa2ind.currentData().fields()
                    field=fields.field(campo2)
                    crs=self.capa.crs()
                    if self.capa==self.capa2ind.currentData():
                        self.iface.messageBar().pushMessage('ERROR',\
                        'Select a different layer than the main layer', level=Qgis.Warning, duration=7)
                    elif field.isNumeric() == False:
                        self.iface.messageBar().pushMessage('ERROR',\
                        'Select a numeric field', level=Qgis.Warning, duration=7)
                    else:
                        if crs.isGeographic():
                            self.iface.messageBar().pushMessage('Layer in geographic coordinates',\
                            'The main layer is in geographic coordinates. Lat/Long The value will'+\
                            'be processed in degrees', level=Qgis.Info, duration=7)
                        indp=indicadorPanel(self.capa,'buffer-contains-sum',titulo,[capa2,dist,campo2,''],umbral,[min,max],estilo=estilo,\
                        anchoP=ancho,altoP=alto,colorBar=self.indBarColor.color(),colorBackground=self.indBackColor.color(),\
                        colorTit=self.indTitleColor.color(),sizeTitle=self.indTitleSize.value(),\
                        colorBase=self.indBaseColor.color(),colorLine=self.indLineColor.color(),\
                        sizeLabel=self.indLabelSize.value(),colorFinal=self.indFinalColor.color(),\
                        colorValue=self.indColorValue.color(),colorMark=self.indMarkColor.color(),relative=formatValue)
                        
                if type(indp)==indicadorPanel:
                    self.listaPaneles.append(indp)
                    #Disminuimos el numero de paneles disponibles
                    np=int(self.labelNp.text())-1
                    self.labelNp.setText(str(np))
            except Exception as e:
                if self.logAcces:
                    self.log.writeLog(str(e))
    
    def cambioModoInd(self):
        modo=self.cbModoInd.currentText()
        if modo=='Sum of an attribute':
            self.cam1Ind.setEnabled(True)
            self.cam2Ind.setEnabled(False)
            self.capa2ind.setEnabled(False)
            self.valorInd.setEnabled(False)
            self.unidadInd.setEnabled(False)
            self.indBufferDistance.setEnabled(False)
        elif modo=='Entities contained in selection':
            self.cam1Ind.setEnabled(False)
            self.cam2Ind.setEnabled(False)
            self.capa2ind.setEnabled(True)
            self.valorInd.setEnabled(False)
            self.unidadInd.setEnabled(False)
            self.indBufferDistance.setEnabled(False)
        elif modo=='Entities contained. count by attribute that coincides with':
            self.cam1Ind.setEnabled(False)
            self.cam2Ind.setEnabled(True)
            self.capa2ind.setEnabled(True)
            self.valorInd.setEnabled(True)
            self.unidadInd.setEnabled(False)
            self.indBufferDistance.setEnabled(False)
        elif modo=='Entities contained at a distance. Buffer':
            self.cam1Ind.setEnabled(False)
            self.cam2Ind.setEnabled(False)
            self.capa2ind.setEnabled(True)
            self.valorInd.setEnabled(False)
            self.unidadInd.setEnabled(False)
            self.indBufferDistance.setEnabled(True)
        elif modo=='Entities contained at a distance that coincides with':
            self.cam1Ind.setEnabled(False)
            self.cam2Ind.setEnabled(True)
            self.capa2ind.setEnabled(True)
            self.valorInd.setEnabled(True)
            self.unidadInd.setEnabled(False)
            self.indBufferDistance.setEnabled(True)
        elif modo=='Sum of attributes of entities contained at a distance':
            self.cam1Ind.setEnabled(False)
            #update cam2Ind only numeric field
            self.cam2Ind.setEnabled(True)
            self.capa2ind.setEnabled(True)
            self.valorInd.setEnabled(False)
            self.unidadInd.setEnabled(False)
            self.indBufferDistance.setEnabled(True)
        elif modo=='Number of entities in the area. Density':
            self.cam1Ind.setEnabled(False)
            self.cam2Ind.setEnabled(False)
            self.capa2ind.setEnabled(True)
            self.valorInd.setEnabled(False)
            self.unidadInd.setEnabled(True)
            self.indBufferDistance.setEnabled(False)
        elif modo=='Sum of attribute between area. Density':
            self.cam1Ind.setEnabled(False)
            #update cam2Ind only numeric field
            self.cam2Ind.setEnabled(True)
            self.capa2ind.setEnabled(True)
            self.valorInd.setEnabled(False)
            self.unidadInd.setEnabled(True)
            self.indBufferDistance.setEnabled(False)
        
    def capaAdicionada(self,listCapas):
        listc=[] #Lista de capas vectoriales
        for i in listCapas:
            try:
                if  i.type()==QgsMapLayer.VectorLayer or isinstance(i,QgsVectorLayer):
                    if i.featureCount()>0:
                        listc.append(i)
                        self.listC.append(i)
            except Exception as e:
                if self.logAcces:
                    self.log.writeLog(e)
        if len(listc)>0:
            for i in listc:
                self.lc.addItem(i.name(),i)
                self.cap2PanelTexto.addItem(i.name(),i)
                self.capa2ind.addItem(i.name(),i)
    
    def capaRemovida(self,ids):
        for i in ids:
            for j in self.listC:
                if i==j.id():
                    self.listC.remove(j)
                    indice=self.lc.findText(j.name())
                    self.lc.removeItem(indice)
                    indice=self.cap2PanelTexto.findText(j.name())
                    self.cap2PanelTexto.removeItem(indice)
                    indice=self.capa2ind.findText(j.name())
                    self.capa2ind.removeItem(indice)

#Excepcion si el usuario selecciona dos capas iguales
#consulta espacial
class ErrorEqualLayers(Exception):
    def __init__(self, message="The main layer and the layer to be queried are the same"):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return self.message
    
