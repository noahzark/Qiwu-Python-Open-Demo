#
# @Author Siyang Zhang
# @Date Aug 21, 2019
# 
# 
# #

import controller as con
import json
import urllib3
import requests
import time
import hashlib
import urllib
import uuid
import socket
import wave
import base64
from urllib import request
from requests_toolbelt.multipart import MultipartEncoder



# appchannel = "feli-tech-test"
# aeskey = "NY8iA0QYXVgsje5pcDiaUOwKsCSjEWlfGlXxJ/9KikY="
# aesiv="5a2wShLw7EWa8Fiw+cWYcQ=="
# privatekey = "1c9f03b3-c920-4d68-b2cd-299a28557890"


# server = 'https://account-center-test.chewrobot.com/'



login_access_token = ""
login_authorization = ""
login_time = ""

class General:

    def __init__(self, controller, appchannel, privatekey, paths):
        self.controller = controller
        self.appchannel = appchannel
        self.privatekey = privatekey
        self.paths = paths

    # Api Token获取接口
    # # 
    def getAccessToken(self):
        # appchannel = self.controller.appchannel
        # privatekey = self.controller.privatekey
        headers = self.controller.getFillSignParams(self.appchannel, self.privatekey)

        # headers = {"content-type":"application/json"}
        server = self.controller.gateway
        path = self.paths["authorize"]
        print(headers)

        r = requests.get(server + path, headers = headers)
    
        json_obj = r.json()

        payload = json_obj["payload"]

        return payload

    # 刷新API Token接口
    # #
    def getRefreshedToken(self, refreshToken):
        server = self.controller.gateway
        path = self.paths["authorize"]
        headers = {}
        headers["Refresh-Token"] = refreshToken
        headers["Timestamp"] = self.controller.getTimeStamp()
        
        r = requests.put(server + path, headers = headers)

        json_obj = r.json()

        return json_obj

    # 注销API Token接口 TODO
    # #
    def deleteToken(self, accessToken, auth):
        server = self.controller.gateway
        path = self.paths["authorize"]
        headers = {}
        headers["Timestamp"] = self.controller.getTimeStamp()
        headers["Access-Token"] = accessToken
        headers["Authorization"] = auth
        print(headers)
        r = requests.delete(server + path, headers = headers)   
        json_obj = r.json() 
        return json_obj


    # 获取验证码接口
    # #
    def getCAPTCHA(self, phoneNumber):
        server = self.controller.gateway
        path = self.paths["captcha"]
        phone_b64 = base64.b64encode(bytes(phoneNumber+":", 'utf-8'))
        headers = {}
        headers["Timestamp"] = self.controller.getTimeStamp()
        payload = self.getAccessToken()
        de_payload = self.controller.decrypt(payload)
        # print(de_payload)
        payload_js = json.loads(de_payload)
        accessToken = payload_js["accessToken"]
        headers["Access-Token"] = accessToken
        print(phone_b64)
        sss = str(phone_b64,'utf-8')
        print(sss)
        headers["Authorization"] = "Basic " + sss
        print(headers)

        r = requests.get(server + path, headers = headers)
        json_obj = r.json() 
        print(json_obj)
        return json_obj

    # 登陆、注册接口
    # phoneNumber 为用户手机号
    # captcha 为获得的验证码
    # #
    def getLogin(self, phoneNumber, captcha):
        server = self.controller.gateway
        path = self.paths["token"]
        authInfo = phoneNumber + ":" + captcha
        auth_b64 = base64.b64encode(bytes(authInfo,'utf-8'))
        auth_b64 = "Basic " + str(auth_b64, 'utf-8')

        headers = {}
        headers["Timestamp"] = self.controller.getTimeStamp()
        global login_time
        login_time = headers["Timestamp"]
        payload = self.getAccessToken()
        de_payload = self.controller.decrypt(payload)

        print(de_payload)
        payload_js = json.loads(de_payload)
        accessToken = payload_js["accessToken"]
        print("这是本次的accessToken, 后续一直用它:\n" + accessToken)
        headers["Access-Token"] = accessToken
        
        headers["Authorization"] = auth_b64
        
        global login_authorization
        login_authorization = auth_b64

        print("header: " + str(headers))

        r = requests.get(server + path, headers = headers)
        json_obj = r.json() 
        print(json_obj)
        pld = json_obj["payload"]


        pld = self.controller.decrypt(pld)
        print("pld:\n" + pld)

        pld = json.loads(pld)

        author = pld["accessToken"]

        params = {"accessToken" : accessToken, "Authorization" : author}

        return params
        # if json_obj["retcode"] == 0:    
        #     ref_payload = json_obj["payload"]
            
        #     de_ref = con.decrypt(ref_payload, aeskey, aesiv)
        #     print("payload: " + de_payload)
        #     jss = json.loads(de_ref)
        #     print("accessToken: " + jss["accessToken"])
        #     global login_access_token
        #     login_access_token = jss["accessToken"]
        #     return jss["accessToken"]
        # else:
        #     print("fail")
        #     print(json_obj)
        #     return "Fail"




    # 刷新Token接口
    # #
    def getRefreshedUserToken(self, phoneNumber, captcha):
        server = self.controller.gateway
        path = self.paths["token"]
        payload = self.getLogin(phoneNumber, captcha)["payload"]
        de_payload = self.controller.decrypt(payload)
        print(de_payload)
        payload_js = json.loads(de_payload)

        accessToken = payload_js["accessToken"]
        refresh = payload_js["refreshToken"]
        headers = {}
        headers["Timestamp"] = self.controller.getTimeStamp()
        headers["Access-Token"] = accessToken
        headers["Authorization"] = "Bearer " + refresh

        r = requests.put(server + path, headers = headers)
        json_obj = r.json() 
        print(json_obj)
        return json_obj

    # 登出接口
    # #
    def getLogout(self, accessToken, auth):
        server = self.controller.gateway
        path = self.paths["token"]
        print("\ndelete:")
        headers = {}
        headers["Timestamp"] = self.controller.getTimeStamp()
        # payload = getAccessToken()
        # de_payload = con.decrypt(payload, aeskey, aesiv)

        # payload_js = json.loads(de_payload)
        # accessToken = payload_js["accessToken"]
        headers["Access-Token"] = accessToken
        headers["Authorization"] = "Bearer " + auth
        print(auth)
        r = requests.delete(server + path, headers = headers)
        json_obj = r.json() 
        print(json_obj)
        return json_obj

    # 
    # 获取用户信息接口
    # #
    def getUserInfo(self, accessToken, auth):
        server = self.controller.gateway
        path = self.paths[""]
        print("getUserInfo")
        headers = {}
        times = self.controller.getTimeStamp()
        headers["Timestamp"] = times
        # payload = getAccessToken()
        # de_payload = con.decrypt(payload, aeskey, aesiv)

        # payload_js = json.loads(de_payload)
        # accessToken = payload_js["accessToken"]
        headers["Access-Token"] = accessToken
        headers["Authorization"] = "Bearer " + auth
        print("headers: ")
        print(headers)

        r = requests.get(server + path, headers = headers)
        json_obj = r.json() 
        print(json_obj)
        return json_obj

    # 添加子账号接口
    # #
    def addSubaccount(self, accessToken, auth, businessId):
        server = self.controller.gateway
        path = self.paths["sub"]
        print("add subaccount")
        headers = {}
        times = self.controller.getTimeStamp()
        headers["Timestamp"] = times
        headers["Access-Token"] = accessToken
        headers["Authorization"] = "Bearer " + auth
        headers["businessId"] = businessId

        r = requests.post(server + path, headers = headers)
        json_obj = r.json() 
        print(json_obj)
        return json_obj

# print("default print")

# getCAPTCHA("13609615024")

# getLogin("13609615024","4283")

# # getRefreshedUserToken("13609615024","1974")

# print("time: " + login_time)
# print("access: " + login_access_token)
# print("auth: " + login_authorization)



# payload = getAccessToken()
# de_payload = con.decrypt(payload, aeskey, aesiv)
# js = json.loads(de_payload)
# refresh = js["refreshToken"]

# jsobj = getRefreshedToken(refresh)

# ref_payload = jsobj["payload"]
# de_ref = con.decrypt(ref_payload, aeskey, aesiv)
# jss = json.loads(de_ref)
# print(js)








