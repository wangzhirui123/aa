# -*- coding: utf-8 -*-
__author__ = 'Px'

import sys
import os
reload(sys)
sys.setdefaultencoding('utf8')

PID = ''
APPLICATIONLOG_PATH = None

IP_LIST = ["192.168.1.128","","",""]
a='3'


LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),'Log/').replace('\\','/')

if __name__ == '__main__':
    print LOG_PATH
