# coding=utf-8
# import urllib.request

# def getHtml(url):
#     page = urllib.request.urlopen(url)
#     html = page.read()
#     return html

# html = getHtml("https://appfigures.com/reports/featured")

# print(html)

# ------------------以上暂时无用





import datetime
import json
import os
import subprocess
import csv
import requests

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
        # logging.info('run_command:(%s) output:\n%s\n' % (command, output))
        # logging.info('run_command:(%s) error :\n%s\n' % (command, err))
        return (output, err)
    except Exception as  e:
        # logging.info('run_command exception: %s' % e)
        return False, False


s = requests.Session()
url_login = 'https://appfigures.com/login?redirect=/account/apps'


# 登录表单数据
formdata = {
    'email': 'chentingting@infolife.mobi',
    'pass': 'qwe123',
    'remember': 'on',
    'redirect': '/account/apps',
    'google_signin_token': ''
}

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

r = s.post(url_login, data=formdata, headers=headers)
aa = s.get('https://appfigures.com/reports/date')
print(aa.request.headers)

content = r.text

# print(content.encode('utf-8'))

with open('../../result.html', 'w', encoding='utf-8') as f:
    f.write(content)

data = ''

with open('../../result.html', 'r', encoding='utf-8') as f:
    for line in f:
        if 'afGlobalProducts' in line:
            data = line[line.index('{'): line.index(';')]

# print(data)
jasonData = json.loads(data)
storeIdDicta = {}
for i in range(6000000, 6100000):
    try:
        storeid = jasonData[str(i)]["storeid"]
        storeIdDicta[jasonData[str(i)]["pid"]] = storeid
        print(storeIdDicta[str(i)])
    except Exception as e:
        continue


command = '''
curl 'https://appfigures.com/handlers/APIProxy.ashx/featured/counts/?count=1&granularity=daily&show_empty=true' -H 'Cookie: G_ENABLED_IDPS=google; olfsk=olfsk9840821044566423; hblid=QwhriSVhG4aZgFWF6059Z0H00JE0RrGB; _af_session=u4avbcrdanl12reszkfooj35; _af_user_token=00032a235975589060c74e3ca93e70cd1366192e; _gat=1; wcsid=CPKpN7QNoI11deLb6059Z0H08K0JE4Ar; _okdetect=%7B%22token%22%3A%2215067372420570%22%2C%22proto%22%3A%22https%3A%22%2C%22host%22%3A%22appfigures.com%22%7D; _ga=GA1.2.788295812.1505383375; _gid=GA1.2.2015179853.1505627750; _oklv=1506737243116%2CCPKpN7QNoI11deLb6059Z0H08K0JE4Ar' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36' -H 'Accept: */*' -H 'Referer: https://appfigures.com/reports/featured' -H 'X-Requested-With: XMLHttpRequest' -H 'If-None-Match: "VoliyEbcvgoHMeEYAlWpLQ=="' -H 'Connection: keep-alive' -H 'X-ST: 9803eed5b41c42d5ab91f1f24e97be47' --compressed'''
result, _e = run_command(command)
products = json.loads(result)[0]["products"]
curl = '''curl 'https://appfigures.com/handlers/APIProxy.ashx/featured/full/{code}/2017-09-30/2017-09-30' -H 'Cookie: G_ENABLED_IDPS=google; _af_session=u4avbcrdanl12reszkfooj35; _af_user_token=00032a235975589060c74e3ca93e70cd1366192e; _okdetect=%7B%22token%22%3A%2215067372420570%22%2C%22proto%22%3A%22https%3A%22%2C%22host%22%3A%22appfigures.com%22%7D; olfsk=olfsk9840821044566423; _okbk=cd4%3Dtrue%2Cvi5%3D0%2Cvi4%3D1506737244143%2Cvi3%3Dactive%2Cvi2%3Dfalse%2Cvi1%3Dfalse%2Ccd8%3Dchat%2Ccd6%3D0%2Ccd5%3Daway%2Ccd3%3Dfalse%2Ccd2%3D0%2Ccd1%3D0%2C; _ok=2074-357-10-5006; wcsid=CPKpN7QNoI11deLb6059Z0H08K0JE4Ar; hblid=QwhriSVhG4aZgFWF6059Z0H00JE0RrGB; _ga=GA1.2.788295812.1505383375; _gid=GA1.2.2015179853.1505627750; _oklv=1506737303120%2CCPKpN7QNoI11deLb6059Z0H08K0JE4Ar' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36' -H 'Accept: */*' -H 'Referer: https://appfigures.com/reports/featured' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'X-ST: 9803eed5b41c42d5ab91f1f24e97be47' --compressed'''
# datetime.datetime.now().strftime("../../%Y-%m-%d-%H.json")
with open(datetime.datetime.now().strftime("../../%Y-%m-%d-%H.json"), 'w', encoding='utf-8') as f:
    i = 0
    f.write("{\"data\":[")
    for item in products:
        result, _e = run_command(curl.format(code=item["product_id"]))
        if result:
            f.write("{\"" + storeIdDicta[item["product_id"]] + "\":" + result.decode('utf-8')+"}")
            f.write(",")
            i = i + 1
            print("正在抓取第" + str(i) + "个...")
        else:
            print("抓取失败:" + str(storeIdDicta[item["product_id"]]) + "," + str(item["product_id"]))
    f.write("{\"a\":{}}")
    f.write("]}")
    
    path = datetime.datetime.now().strftime("../../%Y-%m-%d-%H.json")
    
json1 = json.loads(open(path, 'r', encoding='utf-8').read())

def loop_data(o, k=''):
    global json_ob, c_line
    if isinstance(o, dict):
        for key, value in o.items():
            # if (key == ''):
            loop_data(value, key)
            # else:
            #     loop_data(value, k + '.' + key)
    elif isinstance(o, list):
        for i, el in enumerate(o):
            loop_data(el)
    else:
        if not k in json_ob:
            json_ob[k] = {}
        json_ob[k][c_line] = o


def get_title_rows(json_ob):
    title = []
    row_num = 0
    rows = []
    # print(json_ob)
    for key in json_ob:
        title.append(key)
        v = json_ob[key]
        if len(v) > row_num:
            row_num = len(v)
        continue
    for i in range(row_num):
        row = {}
        for k in json_ob:
            v = json_ob[k]
            if i in v.keys():
                row[k] = v[i]
            else:
                row[k] = ''
        rows.append(row)

    return title, rows


def write_csv(title, rows, csv_file_name):
    with open(csv_file_name, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=title)
        writer.writeheader()
        writer.writerows(rows)


def json_to_csv(object_list):
    global json_ob, c_line
    json_ob = {}
    c_line = 0
    for ov in object_list:
        for o1 in ov:
            loop_data(o1, 'pkg')
            for o2 in ov.get(o1):
                loop_data(o2, 'mun')
                loop_data(ov.get(o1).get(o2))
                c_line += 1
                path1 = ''
                path1 = datetime.datetime.now().strftime("../../%Y-%m-%d-%H.csv")
            title, rows = get_title_rows(json_ob)
            write_csv(title, rows,datetime.datetime.now().strftime("../../%Y-%m-%d-%H.csv"))
            print('完成')


json_to_csv(json1['data'])

# import locale
#
# print(locale.getdefaultlocale())
#
# print('中国'.encode('cp936'))
#
# import sys
#
# sys.stdout.buffer.write('中国'.encode('utf8'))
#
# sys.stdout.buffer.write('♠'.encode('cp437'))
