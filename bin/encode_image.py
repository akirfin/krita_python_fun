import base64


_img_template = '<img src="data:image/png;base64,{base64_data}" alt="title_image" width="512" height="109" title="Title"/>'

def img_embad(img_path):
    base64_data = ""
    with open(img_path, "rb") as f:
        base64_data = base64.b64encode(f.read()).decode('ascii')
    img_tag = _img_template.format(**locals())
    print(img_tag)


if __name__ == "__main__":
    img_embad(r"D:\projects\krita_python_fun\pykrita\arc_welding_tool\resources\title_image.jpg")
