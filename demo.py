#
# @Author Siyang Zhang
# @Date Aug 20, 2019
# 
# 
# #


import json
import urllib3
import requests
import time
import hashlib
import urllib
import uuid
import socket
import wave
from urllib import request
from requests_toolbelt.multipart import MultipartEncoder




server = 'https://robot-service.centaurstech.com/'
appkey = 'qiwurobot'
appsecret = '123456'
nickname = '野獣先輩田所浩二'



def getChatResponse(ask):
    now = int(round(time.time() * 1000))
    uid = getUID("mac")
    verify = digest(appsecret + str(uid) + str(now))

    requestParams = {
        "appkey":appkey,
        "timestamp":now,
        "uid":uid,
        "verify":verify,
        "msg":ask,
        "nickname":nickname
    }

    headers = {"content-type":"application/x-www-form-urlencoded"}

    r = requests.post(server+"api/chat", headers = headers, data = requestParams)
    
    json_obj = r.json()


    if "data" in json_obj:
        print("Append data: " + str(json_obj["data"]))
    else:
        print("There is no extra data")
        s = str(json_obj)
        s = s.replace(', ',', \n ')
        print(s)

    res = json_obj["msg"]
    print(res)

    return res








def getGeoResponse(ask, lng = None, lat = None):

    now = int(round(time.time() * 1000))
    uid = getUID("mac")
    verify = digest(appsecret + str(uid) + str(now))


    requestParams = {
        'appkey':appkey,
        'timestamp':now,
        'uid':uid,
        'verify':verify,
        'msg':ask,
        'nickname':nickname,
        "geo[lng]":lng,
        "geo[lat]":lat
    }

    headers = {"content-type":"application/x-www-form-urlencoded",
               "cache-control":"no-cache"
    }

    r = requests.post(url=server+'api/chat/geo', data=requestParams, headers=headers)
    json_obj = r.json()

    if(lng != None and lat != None):
        if json_obj["retcode"] == 0:
            print("Success")
        else:
            print("Fail")

        s = str(json_obj)
        s = s.replace(', ',', \n ')
        print(s)

    else:
        print("Missing longitude or latitude")
    
    res = json_obj["msg"]
    print(res)
    return res








def getOctetSpeechResponse(file):

    codec = file.split('.')[1]
    now = int(round(time.time() * 1000))
    uid = getUID("mac")
    verify = digest(appsecret + str(uid) + str(now))

    audio = open(file, 'rb')

    data = {"speech" : audio}

    headers = {"content-type":"application/octet-stream"}

    addr = server+'api/speech/chat?' + "appkey=" + appkey + "&timestamp=" + str(now) + "&uid=" + str(uid) + "&verify=" + verify + "&codec=" + codec + "&rate=8000" + "&nickname=" + nickname

    print(addr)
    print(data)

    r = requests.post(url=addr, headers=headers, data=audio)
    
    json_obj = r.json()


    if json_obj["retcode"] == 0:
        print("Success")
    else:
        print("Fail")
        res = json_obj["msg"]
        print(res)


    s = str(json_obj)
    s = s.replace(', ',', \n ')
    print(s)

    return s







def getMultipartSpeechResponse(file):

    now = int(round(time.time() * 1000))
    uid = getUID("mac")
    verify = digest(appsecret + str(uid) + str(now))
    codec = file.split('.')[1]

    addr = server+'api/speech/chat?' + "appkey=" + appkey + "&timestamp=" + str(now) + "&uid=" + str(uid) + "&verify=" + verify + "&codec=" + codec + "&rate=8000" + "&nickname=" + nickname

    print(addr)

    files = open(file, 'rb')
    m = MultipartEncoder({'speech':(file,files)})
    headers = {"content-type":m.content_type}
    print(m.content_type)
    r = requests.post(url=addr, headers=headers, data = m)

    json_obj = r.json()

    print(json_obj)

    if 0 == json_obj["retcode"] :
        print("Success")
    else:
        print("Fail")
        res = json_obj["msg"]
        print(res)


    s = str(json_obj)
    s = s.replace(', ',', \n ')
    print(s)

    return s






#---helpers--------------------------------------------------------------


def digest(plaintext):

    m = hashlib.md5()
    encodedString = plaintext.encode(encoding='utf-8')
    m.update(encodedString)
    hashtext = m.hexdigest()

    while len(hashtext) < 32:
        hashtext = "0" + hashtext
    
    return hashtext







def getUID(addressType):
    if addressType == "mac":
        return get_mac_address()
    elif addressType == "ip":
        return get_ip_address
    else:
        raise Exception('Specify \"ip\" or \"mac\"')






def get_mac_address(): 
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:] 
    s = ":".join([mac[e:e+2] for e in range(0,11,2)])
    s = s.replace(':','-')
    return s






def get_ip_address():
    hostName = socket.getfqdn(socket.gethostname())
    ip = socket.gethostbyname(hostName)
    return ip




#--- main -------------------------------------------------------------------------------
    
print("mac: " + get_mac_address())
print("ip: " + get_ip_address())


# msg = getChatResponse("HELLO")
# msg = getGeoResponse("HELLO")

# msg = getOctetSpeechResponse('qingfenfu.amr')
# msg = getMultipartSpeechResponse('qingfenfu.amr')









