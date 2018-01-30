#!/usr/bin/python
# -*- coding:utf-8 -*-


import re
import logging
import traceback
import requests


class MopubApi(object):
    key_2_db_map = {
        "day": "date",
        "country": "country",
        "app": "appname",
        "adunit": "placement",
        "attempts": "request",
        "impressions": "impression",
        "clicks": "click",
        "conversions": "conversions",
        "line_item": "line_item",
        "revenue": "revenue",
        "ctr": "ctr",

        # "app_id": "app_id",
        # "line_item_id": "line_item_id",
        # "adunit_format": "adunit_format",
        # "network": "network",
        # "creative_id": "creative_id",
        # "creative": "creative",
        # "priority": "priority",
        # "order_id": "order_id",
        # "line_item_type": "line_item_type",
        # "device": "device",
        # "segment": "segment",
        # "adunit_id": "adunit_id",
        # "segment_id": "segment_id",
        # "os": "os",
        # "order": "order"
    }

    def __init__(self, api_key, report_key):
        self.api_key = api_key
        self.report_key = report_key

    def fetch_report(self, date_str):
        '''
        :param date_str: format YYYY-MM-DD
        :return: [{report}]
        '''

        data = self.net_get(date_str)
        return self.parse_data(data)

    def normal_name(self, name):
        if not isinstance(name, (unicode, str)):
            return ''
        name = re.sub(r'[^a-zA-Z]', '_', name.lower())
        name = self.key_2_db_map.get(name, name)
        return name

    def parse_data(self, data):
        ret = []
        try:
            lines = data.split('\n')
            headers = []
            for i, line in enumerate(lines):
                if not line.strip():
                    continue
                columns = line.split(',')
                if i == 0:
                    for header in columns:
                        headers.append(self.normal_name(header))
                    continue
                m = {}
                for j, val in enumerate(columns):
                    name = headers[j]
                    m[name] = val
                ret.append(m)
        except Exception as e:
            logging.error('parse_data():Error:%s' % e)
            traceback.print_exc()
        finally:
            return ret

    def net_get(self, date_str):
        if not isinstance(date_str, (unicode, str)) or not re.match(r'\d{4}-\d{2}-\d{2}', date_str):
            logging.error('Bad Date String:%s' % date_str)
            return ''
        data = ''
        url = 'https://app.mopub.com/reports/custom/api/download_report?' \
              'report_key={report_key}&api_key={api_key}&date={date}' \
            .format(report_key=self.report_key, api_key=self.api_key, date=date_str)
        try:
            r = requests.get(url)
            if r.status_code >= 400:
                logging.info('Error:%s' % r.text)
                data = ''
            else:
                data = r.text
        except Exception as e:
            logging.error('MopubApi.net_get():Exception:%s' % e)
            traceback.print_exc()
        finally:
            return data


if __name__ == '__main__':
    import config
    import json

    mopub_account_list = config.mopub_account_list
    auth = mopub_account_list.values()[0]
    mopub = MopubApi(auth['api_key'], auth['report_key'])
    # _data = mopub.net_get('2017-06-07')
    # with open('tmp.csv', 'w') as f:
    #     f.write(data)
    _data = None
    with open('tmp.csv', 'r') as f:
        _data = f.read()
    _data = mopub.parse_data(_data)
    # _data = mopub.fetch_report('2017-06-07')
    print json.dumps(_data, ensure_ascii=False, indent=4).encode('utf-8')
