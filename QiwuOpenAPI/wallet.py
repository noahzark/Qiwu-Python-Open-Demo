#
# @Author Siyang Zhang
# @Date Aug 23, 2019
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


class Wallet:

    def __init__(self, controller, paths):
        self.controller = controller
        self.paths = paths


    # 查询余额接口
    # #
    def getBalance(self, accessToken, auth):
        server = self.controller.gateway
        path = self.paths["base"]
        headers = {}
        headers["Timestamp"] = self.controller.getTimeStamp()
        headers["Access-Token"] = accessToken
        headers["Authorization"] = auth
        

        addr = server + path
        print(addr)
        r = requests.get(addr, headers = headers)
    
        json_obj = r.json()
        print(json_obj)
        return json_obj

    # 
    # 充值余额接口
    # #
    def chargeBalance(self, accessToken, auth, amount, paymentType, mode):
        server = self.controller.gateway
        path = self.paths["recharge"]
        print("charge balance")
        headers = {}
        headers["Timestamp"] = self.controller.getTimeStamp()
        headers["Access-Token"] = accessToken
        headers["Authorization"] = auth
        headers["Content-Type"] = "application/json"

        print("headers:")
        print(headers)
        params = {"amount" : str(amount), "paymentType" : str(paymentType), "mode" : mode}
        body = self.controller.getEncryptedParamsBody(params)
        # params_en = self.controller.getEncryptedParams(params)

        print(body)
        addr = server + path

        print(addr)
        r = requests.post(addr, headers = headers, data = body)
    
        json_obj = r.json()
        print(json_obj)
        return json_obj

