import os
import imghdr
import logging
import time


class Image():
    def __init__(self, file: os.DirEntry):
        self.file = file


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    source = r"image file/test/"
    # 转换成绝对路径，避免混淆（？）后续 f.path 也会变成绝对路径
    source = os.path.realpath(source)

    # find image files at source folder
    images = (Image(f) for f in os.scandir(source)
              if f.is_file() and imghdr.what(f.path))

    for img in images:
        print(img.name)
