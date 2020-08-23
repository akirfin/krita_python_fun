"""

Sharing readme.md with Krita in plugin documentations.

Write readme.md document and use html and relative image paths, then run this script for document.
adds embeded images to doument ie:
    <img src="./relative_path/to_image.jpg" source="base64 embeded image..."/>

Why so complicated...
- filename must be "readme.md"
- Krita QTextBrowser and GitHub both accept HTML.
- QTextBrowser can't handle relative image paths (QTextBrowser local path not set)
- QTextBrowser absolute path of installed document is unknown
- GitHub works best if relative path is used
- QTextBrowser can use special "source" attribute vs. HTML "src" attribute
- QTextBrowser accepts base64 embeded images
- GitHub can't use base64 embeded images
- bonus: for both "nice" image resolution is different.

"""
import sys
import os

from Qt.QtCore import Qt, QIODevice, QByteArray, QBuffer
from Qt.QtGui import QImage, QTextDocument
from Qt.QtWidgets import QApplication, QWidget, QTextEdit
from Qt.QtXml import QDomDocument


# _img_template = '<img src="{relative_path}" source="data:image/png;base64,{base64_data}" alt="title_image" title="Title"/>'

def embeded_image_scale_to_width(src_path, width_scalar):
    qimage = QImage(src_path)
    new_width = width_scalar * qimage.width()
    qimage.scaledToWidth(new_width, Qt.SmoothTransformation)
    data = QByteArray()
    buffer = QBuffer(data)
    buffer.open(QIODevice.WriteOnly)
    qimage.save(buffer, "JPG")
    base64_data = data.toBase64().data().decode('ascii')
    return "data:image/jpeg;base64,{base64_data}".format(base64_data=base64_data)


def iter_elements(node_list):
    for index in range(node_list.count()):
        yield node_list.at(index).toElement()


def calculate_width_scalar(img_nodes, target_width):
    max_image_width = -1
    for element in iter_elements(img_nodes):
        src_attr = element.attribute("src")
        max_image_width = max(QImage(src_attr).width(), max_image_width)
    if max_image_width > 0:
        return float(target_width) / max_image_width
    else:
        return 1.0


def embed_readme_images(readme_path):
    """
    QTextEdit used to auto detect raw / html / markdown,
    and do the conversion to html.
    """
    readme_dir = os.path.dirname(readme_path)

    editor = QTextEdit()
    with open(readme_path) as f:
        editor.setText(f.read())
    editor.document().setMetaInformation(QTextDocument.DocumentUrl, readme_dir)

    dom_doc = QDomDocument()
    dom_doc.setContent(editor.toHtml())
    img_nodes = dom_doc.elementsByTagName("img")

    width_scalar = calculate_width_scalar(img_nodes, 577.0)

    for element in iter_elements(img_nodes):
        rel_src_path = element.attribute("src")
        if rel_src_path:
            src_path = os.path.abspath(os.path.join(readme_dir, rel_src_path))
            if not os.path.isfile(src_path):
                print("image file missing! (readme_dir={readme_dir!r}, src_path={src_path!r})".format(**locals()))
            else:
                rel_src_path = os.path.relpath(src_path, readme_dir)
                rel_src_path = "./" + rel_src_path.replace("\\", "/")
                element.setAttribute("src", rel_src_path)
                element.setAttribute("source", embeded_image_scale_to_width(src_path, width_scalar=width_scalar))

    html = dom_doc.toString()
    with open(readme_path + "_ng", "w") as f:
        f.write(html)


def walk_pykrita_dir():
    this_dir = os.path.dirname(sys.argv[0])
    pykrita_dir = os.path.join(this_dir, "..", "pykrita")
    for parent, folders, files in os.walk(pykrita_dir):
        for file in files:
            if file.lower() == "readme.md":
                readme_path = os.path.join(parent, file)
                embed_readme_images(readme_path)


if __name__ == '__main__':
    """
    ToDo:
    Change so that path to readme.md is given, then this adds source="..." entry.
    - remove_use_width == remove width="" and use it as scaling for empadded image.
    """
    app = QApplication(sys.argv)

    win = QWidget()
    win.show()

    walk_pykrita_dir()

    sys.exit(app.exec_())

    #img_tag = embeded_image_scale_to_width(
    #    r"D:\projects\krita_python_fun\pykrita\arc_welding_tool\resources\title_image.jpg",
    #    "./resources/title_image.jpg",
    #    577)
    # print(img_tag)

    #img_tag = embeded_image_scale_to_width(
    #    r"D:\projects\krita_python_fun\pykrita\camera_layer\resources\title_image.jpg",
    #    "./resources/title_image.jpg",
    #    577)
    # print(img_tag)

    #img_tag = embeded_image_scale_to_width(
    #    r"D:\projects\krita_python_fun\pykrita\fetch_gallery\resources\title_image.jpg",
    #    "./resources/title_image.jpg",
    #    577)
    # print(img_tag)

    #img_tag = embeded_image_scale_to_width(
    #    r"D:\projects\krita_python_fun\pykrita\layer_meta_data\resources\title_image.jpg",
    #    "./resources/title_image.jpg",
    #    577)
    #print(img_tag)
