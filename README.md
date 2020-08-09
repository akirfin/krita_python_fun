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

or

change line in ./bin/install_plugins_and_start_krita.py
```python
# Change this to something that starts up Krita
krita_app_path = r"D:\Program Files\Krita (x64)\bin\krita.exe"
```
then run install_plugins_and_start_krita.py using python. (works nice when editing code
& testing in Krita (my dev folder is elsewhere...))

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
and then push Qimage to layer node.
