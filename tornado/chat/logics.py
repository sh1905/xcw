import json
from redis import Redis

rds = Redis()

class MsgHistory:
    key = 'chat_history'
    size = 10

    @classmethod
    def add(cls,msg):
        '''记录一条历史消息'''
        json_msg = json.dumps(msg) # 将消息转换成json字符串
        rds.rpush(cls.key,json_msg) # 将消息推入Redis的List中
        rds.ltrim(cls.key,-cls.size,-1) #截出聊天队列的最后size条消息
    @classmethod
    def all(cls):
        '''取出所有的历史消息'''
        all_msg=[]
        for json_msg in rds.lrange(cls.key,-cls.size,-1):
            msg = json.loads(json_msg)#将json字符串转换成消息
            all_msg.append(msg)
        return all_msg





