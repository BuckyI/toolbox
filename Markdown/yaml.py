from ruamel.yaml import YAML
import re
import io
import os
import subprocess


class YAMLGenerator():
    def __init__(self,
                 *,
                 site_name='MkDocsPage',
                 docs_dir='docs',
                 site_dir='sites'):
        self.data = {}
        self.yaml_path = "."

        self.configure()
        self.data['site_name'] = site_name
        self.data['docs_dir'] = os.path.abspath(docs_dir)
        self.data['site_dir'] = os.path.abspath(site_dir)

    def configure(self):
        self.data['site_name'] = 'MkDocsPage'
        self.data['theme'] = {
            "name":
            "material",
            "features":
            ["navigation.tabs", "navigation.indexes", "navigation.top"],
            "language":
            "zh",
            "palette": [{
                "scheme": "default",
                "toggle": {
                    "icon": "material/toggle-switch-off-outline",
                    "name": "Switch to dark mode"
                }
            }, {
                "scheme": "slate",
                "toggle": {
                    "icon": "material/toggle-switch",
                    "name": "Switch to light mode"
                }
            }],
        }
        self.data['use_directory_urls'] = False  # 此项用于 build 结果可以本地打开
        self.data['docs_dir'] = 'docs'  # 使用单引号, 防止转义\
        self.data['site_dir'] = 'sits'
        self.data['markdown_extensions'] = [
            'markdown_captions',  # 给图片添加标题 可选
            'sane_lists',  # 优化列表显示
            'admonition',
            'pymdownx.details',
            'nl2br',
            'def_list',
            'footnotes',
            'meta',
            'md_in_html',
            {
                'toc': {
                    'marker': '[toc]',
                    'permalink': True
                }
            },
            'tables',
            {
                'admonition': {}
            },
            {
                'pymdownx.arithmatex': {
                    'generic': True
                }
            },
            'pymdownx.betterem',
            'pymdownx.caret',
            'pymdownx.mark',
            'pymdownx.tilde',
            {
                'pymdownx.tabbed': {
                    'alternate_style': True
                }
            },
            {
                'pymdownx.tasklist': {
                    'custom_checkbox': True
                }
            },
            'pymdownx.smartsymbols',  # 一些字符序列会自动变成特殊符号
            {
                'pymdownx.superfences': {
                    "custom_fences": [{
                        'name':
                        'mermaid',
                        'class':
                        'mermaid',
                        'format':
                        '!!python/name:pymdownx.superfences.fence_code_format'
                    }]
                }
            }
        ]
        self.data['extra_javascript'] = [
            'javascripts/mathjax.js',
            'https://polyfill.io/v3/polyfill.min.js?features=es6',
            'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'
        ]

    def save(self, path=None):
        if path:
            self.yaml_path = path
        outpath = os.path.join(self.yaml_path, 'mkdocs.yaml')

        with io.StringIO() as buffer:
            yaml = YAML()
            yaml.dump(self.data, buffer)
            # 有一处输出不符合要求, 这里用匹配替换解决
            texts = buffer.getvalue()
            texts = re.sub(pattern=r"'(!!python/name.*?)'",
                           repl=r"\1",
                           string=texts,
                           count=1)
            with open(outpath, mode='w', encoding='utf-8') as f:
                f.write(texts)


if __name__ == '__main__':
    # 切换工作路径到脚本所在文件夹
    scr_path = os.path.split(os.path.realpath(__file__))[0]
    os.chdir(scr_path)
    print(scr_path)
    # ym = YAMLGenerator(site_dir='./test/site/', docs_dir='./test/docs')
    # ym.save()
    # subprocess.call(['mkdocs', 'build'])
