"""
旨在汇总各个小功能，方便使用
"""
import os
import tools

info = input("""
        选择功能：
        1. 输入1使用clipboard
        2. 输入2查看密码
        3. 输入3毛概收集
        4. 输入4markdown添加序号
        5. 获取时间字符串
        """)

if info == "2":
    os.system("python ../xlsx/xlsx.py")
elif info == "1":
    os.system("python ../master_clipboard/clipboard.py")
elif info == "3":
    # 切换工作目录，因为这个脚本里面也用到了工作目录
    os.chdir(os.path.abspath(os.path.join(os.getcwd(), "..", "maogai")))
    flag = 1
    while flag:
        os.system("python maogai.py")
        flag = input("要不要继续")
    else:
        print("结束收集试题")

elif info == "4":
    os.system("python ../markdown_process/mp.py")

elif info == "5":
    tools.str_time()
# 执行结束，暂停
print("程序执行结束")
os.system("pause()")
