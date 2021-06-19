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
import os
import os.path

class logControl:
    def __init__(self):
        self.dir = os.path.dirname(__file__)
        self.path=os.path.join(self.dir,'log.txt')
        
    def canWriteLog(self):
        firtsIntent=False
        if os.path.exists(self.dir):
            if os.access(self.dir,os.W_OK):
                firtsIntent=True
            else:
                return False
        else:
            return False
        test=os.path.join(self.dir,'test.txt')
        if firtsIntent==True:
            try:
                f=open(test,'w+t')
                f.write('prueba escritura')
                f.close()
                os.remove(test)
                return True
            except IOError:
                return False
    
    def writeLog(self,text):
        if os.path.isfile(self.path):
            with open(self.path,'at') as file:
                file.write("\n"+text)
        else:
            with open(self.path,'wt') as file:
                file.write("\n"+'text')
                
            
