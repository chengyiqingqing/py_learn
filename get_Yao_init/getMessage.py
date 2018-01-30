import json
import datetime
import time
import traceback
import csv
import requests
import os.path
package_name=[]
with open('package.txt','r') as file:
    for line in file:
        package_name.append(line.split('\n')[0])
print(package_name)
body_array = []
for body_name in package_name:
    body = {"method": "fetchStats",
            "params": {"1": [
                {"1": {"1": body_name, "2": 1}, "2": -182, "3": -1,
                 "7": [17],
                "8": [56, 57, 58, 59, 60, 15, 16],
                "12": 2,
                "15": 1,
                "17": "FOX_RATINGS"}]},
            "xsrf": "AMtNNDEUbg5eg9r5yX3S0S4-S0YZDkYL-A:1502443362818"}
    body_array.append(body)
print(body_array)
proxies = {
    "http": "http://127.0.0.1:1080",
    "https": "http://127.0.0.1:1080",
    "http":"http://192.168.1.187:8118",
}
default_headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.8",
    "cache-control": "no-cache, no-store, max-age=0, must-revalidate",
    "content-type": "application/javascript; charset=UTF-8",
    "origin": "https://play.google.com",
    "pragma": "no-cache",
    "referer": "https://play.google.com/apps/publish/?dev_acc=06161861376464805340",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko)"
                  "Chrome/60.0.3112.90 Safari/537.36",
    "x-chrome-uma-enabled": "1",
    "x-client-data": "CKa1yQEIhbbJAQiktskBCMG2yQEIi5jKAQj7nMoBCKmdygEIoqLKAQ==",
    "x-gwt-module-base": "https://ssl.gstatic.com/play-apps-publisher-rapid/fox/335ae41eb7388144e7594bb55fce5a31/fox/gwt/",
    "x-gwt-permutation": "4D9A53C0606A8F99A937CC2C9DFC0F2D",
}
cookie = {
    "_ga": "GA1.3-3.1829808074.1490606941",
    "NID": "109=tnXCRFvuE0yOrrz2mzId-cC2X-qDn0eGLXovzHU46hp-UlA03fZ1GJRV9cHw--Glzig7FTDRYXQgMs7-6wVipPhp6ShLMlwrzH-Msou2HMmcjNfQY90XYPcl-3NyB43fH4x3zYVZ5e-y-K1ax9gAdx1K4Ze3KMgUUyzvJgZLlhayVYFwtOohaV61PhCUoc1k0objbExr18NeecKUCLkF-j1IKoVqRx74uOIB952YKA1iZo9Bx_MMtRHbMw",
    "SID": "BgUvvp5mNQOoyOJUzDBbw3ZMtq9Izq0Yw7n-vNAL7cS_-0Spjs5tt7PNsi8AWiDdWRB83Q.",
    "HSID": "AqZp59sIz71tqmSOx",
    "SSID": "ABeVHmO81jWUvJ8_K",
    "APISID": "T2IN-emnkXcCHAyA/AJFty2Y3nPG-HkKOe",
    "SAPISID": "KUBt3MYdos8NGI2V/AtQPUgFja8Tq3THri"
}
# url = "https://play.google.com/apps/publish/statistics?dev_acc={dev_acc}".format(dev_acc = dev_acc)
# def get_package(dev_acc, default_headers):
#     url = "https://play.google.com/apps/publish/androidapps?dev_acc={dev_acc}".format(dev_acc=dev_acc)
#     body = {"method": "fetchIndex",
#             "parmas": "{}",
#             "xsrf:": "AMtNNDGVR5K-53Me3560pJT9kSyGwfjUjg:1502418468353"
#            }
#
#     data = connect_GP(url, default_headers, body)
#     print(data)
#     package_data = []
#     package_name = data.get('result').get('1')
#     i = 0
#     for v in range(len(package_name)):
#         name = package_name[v].get('2')
#         if 'mobi' in name:
#             package_data[i] = name
#             i += 1
#         else:
#             continue
#     return package_data
#
def connect_gp(url, default_headers, body):
    json_body = json.dumps(body)
    r = requests.post(url, headers=default_headers, cookies=cookie, data=json_body, proxies=proxies, timeout=60, verify=False)
    res = r.json()
    _xsrf = res.get("xsrf", None)
    return res
def get_data(dev_acc, default_headers, body):
    url = "https://play.google.com/apps/publish/statistics?dev_acc={dev_acc}".format(dev_acc=dev_acc)
    data = connect_gp(url, default_headers, body)
    return data
    # for v in range(len(data)):
    #     time = data[v].get('1')[0]
    #     every_week_avg_rank = data[v].get('2')[5].get('2')
    #     totally_week_avg_rank = data[v].get('2')[6].get('2')
    #     a = {'时间': time, '每周平均评分': every_week_avg_rank, '累计平均评分': totally_week_avg_rank}
    #     rows.append(a)
    # head = ['时间', '每周平均评分', '累计平均评分']
    # with open('demo.csv', 'w') as file:
    #     file_csv = csv.DictWriter(file, head)
    #     file_csv.writeheader()
    #     file_csv.writerows(rows)
    #     print(time + " " + every_week_avg_rank + "  " + totally_week_avg_rank)
