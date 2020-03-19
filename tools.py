# -*- coding: utf-8 -*-
__author__ = 'Px'
import requests
import sys
import os
import base64
from concurrent.futures import ThreadPoolExecutor
import socket
import numbers
import subprocess
import datetime
import json
import time
import gevent
import gevent.monkey
from config.config import PID,IP_LIST,LOG_PATH
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import ConnectionError
gevent.monkey.patch_socket()
reload(sys)
sys.setdefaultencoding('utf8')


def color_print(msg,color='red', exits=False):

    color_msg = {'blue': '\033[1;36m%s\033[0m',
                 'green': '\033[1;32m%s\033[0m',
                 'yellow': '\033[1;33m%s\033[0m',
                 'red': '\033[1;31m%s\033[0m',
                 'title': '\033[30;42m%s\033[0m',
                 'info': '\033[32m%s\033[0m'}
    msg = color_msg.get(color, 'red') % msg
    print msg

def push_log(info):
    HOST = '103.214.168.94'
    PORT = 8222
    s = socket.socket()
    s.connect((HOST,PORT))
    s.send(info)

def transcoding(info):
    return base64.b64decode(info)

def deleteinfo(userid,ip):
    '''删除人员'''
    photo_data = {
        'pass':'123456',
        'id':'%s'%userid
            }
    #print userid,ip
    result = requests.post('http://{}:8090/person/delete'.format(ip),data=photo_data).content

class Applylog(object):

    def transcoding(self,info):

       return base64.b64decode(info)



    @classmethod
    def writelog(cls,somthing):
        if not os.path.exists(os.path.join(os.path.dirname(__file__),'Log')):
            os.mkdir(os.path.join(os.path.dirname(__file__),'Log'))
        with open(os.path.join(os.path.dirname(__file__),'Log/{}'.format(str(datetime.date.today())[:-3])),'a+')as f:
            now_date = str(datetime.datetime.now())
            f.write('{}:A history of the application running {}\n{}'.format(PID,now_date,somthing))
            push_log('{}:A history of the application running {}\n{}'.format(PID,now_date,somthing))

    def readlog(self,logpath):
        with open(logpath,'r+')as f:
            for i in f.readlines():
                print i.replace('\n','')

class AllUser(object):

    def __init__(self,user_list,business):
        self.pwd = '123456'
        self.user = user_list
        self.status = True
        self.business = business
    def __get__(self, instance, owner):

        return self.user

    def __getitem__(self, item):

        cls = type(self)
        if isinstance(item,numbers.Integral):
            print '11'
            return cls(user_list = self.user[item],business=self.business)
        return self.user[item]

    def deleteinfo(self,ip):

        photo_data = {
        'pass':'123456',
        'id':'%s'%self.user['id']
            }
        result = requests.post('http://{}:8090/person/delete'.format(ip),data=photo_data).content

    def delete_allinfo(self):
        for i in IP_LIST:
            self.deleteinfo(i)

    def push_photo(self,ip):

        photo_data = {
            'pass':'123456',
            'personId':'%s'%self.user['id'],
            'faceId':'',
            'imgBase64':base64.b64encode(requests.get(self.user['img_oss']).content)
        }
        try:
            photo_result = requests.post(url='http://{}:8090/face/create'.format(ip),data=photo_data).content
            photo_reg_info = json.loads(photo_result)
            if 'false' in photo_result:
                self.deleteinfo(ip)
                print u' {}  {}:照片添加失败-{} 人脸识别设备已删除该人员信息,请重新录入'.format(ip,photo_reg_info['msg'],self.user['realname'])
                
            else:
                print u' {}  {}:照片添加成功-{}'.format(ip,photo_reg_info['data'],self.user['realname'])
                update_user = requests.get('http://192.168.1.85:8090/noInUser/updateUserenterByUserId?user_id=%s&type=%s'%(self.user['id'],self.business))
        except ConnectionError:
            print '{},网络连接错误'.format(ip)
        except Exception as e:
            print e

    def push_personnel(self,ip):

        person_data = {
            'pass':self.pwd,
            'permanent':self.user['permanent'],
            'person':'{"id":"%s","idcardNum":"","name":"%s","IDNumber":"","jobNumber":"","facePermission":"2","idCardPermission":"2","faceAndCardPermission":"2","ID Permission":"2"}'%(self.user['id'],self.user['realname'])
        }

        try:
            person_result = requests.post('http://{}:8090/person/create'.format(ip),data=person_data).content
            if json.loads(person_result)['success'] == True:
                print u' {}  人员信息添加成功-{}'.format(ip,self.user['realname'])

                if self.user['permanent'] ==3:
                    end_time = self.user.get('end_time')
                    data = {'personId':json.loads(person_result)['data']['id'],'time':end_time,'pass':'123456'}
                    permissions = requests.post('http://{}:8090/person/permissionsCreate'.format(ip),data=data).content
                    if json.loads(permissions)['success'] ==True:
                        print u'授权人员授权成功'
                elif self.user['permanent'] ==1:
                    out_time = self.user.get('out_time')
                    #out_time = '2020-03-12 10:00:00'

                    data = {'personId':json.loads(person_result)['data']['id'],'time':out_time,'pass':'123456'}
                    permissions = requests.post('http://{}:8090/person/permissionsCreate'.format(ip),data=data).content
                    if json.loads(permissions)['success'] ==True:
                        print u'访客授权成功'
                self.push_photo(ip)
            else:
                print u' {}  人员信息添加失败-{},{} 人脸识别设备已删除该人员信息,请重新录入'.format(ip,self.user['realname'],json.loads(person_result)['msg'])
                
                self.deleteinfo(ip)
                return None
            

        except ConnectionError:
            print '{},网络连接错误'.format(ip)
        except Exception as e:
            print e

    def push_info(self):
        IP_LISTs = [i for i in IP_LIST if i !=""]
        with ThreadPoolExecutor(2)as T:
            T.map(self.push_personnel,IP_LISTs)



class UploadFile(object):

    def __init__(self,file_list):
        self.file = file_list

    def __get__(self, instance, owner):
        return self.file

    def __getitem__(self, item):
        cls = type(self)
        if isinstance(item,numbers.Integral):
            return cls(file_list = self.file[item])
        return self.file[item]

    @classmethod
    def file_list(cls,path):
        return os.listdir(path)

    def upload(self):
        with open(LOG_PATH+self.file,'a+')as f:
            data = f.read()



if __name__ == '__main__':
    print LOG_PATH
    
    # update_user = requests.get('http://111.62.41.223/user/updateUserenterByUserId?user_id=%s'%1)
    person_data = {
            'pass':'123456',
            'person':'{"id":"%s","idcardNum":"","name":"%s","IDNumber":"","jobNumber":"","facePermission":"2","idCardPermission":"2","faceAndCardPermission":"2","ID Permission":"2"}'%(1,'张三')
        }
