"""
metadata related file operation
"""
import os
import platform
import warnings
from shutil import copy2, copystat


def copy_status(src: str, dst: str):
    assert os.path.exists(src) and os.path.exists(dst)
    copystat(src, dst, follow_symlinks=False)


def copy_metadata(scr, dest):
    warnings.warn(
        "`copy_metadata` is deprecated, because I dont think we should mess up the create time",
        DeprecationWarning,
    )
    assert platform.system() == "Windows"
    from pywintypes import Time
    from win32file import (
        GENERIC_READ,
        GENERIC_WRITE,
        OPEN_EXISTING,
        CloseHandle,
        CreateFile,
        GetFileTime,
        SetFileTime,
    )

    # link images in scr and dest that have same name
    scr_files = [f for f in os.scandir(scr) if f.is_file()]
    scr_filenames = [f.name for f in scr_files]
    dest_files = [f for f in os.scandir(dest) if f.is_file()]
    scr_dest_pairs = []
    for f in dest_files:
        try:
            i = scr_filenames.index(f.name)
            scr_dest_pair = (scr_files[i], f)
            scr_dest_pairs.append(scr_dest_pair)
        except ValueError:
            print(f"{f.name} dont have a source file.")

    # copy time metadata
    for s, d in scr_dest_pairs:
        scr_fh = CreateFile(s.path, GENERIC_READ, 0, None, OPEN_EXISTING, 0, 0)
        dest_fh = CreateFile(d.path, GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
        createTimes, accessTimes, modifyTimes = GetFileTime(scr_fh)
        # 有时候复制文件等操作会刷新创建时间，这里修改一下，让创建时间是最早的
        if createTimes > modifyTimes:
            createTimes = modifyTimes
        SetFileTime(dest_fh, createTimes, accessTimes, modifyTimes)
        CloseHandle(scr_fh)
        CloseHandle(dest_fh)
