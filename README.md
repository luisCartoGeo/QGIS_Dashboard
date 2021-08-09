# QGIS_Dashboard

<table align="center">
    <p align = "center">
      <a href="https://www.linkedin.com/in/luisedpg/"><img alt="LuisGeo" src="https://img.shields.io/badge/AUTOR-Luis%20Eduardo%20Perez%20Graterol-brightgreen"></a>
      <a href="https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2FluisCartoGeo%2FQGIS_Dashboard%2F"><img alt="Twitter" src="https://img.shields.io/twitter/url?label=TWITTER&style=social&url=https%3A%2F%2Ftwitter.com%2FLuiseperezg"></a>
      </P>
</table>
<h2><b>Repository of the plugin for building Dashboards in QGIS</b></h2><br>.
The purpose of the <strong>QGIS Dashboard</strong> plugin is to allow the creation of dashboards on the QGIS screen.<br><br>
<hr></hr>
<h2>THIS PLUGIN IS IN DEVELOPMENT (PRODUCTION)</h2>.
<center><img style="text-align:center" src="https://github.com/luisCartoGeo/QGIS_Dashboard/blob/main/trabajando.gif" style="max-width:80%;"></center>
<hr></hr>

## Table of Contents

- [Introduction](https://www.linkedin.com/pulse/overview-installation-qgis-dashboard-plugin-perez-graterol)
- [Why does QGIS need a Dashboard](https://www.linkedin.com/pulse/overview-installation-qgis-dashboard-plugin-perez-graterol)
- [Installation of the QGIS Dashboard plugin](https://www.linkedin.com/pulse/overview-installation-qgis-dashboard-plugin-perez-graterol)
    - [Procedure for downloading the plugin](https://www.linkedin.com/pulse/overview-installation-qgis-dashboard-plugin-perez-graterol)
    - [Procedure for the installation](https://www.linkedin.com/pulse/overview-installation-qgis-dashboard-plugin-perez-graterol)
 - [QGIS Dashboard Plugin features](#QGIS-Dashboard-Plugin-features)
 - [<b>Fast tutorial</b>](#Fast-tutorial)
 - [Tutorial](#tutorial)
    - [General functioning of the plugin](#general-functioning-of-plugin)
    - [Charts and indicators available](#charts-and-indicators-available)
    - [Wizard for creating panels](#wizard-for-creating-panels)
        - [Initial configuration](#initial-configuration)
            - [Number of panels to build](#Number-of-panels-to-build)
            - [Initial size and position](#Initial-size-and-position)
            - [Additional options](#Additional-options)
        - [Design of charts and indicators](#Design-of-charts-and-indicators)
            - [Text panel](#Text-panel)
                - [Assigning a style](#Assigning-a-style)
                - [Setting colors](#Setting-color-colors)
                - [Integrating and configuring an icon](#Integrating-and-configuring-an-icon)
                - [Data queries](#Data-queries)
                    - [Totalize an attribute](#Totalize-an-attribute)
                    - [Percentage. Proportion](#Percentage.-Proportion)
                    - [Statistics of an attribute](#Statistics-of-an-attribute)
                - [Spatial queries](#Spatial-queries)
                    - [Contained entities. Polygons](#Contained-entities.-Polygons)
                    - [Entities at a distance. Lines-points](#Entities-at-a-distance.-Lines-points)
                    - [Contained entities matching with](#Contained-entities-matching-with)
                    - [Entities at a distance containing with](#Entities-at-a-distance-containing-with)
            - [Indicator Graph](#Indicator-Plot)
            - [Bar Chart](#Bar-Chart)
            - [Line chart - Series](#Line-charts.-Series)
    - [Move, resize and delete panels](#Move-and-resize-panels)
    - [Make panels transparent](#Transparent-panels)
    - [Save a dashboard](#Save-a-board)
    - [Open a board from file](#Open-a-board-from-file)

## Tutorial

### General functioning of the plugin
The <strong>Dashboards</strong> are built by creating panels which will contain indicators or graphs, the panels are customizable, the user can move, delete, resize using the QGIS annotation tools.
This plugin takes advantage and extends through Python the <strong>Html Annotations</strong> of QGIS to give them more functionality, display graphs, respond to events.

### Charts and indicators available

So far the plugin has four types of panels:
<ul><li><b>Text panels:</b> they display a value or indicator of a dataset or spatial query. This panel although simple, presents the widest variety of styles and configurations. The value displayed can come from a statistical summary of a dataset or a spatial query. The spatial query options will vary depending on the geometry of the layer being queried. If it is a <strong>polygon</strong> layer you can query the contained entities belonging to another layer, you can also query the entities contained at a specified distance from the selected entities of the polygon layer (buffer). If it is <strong>line</strong> or <strong>point</strong> you can only query the contained entities of another layer at a specified distance from the selected entities.
  <li><b>Bullet chart</b> also called 'bullet' or 'speedometer' chart, similarly to the text panel it displays a value or indicator, but in a context that facilitates its interpretation, the user must specify a range within which the value is expected to oscillate, plus a threshold value, after which the condition is considered unfavorable or favorable.
<li><b>Bar Chart</b> can display a bar chart of a numeric field given the categories of a text field in the attribute table. You can also generate the chart from a set of numeric fields present in the attribute table. As for the style you can configure colors and text sizes, you can also assign a color to the bars or use one of the available color palettes.</li>.
  <li><b>Line chart</b> by means of this chart you can represent a set of data presenting a chronological sequence. It presents similar style configuration options to the bar chart. You can plot only points if you set a line thickness equal to 0, lines of the specified thickness or filled areas.</li><li>
  </ul>
<img width="80%" src="https://github.com/luisCartoGeo/QGIS_Dashboard/blob/main/DASHBOARDS.jpg" style="max-width:100%;">
