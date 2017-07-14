import os
import configparser
from Util.utilClass import LazyProperty

class GetConfig(object):
    def __init__(self,name="config.ini"):
        self.pwd = os.path.split(os.path.realpath(__file__))[0]
        self.config_path = os.path.join(os.path.split(self.pwd)[0],name)
        self.configHandler = configparser.ConfigParser()
        self.configHandler.read(self.config_path)

    @LazyProperty
    def dbType(self):
        return self.configHandler.get('DB','type').strip()

    @LazyProperty
    def dbName(self):
        return self.configHandler.get('DB','name1').strip(),self.configHandler.get('DB','name2').strip()

    @LazyProperty
    def dbHost(self):
        return self.configHandler.get('DB','host').strip()

    @LazyProperty
    def dbPort(self):
        return int(self.configHandler.get('DB','port').strip())

    @LazyProperty
    def proxyGetter(self):
        return self.configHandler.options('ProxyGetter')

if __name__ == '__main__':
    handler = GetConfig()
    print("DB name", handler.dbName)
    print("DB host", handler.dbHost)
    print("DB port", handler.dbPort)
    print("Proxy getters", handler.proxyGetter)