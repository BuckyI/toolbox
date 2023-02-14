import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askokcancel, showinfo
import windnd
import uuid
import logging
from image import Image, scan, add_handler
from pathlib import Path
import enum


class TagMode(enum.Enum):
    "Combobox 选项"
    DefaultTags = "自动识别标签（程序默认）"
    NoTags = "无标签"
    CustomTags = "自定义标签"
    FileNameTags = "文件名作为标签"


class Window(object):
    def __init__(self):
        self.create_window()
        self.root.mainloop()

    def create_window(self):
        self.root = tk.Tk()
        self.root.title('图片归档')

        # 设定图片标签
        frm_tag = tk.LabelFrame(self.root, text="设定标签")
        frm_tag.pack()
        self.tagmode = tk.StringVar()  # 存储当前选项
        com = ttk.Combobox(
            master=frm_tag,  # 父容器
            state='readonly',  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
            textvariable=self.tagmode,
            values=[i.value for i in TagMode],  # 设置下拉框的选项
        )
        com.current(0)  # 默认无标签
        com.pack(side=tk.LEFT)

        self.tag = tk.Entry(frm_tag, show=None, font=('思源黑体', 15))
        self.tag.pack(side=tk.RIGHT)

        # 拖动文件触发重命名
        windnd.hook_dropfiles(self.root, func=self.rename_selected_images)

    def rename_selected_images(self, urls):
        paths = [Path(url.decode('gbk')) for url in urls]

        # load images
        images = []
        for p in paths:
            if not p.exists():  # 路径中存在特殊字符时会读取失败
                logging.error("load failed due to encoding error): %s", p)
                showinfo(message=f"load failed due to encoding error): {p}")
                continue
            images.extend(scan(p.absolute()))

        # load tags
        mode = TagMode(self.tagmode.get())
        if mode == TagMode.NoTags:
            tags = []
            for img in images:
                img.set_tags(tags, reset=True)
        elif mode == TagMode.CustomTags:
            tags = self.tag.get().split()
            for img in images:
                img.set_tags(tags, reset=True)
        elif mode == TagMode.FileNameTags:
            for img in images:
                tags = img.path.stem.split()
                img.set_tags(tags, reset=True)
        elif mode == TagMode.DefaultTags:
            # default behavior of Image
            pass

        # sort images to avoid name conflict
        sorted_images = {}
        for img in images:  # 根据期望路径为图片归类
            path = img.ideal_path
            img_ls = sorted_images.setdefault(path, [])
            img_ls.append(img)
        for path in sorted_images:
            img_ls = sorted_images[path]
            if len(img_ls) == 1:
                img_ls[0].rename()
            else:
                # 存在多个同名文件，按照时间从小到大排序添加序号
                img_ls.sort(
                    key=lambda img: img.time,
                    reverse=False,
                )
                for index, img in enumerate(img_ls):
                    img.index = index + 1  # 序号从 1 开始
                    img.rename()
        showinfo(message="Image rename completed")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s: %(message)s')
    add_handler()
    w = Window()
