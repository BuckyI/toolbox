import os
import json
from pprint import pprint
import argparse
import time
from json2html import json2html


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


def compare_dir(dir1, dir2):
    file_tree1 = scan_dir(dir1)
    file_tree2 = scan_dir(dir2)
    diff = set(file_tree1.keys()) ^ set(file_tree2.keys())
    return diff


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
    with open(name, "w", encoding="utf-8") as f:
        json.dump(file_tree, f, ensure_ascii=False, sort_keys=True)
    # with open(name, "r", encoding="utf-8") as f:
    #     file_tree = json.load(f)
    #     pprint(file_tree)

    # save interactive html
    html_name = os.path.splitext(name)[0] + ".html"
    html = json2html.convert(json=file_tree,
                             table_attributes="border='1 solid black'")
    with open(html_name, 'w', encoding="utf-8") as f:
        f.write(html)

    print(f"finished🎃 \nfrom: {top}\nto: {name} & html")
