import asyncio
from ruia import Item, TextField, AttrField


# class PythonDocumentationItem(Item):
#     title = TextField(css_select='title')
#     tutorial_link = AttrField(xpath_select="//a[text()='Tutorial']", attr='href')
class PythonDocumentationItem(Item):
    target_item = TextField(css_select='#info span')
    title = TextField(css_select='h2 a')



async def main():
    url = 'https://docs.python.org/3/'
    item = await PythonDocumentationItem.get_item(url=url)
    print(item.title)
    print(item.tutorial_link)


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