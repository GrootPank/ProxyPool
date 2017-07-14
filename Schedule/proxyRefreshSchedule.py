import threading

from apscheduler.schedulers.blocking import BlockingScheduler

from Manager.proxyManager import ProxyManager
from Util.logHandler import LogHandler
from Util.utilFunction import validProxy


class ProxyRefreshSchedule(ProxyManager):
    def __init__(self):
        ProxyManager.__init__(self)
        self.logger = LogHandler("refresh_shedule")

    def valid_Proxy(self):
        """
        valid the proxy in origal proxy pool, put the useful proxies in useful proxy pool
        :return: 
        """
        proxy = self.pop()
        self.logger.info("*************Start Valid proxies************* ")
        while proxy:
            if validProxy(proxy.decode("utf-8")):
                self.put(proxy)
                self.logger.info("{0} validation pass".format(proxy))
            else:
                self.logger.info("{0} validation failed".format(proxy))
            proxy = self.pop()
        self.logger.info("##############Valid proxies is complete ################ ")


def doValidProxy():
    sh = ProxyRefreshSchedule()
    sh.valid_Proxy()


def main(threadMun=5):
    sh = ProxyRefreshSchedule()
    sh.refresh()
    threads = [threading.Thread(target=doValidProxy) for item in range(threadMun)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def run():
    schedule = BlockingScheduler()
    schedule.add_job(main,'interval',hours=1)
    schedule.start()

if __name__ == '__main__':
    main()