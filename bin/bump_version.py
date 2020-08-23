"""

bump __version__ = in (".py", ".md") files
and clean line endings.

"""
import re
import os
import sys
from contextlib import contextmanager


@contextmanager
def open_new(file_path, exists_ok=True):
    try:
        fd = os.open(file_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
        f = os.fdopen(fd, "wb")
    except OSError as e:
        if not ((e.errno == errno.EEXIST) and exists_ok):
            raise  # skipped only if exits and exists_ok
    else:
        try:
            yield f
        finally:
            f.close()


if __name__ == "__main__":
    this_dir = os.path.dirname(sys.argv[0])
    project_dir = os.path.abspath(os.path.join(this_dir, ".."))
    version_re = re.compile(r"(?P<head>^.*__version__\s*=\s*[\"']?)(?P<version>\d+\.\d+\.\d+)(?P<tail>[\"']?.*$)")

    for parent, folders, files in os.walk(project_dir):
        # prune hidden
        folders[:] = (f for f in folders if not f.startswith("."))
        files[:] = (f for f in files if not f.startswith("."))
        for file_name in files:
            if file_name.endswith((".py", ".md")):
                file_path = os.path.join(parent, file_name)

                content = None
                with open(file_path, "r") as f:
                    content = f.read()

                new_content = []
                for line_number, line in enumerate(content.splitlines(), start=1):
                    found = version_re.search(line)
                    if found:
                        version_str = found.group("version")
                        major, minor, batch = (int(t) for t in version_str.split("."))
                        next_major, next_minor, next_batch = major, minor, batch

                        print('{file_path} [line: {line_number}] __version__ = "{major}.{minor}.{batch}"'.format(**locals()))
                        bump_version = input("do you wish to bump? (a=add to version) (y/n/a)").strip().lower()

                        if bump_version in {"y", "yes"}:
                            # yes
                            next_batch += 1
                        elif bump_version in {"a", "add"}:
                            # add to version
                            next_major += max(0, int(input("major +") or "0"))
                            next_minor += max(0, int(input("minor +") or "0"))
                            next_batch += max(0, int(input("batch +") or "0"))
                        else:
                            # default is no change
                            pass
                        new_line = version_re.sub(r"\g<head>{next_major}.{next_minor}.{next_batch}\g<tail>".format(**locals()), line)
                        print(new_line)
                        new_content.append(new_line)
                    else:
                        new_content.append(line)

                new_file_path = file_path +"_new"
                with open_new(new_file_path, exists_ok=False) as f:
                    for line in new_content:
                        f.write((line + "\n").encode("utf-8"))

                # remove old file
                os.remove(file_path)
                # os.rename(file_path, file_path + "_bu")

                # rename new file
                os.rename(new_file_path, file_path)
