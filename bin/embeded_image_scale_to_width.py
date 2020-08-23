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

from Qt.QtCore import Qt, QIODevice, QByteArray, QBuffer, QTimer
from Qt.QtGui import QImage, QTextDocument
from Qt.QtWidgets import QApplication, QWidget, QTextEdit
from Qt.QtXml import QDomDocument


# _img_template = '<img src="{relative_path}" source="data:image/png;base64,{base64_data}" alt="title_image" title="Title"/>'

def traverse_strip_style_xml_node_suck_sucks_suuuuck(node):
    cursor = node.firstChild()
    while not cursor.isNull():
        if cursor.isElement():
            element = cursor.toElement()
            if not element.isNull():
                if element.hasAttribute("style"):
                    element.removeAttribute("style")
        traverse_strip_style_xml_node_suck_sucks_suuuuck(cursor)
        cursor = cursor.nextSibling()


def embeded_image_scale_to_width(src_path, width_scalar):
    qimage = QImage(src_path)
    new_width = width_scalar * qimage.width()
    qimage = qimage.scaledToWidth(new_width, Qt.SmoothTransformation)
    data = QByteArray()
    buffer = QBuffer(data)
    buffer.open(QIODevice.WriteOnly)
    qimage.save(buffer, "JPG")
    base64_data = data.toBase64().data().decode('ascii')
    return "data:image/jpeg;base64,{base64_data}".format(base64_data=base64_data)


def iter_elements(node_list):
    for index in range(node_list.count()):
        yield node_list.at(index).toElement()


def calculate_width_scalar(readme_dir, img_nodes, target_width):
    max_image_width = -1
    for element in iter_elements(img_nodes):
        src_attr = element.attribute("src")
        if src_attr.startswith("data:image"):
            continue
        src_path = os.path.abspath(os.path.join(readme_dir, src_attr))
        max_image_width = max(QImage(src_path).width(), max_image_width)
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
        dada = f.read()
        editor.setText(dada)
        #print(readme_path)
        #print(dada)
    editor.document().setMetaInformation(QTextDocument.DocumentUrl, readme_dir)
    html = editor.toHtml()
    #print(html)

    dom_doc = QDomDocument()
    dom_doc.setContent(html)

    # remove <head> * </head>
    for element in iter_elements(dom_doc.elementsByTagName("html")):
        head = element.firstChildElement("head")
        if not head.isNull():
            element.removeChild(head)

    # remove style
    traverse_strip_style_xml_node_suck_sucks_suuuuck(dom_doc)

    img_nodes = dom_doc.elementsByTagName("img")
    width_scalar = calculate_width_scalar(readme_dir, img_nodes, 577.0)

    for element in iter_elements(img_nodes):
        rel_src_path = element.attribute("src")
        if rel_src_path.startswith("data:image"):
            print("Embeded src. skipping! (readme_path={readme_path!r})".format(**locals()))
            return
        if rel_src_path:
            src_path = os.path.abspath(os.path.join(readme_dir, rel_src_path))
            if not os.path.isfile(src_path):
                print("image file missing! (readme_dir={readme_dir!r}, src_path={src_path!r})".format(**locals()))
            else:
                rel_src_path = os.path.relpath(src_path, readme_dir)
                rel_src_path = "./" + rel_src_path.replace("\\", "/")
                # attribute order must be correct !!!
                element.removeAttribute("src")
                element.setAttribute("source", embeded_image_scale_to_width(src_path, width_scalar=width_scalar))
                element.setAttribute("src", rel_src_path)


    html = dom_doc.toString()
    with open(readme_path, "wb") as f:
        f.write(html.encode("utf-8"))


def walk_pykrita_dir():
    this_dir = os.path.dirname(sys.argv[0])
    pykrita_dir = os.path.join(this_dir, "..", "pykrita")
    for parent, folders, files in os.walk(pykrita_dir):
        for file in files:
            if file.lower() == "readme.md":
                readme_path = os.path.join(parent, file)
                embed_readme_images(readme_path)
    print("done!")


if __name__ == '__main__':
    """
    ToDo:
    Change so that path to readme.md is given, then this adds source="..." entry.
    - remove_use_width == remove width="" and use it as scaling for empadded image.
    """
    app = QApplication(sys.argv)

    win = QWidget()
    win.show()

    ti = QTimer.singleShot(1000, walk_pykrita_dir)

    sys.exit(app.exec_())
