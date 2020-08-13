from Qt.QtCore import Qt, QIODevice, QByteArray, QBuffer
from Qt.QtGui import QImage


_img_template = '<img src="{relative_path}" source="data:image/png;base64,{base64_data}" alt="title_image" title="Title"/>'

def embeded_image_scale_to_width(img_path, relative_path, width):
    qimage = QImage(img_path).scaledToWidth(width, Qt.SmoothTransformation)
    data = QByteArray()
    buffer = QBuffer(data)
    buffer.open(QIODevice.WriteOnly)
    qimage.save(buffer, "JPG")
    base64_data = data.toBase64().data().decode('ascii')
    return _img_template.format(**locals())

def embed_images(filepath):
    xml = QDomDocument()
    for node in xml.findTags("img"):
        node.

if __name__ == '__main__':
    """
    ToDo:
    Change so that path to readme.md is given, then this adds source="..." entry.
    - remove_use_width == remove width="" and use it as scaling for empadded image.
    """
    img_tag = embeded_image_scale_to_width(
        r"D:\projects\krita_python_fun\pykrita\arc_welding_tool\resources\title_image.jpg",
        "./resources/title_image.jpg",
        577)
    # print(img_tag)

    img_tag = embeded_image_scale_to_width(
        r"D:\projects\krita_python_fun\pykrita\camera_layer\resources\title_image.jpg",
        "./resources/title_image.jpg",
        577)
    # print(img_tag)

    img_tag = embeded_image_scale_to_width(
        r"D:\projects\krita_python_fun\pykrita\fetch_gallery\resources\title_image.jpg",
        "./resources/title_image.jpg",
        577)
    # print(img_tag)
