<h2><b>Repository of the plugin code for building Dashboards in QGIS</b></h2><br>.
The purpose of the <strong>QGIS Dashboard</strong> plugin is to allow the creation of dashboards on the QGIS screen.<br><br>
<hr></hr>
<h2>THIS PLUGIN IS IN DEVELOPMENT (PRODUCTION)</H2>.
<img width="80%" src="https://github.com/luisCartoGeo/QGIS_Dashboard/blob/main/trabajando.gif" style="max-width:80%;">
<hr></hr>
The <strong>Dashboards</strong> are built by creating panels which will contain indicators or graphs, the panels are customizable, the user can move, delete, resize using the QGIS annotation tools.<br><br>
This plugin leverages and extends through Python the <strong>Html Annotations</strong> of QGIS to give them more functionality, display graphs, respond to events.

<h2><strong>Installation and requirements</strong></h2>.
This plugin has <B>NO</B> special requirements, simply install on a QGIS3.10 version or higher.

<h1><b>User interface</b></h1>.
<img width="100%" src="https://user-images.githubusercontent.com/79421833/122484184-1c37c280-cfa2-11eb-9545-56e7be7a38ee.jpg" style="max-width:100%;">

<h1><b>Graphs and indicators</h1></b>.
So far the plugin has four types of dashboards:
<ul><li><b>Text panels:</b> they display a value or indicator of a dataset or spatial query. This panel although simple, presents the widest variety of styles and configurations. The value displayed can come from a statistical summary of a dataset or a spatial query. The spatial query options will vary depending on the geometry of the layer being queried. If it is a <strong>polygon</strong> layer you can query the contained entities belonging to another layer, you can also query the entities contained at a specified distance from the selected entities of the polygon layer (buffer). If it is <strong>line</strong> or <strong>point</strong> you can only query the contained entities of another layer at a specified distance from the selected entities.
  <li><b>Bullet chart</b> also called 'bullet' or 'speedometer' chart, similarly to the text panel it displays a value or indicator, but in a context that facilitates its interpretation, the user must specify a range within which the value is expected to oscillate, plus a threshold value, after which the condition is considered unfavorable or favorable.
  This panel will allow similar query options as the text panel.</li>.
  <li><b>Bar Chart</b> can display a bar chart of a numeric field given the categories of a text field of the attribute table. You can also generate the chart from a set of numeric fields present in the attribute table. As for the style you can configure colors and text sizes, you can also assign a color to the bars or use one of the available color palettes.</li>.
  <li><b>Line chart</b> by means of this chart you can represent a set of data presenting a chronological sequence. It presents similar style configuration options to the bar chart. You can plot only points if you set a line thickness equal to 0, lines of the specified thickness or filled areas.</li><li>
  </ul>
<img width="100%" src="https://github.com/luisCartoGeo/QGIS_Dashboard/blob/main/DASHBOARDS.jpg" style="max-width:100%;">
