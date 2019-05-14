is_test = True
# is_test = False

print('测试模式：', is_test)

if is_test:
    words = ['教育领域']  # 要搜索的关键词
else:
    words = ['教育领域', '赛事', '教师', '人工智能', '教育信息化']

# 筛选新闻发布时间（起始时间）
min_year = 2018
min_month = 1
min_day = 1

# 工人数
worker_numbers = 1
# 并发数
concurrency = 1

request_config = {
    'RETRIES': 2,
    'DELAY': 10,
    'TIMEOUT': 10,
}
