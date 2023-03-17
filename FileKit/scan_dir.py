import os
from pathlib import Path
import json
from pprint import pprint

top = r"C:\Users\45489\Documents\GitHub\toolbox\Markdown"
file_tree = {"root": top}
for dirpath, dirnames, filenames in os.walk(top):
    depth = dirpath.replace(top, '').count(os.sep)
    file_tree[dirpath] = {
        "depth": depth,
        "dirnames": dirnames,
        "filenames": filenames
    }
pprint(file_tree)

with open("test.json", "w+") as f:
    json.dump(file_tree, f)
with open("test.json", "r") as f:
    test = json.load(f)
    pprint(test)
