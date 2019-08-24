#
# @Author Siyang Zhang
# @Date Aug 22, 2019
# 
# 
# #

import controller as con
import general as gen
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

# login_access_token = ""
# login_auth = ""
# login_time = 0


class Order:

    def __init__(self, controller, paths):
        self.controller = controller
        self.paths = paths
        

    # 
    # 获取订单详情接口
    # #
    def getOrder(self, accessToken, auth, orderId):
        print("get order")
        server = self.controller.gateway
        path = self.paths["order"]
        print(server)
        headers = {}
        headers["Timestamp"] = self.controller.getTimeStamp()
        headers["Access-Token"] = accessToken
        headers["Authorization"] = auth 

        # headers["orderId"] = orderId 
        orderId = "orderId=" + orderId

        print("headers: ")


        orderId_en = str(self.controller.encrypt(orderId))
        print(orderId_en)
        orderId_en = orderId_en[2:len(orderId_en)-1]
        print(orderId_en)
        
        r = requests.get(server + path + "?q="+orderId_en, headers = headers)
        json_obj = r.json() 
        print(json_obj)
        return json_obj


    # 
    # 获取订单列表接口
    # #
    def getOrderList(self, accessToken, auth, state = 0, lastId = "", pageSize = "", orderType = ""):
        print("get order list")
        server = self.controller.gateway
        path = self.paths["order"]
        headers = {}
        headers["Timestamp"] = self.controller.getTimeStamp()
        headers["Access-Token"] = accessToken
        headers["Authorization"] = auth 

        params = {}
        params["state"] = str(state)
        params["lastId"] = str(lastId)
        params["pageSize"] = str(pageSize)
        params["orderType"] = str(orderType)

        params_str = self.controller.getEncryptedParams(params)
        r = requests.get(server+ path + "?q="+params_str, headers = headers)
        json_obj = r.json() 
        # py = json_obj["payload"]
        # de_py = self.controllerdecrypt(py, aeskey, aesiv)
        print(json_obj)

        return json_obj


    # 
    # 取消订单接口
    # #
    def cancelOrder(self, accessToken, auth, orderId):
        print("cancel order")
        server = self.controller.gateway
        path = self.paths["order"]
        headers = {}
        headers["Timestamp"] = self.controller.getTimeStamp()
        headers["Access-Token"] = accessToken
        headers["Authorization"] = auth 

        # headers["orderId"] = orderId 
        orderId = "orderId=" + orderId

        print("headers: ")


        orderId_en = str(self.controller.encrypt(orderId))
        print(orderId_en)
        orderId_en = orderId_en[2:len(orderId_en)-1]
        print(orderId_en)
        addr = server + path + "?q="+orderId_en
        print(addr)
        r = requests.delete(addr, headers = headers)
        json_obj = r.json() 
        print(json_obj)
        return json_obj

# gen.default()

# print(login_time)