from ruia import Request, Spider, AttrField, TextField, Item
from ruia import Middleware
from . import top_config
from .db import data


def clean_time(time_txt: str):
    time_txt = time_txt.rstrip('-')
    time_txt = time_txt.rstrip(' ')
    return time_txt


min_time = '{}年{:0>2d}月{:0>2d}日'.format(top_config.min_year, top_config.min_month, top_config.min_day)

middleware = Middleware()


@middleware.request
async def print_on_request(request):
    ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    request.headers.update({'User-Agent': ua})


class FishItem(Item):
    target_item = TextField(css_select='div.m_search_list dl')
    title = TextField(css_select='h2 a')
    date = TextField(css_select='dd.search_laiyuan')
    url = AttrField(css_select='h2 a', attr='href')


class FishSpider(Spider):
    if top_config.is_test:
        page_max = 1
    else:
        page_max = 10
    config = {'number': 8}
    start_urls = []
    for word in top_config.words:
        for page in range(1, page_max + 1):
            start_urls.append(
                'http://www.moe.gov.cn/was5/web/search?channelid=224838&searchword={word}&page={page}'.format(
                    word=word, page=page
                ))
    concurrency = 2

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
            if date >= min_time:
                time_ok = True
                data.append({
                    'url': 'http://www.cast.org.cn' + item.url,
                    'title': item.title,
                    'date': date,
                })
            else:
                time_ok = False
            print('{}\t{}\t{}'.format(item.title, item.date, time_ok))
        except Exception as e:
            self.logger.exception(e)


def test_spider():
    FishSpider.start(middleware=middleware)
    data.save()


if __name__ == '__main__':
    # test_spider()
    pass
