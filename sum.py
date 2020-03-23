"""
旨在汇总各个小功能，方便使用
"""
import os

info = input("""
        选择功能：
        1. 直接回车使用clipboard
        2. 输入东西查看密码
        """)

if info:
    os.system("python xlsx.py")
else:
    os.system("python clipboard.py")

# 执行结束，暂停
print("程序执行结束")
os.system("pause()")
