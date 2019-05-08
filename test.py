# from lxml import etree
# import requests
#
# url = 'http://www.cast.org.cn/jrobot/search.do?webid=1&pg=&p=&q=%E8%B5%9B%E4%BA%8B'
# res = requests.get(url)
# root = etree.HTML(res.text)


import asyncio
from ruia import Item, TextField, AttrField


class FishItem(Item):
    target_item = TextField(css_select='#info span')
    title = TextField(css_select='a')
    # date = TextField(css_select='dd.search_laiyuan')



async def main():
    url = 'http://www.miit.gov.cn/search/search'
    body = {
        'urls': 'http://www.miit.gov.cn/',
        'sortKey': 'showTime',
        'sortFlag': -1,
        'fullText': '比赛',
        'sortType': 1,
        'indexDB': 'css',
        'pageSize': 6,
        'pageNow': 1,
    }
    async for item in FishItem.get_items(url=url, method='POST', data=body):
        print(f'Title={item.title}')


if __name__ == '__main__':
    # Python 3.7 required
    # asyncio.run(main())

    # For python 3.6
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
