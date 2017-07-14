from DB.RedisClient import RedisClient
from Util.getConfig import GetConfig
from Util.logHandler import LogHandler
from ProxyGetter.proxyGetter import ProxyGetter

class ProxyManager(object):
    def __init__(self):
        self.logger = LogHandler('ProxyManger')
        self.dbClient = RedisClient()
        self.config = GetConfig()
        self.orignal_proxy_name,self.useful_proxy_name = self.config.dbName

    def refresh(self):
        for proxyGetFunc in self.config.proxyGetter:
            # proxy_set = set()
            for proxy in getattr(ProxyGetter,proxyGetFunc.strip())():
                if proxy:
                    self.logger.info("{func} fetch proxy {proxy}".format(func=proxyGetFunc,proxy=proxy))
                    # proxy_set.add(proxy.strip())
                    self.dbClient.lput(self.orignal_proxy_name,proxy)

    def get(self):
        """
        从可用代理池中获取一个可用代理
        :return: one useful proxy
        """
        return self.dbClient.sgetOne(self.useful_proxy_name)[0]

    def getAll(self):
        return self.dbClient.sgetAll(self.useful_proxy_name)

    def spop(self):
        """
        从可用代理池中获随机一个代理，并删除
        """
        return self.dbClient.spop(self.useful_proxy_name)

    def pop(self):
        """
        从原始代理池中获一个然后删除
        :return: one original proxy
        """
        return self.dbClient.rpop(self.orignal_proxy_name)

    def put(self,value):
        """
        save validproxy into useful proxy pool
        :param value: 
        :return: 
        """
        self.dbClient.sput(self.useful_proxy_name,value)

    def delete(self, value):
        """
        可用数据库中删除一个代理
        :return: 
        """
        self.dbClient.sdeleteValue(self.useful_proxy_name,value)

    def getStatus(self):
        return self.dbClient.sgetStatues()


if __name__ == '__main__':
    manager = ProxyManager()
    manager.refresh()
    for i in range(10):
        print(manager.pop())
