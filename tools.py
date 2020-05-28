import time
import pyperclip


def str_time():
    """获取时间字符串，从列表中选择"""
    str_time_ls = []
    str_time_ls.append(time.strftime("%Y.%m.%d"))
    for index, value in enumerate(str_time_ls):
        print(index + 1, ".", value)
    try:
        result = str_time_ls[int(input("choose time")) - 1]
        pyperclip.copy(result)
    except Exception:
        print("error! T^T")
