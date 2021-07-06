# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QGISDashboard
                                 A QGIS plugin
 This plugin allows the construction and management of Dashboards on screen.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-06-14
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Luis Eduardo Perez https://www.linkedin.com/in/luisedpg/
        email                : luis3176@yahoo.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QLabel,QDoubleSpinBox, QGraphicsItem,\
     QGraphicsOpacityEffect, QMessageBox 

from qgis.core import QgsAnnotation, QgsHtmlAnnotation, QgsProject, QgsMapLayer, QgsVectorLayer
from qgis.gui import QgsMapCanvas, QgsMapCanvasAnnotationItem
# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .QGISDashboardDialog import dashDialog
import os.path
from .panels.textPanel import textPanel
from .panels.indicadorPanel import indicadorPanel
from .panels.seriesPanel import seriesPanel
from .panels.barrasPanel import barrasPanel
from .panels.groupPanel6 import groupPanel
from .panels.adminPanel import adminPanel

class QGISDashboard:
    """QGISDashboard Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'QGISDashboard_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions= []
        self.menu= self.tr(u'&QGISDashboard')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('QGISDashboard', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """
        Create the menu entries and toolbar icons inside the QGIS GUI.
        Creates and adds widgets in the interface, button bar
        """
        self.dir=os.path.dirname(__file__)
        icon_path=self.dir+'//icon.png'
        #icon_path = ':/plugins/QGIS_Dashboard/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Dashboard Builder'),
            callback=self.run,
            whats_this=self.tr(u'Allows the construction and management of Dashboards'),
            parent=self.iface.mainWindow())
        self.ltrans=QLabel('Transparency')
        self.transparency=QDoubleSpinBox()
        self.transparency.setRange(0.000,1.000)
        self.transparency.setValue(1.00)
        self.transparency.setDecimals(2)
        self.transparency.setSingleStep(0.05)
        self.transparency.valueChanged.connect(self.changeTrans)
        self.transparency.setToolTip('Modify the transparency of the dashboards')
        self.labelT=self.iface.addToolBarWidget(self.ltrans)
        self.actionTransparency=self.iface.addToolBarWidget(self.transparency)
        self.actions.append(self.labelT)
        self.actions.append(self.actionTransparency)
        
        self.manager=adminPanel(self.iface.mapCanvas())
        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&QGISDashboard'),
                action)
            self.iface.removeToolBarIcon(action)
            

    def changeTrans(self):
        """
        Allows to modify the transparency of the panels
        """
        canvas=self.iface.mapCanvas()
        list_ai=canvas.annotationItems() 
        listPanels=[]
        for j,i in enumerate(list_ai):
            if type(i.annotation())==textPanel or type(i.annotation())==seriesPanel\
            or type(i.annotation())==indicadorPanel or type(i.annotation())==barrasPanel:
                if i.isVisible()==True:
                    if j==0:
                        if type(i.graphicsEffect())!=QGraphicsOpacityEffect:
                            i.setGraphicsEffect(QGraphicsOpacityEffect())
                        else:
                            i.graphicsEffect().setOpacity(round(self.transparency.value(),2))
                        listPanels.append(i.annotation())
                    else:
                        if i.annotation() in listPanels:
                            i.hide()
                        else:
                            if type(i.graphicsEffect())!=QGraphicsOpacityEffect:
                                i.setGraphicsEffect(QGraphicsOpacityEffect())
                            else:
                                i.graphicsEffect().setOpacity(round(self.transparency.value(),2))
                            listPanels.append(i.annotation())
                    
    def run(self):
        """Displays the wizard for the configuration and creation of panels."""
        pry=QgsProject.instance() 
        listacapas= pry.mapLayers().values()  
        listC=[] #Lista de capas vectoriales
        for i in listacapas:
            try:
                if  i.type()==QgsMapLayer.VectorLayer or isinstance(i,QgsVectorLayer):
                    if i.featureCount()>0:
                        listC.append(i)
            except Exception as e:
                if self.logAcces:
                    self.log.writeLog(e)
                QMessageBox.critical(None, 'ERROR', str(e))
        #Si no hay capas cerrar
        if len(listC)==0:
            QMessageBox.critical(None, 'ERROR NOT VECTOR LAYERS', 'There are no vector layers to be analyzed, preload one or more layers')
        else:
            # Create the dialog with elements (after translation) and keep reference
            # Only create GUI ONCE in callback, so that it will only load when the plugin is started
            if self.first_start == True:
                self.first_start = False
                self.dlg = dashDialog(self.iface,self.manager)
                # show the dialog
                self.dlg.show()
            elif  self.first_start == False:
                self.dlg = dashDialog(self.iface,self.manager)
                # show the dialog
                self.dlg.show()
#                self.dlg.paginador.setCurrentIndex(0)
#                self.dlg.procPanelT.setEnabled(True)
#                self.dlg.procIndicador.setEnabled(True)
#                self.dlg.procBarras.setEnabled(True)
#                self.dlg.procSeries.setEnabled(True)
#                self.dlg.show()

