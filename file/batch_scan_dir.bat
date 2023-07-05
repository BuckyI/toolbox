@echo off & chcp 65001
cd F:/
set scan_list=Comics Document Music Pictures "This is my life" Videos "泛笔记" "学习使我快乐" 
for %%x in (%scan_list%) do (
    echo python c:/Users/45489/Documents/GitHub/toolbox/FileKit/scan_dir.py --folder %%x --output Func/file_tree_backup/
)
pause