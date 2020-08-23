"""
Sharing readme.md with Krita in plugin documentations.

Write readme.md document and use html and relative image paths, then run this script for document.
adds embeded images to doument ie:
    <img src="./relative_path/to_image.jpg" source="base64 embeded image..."/>

Why so complicated...
- filename must be "readme.md"
- Krita QTextBrowser and GitHub both accept HTML.
- QTextBrowser can't handle relative image paths (QTextBrowser.document() QTextDocument.DocumentUrl not set)
- QTextBrowser absolute path of installed document is unknown
- GitHub works best if relative path is used
- QTextBrowser can use special "source" attribute vs. HTML "src" attribute
- QTextBrowser uses last attribute if both src & source are used.
- QTextBrowser accepts base64 embeded images
- GitHub can't use base64 embeded images
- bonus: for both "nice" image resolution is different.
- bonus+: path separator \o/
- bonus++: xml attribute order sucks!
"""

import sys
import os
import re
from xml.etree import ElementTree

from Qt.QtCore import Qt, QIODevice, QByteArray, QBuffer, QTimer
from Qt.QtGui import QImage, QTextDocument
from Qt.QtWidgets import QApplication, QTextEdit


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


def calculate_width_scalar(readme_dir, img_nodes, target_width):
    max_image_width = -1
    for img in img_nodes:
        src_attr = img.attrib.get("src", "")
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

    dada = None
    with open(readme_path) as f:
        dada = f.read()
    # strip old embeded dada
    dada = re.sub(r'source=\"data:image.*\"', "", dada)

    editor = QTextEdit()
    editor.setText(dada)
    editor.document().setMetaInformation(QTextDocument.DocumentUrl, readme_dir)
    html = editor.toHtml()

    image_elements = list()
    root = ElementTree.fromstring(html)
    for element in root.iter():
        for sub in element[:]:
            if sub.tag == "head":
                element.remove(sub)
        element.attrib.pop("style", None)
        if element.tag == "img":
            image_elements.append(element)

    width_scalar = calculate_width_scalar(readme_dir, image_elements, 577.0)

    for img in image_elements:
        rel_src_path = img.attrib.get("src", "")
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
                # ElementTree in python<3.8 uses sort(dict.items())
                # sooo... lets make sure that there is alphaphetical dummy prefix...
                new_attributes = [
                        ("001_DEL_XML_SUCKS_src", rel_src_path),
                        ("002_DEL_XML_SUCKS_source", embeded_image_scale_to_width(src_path, width_scalar=width_scalar))]
                new_attributes.extend((k, v) for k, v in sorted(img.attrib.items()) if k not in {"src", "source"})
                img.attrib.clear()
                img.attrib.update(new_attributes)

    html = ElementTree.tostring(root).decode()
    html = re.sub(r"\d{3}_DEL_XML_SUCKS_", "", html)
    with open(readme_path, "wb") as f:
        f.write(html.encode("utf-8"))


def walk_pykrita_dir():
    try:
        this_dir = os.path.dirname(sys.argv[0])
        pykrita_dir = os.path.join(this_dir, "..", "pykrita")
        for parent, folders, files in os.walk(pykrita_dir):
            for file in files:
                if file.lower() == "readme.md":
                    readme_path = os.path.join(parent, file)
                    embed_readme_images(readme_path)
        print("done!")
    finally:
        app = QApplication.instance()
        app.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    _ = QTimer.singleShot(0, walk_pykrita_dir)
    sys.exit(app.exec_())
