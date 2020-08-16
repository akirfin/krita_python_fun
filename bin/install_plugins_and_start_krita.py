"""

Install plugins to Krita and run Krita with console.

"""

import sys
import os
from shutil import \
        copy2, copytree, rmtree
from subprocess import \
        Popen, PIPE


# Change this to something that starts up Krita
krita_app_path = r"D:\Program Files\Krita (x64)\bin\krita.exe"


def get_krita_resource_dir():
    platform_dirs = [
            ("linux",  r"~/.local/share/krita/pykrita"),
            ("darwin", r"~/.local/share/krita/pykrita"),
            ("win32",  r"~\AppData\Roaming\krita\pykrita")]
    for prefix, dir in platform_dirs:
        if sys.platform.startswith(prefix):
            return os.path.expanduser(dir)
    raise RuntimeError("Not supported platform, Krita resource dir can NOT be solved. (platform: {sys.platform!r})".format(**locals()))


def run_krita():
    """
    Pipe left for future redirecting...
    """
    process = Popen(krita_app_path, stdout=PIPE)
    while process.poll() is None:
        data = process.stdout.readline()
        sys.stdout.write(data.decode("utf-8"))
        sys.stdout.flush()
    # read lingering data
    data = process.stdout.read()
    sys.stdout.write(data.decode("utf-8"))
    sys.stdout.flush()


if __name__ == "__main__":
    this_dir = os.path.dirname(sys.argv[0])
    krita_resource_dir = get_krita_resource_dir()

    pykrita_src_dir = lambda entry: os.path.abspath(os.path.join(this_dir, "..", "pykrita", entry))
    pykrita_trg_dir = lambda entry: os.path.abspath(os.path.join(krita_resource_dir, entry))

    check_src_dir = pykrita_src_dir(".")
    check_trg_dir = pykrita_trg_dir(".")
    if check_src_dir == check_trg_dir:
        raise RuntimeError("Insanity check! source dir is destination dir? (Stopping, bad install!)")

    for entry in ("arc_welding_tool", "camera_layer", "fetch_gallery", "layer_meta_data"):
        src_dir = pykrita_src_dir(entry)
        trg_dir = pykrita_trg_dir(entry)
        if os.path.isdir(trg_dir):
            rmtree(trg_dir)
            print(f'remove old folder\nrmtree("{trg_dir}")')
        copytree(src_dir, trg_dir)
        print(f'copytree("{src_dir}",\n         "{trg_dir}")\n')

    for entry in ("arc_welding_tool.desktop", "camera_layer.desktop", "fetch_gallery.desktop", "layer_meta_data.desktop"):
        src_dsk = pykrita_src_dir(entry)
        copy2(src_dsk, krita_resource_dir)
        print(f'copy2("{src_dsk}",\n      "{krita_resource_dir}")\n')

    print("\nrun_krita()\n")
    run_krita()
