import os
import imghdr
import logging
import time
import re


class Image():
    def __init__(self, file: os.DirEntry):
        self.file = file
        self.tags = []
        self.get_time()
        self.analyze_filename()

    def get_time(self):
        "获得文件最早创建时间 timestr 作为文件名的一部分"
        path = self.file.path
        modify_time = os.path.getmtime(path)
        create_time = os.path.getctime(path)
        self.time = create_time if modify_time > create_time else modify_time
        self.timestr = time.strftime('%Y%m%d', time.localtime(self.time))
        return self.timestr

    def analyze_filename(self):
        "从文件名中提取信息"
        name = os.path.splitext(self.file.name)[0]
        tags = name.split()
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
        logging.debug("analyze_filename: %s", self.tags)

    def generate_name(self):
        infos = [self.timestr]
        infos.extend(self.tags)

        infostr = " ".join(infos)
        ext = os.path.splitext(self.file.path)[1].lower()
        return infostr + ext


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    source = r"image file/test/"
    # 转换成绝对路径，避免混淆（？）后续 f.path 也会变成绝对路径
    source = os.path.realpath(source)

    # find image files at source folder
    images = (Image(f) for f in os.scandir(source)
              if f.is_file() and imghdr.what(f.path))

    for img in images:
        logging.info(img.generate_name())
