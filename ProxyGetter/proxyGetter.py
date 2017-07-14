import requests
import time
import re
from pyquery import pyquery
from Util.utilFunction import getHTMLText, getHTMLTree
HEADERS = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
}
class ProxyGetter(object):
    def __init__(self):
        pass

    @staticmethod
    def get_kuaidaili_proxies(pages=5):
        for page in range(1,pages+1):
            url = "http://www.kuaidaili.com/free/inha/{0}/".format(page)
            response = requests.get(url,headers=HEADERS)
            if response.status_code == 200:
                pq = pyquery.PyQuery(response.text)
            else:
                print(response.status_code)
                return
            for item in pq("tbody > tr"):
                td = item.findall('td')
                yield td[0].text+":"+td[1].text
            time.sleep(5)

    @staticmethod
    def get_66ip_proxies(num=50):
        url = "http://m.66ip.cn/mo.php?sxb=&tqsl={}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=".format(
            num)
        html = getHTMLText(url, headers = HEADERS)
        pattern = re.compile("\d+\.\d+\.\d+\.\d+\:\d+")
        proxies = pattern.findall(html)
        for proxy in proxies:
            yield proxy


    @staticmethod
    def get_xicidaili_proxies(page_num=2):
        url_list = ['http://www.xicidaili.com/nt/' ,'http://www.xicidaili.com/nn/']
        for url in url_list:
            for num in range(1,page_num+1):
                url = url + str(num)
                tree = getHTMLTree(url, HEADERS)
                for item in tree.xpath("//table[@id='ip_list']/tr[@class]"):
                    # print(item)
                    yield ":".join(item.xpath('./td/text()')[0:2])
                time.sleep(5)

    @staticmethod
    def get_goubanjia_proxies(page_num=1):
        #网站的反扒策略，request请求到的ip没问题，但是端口号是不正确的
        #没有找到端口的数据来源，所以要获得正确的端口，需要通过phamjs
        url = "http://www.goubanjia.com/free/gngn/index{page}.shtml"
        for num in range(1,page_num+1):
            url = url.format(page=num)
            tree = getHTMLTree(url,HEADERS)
            for item in tree.xpath ("//table[@ class='table']/tbody/tr"):
                yield "".join(item.xpath("./td[@class='ip']/span/text() | ./td[@class='ip']/div/text()|./td[@class='ip']/text()"))





if __name__ == '__main__':
    getter = ProxyGetter()
    for i in getter.get_goubanjia_proxies():
        print(i)
