from ruia import Request, Spider, AttrField, TextField, Item
from ruia import Middleware

from . import top_config
from .db import data

# min_time = '{}年{:0>2d}月{:0>2d}日'.format(top_config.min_year, top_config.min_month, top_config.min_day)
min_time = '{}-{:0>2d}-{:0>2d}'.format(top_config.min_year, top_config.min_month, top_config.min_day)


class FishItem(Item):
    target_item = TextField(css_select='div.jsearch-result-box')
    title = TextField(css_select='div.jsearch-result-title')
    date = TextField(css_select='span.jsearch-result-date')
    url = AttrField(css_select='div.jsearch-result-title a', attr='href')

    async def clean_date(self, value):
        date = value.rstrip('-')
        date = date.rstrip(' ')
        date = date.rstrip('日')
        date = date.replace('年', '-').replace('月', '-')
        return date

    async def clean_url(self, value):
        url = 'http://www.cast.org.cn' + value
        return url


class FishSpider(Spider):
    if top_config.is_test:
        number = 6
    else:
        number = 1000
    config = {'number': 8}
    start_urls = []
    for word in top_config.words:
        start_urls.append('http://www.cast.org.cn/jrobot/search.do?webid=1&pg={number}&p=&q={word}'.format(
            number=number, word=word
        ))
    concurrency = 3

    async def parse(self, response):
        for index, url in enumerate(self.start_urls):
            yield Request(
                url,
                callback=self.parse_item,
                metadata={'index': index}
            )

    async def parse_item(self, response):
        async for item in FishItem.get_items(html=response.html):
            yield item

    async def process_item(self, item):
        try:
            if item.url not in data.url_set:
                if item.date >= min_time:
                    time_ok = True
                    data.append({
                        'origin': '科学技术协会',
                        'date': item.date,
                        'title': item.title,
                        'url': item.url,
                    })
                else:
                    time_ok = False
                print('{}\t{}\t{}'.format(item.title, item.date, time_ok))
        except Exception as e:
            self.logger.exception(e)


def test_spider():
    FishSpider.start()
    data.save()


if __name__ == '__main__':
    # test_spider()
    pass
