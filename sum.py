"""
旨在汇总各个小功能，方便使用
"""
import os

info = input("""
        选择功能：
        1. 输入1使用clipboard
        2. 输入2查看密码
        3. 输入3毛概收集
        4. 输入4markdown添加序号
        """)

if info == "2":
    os.system("python ../xlsx/xlsx.py")
elif info == "1":
    os.system("python ../master_clipboard/clipboard.py")
elif info == "3":
    # 切换工作目录，因为这个脚本里面也用到了工作目录
    os.chdir(os.path.abspath(os.path.join(os.getcwd(), "..", "maogai")))
    os.system("python exe.py")
elif info == "4":
    os.system("python ../markdown_process/mp.py")

# 执行结束，暂停
print("程序执行结束")
os.system("pause()")
