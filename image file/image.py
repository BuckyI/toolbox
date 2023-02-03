import os
from pathlib import Path
import imghdr
import logging
import time
import re
import uuid


class Image():
    def __init__(self, path: str):
        self.path = Path(path)
        self.tags = []
        self.analyze_filename()
        self.index = 0  # 同系列图片的序号

    @property
    def time(self):
        "文件最早创建时间"
        mtime = self.path.stat().st_mtime
        ctime = self.path.stat().st_ctime
        return ctime if mtime > ctime else mtime

    @property
    def timestr(self):
        "字符化的文件最早创建时间"
        return time.strftime('%Y%m%d', time.localtime(self.time))

    def analyze_filename(self):
        "从文件名中提取信息"
        tags = self.path.stem.split()
        # filter unwanted tags
        clean_tags = []
        for tag in tags:
            if m := re.match(r"20\d{6}", tag):
                # 日期信息，已标注的优先级较高，可作为文件日期
                # TODO: 这里可以添加一个识别日期的 class，多添加需要的模式
                # TODO: 根据文件名识别日期，修改文件本身的日期
                pass
            elif re.match(r"[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}", tag):
                # uuid
                pass
            else:
                # 标签可能以 `#`开头，去掉这个不必要的标识
                tag = re.match(r"#?(.*)", tag).group(1)
                clean_tags.append(tag)
        # 最后一个标签是数字时（一般是为避免重名标的序号或无意义）可舍弃
        if len(clean_tags) > 0 and clean_tags[-1].isdigit():
            clean_tags.pop()
        self.tags = clean_tags
        logging.debug("from filename get tags: %s", self.tags)

    @property
    def ideal_name(self):
        "图片名：时间信息 + 标签 + 必要的序号"
        infos = []
        infos.append(self.timestr)
        infos.extend(self.tags)
        if self.index != 0:
            infos.append(str(self.index))
        return " ".join(infos)

    @property
    def ideal_path(self):
        return self.path.with_stem(self.ideal_name)

    def set_tags(self, tags: list, *, reset=False):
        if reset:
            self.tags = tags
        else:
            self.tags.extend(tags)

    def rename(self):
        scr = self.path
        dst = self.ideal_path
        if scr == dst:
            logging.info(f"[RENAME] \"{scr.name}\" unchanged")
        else:
            if dst.exists():
                dst = scr.with_stem(f"{self.ideal_name} {uuid.uuid4()}")
                logging.warning(
                    f"\"{dst.name}\" has alreadly existed! try uuid")
            self.path = scr.rename(dst)  # 进行重命名并对存储的路径进行跟踪
            logging.info(f"[RENAME] from \"{scr.name}\" to \"{dst.name}\"")


def scan(path: str, recursive=False):
    """scan all image files in path (recursicely)"""
    if os.path.isfile(path) and imghdr.what(path):
        yield Image(path)
    elif os.path.isdir(path):
        for f in os.scandir(path):
            if f.is_file() and imghdr.what(f.path):
                yield Image(f.path)
            elif recursive and f.is_dir():
                yield from scan(f.path, recursive)
    return "scan complete"


def add_handler():
    "部分图片处理 log 输出到本地文件"
    name = "Image Info to File Log"
    if name in [h.name for h in logging.root.handlers]:
        return  # 已经存在了就不重复添加
    handler = logging.FileHandler("images_change.log")
    handler.set_name(name)
    handler.setLevel(logging.INFO)
    handler.addFilter(lambda s: "[RENAME]" in s.msg)  # msg 含 RENAME 时，保存到文件
    handler.setFormatter(logging.Formatter('%(asctime)s : %(message)s'))
    logging.root.addHandler(handler)  # add handler to root logger
    logging.debug("add log handler '%s' to '%s'", handler.name,
                  logging.root.name)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s: %(message)s')
    add_handler()
    source = r"image file/test/"
    # 转换成绝对路径，避免混淆（？）后续 f.path 也会变成绝对路径
    source = os.path.realpath(source)

    # find image files at source folder
    images = (Image(f.path) for f in os.scandir(source)
              if f.is_file() and imghdr.what(f.path))

    for img in images:
        # tags = input(f"input tags of {img.file.name}: ")
        img.set_tags("tag1 tag2".split(), reset=True)
        # rename
        img.rename()
