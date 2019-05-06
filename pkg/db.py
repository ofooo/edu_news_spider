import pandas as pd
import os
import json
import csv
from . import top_config
import pandas as pd


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
        self.url_set = set()
        self.filepath = filepath
        if os.path.isfile(filepath):
            self.data = json.load(open(filepath))
            for line in self.data:
                self.url_set.add(line.get('url'))
        else:
            self.data = []

    def append(self, line):
        self.url_set.add(line.get('url'))
        self.data.append(line)

    def save(self):
        with open(self.filepath, 'w') as f:
            f.write(json.dumps(self.data, indent=2, ensure_ascii=False))

    def head(self, row=5):
        for line in self.data[:row]:
            print(line)


# class PandasDb:
#
#     def __init__(self, filepath='./data.csv'):
#         self.filepath = filepath
#         if os.path.isfile(filepath):
#             self.data = pd.read_csv(filepath)
#         else:
#             self.data = pd.DataFrame(columns=['url', '发表时间', '标题', '来源', '内容'])
#
#     def append(self, line):
#         self.data.append(line, ignore_index=True)
#
#     def save(self):
#         self.data.to_csv(self.filepath)


class CsvDb:
    def __init__(self, filepath='./data.json'):
        self.url_set = set()
        self.filepath = filepath
        if os.path.isfile(filepath):
            self.data = csv.DictReader(filepath)
            for line in self.data:
                self.url_set.add(line.get('url'))
        else:
            f = open(filepath, 'w', newline='')
            headers = ['origin', 'date', 'title', 'url']
            self.data = csv.DictWriter(f, headers)
            self.data.writeheader()
        print('urlset =', self.url_set)

    def append(self, line):
        if 'url' not in line:
            print('Error! DB line = {} 缺少key="url"'.format(line))
        url = line.get('url')
        if url not in self.url_set:
            self.url_set.add(url)
            self.data.writerow(line)

    def save(self):
        pass
        # with open(self.filepath, 'w') as f:
        #     f.write(json.dumps(self.data, indent=2, ensure_ascii=False))

    def head(self, row=5):
        for line in self.data[:row]:
            print(line)


class PandasDb:
    def __init__(self, filepath='./data.json'):
        self.url_set = set()
        self.filepath = filepath
        if os.path.isfile(filepath):
            self.data = pd.read_csv(filepath, header=0)
            self.url_set = set(self.data['url'])
        else:
            self.data = pd.DataFrame()
        print('读取数据数量 =', len(self.url_set))

    def append(self, line):
        if 'url' not in line:
            print('Error! DB line = {} 缺少key="url"'.format(line))
        url = line.get('url')
        if url not in self.url_set:
            self.url_set.add(url)
            self.data = self.data.append(line, ignore_index=True)

    def save(self):
        self.data.to_csv(self.filepath)

    def head(self, row=5):
        print(self.data.head(row))


save_path = root('./data/data.csv')
print('数据存储在', save_path)
os.makedirs(os.path.dirname(save_path), exist_ok=True)

# 存储数据接口
data = PandasDb(save_path)
