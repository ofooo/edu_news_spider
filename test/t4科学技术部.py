import asyncio
from ruia import Item, TextField, AttrField


# class PythonDocumentationItem(Item):
#     title = TextField(css_select='title')
#     tutorial_link = AttrField(xpath_select="//a[text()='Tutorial']", attr='href')
class FishItem(Item):
    target_item = TextField(css_select='td [width="530"]')
    title = TextField(css_select='a')
    date = TextField(css_select='td')
    url = AttrField(css_select='a', attr='href')

    async def clean_date(self, value):
        date = value[-10:]
        date = date.replace('.', '-')
        return date



async def main():
    url = 'http://znjs.most.gov.cn/wasdemo/search?page=2&channelid=44374&searchword=教师&sortfield=-DOCRELTIME&prepage=20'
    async for item in FishItem.get_items(url=url):
        print('-' * 60)
        print(item.title)
        print(item.date)
        print(item.url)



if __name__ == '__main__':
    # Python 3.7 required
    # asyncio.run(main())

    # For python 3.6
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())

# Output:
# [2019:01:21 18:19:02]-Request-INFO  request: <GET: https://docs.python.org/3/>
# 3.7.2 Documentation
# tutorial/index.html