import base64



_img_template = '<img src="{relative_path}" source="data:image/png;base64,{base64_data}" alt="title_image" width="512" height="109" title="Title"/>'

def img_embad(img_path):
    base64_data = ""
    relative_path = "./resources/title_image.jpg"
    with open(img_path, "rb") as f:
        base64_data = base64.b64encode(f.read()).decode('ascii')
    img_tag = _img_template.format(**locals())
    print(img_tag)

if __name__ == '__main__':
    #img_embad(r"D:\projects\krita_python_fun\pykrita\arc_welding_tool\resources\title_image.jpg")
    #img_embad(r"D:\projects\krita_python_fun\pykrita\camera_layer\resources\title_image.jpg")
    #img_embad(r"D:\projects\krita_python_fun\pykrita\fetch_gallery\resources\title_image.jpg")
