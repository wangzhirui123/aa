# -*- coding: utf-8 -*-
__author__ = 'Px'

import sys
import json
import base64
import time
import gevent
import requests
import gevent.monkey
from tools import AllUser
gevent.monkey.patch_socket()
from requests.exceptions import ConnectionError
from config.config import PID
from config.config import IP_LIST
reload(sys)
sys.setdefaultencoding('utf8')
STATUS = 1

if __name__ == '__main__':
    IP_LISTs = [i for i in IP_LIST if i !=""]
    for ip in IP_LISTs:
        try:
            code = requests.get('http://{}:8090'.format(ip))
        except ConnectionError:
            print u'{}网络错误'.format(ip)
            STATUS = 0

    if STATUS:

        try:
            #0、工地 1、学校 2、社区 3、公共服务 4、工厂 5、餐饮、
            alluser = AllUser(json.loads(requests.get('http://111.62.41.222:8083/noInUser/queryNoInUserByPId?project_id=%s&type=%s'%(PID,0)).content),0)

            [item.push_info() for item in alluser]
            time.sleep(3)
        except ValueError:
            print u"检查项目ID配置"
    else:
        print u"请检查网路"

