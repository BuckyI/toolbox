import os
from pathlib import Path
import imghdr
import logging
import time
import re
import uuid


class Image():
    def __init__(self, file: os.DirEntry):
        self.file = file
        self.path = Path(file.path)
        self.tags = []
        self.get_timestr()
        self.analyze_filename()

    def get_timestr(self):
        "获得文件最早创建时间 timestr 作为文件名的一部分"
        mtime = self.file.stat().st_mtime
        ctime = self.file.stat().st_ctime
        self.time = ctime if mtime > ctime else mtime
        self.timestr = time.strftime('%Y%m%d', time.localtime(self.time))
        return self.timestr

    def analyze_filename(self):
        "从文件名中提取信息"
        tags = self.path.stem.split()
        # 以 20 开头的 8 位数字，认为是该文件已经标注好的日期信息
        if m := re.match(r"20\d{6}", tags[0]):
            # 已标注的优先级较高，作为文件日期
            self.timestr = m.group()
            self.tags.extend(tags[1:])
        else:
            self.tags.extend(tags)
        # 最后一个标签是数字时（一般是为避免重名标的序号或无意义）可舍弃
        if len(self.tags) > 0 and self.tags[-1].isdigit():
            self.tags.pop()
        # 标签可能以 `#`开头，去掉这个不必要的标识
        self.tags = [re.match(r"#?(.*)", s).group(1) for s in self.tags]
        logging.debug("from filename get tags: %s", self.tags)

    @property
    def ideal_name(self):
        "图片名：时间信息 + 标签 + 必要的序号"
        return self.timestr + " " + " ".join(self.tags)

    def set_tags(self, tags: list, *, reset=False):
        if reset:
            self.tags = tags
        else:
            self.tags.extend(tags)


def scan(path: str, recursive=False):
    """scan all image files in path (recursicely)"""
    for f in os.scandir(path):
        if f.is_file() and imghdr.what(f.path):
            yield Image(f)
        elif recursive and f.is_dir():
            yield from scan(f.path, recursive)
    return "scan complete"


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s: %(message)s')
    handler = logging.FileHandler("images_change.log")
    handler.setLevel(logging.INFO)
    handler.addFilter(lambda s: "[RENAME]" in s.msg)  # msg 含 RENAME 时，保存到文件
    handler.setFormatter(logging.Formatter('%(asctime)s : %(message)s'))
    rootLogger = logging.getLogger()
    rootLogger.addHandler(handler)  # add handler to root logger

    source = r"image file/test/"
    # 转换成绝对路径，避免混淆（？）后续 f.path 也会变成绝对路径
    source = os.path.realpath(source)

    # find image files at source folder
    images = (Image(f) for f in os.scandir(source)
              if f.is_file() and imghdr.what(f.path))

    for img in images:
        # tags = input(f"input tags of {img.file.name}: ")
        img.set_tags("tag1 tag2".split(), reset=True)
        # rename
        scr = img.path
        dst = scr.with_stem(img.ideal_name)
        if scr == dst:
            logging.info(f"[RENAME] \"{scr.name}\" unchanged")
        else:
            if dst.exists():
                dst = scr.with_stem(f"{img.ideal_name} {uuid.uuid4()}")
                logging.warning(
                    f"\"{dst.name}\" has alreadly existed! try uuid")
            scr.rename(dst)
            logging.info(f"[RENAME] from \"{scr.name}\" to \"{dst.name}\"")