with open('demo.csv', 'w') as file:
    j= 0
    for v in body_array:
        data = get_data('06161861376464805340', default_headers, v).get("result").get("1")[0].get("1")
        name = package_name[j]
        j = j + 1
        rows = []
        time_row=[]
        every_row=[]
        totally_row=[]
        for i in range(len(data)):
            time = data[i].get('1')[0]
            every_week_avg_rank = data[i].get('2')[5].get('2')
            totally_week_avg_rank = data[i].get('2')[6].get('2')
            time_row.append(time)
            every_row.append(str(every_week_avg_rank))
            totally_row.append(str(totally_week_avg_rank))
        
        # rows.append(a)
        file.write(name + '\n')
        file.write('\n')
        file.write('time' + ',')
        for line in time_row:
            file.write(line + ',')
        file.write('\n' + 'every_week' + ',')
        for line in every_row:
            file.write(line + ',')
        file.write('\n' + 'week' + ',')
        for line in totally_row:
            file.write(line + ',')
        file.write('\n')
        file.write('\n')
#ok
# def parse_cookies(cookie_text):
#     cookies = {}
#     items = cookie_text.split(";")
#     for item in items:
#         key, value = item.split("=", 1)
#         key = key.strip()
#         value = value.strip()
#         cookies[key] = value
#     return cookies
# def package():
#     url = "https://play.google.com/apps/publish/androidapps?dev_acc=06161861376464805340"
#     default_headers = {
#         "accept": "*/*",
#         "accept-encoding": "gzip, deflate, br",
#         "accept-language": "zh-CN,zh;q=0.8",
#         "cache-control": "no-cache, no-store, max-age=0, must-revalidate",
#         "content-type": "application/javascript; charset=UTF-8",
#         "origin": "https://play.google.com",
#         "pragma": "no-cache",
#         "referer": "https://play.google.com/apps/publish/?dev_acc=06161861376464805340",
#         "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
#         "x-chrome-uma-enabled": "1",
#         "x-client-data": "CKa1yQEIhbbJAQiktskBCMG2yQEIi5jKAQj7nMoBCKmdygEIoqLKAQ==",
#         "x-gwt-module-base": "https://ssl.gstatic.com/play-apps-publisher-rapid/fox/335ae41eb7388144e7594bb55fce5a31/fox/gwt/",
#         "x-gwt-permutation": "4D9A53C0606A8F99A937CC2C9DFC0F2D",
#     }
#     cookie = parse_cookies("_gat=1; _ga=GA1.3-3.1829808074.1490606941; _gid=GA1.3-3.714203743.1502258747; __utma=1.1829808074.1490606941.1490606941.1490606941.1; __utmz=1.1490606941.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); SID=BgUvvp5mNQOoyOJUzDBbw3ZMtq9Izq0Yw7n-vNAL7cS_-0Spjs5tt7PNsi8AWiDdWRB83Q.; HSID=AqZp59sIz71tqmSOx; SSID=ABeVHmO81jWUvJ8_K; APISID=T2IN-emnkXcCHAyA/AJFty2Y3nPG-HkKOe; SAPISID=KUBt3MYdos8NGI2V/AtQPUgFja8Tq3THri; NID=109=OfoPEeESEuAozgKBBgW4iA4zV-6KWxyZNUI3BqeAhPA_xFeve7UM-oJjGNZ1h8-LZXNAvQz_qWixAI-JeJg-L0DxdGsMaNdz2NW1wySQgwPw6a-D7fd9t6UpkN-EnUcWMpKCPzssnCxjWUhF9wZxr8oA4x9RplQSkMy8I4m874sF56nUZbFrhhQEEbX8HTPQVd1EIzVEWaihusJC2UvkmQJlZmGLAoXB2H0TvROOR_8OiLlGLl2-SAihlw; enabledapps.uploader=0; SIDCC=AA248bdijwOBEnAnaOA2ErnMl2de4c1R7LxFNPH6zAmr0fmlZ6P-na092JsuhoJbZZ8s5idSwaqq9sCYn-hd9Q")
#     print(cookie)
#     body = {"method": "fetchIndex",
#             "parmas": "{}",
#             "xsrf:": "AMtNNDFcwI2sKXGDnkH6dOiB9WqCGebpAQ:1502431283044"}
#     json_body = json.dumps(body)
#     # # r = requests.post(url, headers=default_headers, cookies=cookie, data=json_body, proxies=None, timeout=60, verify=False)
#     #
#     # res = r.json()
#     # print(res)
#     # return res
#
# get_data('06161861376464805340',default_headers,body)