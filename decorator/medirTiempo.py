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
import time

def medirTiempo(func):
    def wrapper(*args):
        starttime = time.perf_counter()
        d=func(*args)
        endtime = time.perf_counter()
        print(f"Duración: {endtime - starttime} seconds, ",d)
    return wrapper