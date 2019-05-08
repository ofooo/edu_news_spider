from pkg.db import data
from pkg import s1中国科学技术协会
from pkg import s2中华人民共和国教育部
from pkg import s3工信部

# s1中国科学技术协会.FishSpider.start()
# s2中华人民共和国教育部.FishSpider.start(middleware=s2中华人民共和国教育部.middleware)
s3工信部.FishSpider.start()
data.save()
