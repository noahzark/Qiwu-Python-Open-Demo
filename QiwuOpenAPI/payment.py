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

class Payment:

    def __init__(self, controller, paths):
        self.controller = controller
        self.paths = paths

    # APP支付接口
    # #
    def getPayment(self,accessToken, auth, orderId, paymentType):
        server = self.controller.gateway
        path = self.paths["pay"]
        headers = {}
        headers["Timestamp"] = self.controller.getTimeStamp()
        headers["Access-Token"] = accessToken
        headers["Authorization"] = auth
        
        params = {"orderId" : orderId, "paymentType" : paymentType}
        params_en = self.controller.getEncryptedParams(params)
        addr = server + path + "?q=" + params_en
        print(addr)
        r = requests.get(addr, headers = headers)
    
        json_obj = r.json()
        print(json_obj)
        return json_obj


    # 二维码支付接口
    # #
    def getPaymentQR(self,accessToken, auth, orderId, paymentType):
        server = self.controller.gateway
        path = self.paths["pay-by-qr"]
        headers = {}
        headers["Timestamp"] = self.controller.getTimeStamp()
        headers["Access-Token"] = accessToken
        headers["Authorization"] = auth

        
        params = {"orderId" : orderId, "paymentType" : paymentType}
        params_en = self.controller.getEncryptedParams(params)
        addr = server + path + "?q=" + params_en
        print(addr)
        r = requests.get(addr, headers = headers)
    
        json_obj = r.json()
        print(json_obj)
        return json_obj