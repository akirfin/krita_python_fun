# krita_python_fun
Fun with python in krita

--- Under construction ---

Contains experimental example python plugins for Krita.
May give some ideas how to do things.

## How to install
```
copy files and folders from ./pykrita to
  linux/mac:  ${HOME}/.local/share/krita/pykrita
  win:        ${HOME}\AppData\Roaming\krita\pykrita
```

(Krita really should have some enviroment variable for plugin folders like
`KRITA_PLUGINS_PATH="/path/myplugins:/more/plugins:~/dev/krita_python_fun"`,
pleeease!, cherry on top!)


## arc_welding_tool
How to add new tool to Krita.
Add button to toolbar
Show tool context gizmo in viewport.

## camera_layer
Custom layer node that pulls pixels from camera.

## fetch_gallery
Fetch image data from url to QImage,
and then push QImage to layer node.

## layer_meta_data
show extra secton in layer properties.
JSON tree of user defined settings.
(currntly JSON is stored in DublinCore.publisher field.)
(note: Krita bug in DublinCore.description, it is NOT saved!)

## future ideas
OpenStreetMap for krita
glTF layer ??? (show glTF in layer or use layers as textures?)
PixFika for Krita: (Shadertoy + glsl sandbox + PixFika)
Tutor: interactive drawing tutor
Multi user Krita: One document multiple interactive users. (sync layers + show fake cursors)
