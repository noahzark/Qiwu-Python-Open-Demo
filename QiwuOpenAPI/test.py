#
# @Author Siyang Zhang
# @Date Aug 23, 2019
# 
# 
# #

import controller as con
import general as gen
import payment as pay
import wallet as wal
import json
import order
import yaml






with open('accountInfo.yaml','r') as f1:
    accountInfo = yaml.load(f1, Loader = yaml.FullLoader)

with open('globals.yaml', 'r') as f2:
    globalInfo = yaml.load(f2, Loader = yaml.FullLoader)
print("account:")
print(accountInfo)

print("\nglobal:")
print(globalInfo)

paths = globalInfo["paths"]




appchannel = globalInfo["appchannel"]
aeskey = globalInfo["aesKey"]
aesiv = globalInfo["aesIv"]
privatekey = globalInfo["privateKey"]
server = globalInfo["base"]
phoneNumber = str(accountInfo["phoneNumber"])
captcha = str(accountInfo["captcha"])
orderId = accountInfo["orderId"]



class Tester:

    def __init__(self, controller, phoneNumber, captcha, orderId, appchannel, privatekey, paths):
        self.controller = controller
        self.general = gen.General(controller, appchannel, privatekey, paths)
        self.order = order.Order(controller, paths)
        self.payment = pay.Payment(controller, paths)
        self.wallet = wal.Wallet(controller, paths)
        self.phoneNumber = phoneNumber
        self.captcha = captcha
        self.orderId = orderId


    def foo(self, x, y):
        print("tester foo " + y + x)

    def call_API(self, API_function, params):
        login_json_obj = self.general.getLogin(self.phoneNumber, self.captcha)
        accessToken = login_json_obj["accessToken"]
        authorization = login_json_obj["Authorization"]
        
        newparams = {}
        newparams["accessToken"] = accessToken
        newparams["auth"] = authorization
        for key in params:
            if key != "self":
                newparams[key] = params[key]
        
        print("newparams are:")
        print(newparams)
        # try:
        response_json = API_function(**newparams)

        if "payload" in response_json:
            print("Success")
            print("payload:")
            payload_en = response_json["payload"]
            payload_de = self.controller.decrypt(payload_en)
            print(payload_de)
        else:
            print("Fail")
            print(response_json)
        # except:
        #     print("Please give correct input parameters.")




def testAPI():
    controller = con.Controller(appchannel,aeskey,aesiv, server)
    tester = Tester(controller, phoneNumber, captcha, orderId, appchannel, privatekey, paths)

    params = {"self":tester.wallet, "amount":0.01, "paymentType":"WECHAT_PAY", "mode":"APP"}
    tester.call_API(tester.wallet.chargeBalance,params)
    
    return


testAPI()





