<html>
<h2>Fun with python in krita</h2>
<p>--- Under construction ---</p>
__version__ = 0.0.0
<p>Contains experimental example python plugins for Krita.
May give some ideas how to do things.</p>

<h3>How to install</h3>
<hr size=1>
<pre>
```
copy files and folders from ./pykrita to
  linux/mac:  ${HOME}/.local/share/krita/pykrita
  win:        ${HOME}\AppData\Roaming\krita\pykrita
```
</pre>

<p>(Krita really should have some enviroment variable for plugin folders like
`KRITA_PLUGINS_PATH="/path/myplugins:/more/plugins:~/dev/krita_python_fun"`,
pleeease!, cherry on top!)</p>

<h3>arc_welding_tool</h3>
<hr size=1>
<p>How to add new tool to Krita.
Add button to toolbar
Show tool context gizmo in viewport.</p>

<h3>camera_layer</h3>
<hr size=1>
<p>Custom layer node that pulls pixels from camera.</p>

<h3>fetch_gallery</h3>
<hr size=1>
<p>Fetch image data from url to QImage,
and then push QImage to layer node.</p>

<h3>layer_meta_data</h3>
<hr size=1>
<p>show extra secton in layer properties.
JSON tree of user defined settings.
(currntly JSON is stored in DublinCore.publisher field.)
(note: Krita bug in DublinCore.description, it is NOT saved!)</p>

<h3>future ideas</h3>
<hr size=1>
<p>Krita Shelfs: place scripts, actions with settings, filepaths, then just click or drag & drop to target
OpenStreetMap layer: fetch any place on earth!
glTF layer: show glTF in layer or use layers as textures?
PixFika layer: Shadertoy + glsl sandbox + PixFika compatible layer
Tutor: interactive drawing tutor
Multi user Krita: One document multiple interactive users. (sync layers + show fake cursors)
PyKrita Unit test runner</p>

</html>
