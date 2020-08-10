"""

Translate readme.md -> readme.html

"""

import os
import sys
from markdown2 import markdown


def translate_readme(src_md, trg_html, resources_dir=None):
    """
    So much insanity!
    translate readme.md -> readme.html
    (I only write one documentation for each thingie!)
    """
    if resources_dir:
        resources_dir = resources_dir.replace("\\", "/").rstrip("/") +"/"
    with open(src_md, "r") as src, open(trg_html, "w") as trg:
        html = markdown(src.read())
        if resources_dir:
            html = html.replace('alt="title_image"', 'alt="title_image" width="512" height="109"')
            # html = html.replace("./resources/", resources_dir)
            """
            <html>
              <head>
                <title>Display Image</title>
              </head>
              <body>
                {put_translated_here}
                # embed all images!!!
                <img style='display:block; width:100px;height:100px;' id='base64image'                 
                   src='data:image/jpeg;base64, LzlqLzRBQ...<!-- base64 data -->' />

              </body>
            </html>
            """
        html = html.replace("?raw=true", "")
        trg.write(html)


if __name__ == '__main__':
    print("Fix me more!, absolute paths are also bad!")

    this_dir = os.path.dirname(sys.argv[0])

    pykrita_dir = os.path.join(this_dir, "..", "pykrita")
    parent, folders, files = next(os.walk(pykrita_dir))

    for folder in folders:
        dir = os.path.abspath(os.path.join(parent, folder))
        src_md = os.path.join(dir, "readme.md")
        trg_html = os.path.join(dir, "readme.html")
        resources_dir = os.path.join(dir, "resources")
        translate_readme(src_md, trg_html, resources_dir=resources_dir)
