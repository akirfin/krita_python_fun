"""

bump __version__ = in (".py", ".md") files
and clean line endings.

"""
import re

if __name__ == "__main__":
    this_dir = os.path.dirname(sys.argv[0])
    project_dir = os.path.abspath(os.path.join(this_dir, ".."))
    version_re = re.compile(r"__version__\s*=\s*[\"']?(\d+\.\d+\.\d+)[\"']?")

    for parent, folders, files in os.walk(project_dir):
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
                        version_str = found.group(1)
                        major, minor, batch = (int(t) for t in version_str.split("."))
                        next_major, next_minor, next_batch = major, minor, batch

                        print('{python_file_path} [line: {line_number}] __version__ = "{major}.{minor}.{batch}"'.format(**locals()))
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
                        new_line = version_re.sub(line, "{next_major}.{next_minor}.{next_batch}")
                        new_content.append(new_line)
                    else:
                        new_content.append(line)

                new_file_path = file_path +"_new"
                with open_new(new_file_path, "w") as f:
                    f.write(new_content.join("\n"))

                # remove old file
                # os.remove(file_path)

                # rename new file
                # os.rename(new_file_path, file_path)
