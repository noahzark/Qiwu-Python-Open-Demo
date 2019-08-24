#
# @Author Siyang Zhang
# @Date Aug 21, 2019
# 
# 
# 
# Helper functions:
# encode, decode, encrypt, decrypt, etc...
# 
# 
# 
# 
# 
# 
# #

import time
import hashlib
import Cryptodome
import base64
import json
from Cryptodome.Cipher import AES

# BS = 16
# pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
# appchannel = "feli-tech-test"
# aeskey = "NY8iA0QYXVgsje5pcDiaUOwKsCSjEWlfGlXxJ/9KikY="
# aesiv="5a2wShLw7EWa8Fiw+cWYcQ=="

class Controller:

    # 
    # 构造函数，
    # #
    def __init__(self, appchannel, aeskey, aesiv, gateway):
        self.appchannel = appchannel
        self.aeskey = aeskey
        self.aesiv = aesiv
        self.gateway = gateway


    # 
    # 获取签名
    # #
    def getFillSignParams(self, appChannel, privateKey):
        requestParams = {"App-Channel": appChannel,
                        "Timestamp" : self.getTimeStamp()  
        }
        # print(requestParams["Timestamp"])
        sortedParams = self.getSortedParams(requestParams)
        paramsStrToEncrypt = sortedParams + privateKey

        m = hashlib.sha1()
        encodedString = paramsStrToEncrypt.encode(encoding='utf-8')
        m.update(encodedString)
        hashtext = m.hexdigest()

        requestParams["Sign"] = hashtext

        return requestParams

    # 
    # 获取时间戳
    # #
    def getTimeStamp(self):
        return str(int(round(time.time() * 1000))) 

    def getSortedParams(self, requestParams):
        if requestParams == None or len(requestParams) == 0:
            return ""
        else:
            res = ""
            for key in sorted(requestParams.keys()):
                res += "&" + key + "=" + requestParams[key]

            res = res[1:]
            return res

    # 
    # AES加密前补位
    # #
    def add_to_16(self, text):
        if len(text.encode('utf-8')) % 16:
            add = 16 - (len(text.encode('utf-8')) % 16)
        else:
            add = 0

        text = text + ('\0' * add)
        return text


    # 
    # AES_CBC PKCS5Padding加密
    # #
    def encrypt(self, text):
        aeskey = self.aeskey
        aesiv = self.aesiv
        BS = 16
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)  

        mode = AES.MODE_CBC


        text = pad(text)
        text = text.encode()


        aeskey = base64.b64decode(aeskey)
        aesiv = base64.b64decode(aesiv)

        cryptos = AES.new(aeskey,mode,aesiv)
        
        cipher_text = cryptos.encrypt(text)
        
        res = base64.b64encode(cipher_text)

        return res



    # 
    # AES_CBC PKCS5Padding解密
    # #
    def decrypt(self, text):
        aeskey = self.aeskey
        aesiv = self.aesiv
        # BS = 16
        # pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

        mode = AES.MODE_CBC
        
        # text = pad(text)
        text = base64.b64decode(text)
        aeskey = base64.b64decode(aeskey)
        aesiv = base64.b64decode(aesiv)

        cryptos = AES.new(aeskey, mode, aesiv)
        de = cryptos.decrypt(text) 

        # de = str(de,'utf-8')
        res = str(de, 'utf-8')
        # print("decrypt")
        # print(res)
        i = 1




        if("}" not in res):
            return res

        while i < len(res):
            # print(res[-i])
            if res[-i] != '}':
                i += 1
            else:
                break
        i -= 1


        return res[:-i]



    def toJSONstr(self, js):
        s = json.dumps(js)
        s = s.replace(",",",\n ")
        s = s.replace("}","\n}")
        s = s.replace("{","{\n ")
        return s


    # 
    # 加密参数
    # #
    def getEncryptedParams(self, params):
        res = ""
        for key in params:
            res += "&"+str(key)+"="+str(params[key])

        res = res[1:]
        print("res = " + res)
        # print(aeskey,aesiv)
        res = self.encrypt(res)
        res = str(res)
        res = res[2:len(res)-1]
        res = res.replace("+","%2B")
    
        return res
    # 
    # 加密参数body
    # #
    def getEncryptedParamsBody(self, params):
        body_str = json.dumps(params)
        body_str = body_str.replace(' ','')
        body_en = self.encrypt(body_str)
        body_en_str = str(body_en)
        res = body_en_str[2:len(body_en_str)-1]
        return res





privatekey = "1c9f03b3-c920-4d68-b2cd-299a28557890"
payload = "KoXy1gC9/yvcK5wvWviErJfMQ3cVdqTa1Z96MCikrw69iReSDlwg1pw3MM4wtoVThg+dtc5/ydmqaLdXvVxZwXIYtrGDMT+1/FYAewqo3vNoPbvSdSAms/p8MI550RPd6+FzDDUbNXWPLFjjTcwhGOtxg7Jaz1mKlbCeyabJ/W4kAM/pICPgxpLG37IYGViBUWu5RRWEkcUjr6g7ReRVhHvd44OlLnxEkm48dACdD735DnZ2IaRsWJ2b36JxLwes"


key="7psGzvtQh4OooXtmRK7G36oYwYobHGyDDQ81DTfV1KE=" 
iv="5a2wShLw7EWa8Fiw+cWYcQ=="

raw = "hello=1&world=2"

rawde = "xGeToqBGYADr8/KQomlNNg=="

# params = {"hello" : 1, "world" : 2}
# body = getEncryptedParamsBody(params)
# body = '{"hello":1,"world":2}'
# body_en = encrypt(body, key, iv)

# body = getEncryptedParamsBody(params)
# print(body)
# params = {"a" : 1, "bc" : 2, "asdasd" : 114}
# s = "a=1&bc=2&asdasd=114"
# s = encrypt(s,aeskey, aesiv)
# s = str(s)
# s = s[2:len(s)-1]
# print(getEncryptedParams(params))
# print(s)
# print("controller")

# en = encrypt(raw, key, iv)
# de = decrypt(rawde, key, iv)
# dee = decrypt(payload, aeskey, aesiv)
# dee = str(dee)[2:]
# print(en)
# print(de)
# print(dee)
# print(base64.b64encode(rawde))
# de = decrypt(str(en), aeskey, aesiv)

# rawde = "xGeToqBGYADr8/KQomlNNg=="

# print(decrypt(rawde, key, iv))

# s = "13609615024"
# sb = bytes(s,'utf-8')
# print(base64.b64encode(sb))

