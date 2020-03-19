# -*- coding: utf-8 -*-
__author__ = 'Px'

import sys
import re
import time
import json
import requests
from concurrent.futures import ThreadPoolExecutor

from config.config import PID
reload(sys)
sys.setdefaultencoding('utf8')

URL = "http://111.62.41.223/equipment/queryUserAndUserFace?project_id={}".format(PID)
try:
    data = json.loads(requests.get(URL).content)['data']
except:
    data = {}
IP = raw_input(r'Enter IP address:')

def deleteinfo(Id):
    photo_data = {
    'pass':'123456',
    'id':'%s'%Id
        }

    result = requests.post('http://{}:8090/person/delete'.format(IP),data=photo_data).content
def deleteinfobyitem(item):
    photo_data = {
    'pass':'123456',
    'id':'%s'%item['id']
        }

    result = requests.post('http://{}:8090/person/delete'.format(IP),data=photo_data).content
    print result
def transmission(item):


        person_data = {
            'pass':"123456",
            'person':'{"id":"%s","idcardNum":"","name":"%s","IDNumber":"","jobNumber":"","facePermission":"2","idCardPermission":"2","faceAndCardPermission":"2","ID Permission":"2"}'%(item['id'],item['realname'])
        }
        try:
            person_result = requests.post('http://{}:8090/person/create'.format(IP),data=person_data).content

            if 'true' in person_result:
                print u' {}  人员信息添加成功-{}'.format(IP,item['realname'])
            else:
                print u' {}  人员信息添加失败-{},{} 人脸识别设备已删除该人员信息,请重新录入'.format(IP,item['realname'],json.loads(person_result)['msg'])

                deleteinfo(item['id'])
                return None
        except Exception as e:
            print e

        photo_data = {
        'pass':'123456',
        'personId':'%s'%item['id'],
        'faceId':'',
        'imgBase64':base64.b64encode(requests.get(item['img_oss']).content)
    }
        try:
            photo_result = requests.post(url='http://{}:8090/face/create'.format(IP),data=photo_data).content
            photo_reg_info = json.loads(photo_result)
            if 'false' in photo_result:
                deleteinfo(item['id'])
                print u' {}  {}:照片添加失败-{} 人脸识别设备已删除该人员信息,请重新录入'.format(IP,photo_reg_info['msg'],item['realname'])

            else:
                print u' {}  {}:照片添加成功-{}'.format(IP,photo_reg_info['data'],item['realname'])
        except Exception as e:
            print e


if __name__ == '__main__':
    with ThreadPoolExecutor(1) as T:
        T.map(transmission,data)
        #T.map(deleteinfobyitem,data)

