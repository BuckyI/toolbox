import os
from pathlib import Path
import imghdr
import logging
import time
import re
import uuid
from win32_setctime import setctime
import enchant


class Image():
    def __init__(self, path: str):
        self.path = Path(path)
        self.tags = []
        self.extracted_timestr = None
        self.analyze_filename()
        self.set_time_status(self.extracted_timestr)  # 修正图片创建时间
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
        nc = NameChecker(self.path.stem)
        self.tags = nc.get_tags()
        self.extracted_timestr = nc.date
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

    def set_time_status(self, set_time: str = None, format="%Y%m%d"):
        """change file time status, it compares folowing three times
        set the create time with the earlist proper one
        - input set_time
        - os.stat mtime
        - os.stat ctime
        # TODO: format 添加 时分秒
        """
        def str_time(t):
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))

        # 候选人
        times = [self.path.stat().st_ctime, self.path.stat().st_mtime]
        if set_time:
            try:
                st_stime = time.strptime(set_time, format)
                stime = time.mktime(st_stime)
                # 由于输入字符串只有年月日，默认的时分秒为0，要避免因此而误调整
                st_times = [time.localtime(t)[0:3] for t in times]
                st_stime = st_stime[0:3]
                if st_times[0] != st_stime and st_times[1] != st_stime:
                    times.append(stime)
            except OverflowError:
                logging.error("输入的时间错误 %s", set_time)
                return

        # 找到最远的时间
        i = times.index(min(times))
        if i != 0:
            setctime(self.path.absolute(), times[i])
            logging.info("[cTime change] file '%s' from %s to %s",
                         self.path.name, str_time(times[0]),
                         str_time(times[i]))


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


class NameChecker():
    "从名称中提取信息"
    special_word = ["jike"]

    def __init__(self, name):
        self.name = name
        self.tags = name.split()
        self.date = None

    def contains_English(self, s):
        words = s.split()
        english_dict = enchant.Dict("en_US")
        # Check if any of the words are in the English dictionary
        return any(english_dict.check(word) for word in words)

    def contains_Chinese(self, s):
        return any(re.search(r'[\u4e00-\u9fff]', char) for char in s)

    def is_random(self, s):
        return re.match(r"\w{20,}", s)

    def is_uuid(self, s):
        return re.match(r"[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}", s)

    def is_digit(self, s):
        return s.isdigit()

    def _get_date(self, s):
        "deprecated"
        #  recognize a date string with YYYY-MM-DD HH:mm:ss
        pattern = r'(?P<year>20\d{2})(?P<month>\d{2})(?P<day>\d{2})(?P<detail>(?P<hour>\d{2})(?P<minute>\d{2})(?P<second>\d{2}))?'
        match = re.match(pattern, s)
        if match is None:
            return False  # not a date
        date_dict = match.groupdict()

        # Check if the date values are valid
        if not (1 <= int(date_dict['month']) <= 12
                and 1 <= int(date_dict['day']) <= 31):
            return False
        # Check if hour, minute, and second are valid
        if date_dict['detail'] and not (0 <= int(date_dict['hour']) <= 23 and
                                        0 <= int(date_dict['minute']) <= 59 and
                                        0 <= int(date_dict['second']) <= 59):
            return False
        self.date = match.group()
        return True

    def get_date(self, s):
        pattern = r'(20\d{6})(\d{6})?'
        match = re.match(pattern, s)
        if match is None:
            return False  # not a date
        format = "%Y%m%d%H%M%S" if match.group(2) else "%Y%m%d"
        try:
            st_time = time.strptime(s, format)
            self.date = time.strftime("%Y%m%d", st_time)
            return True
        except ValueError:
            return False

    def contains_special_word(self, s):
        "some name has special meanings, like 'jike' means an app"
        for i in self.special_word:
            if i in s:
                return True
        else:
            return False

    def name_sensible(self, s, tolerant=True):
        "contains either English word or Chinese character"
        if (self.contains_English(s) or self.contains_Chinese(s)
                or self.contains_special_word(s) or self.is_digit(s)):
            return True
        elif self.is_uuid(s) or self.is_random(s):
            return False
        else:  # not matched by any rules, return tolerant
            return tolerant

    def clean_prefix(self, s):
        return re.match(r"#?(.*)", s).group(1)

    def get_tags(self):
        result = []
        for tag in self.tags:
            if not self.date and self.get_date(tag):
                # if not have date, then get date, if success, continue
                continue
            if self.name_sensible(tag):
                tag = self.clean_prefix(tag)
                result.append(tag)
        else:
            # 最后一个标签是数字时（一般是为避免重名标的序号或无意义）可舍弃
            if len(result) > 0 and result[-1].isdigit():
                result.pop()
            return result


def add_handler():
    "部分图片处理 log 输出到本地文件"

    def match(s):
        msg = s.msg
        mode = ["[RENAME]", "[cTime change]"]
        for m in mode:
            if m in msg:
                return True
        else:
            return False

    name = "Image Info to File Log"
    if name in [h.name for h in logging.root.handlers]:
        return  # 已经存在了就不重复添加
    handler = logging.FileHandler("images_change.log")
    handler.set_name(name)
    handler.setLevel(logging.INFO)
    handler.addFilter(match)
    handler.setFormatter(logging.Formatter('%(asctime)s : %(message)s'))
    logging.root.addHandler(handler)  # add handler to root logger
    logging.debug("add log handler '%s' to '%s'", handler.name,
                  logging.root.name)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s: %(message)s')
    add_handler()
    source = r"imageKit/test/"
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
