from django.http import HttpResponse
import datetime
import urllib3
import json
def hello(request):

    return HttpResponse("Hello world")

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def get_cmdate(request):
    http = urllib3.PoolManager()
    Date = []
    for offset in range(0, 50, 15):
        url = "http://locker.cmcm.com/theme/recomm?cnl=locker&cv=47071779&lang=zh_cn&mcc=&pagenum=15&offset={offset}&minwidth=1080&sysver=22&memory=1795&inclocal=1".format(offset=offset)
        res = http.urlopen('GET', url)
        res = str(res.data)
        request = res[2:len(res) - 3]
        request = json.loads(request)
        if request.get('data').get('offset') == -1:
            break
        else:
            Date.append(request.get('data').get('items'))
            # print(Date)
        offset += 15
    data = ''
    print(Date)
    for items in Date:
        for item in items:
            url = item.get('images')[0].get('url')
            data += "downloads: " + str(item.get('downolads')) + "  包名：" + item.get('package_name') + "<br>" +"<img src='{url}' width = \"72px\" height = \"128px\"/><br><br>".format(url = url)
    html = "<html><body><span>%s</span></body></html>" % data
    return HttpResponse(html)