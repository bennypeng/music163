# music163 with scrapy
> 小弟抱以学习python与scrapy的心态完成此项目，请大家海涵，勿喷。
> 如有建议，可进行pull request，谢谢！

## 如何使用？

### 安装依赖
```sh
python3.7 -m pip install scrapy pymongo requests fake_useragent
```

注意: 需要预先安装好mongodb

### 运行步骤
```sh
git clone git@github.com:bennypeng/music163.git
cd music163
scrapy crawl kuaidaili   # 爬取kuaidaili代理ip
scrapy crawl xicidaili   # 爬取xicidaili代理ip
scrapy crawl hotcomments # 爬取所有歌手评论
```

## 更新日志
### [1.0.0] - 2019-01-24
- 增加爬虫hotcomments用于爬取歌曲热评
- 增加爬虫xicidaili用于爬取可用代理ip
- 增加爬虫kuaidaili用于爬取可用代理ip
- 使用fake_useragent生成随机USER-AGENT