#! /usr/bin/env python
# -*- coding:utf-8 -*-


mysql_config = {
    "host": "127.0.0.1",
    "user": "user",
    "passwd": "password",
    "dbname": "db"
}
clean_sql_file = False
table_name = "gp_developer_rank"
event_table_name = "gp_search_event_test"
result_data_tb = "gp_developer_rank"
keyword_score_tb = "gp_keyword_score"

mail_auth = {
    'smtp_server_host': 'mail.amberweather.com',
    'smtp_server_port': '25',
    'user': 'python',
    'password': 'python&mail',
    'sender': 'root@mail.amberweather.com'
}

mail_list = [
    "louxiao@amberweather.com"
]

proxy_list = {
    "https": "socks5://127.0.0.1:1080",
    "http": "socks5://127.0.0.1:1080",
}
proxies_config = {
    "us": {
        "https": "http://127.0.0.1:8118",
        "http": "http://127.0.0.1:8118",
    },
    "ru": {
        "https": "http://127.0.0.1:8118",
        "http": "http://127.0.0.1:8118",
    },
    "in": {
        "https": "http://127.0.0.1:8118",
        "http": "http://127.0.0.1:8118",
    },
    "kr": {
        "https": "http://127.0.0.1:8118",
        "http": "http://127.0.0.1:8118",
    },
    "de": None,
}
search_check_limit = 20

search_list = [
    {
        "keyword": "best android widget",
        "lang": "en-US",
        "country": "us"
    },
    {
        "keyword": "weather widget",
        "lang": "en-US",
        "country": "us"
    },
    {
        "keyword": "best android widget",
        "lang": "en-IN",
        "country": "in"
    },
    {
        "keyword": "weather widget",
        "lang": "en-IN",
        "country": "in"
    },
    {
        "keyword": "Погода",
        "lang": "ru-RU",
        "country": "ru"
    },
    {
        "keyword": "виджет погоды",
        "lang": "ru-RU",
        "country": "ru"
    },
    {
        "keyword": "날씨",
        "lang": "ko-KR",
        "country": "kr"
    },
    {
        "keyword": "wetter",
        "lang": "de-DE",
        "country": "de"
    },
    {
        "keyword": "wetter widget",
        "lang": "de-DE",
        "country": "de"
    },
]

developer_list = [
    {
        "developer": "Fotoable,Inc.",
        "lang": "en-US",
        "country": "us"
    },
    {
        "developer": "Tool+Box+Studio",
        "lang": "en-US",
        "country": "us"
    },
    {
        "developer": "MobiDev+Studio",
        "lang": "en-US",
        "country": "us"
    },
    {
        "developer": "Z+Lock+Screen+Team",
        "lang": "en-US",
        "country": "us"
    },
    {
        "developer": "Mobilead+Inc.",
        "lang": "en-US",
        "country": "us"
    },
    {
        "developer": "Photo+Editor+Creative",
        "lang": "en-US",
        "country": "us"
    },
]

keyword_config = {
    "dir" : {
        "keyword_list": "/tmp/keyword_txt",
        "out_sql" : '/tmp/out_sql_data',
    }
}

my_developer = [
    '📡 Weather Widget Theme Dev Team'
]

rank_score = {
    '1'  : 100,
    '2'  : 80,
    '3'  : 50,
    '4'  : 30,
    '5'  : 11,
    '6'  : 8,
    '7'  : 8,
    '8'  : 4,
    '9'  : 4,
    '10' : 4
}


