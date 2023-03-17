import os
import json
from pprint import pprint
import argparse
import time


def scan_dir(top: str):
    file_tree = {"root": top}
    for dirpath, dirnames, filenames in os.walk(top):
        depth = dirpath.replace(top, '').count(os.sep)
        file_tree[dirpath] = {
            "depth": depth,
            "dirnames": dirnames,
            "filenames": filenames
        }
    return file_tree


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder",
                        help="the folder path to scan",
                        default=".")
    parser.add_argument("--output",
                        help="the folder path of the json file to output",
                        default=".")
    args = parser.parse_args()

    # # 切换工作目录至脚本所在文件夹，影响相对路径的解读
    # scr_path = os.path.split(os.path.realpath(__file__))[0]
    # os.chdir(scr_path)
    assert os.path.exists(args.folder), "given folder dosen't exist!"
    assert os.path.exists(args.output), "output folder dosen't exist!"

    top = os.path.abspath(args.folder)
    file_tree = scan_dir(top)
    # pprint(file_tree)

    # save json
    names = [
        time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())),
        os.path.basename(top)
    ]
    name = " ".join(names) + ".json"
    name = os.path.abspath(os.path.join(args.output, name))
    assert not os.path.exists(name)
    with open(name, "w") as f:
        json.dump(file_tree, f)
    # with open("test.json", "r") as f:
    #     file_tree = json.load(f)
    print(f"finished🎃 \nfrom: {top}\nto: {name}")
