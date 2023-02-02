import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askokcancel, showinfo
import windnd

import logging
from image import Image, scan


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

