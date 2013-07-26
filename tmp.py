# -*- encoding: utf-8 -*-


import redis
from settings.local import *

redis_pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


    

def main():
    pass
    

if __name__=='__main__':

    main()
    