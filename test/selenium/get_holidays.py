import csv
import requests
from lxml import etree


class WanNianRiLi(object):
    """万年日历接口数据抓取
    Params:year 四位数年份字符串
    """

    def __init__(self, year):
        self.year = year
        data = self.parseHTML()

    def parseHTML(self):
        """页面解析"""
        url = 'https://wannianrili.bmcx.com/ajax/?q=2021-06&v=20031912'
        s = requests.session()
        headers = {
            'Host': 'wannianrili.bmcx.com',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://wannianrili.51240.com/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        result = []
        # 生成月份列表
        dateList = [self.year + '-' + '%02d' % i for i in range(1, 13)]
        for year_month in dateList:
            s = requests.session()
            url = 'https://wannianrili.bmcx.com/ajax/?q=2021-06&v=20031912'
            payload = {'q': year_month, 'v': 20031912}
            response = s.get(url, headers=headers)
            element = etree.HTML(response.text)
            html = element.xpath('//div[@class="wnrl_riqi"]')
            print('In Working:', year_month)
            for _element in html:
                # 获取节点属性
                item = _element.xpath('./a')[0].attrib
                if 'class' in item:
                    if item['class'] == 'wnrl_riqi_mo' or item['class'] == 'wnrl_riqi_xiu':
                        _span = _element.xpath('.//text()')
                        result.append(year_month + '-' + _span[0])
        print(result)
        return result


if __name__ == '__main__':
    rili = WanNianRiLi('2021')