"""

Install plugins to Krita and run Krita with console.

"""

import sys
import os
from shutil import copy2, copytree, rmtree
from subprocess import Popen, PIPE


# Change this to something that starts up Krita
krita_app_path = r"D:\Program Files\Krita (x64)\bin\krita.exe"


def get_krita_resource_dir():
    platform_dirs = [
            ('linux',  "~/.local/share/krita/pykrita"),
            ('darwin', "~/.local/share/krita/pykrita"),
            ('win32',  "~\AppData\Roaming\krita\pykrita")]
    for prefix, dir in platform_dirs:
        if sys.platform.startswith(prefix):
            return os.path.expanduser(dir)
    raise RuntimeError('Not supported platform, Krita resource dir can NOT be solved. (platform: {sys.platform!r})'.format(**locals()))


def run_krita():
    """
    Pipe left for future redirecting...
    """
    process = Popen(krita_app_path, stdout=PIPE)
    while process.poll() is None:
        data = process.stdout.readline()
        sys.stdout.write(data.decode('utf-8'))
        sys.stdout.flush()
    # read lingering data
    data = process.stdout.read()
    sys.stdout.write(data.decode('utf-8'))
    sys.stdout.flush()


if __name__ == '__main__':
    this_dir = os.path.dirname(sys.argv[0])

    pykrita_dir = os.path.join(this_dir, "..", "pykrita")
    krita_resource_dir = get_krita_resource_dir()
    parent, folders, files = next(os.walk(pykrita_dir))

    for folder in folders:
        src = os.path.abspath(os.path.join(parent, folder))
        trg = os.path.join(krita_resource_dir, folder)
        if os.path.isdir(trg):
            # rmtree(trg)
        copytree(src, trg)
    for file in files:
        src = os.path.abspath(os.path.join(parent, file))
        copy2(src, krita_resource_dir)

    run_krita()
