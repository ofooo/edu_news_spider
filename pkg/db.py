import pandas as pd
import os
import json
from . import top_config


def root(*f, relative_root='../'):
    # relative_root 当前代码目录相对root的相对路径
    for t in f:
        if t[:1] == '/':
            print('Warning: root()包含绝对路径 参数={}'.format(f))
            break
    code_dir = os.path.dirname(os.path.realpath(__file__))
    long_path = os.path.join(code_dir, relative_root, *f)
    return long_path


class JsonDb:
    def __init__(self, filepath='./data.json'):
        self.filepath = filepath
        if os.path.isfile(filepath):
            self.data = json.load(open(filepath))
        else:
            self.data = []

    def append(self, line):
        self.data.append(line)

    def save(self):
        with open(self.filepath, 'w') as f:
            f.write(json.dumps(self.data, indent=2, ensure_ascii=False))

    def head(self, row=5):
        for line in self.data[:row]:
            print(line)


class PandasDb:

    def __init__(self, filepath='./data.csv'):
        self.filepath = filepath
        if os.path.isfile(filepath):
            self.data = pd.read_csv(filepath)
        else:
            self.data = pd.DataFrame(columns=['url', '发表时间', '标题', '来源', '内容'])

    def append(self, line):
        self.data.append(line, ignore_index=True)

    def save(self):
        self.data.to_csv(self.filepath)


save_path = root('./data/data.json')
print('数据存储在', save_path)
os.makedirs(os.path.dirname(save_path), exist_ok=True)

# 存储数据接口
data = JsonDb(save_path)
