#! /usr/bin/env python2
# -*- coding:utf-8 -*-
import hashlib
import json
import logging
import time


def format_utc_time(t):
    try:
        t = float(t)
    except Exception as e:
        t = 1
    tm = time.gmtime(t)
    return time.strftime('%Y-%m-%d %H:%M:%S', tm)


def is_float(t):
    try:
        float(t)
        return True
    except:
        return False


# Aws Mobile Analytics Parser
class AwsMAEventParser(object):
    def __init__(self):
        self._default_value = {
            'event_type': '',
            'client_time': '1000',
            'arrival_time': '1000',
            'aws_app_id': '',
            'package_name': '',
            'client_id': '',
            'country': '',
            'lang': '',
            'brand': '',
            'model': '',
            'os_name': '',
            'os_version': '',
            'hash': ''
        }

    def parser(self, js_text):
        res = None
        try:
            m = self._default_value.copy()
            m['hash'] = hashlib.sha1(js_text).hexdigest()
            j = json.loads(js_text)
            m['event_type'] = j.get('event_type', '')
            m['client_time'] = j.get('event_timestamp', 1000)
            m['arrival_time'] = j.get('arrival_timestamp', 1000)

            for param in ['client_time', 'arrival_time']:
                val = m[param]
                if is_float(val):
                    val = float(val) / 1000
                else:
                    val = 1
                m[param] = format_utc_time(val)

            application = j.get('application')
            if application:
                m['aws_app_id'] = application.get('app_id', '')
                m['package_name'] = application.get('package_name', '')

            client = j.get('client')
            if client:
                m['client_id'] = client.get('client_id', '')

            device = j.get('device')
            if device:
                locale = device.get('locale')
                if locale:
                    m['country'] = locale.get('country', '')
                    m['lang'] = locale.get('language', '')

                m['brand'] = device.get('make', '')
                m['model'] = device.get('model', '')

                platform = device.get('platform')
                if platform:
                    m['os_name'] = platform.get('name', '')
                    m['os_version'] = platform.get('version', '')

            # handle attributes
            attributes = j.get('attributes')
            if attributes:
                attr = self.parser_custom_attribute(attributes)
                if attr and isinstance(attr, dict):
                    m.update(attr)
            # handle metrics
            metrics = j.get('metrics')
            if metrics:
                _metrics = self.parser_custom_metrics(metrics)
                if _metrics and isinstance(_metrics, dict):
                    m.update(_metrics)

            res = m
        except Exception as e:
            res = None
            logging.exception('%s:[%s]' % (self.__class__.__name__, e))
        finally:
            return res

    def parser_custom_attribute(self, attributes):
        return None

    def parser_custom_metrics(self, metrics):
        return None


class PushAwsMAParser(AwsMAEventParser):
    _custom_attribute_default_value = {
        'device_id': '',
        'ip_country': '',
        'sim_country': '',
        'msg_id': '0',
        'mid': '0',
        'push_type': '',
        'push_count': '0',
        'fetch_img_status': '0',
        'app_type': '',

    }

    def parser_custom_attribute(self, attributes):
        if attributes:
            m = self._custom_attribute_default_value.copy()
            m['device_id'] = attributes.get('DeviceId', '')
            m['ip_country'] = attributes.get('ipCountry', '')
            m['sim_country'] = attributes.get('simCountry', '')
            m['msg_id'] = attributes.get('msg_id', '0')
            m['mid'] = attributes.get('mid', '0')
            m['push_type'] = attributes.get('push_type', '')
            m['push_count'] = attributes.get('push_count', '0')
            m['fetch_img_status'] = attributes.get('fetch_img_status', '0')
            m['app_type'] = attributes.get('app_type', '')
            return m
        else:
            return None


class StoreAwsMAParser(AwsMAEventParser):
    _custom_attribute_default_value = {
        'device_id': '',
        'ip_country': '',
        'sim_country': '',
        'app_type': '',
        'store_version': '',
        'store_item_type': '',
        'pkg_name': '',
        'open_count': '0',
    }

    def parser_custom_attribute(self, attributes):
        if attributes:
            m = self._custom_attribute_default_value.copy()
            m['device_id'] = attributes.get('DeviceId', '')
            m['ip_country'] = attributes.get('ipCountry', '')
            m['sim_country'] = attributes.get('simCountry', '')
            m['app_type'] = attributes.get('app_type', '')
            m['store_version'] = attributes.get('store_version', '')
            m['store_item_type'] = attributes.get('store_item_type', '')
            m['pkg_name'] = attributes.get('pkg_name', '')
            m['open_count'] = attributes.get('open_count', '0')
            return m
        return None


# -- common parser function

__store_parser_json = StoreAwsMAParser().parser


def store_parser_json(js_text):
    m = __store_parser_json(js_text)
    if m and isinstance(m, dict):
        m['time'] = m.get('arrival_time', '')
    return m


__push_parser_json = PushAwsMAParser().parser


def push_parser_json(js_text):
    m = __push_parser_json(js_text)
    if m and isinstance(m, dict):
        m['time'] = m.get('arrival_time', '')
    return m


if __name__ == '__main__':
    p = StoreAwsMAParser()
    with open('a.json', 'r') as f:
        print p.parser(f.read())
