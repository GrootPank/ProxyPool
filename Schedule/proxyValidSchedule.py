from apscheduler.schedulers.blocking import BlockingScheduler

from Manager.proxyManager import ProxyManager
from Util.logHandler import LogHandler
from Util.utilFunction import validProxy

class ProxyValidSchedule(ProxyManager):
    def __init__(self):
        super(ProxyValidSchedule, self).__init__()
        self.logger = LogHandler("valid_schedule")

    def valid_Proxy(self):
        proxy = self.spop()
        temp_pool = ["115.186.179.217:53281","125.62.193.18:53281","115.220.148.137:808",
                     "118.117.136.19:9000","85.185.111.121:80","176.237.139.8:8080","125.89.123.224:808","60.167.132.226:808","180.118.241.200:808"]
        self.logger.info("*************Start Valid proxies************* ")
        while proxy:
            if isinstance(proxy,bytes):
                proxy = proxy.decode("utf-8")
            if validProxy(proxy):
                temp_pool.append(proxy)
                self.logger.info("{0} validation pass".format(proxy))
            else:
                self.logger.info("{0} validation failed".format(proxy))
            proxy = self.spop()
        self.logger.info("##############Valid proxies is complete ################ ")
        if temp_pool:
            for proxy in temp_pool:
                self.put(proxy)




def doValid():
    schedule = ProxyValidSchedule()
    schedule.valid_Proxy()

def run():
    scheduler = BlockingScheduler()
    scheduler.add_job(doValid,'interval',minutes=30)
    scheduler.start()

if __name__ == '__main__':
    # run()
    doValid()