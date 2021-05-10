import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str


    def pack(self) -> bytes:

        string = str.encode(self.name, "utf-8")
        return struct.pack(
            f">10i20sh{len(string) + 3}s",
            self.ctime_s,
            self.ctime_n,
            self.mtime_s,
            self.mtime_n,
            self.dev,
            self.ino & 0xFFFFFFFF,
            self.mode,
            self.uid,
            self.gid,
            self.size,
            self.sha1,
            self.flags,
            string,
        )


    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        
        content = struct.unpack(">10i20sh", data[0:62])
        data = data[62:]
        last_byte = data.find(b"\x00\x00\x00")
        return GitIndexEntry(
            content[0],
            content[1],
            content[2],
            content[3],
            content[4],
            content[5],
            content[6],
            content[7],
            content[8],
            content[9],
            content[10],
            content[11],
            data[0:last_byte].decode(),
        )
    

def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:

    index = pathlib.Path(gitdir / "index")
    res: tp.List[GitIndexEntry] = []
    if not index.exists():
        return res
    with index.open("rb") as f:
        data = f.read()
    dir, version, cnt = struct.unpack(">4s2i", data[0:12])
    data = data[12:]
    for i in range(cnt):
        res.append(GitIndexEntry.unpack(data))
        data = data[62:]
        next_byte = data.find(b"\x00\x00\x00")
        data = data[next_byte + 3:]
    f.close()
    return res
    


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    
    res = []
    res.append(b"DIRC")
    res.append(struct.pack(">2i", 2, len(entries)))
    for i in entries:
        res.append(i.pack())
    index = gitdir / "index"
    data = b"".join(res)
    res.append(struct.pack(">20s", hashlib.sha1(data).digest()))
    pathlib.Path(index).touch()
    with index.open("wb") as f:
        f.write(b"".join(res))
        f.close()


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:

    for i in read_index(gitdir):
        if details:
            print(f"{i.mode:o} {i.sha1.hex()} 0\t{i.name}")
        else:
            print(i.name)


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:

    index= gitdir / "index"
    res = []
    if os.path.isfile(index):
        res = read_index(gitdir)
    else:
        pathlib.Path(index).touch()
    for i in paths:
        info = os.stat(i)
        with i.open("r") as f:
            data = f.read()
            f.close()
        sha = hashlib.sha1((f"blob {len(data)}\0" + data).encode())
        entry = GitIndexEntry(
            int(info.st_ctime),
            0,
            int(info.st_mtime),
            0,
            info.st_dev,
            info.st_ino,
            info.st_mode,
            info.st_uid,
            info.st_gid,
            info.st_size,
            sha.digest(),
            0,
            str(i.as_posix()),
        )
        if entry in res:
            continue
        hash_object(data.encode(), "blob", True)
        k = 0
        while k < len(res):
            if res[k].name == entry.name:
                res[k] = entry
                break
            k += 1
        if k == len(res):
            res.append(entry)
    res.sort(key=lambda x: x.name)
    write_index(gitdir, res)
    
