import json
import datetime
import time
import traceback
import csv
import os
import requests
import subprocess

from getPkgName import getWidgetPkgNameArray
from getPkgName import getAmberPkgNameArray
KEY_FILE_NAME = 'pkgLanguageKey'

baseLanguageArray = ['EN-US', 'AR', 'ZH-HK', 'ZH-CN', 'ZH-TW', 'NL-NL', 'EN-AU', 'EN-IN', 'EN-CA', 'EN-GB', 'FR-FR', 'FR-CA', 'DE-DE', 'ID', 'IT-IT', 'JA-JP', 'KO-KR', 'MS', 'PL-PL', 'PT-BR', 'PT-PT', 'RO', 'RU-RU', 'ES-419', 'ES-ES', 'ES-US', 'TH', 'TR-TR', 'UK', 'VI']



#================语言抓抓抓


#代理
proxies = {
    "http": "http://127.0.0.1:8118",
    "https": "http://127.0.0.1:8118",
    # "http":"http://192.168.1.187:8118",
}


default_headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.8,en;q=0.6",
    "cache-control": "no-cache, no-store, max-age=0, must-revalidate",
    "content-type": "application/javascript; charset=UTF-8",
    "origin": "https://play.google.com",
    "pragma": "no-cache",
    "referer": "https://play.google.com/apps/publish/?dev_acc=06161861376464805340",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko)"
                  "Chrome/60.0.3112.90 Safari/537.36",
    "x-chrome-uma-enabled": "1",
    "x-client-data": "CK61yQEIj7bJAQimtskBCMS2yQEIqZ3KAQ==",
    "x-gwt-module-base": "https://ssl.gstatic.com/play-apps-publisher-rapid/fox/bc58dcff4606f3cef508f61a36070fb0/fox/gwt/",
    "x-gwt-permutation": "F65123E718D31FC0C8171F0098821A97",
}



cookie = {
    "_ga": "GA1.3-3.478732673.1498454345",
    "NID": "110=uc2RG7i02CjHDEZX4kbmSFS2mmkRe5Mjq-6u5Vago3qHMPy4s3z2h21vGhzVg-0zy6HEW7iIBYmPZm66HvtRHR_0WSerHOd9sgbnOR8vUQXV4ygBNv1cv-o-4kPwAHBMbTqSInTNHXJZDb0rDT43qpv-ci11P8cR8gB3eu-sVtkqSl4Z3KlZ4eP8en_TjCYAEODDCscJ9xemW2WKLJ_Dqfo1D9s",
    "SID": "DQUvvjQHKfnv3BAn5LUh4aSqQA9FrXae37YQT2D8KvetsE33PDwyZfPwtZ4McSd-d87nXg.",
    "HSID": "APPIOgNWeGT2-2atY",
    "SSID": "AUtclsGZnL40u9DjB",
    "APISID": "RE2ygbv_g7QMMbqa/AUZb-ikSpiQUjWVt8",
    "SAPISID": "DVHaMfBzmroa_8A5/AhNVTzI1lPFWKe4J5"
}

# 连接
def connect_gp(url, default_headers, body):

    json_body = json.dumps(body)
    r = requests.post(url, headers=default_headers, cookies=cookie, data=json_body, proxies=proxies, timeout=60, verify=False)
    res = r.json()
    return res

# 拿数据
def get_data(dev_acc, default_headers, body):
    url = "https://play.google.com/apps/publish/androidapps?dev_acc={dev_acc}".format(dev_acc=dev_acc)
    data = connect_gp(url, default_headers, body)
    return data


# 执行shell命令
def run_command(command):
    try:
        p = subprocess.Popen(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE,
                             shell=True, env=os.environ)
        # print(command)
        (output, err) = p.communicate()
        # print((output,err))
        #logging.info('run_command:(%s) output:\n%s\n' % (command, output))
        #logging.info('run_command:(%s) error :\n%s\n' % (command, err))
        return (output, err)
    except Exception as  e:
        #logging.info('run_command exception: %s' % e)
        return False , False


count = 0

