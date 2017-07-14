from Util.logHandler import LogHandler
import requests
from selenium import webdriver
from lxml import etree
logger = LogHandler(__name__)


def validProxy(proxy):
    proxies = {
                'https':'https://'+proxy,
                'http': 'http://'+proxy,
    }
    headers={
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',

    }
    try:
        response = requests.get("https://www.baidu.com",headers=headers,proxies=proxies,timeout=20,verify=False)
        if response.status_code == 200:
            logger.info("{proxy} is ok!".format(proxy=proxy))
            return True
        else:
            logger.info("{proxy} is bad!~".format(proxy=proxy))
            return False
    except Exception as e:
        logger.error(e)
        return False


def getHTMLText(url, headers={'user': 'Mozilla/5.0'}):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
        else:
            return response.status_code
    except:
        return response.status_code


def getHTMLTree(url, headers={'user': 'Mozilla/5.0'}):
    try:
        response = requests.get(url, headers=headers, timeout=10,verify=False)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return etree.HTML(response.content)
        else:
            return response.status_code
    except:
        return response.status_code


def phantomJsHtmlTree(url):
    driver = webdriver.PhantomJS()
    driver.get(url)
    return etree.HTML(driver.page_source)


if __name__ == '__main__':
    if validProxy("111.243.96.109:8416"):
        print("ok")