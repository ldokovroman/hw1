import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:

    if "GIT_DIR" not in os.environ:
        git_dir = pathlib.Path(".git")
    else:
        git_dir = os.environ.get("GIT_DIR", default=".git")
    while os.path.isdir(workdir):
        if os.path.isdir(workdir / pathlib.Path(git_dir)):
            return pathlib.Path(workdir) / git_dir
        if workdir == ".":
            break
        workdir = pathlib.Path(os.path.dirname(workdir))
    raise Exception("Not a git repository")



    

def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:

    if os.path.isfile(workdir):
        raise Exception(f"{workdir} is not a directory")
    if "GIT_DIR" not in os.environ:
        git_dir = workdir / pathlib.Path(".git")
    else:
        git_dir = workdir / pathlib.Path(os.environ["GIT_DIR"])
    os.mkdir(git_dir)
    os.makedirs(git_dir / "refs" / "heads")
    os.mkdir(git_dir / "refs" / "tags")
    os.mkdir(git_dir / "objects")
    with (git_dir / "HEAD").open("w") as f:
        f.write("ref: refs/heads/master\n")
    with (git_dir / "config").open("w") as f:
        f.write(
            "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n"
        )
    with (git_dir / "description").open("w") as f:
        f.write("Unnamed pyvcs repository.\n")
    return git_dir
    
