from lxml import etree
import requests

url = 'http://www.cast.org.cn/jrobot/search.do?webid=1&pg=&p=&q=%E8%B5%9B%E4%BA%8B'
res = requests.get(url)
root = etree.HTML(res.text)
