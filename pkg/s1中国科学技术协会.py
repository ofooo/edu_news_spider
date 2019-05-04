from ruia import Request, Spider, AttrField, TextField, Item
from ruia import Middleware

from . import top_config
from .db import data


def clean_time(time_txt: str):
    time_txt = time_txt.rstrip('-')
    time_txt = time_txt.rstrip(' ')
    return time_txt


min_time = '{}年{:0>2d}月{:0>2d}日'.format(top_config.min_year, top_config.min_month, top_config.min_day)


class FishItem(Item):
    target_item = TextField(css_select='div.jsearch-result-box')
    title = TextField(css_select='div.jsearch-result-title')
    date = TextField(css_select='span.jsearch-result-date')
    url = AttrField(css_select='div.jsearch-result-title a', attr='href')


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
            date = clean_time(item.date)
            url = 'http://www.cast.org.cn' + item.url
            if url not in data.url_set:
                if date >= min_time:
                    time_ok = True
                    data.append({
                        'origin': '科学技术协会',
                        'date': date,
                        'title': item.title,
                        'url': url,
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
