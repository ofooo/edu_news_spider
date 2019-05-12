from ruia import Request, Spider, AttrField, TextField, Item
from ruia import Middleware
from . import top_config
from .db import data
import traceback
import sys

min_time = '{}-{:0>2d}-{:0>2d}'.format(top_config.min_year, top_config.min_month, top_config.min_day)

middleware = Middleware()


@middleware.request
async def print_on_request(self, request):
    ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    request.headers.update({'User-Agent': ua})


class FishItem(Item):
    target_item = TextField(css_select='#info ')
    title = TextField(css_select='h2 a')
    date = TextField(css_select='dd.search_laiyuan')
    url = AttrField(css_select='h2 a', attr='href')

    async def clean_date(self, value):
        date = value.split('(')[1]
        date = date.rstrip(')')
        print('date =', date)
        return date


class FishSpider(Spider):
    if top_config.is_test:
        page_size = 7
    else:
        page_size = 1000
    start_urls = []
    word = ' '.join(top_config.words)
    start_urls.append('http://www.miit.gov.cn/search/search')
    concurrency = 2
    body = {
        'urls':'http://www.miit.gov.cn/',
        'sortKey':'showTime',
        'sortFlag':-1,
        'fullText':word,
        'sortType':1,
        'indexDB':'css',
        'pageSize':page_size,
        'pageNow':1,
    }
    async def parse(self, response):
        for index, url in enumerate(self.start_urls):
            yield Request(
                url,
                method='POST',
                data=self.body,
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
                        'origin': '工信部',
                        'date': item.date,
                        'title': item.title,
                        'url': item.url,
                    })
                else:
                    time_ok = False
                print('{}\t{}\t{}'.format(item.title, item.date, time_ok))
        except Exception as e:
            self.logger.exception(e)

    async def _run_request_middleware(self, request: Request):
        if self.middleware.request_middleware:
            for middleware in self.middleware.request_middleware:
                try:
                    await middleware(self, request)
                # except TypeError:
                #     self.logger.error(
                #         f"<Middleware {middleware.__name__}: must be a coroutine function"
                #     )
                except Exception as e:
                    error = '\n'.join(traceback.format_exception(*sys.exc_info()))
                    print(error)
                    print(self._run_request_middleware)


def test_spider():
    FishSpider.start(middleware=middleware)
    data.save()


if __name__ == '__main__':
    # test_spider()
    pass
