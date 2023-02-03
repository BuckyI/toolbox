import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askokcancel, showinfo
import windnd
import uuid
import logging
from image import Image, scan, add_handler
from pathlib import Path


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
        self.tag_type = tk.StringVar()  # 如何添加标签
        com = ttk.Combobox(
            master=frm_tag,  # 父容器
            state='readonly',  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
            textvariable=self.tag_type,
            values=["无标签", "自定义标签", "文件名作为标签"],  # 设置下拉框的选项
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
                continue
            images.extend(scan(p.absolute()))

        # load tags
        tag_type = self.tag_type.get()
        if tag_type == "无标签":
            tags = []
            for img in images:
                img.set_tags(tags, reset=True)
        elif tag_type == "自定义标签":
            tags = self.tag.get().split()
            for img in images:
                img.set_tags(tags, reset=True)
        elif tag_type == "文件名作为标签":
            tags = img.path.name.split()
            for img in images:
                img.set_tags(tags, reset=True)
        else:  # default behavior of Image
            pass

