import random
import redis

from Util.getConfig import GetConfig
from Util.utilClass import Singleton

class RedisClient(object):
    """
    redis client
    redis中存储免费代理地址，所有Ip地址存在一个列表中
    
    """
    def __init__(self,):
        # self.tableName = name
        self.config = GetConfig()
        self.__conn = redis.Redis(host=self.config.dbHost, port=self.config.dbPort, db=1)

    def lgetOne(self,key):
        proxies = self.__conn.lrange(key, 0, -1)
        return random.choice(proxies) if proxies else None

    def rpop(self, key):
        return self.__conn.rpop(key)

    def lgetAll(self,key):
        return self.__conn.lrange(key, 0, -1)

    def lput(self, key, value):
        if isinstance(value,list):
            self.__conn.rpush(key,*value)
        else:
            self.__conn.rpush(key,value)

    def ldeleteValue(self, key, value, num=0):
        self.__conn.lrem( key, value, num=num)

    def lgetStatus(self, key):
        return self.__conn.llen(key)

    def deleteAll(self,key):
        self.__conn.delete(key)

    def spop(self, key):
        return self.__conn.spop(key)

    def sgetOne(self,key):
        return self.__conn.srandmember(key,1)

    def sgetAll(self,key):
        return self.__conn.smembers(key)

    def sput(self,key, value):
        if isinstance(value, list):
            self.__conn.sadd(key, *value)
        else:
            self.__conn.sadd(key, value)

    def sdeleteValue(self, key, value):
        self.__conn.srem(key, value)

    def sgetStatues(self,key):
        return self.__conn.scrd(key)



if __name__ == '__main__':
    client = RedisClient()
    client.lput("test",["192.168.1.1:2345","192.168.2.1:1234"])
    print(client.lgetAll("test"))
    client.ldeleteValue("test","192.168.2.1:1234")
    print(client.lgetOne("test"))
    print(client.lgetAll('test'))

    client.sput('test1',[1,2,3,4])
    print(client.sgetAll('test1'))
    client.sdeleteValue('test1',2)
    print(client.sgetOne('test1'))
    print(client.sgetAll('test1'))

    client.deleteAll('test')
    client.deleteAll('test1')