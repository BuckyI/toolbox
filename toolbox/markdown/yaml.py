from ruamel.yaml import YAML
import re
import io
import os
import subprocess
from pathlib import Path
from datetime import datetime


class Feature():
    nav_tabs = "navigation.tabs"
    nav_sections = "navigation.sections"
    nav_expand = "navigation.expand"
    nav_indexes = "navigation.indexes"
    nav_top = "navigation.top"
    nav_instant = "navigation.instant"
    nav_tracking = "navigation.tracking"
    search_suggest = "search.suggest"
    search_highlight = "search.highlight"
    header_autohide = "header.autohide"


class mkdocsYAML():

    def __init__(self,
                 *,
                 site_name='MkDocsPage',
                 docs_dir='docs',
                 site_dir='sites',
                 features: list[str] = None,
                 keep_yaml=False):
        self.data = {}
        self.yaml_path = "."
        self.keep_yaml = keep_yaml
        self.basic_configure()
        self.data['site_name'] = site_name
        self.data['docs_dir'] = str(Path(docs_dir).absolute())
        self.data['site_dir'] = str(Path(site_dir).absolute())
        if features:
            features = [
                i for i in features if i not in self.data['theme']['features']
            ]
            self.data['theme']['features'].extend(features)

        self.yaml = None
        self.generate_yaml()

    def basic_configure(self):
        self.data['site_name'] = 'MkDocsPage'
        self.data['theme'] = {
            "name":
            "material",
            "features": [
                # Feature.nav_tabs,
                Feature.nav_sections,
                Feature.nav_expand,
                Feature.nav_indexes,
                Feature.nav_top,
                # Feature.nav_instant,
                # Feature.nav_tracking,
                Feature.search_suggest,
                Feature.search_highlight,
                Feature.header_autohide,
            ],
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
        self.data['plugins'] = ["offline", "search"]
        self.data['extra_javascript'] = [
            'javascripts/mathjax.js',
            'https://polyfill.io/v3/polyfill.min.js?features=es6',
            'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'
        ]
        self.data['copyright'] = "Copyright &copy; {} Mightymjolnir".format(
            datetime.today().year)

    def generate_yaml(self):
        outpath = Path(self.yaml_path) / 'mkdocs.yaml'
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
        self.yaml = outpath
        return self

    def build(self):
        assert self.yaml.exists(), f"文档路径错误 {self.yaml.absolute()}"
        subprocess.run(
            ['mkdocs', 'build', '--config-file',
             self.yaml.absolute()])
        return self

    # def __del__(self):
    # if self.yaml and not self.keep_yaml:
    #     self.yaml.unlink()


if __name__ == '__main__':
    # 切换工作路径到脚本所在文件夹
    os.chdir(Path(__file__).absolute().parent)

    site_dir = './test/site/'
    docs_dir = './test/docs'
    # 生成
    ym = mkdocsYAML(site_name='test:)',
                    site_dir=site_dir,
                    docs_dir=docs_dir,
                    features=['navigation.tabs', "navigation.indexes"],
                    keep_yaml=True)
    # subprocess.run(['mkdocs', 'build', '--config-file', 'mkdocs.yaml'])
    # ym.build()
    ym.generate_yaml()

    # subprocess.run(['mkdocs', 'build', '--config-file', "mkdocs.yaml"])