# 向文件末尾追加amber包的语言比对信息
def appendAmberPkgLanguageInfo():
    pkgNameArray = getAmberPkgNameArray()
    com1 = r'''curl 'https://play.google.com/apps/publish/androidapps?dev_acc=01419791378100621000' -H 'origin: https://play.google.com' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: zh-CN,zh;q=0.8,en;q=0.6' -H 'x-gwt-permutation: F65123E718D31FC0C8171F0098821A97' -H 'x-gwt-module-base: https://ssl.gstatic.com/play-apps-publisher-rapid/fox/bc58dcff4606f3cef508f61a36070fb0/fox/gwt/' -H 'cookie: _ga=GA1.3-3.478732673.1498454345; _gid=GA1.3-3.1965325179.1502864164; CONSENT=YES+CN.zh-CN+20170604-09-0; SID=DQUvvjQHKfnv3BAn5LUh4aSqQA9FrXae37YQT2D8KvetsE33PDwyZfPwtZ4McSd-d87nXg.; HSID=APPIOgNWeGT2-2atY; SSID=AUtclsGZnL40u9DjB; APISID=RE2ygbv_g7QMMbqa/AUZb-ikSpiQUjWVt8; SAPISID=DVHaMfBzmroa_8A5/AhNVTzI1lPFWKe4J5; _ga=GA1.3.478732673.1498454345; _gid=GA1.3.1965325179.1502864164; NID=110=qy4vav8m6HY28fn41AHu42kXpqE14zyzGUmZqjoiK5Gs-T9NL388I1SApIO1M-DBMur56og1twxQeojgZojWwKYGHbvWTUOchoBz9FwNwyWUAXpUWO2NtmZ-uCufRiBrqObFxf1I26WFJmh1nL_GNQZzrT0tCGBwqld0zkoQm_ur3Sicy209EqFH5bfIeFsE7RhcJSHcVWdJjtZKGPNixpNf5pY; enabledapps.uploader=0; SIDCC=AA248bdYBpkcMhyFDF5mSWFAzKoxFEumG3CgD3usMuz9dDfTz0gG3ZwGqt4-Z0EVFkTRe-Oe0yJvJD617elbvw' -H 'x-client-data: CK61yQEIj7bJAQimtskBCMS2yQEIqZ3KAQ==' -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36' -H 'content-type: application/javascript; charset=UTF-8' -H 'accept: */*' -H 'referer: https://play.google.com/apps/publish/?dev_acc=01419791378100621000' -H 'authority: play.google.com' --data-binary '{"method":"fetch","params":"{\"1\":[\"'''
    com2 = r'''\"],\"3\":0}","xsrf":"AMtNNDHtrb9Zk3mfqSNLkWZ7ORxw1mwgBA:1502943730284"}' --compressed'''
    with open('result.csv', 'a') as f: #追加模式打开
        for pn in pkgNameArray:
            result,_ = run_command(com1 + pn + com2)

            global count
            print(count)
            count = count +1
            print(pn)

            result = json.loads(result.decode('utf-8'))
            f.write(result.get('result').get('1')[0].get('1').get('1') + ',')
            lackArray = baseLanguageArray.copy()
            # 对比语言，多出来的和少了的
            resList = result.get('result').get('1')[0].get('1').get('2').get('1')
            extra = ''
            lack = ''
            for item in resList:
                language = item.get('1').upper()
                if item.get('7'):# 如果有7這个属性表示這是已经翻译的语言
                    if language not in baseLanguageArray:
                        extra = extra + ' | ' + language
                    if language in lackArray:
                        lackArray.remove(language)
            extra = extra[3:]
            for language in lackArray:
                lack = lack + ' | ' + language
            lack = lack[3:]
            f.write(extra + ',' + lack + '\n')


def my_request(body):
    try:
        return get_data('06161861376464805340', default_headers, body)
    except Exception as e:
        return my_request(body)

# 向文件写入widget语言比对信息
def writeWidgetPkgLanguageInfo():


    pkgNameArray = getWidgetPkgNameArray()

    #从文件里取KEY
    xsrfKey = ''
    with open(KEY_FILE_NAME, 'r') as f:
        xsrfKey = f.read()
    
    #每一个请求的body叠在一起的数组
    body_array = []
    for pkgName in pkgNameArray:
        body = {"method": "fetch",
                "params": {"1": [pkgName],
                            "3": 0},
                "xsrf": xsrfKey}
        body_array.append(body)
    
    with open('result.csv', 'w') as f:
        f.write('PkgName' + ',' + 'Extra' + ',' + 'Lack' + '\n')
        for body in body_array:

            global count
            print(count)
            count = count + 1
            print(body.get('params').get('1')[0])
            result = my_request(body)

            # 写第一列的包名
            f.write(result.get('result').get('1')[0].get('1').get('1') + ',')
            lackArray = baseLanguageArray.copy()
            # 写入新key
            # xsrfKey = result.get('xsrf')
            # with open(KEY_FILE_NAME, 'w') as f_key:
            #     f_key.write(xsrfKey)
            # 拿数据  TODO：对比语言，多出来的和少了的
            resList = result.get('result').get('1')[0].get('1').get('2').get('1')
            extra = ''
            lack = ''
            for item in resList:
                language = item.get('1').upper()
                if item.get('7'):# 如果有7這个属性表示這是已经翻译的语言
                    if language not in baseLanguageArray:
                        extra = extra + ' | ' + language
                    if language in lackArray:
                        lackArray.remove(language)
            extra = extra[3:]
            for language in lackArray:
                lack = lack + ' | ' + language
            lack = lack[3:]
            f.write(extra + ',' + lack + '\n')
    
# 写widget包信息
writeWidgetPkgLanguageInfo()
# 追加amber包信息
appendAmberPkgLanguageInfo()
# print('\n+++++-----=====-----+++++=====-----+++++=====-----+++++=====')
# print('\n+++++-----=====-----+++++=====-----+++++=====-----+++++=====')
# print('\n+++++-----=====-----+++++=====-----+++++=====-----+++++=====')
