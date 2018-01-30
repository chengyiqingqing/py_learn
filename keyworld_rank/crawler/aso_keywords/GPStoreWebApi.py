#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-

import json
import logging
import traceback
import urllib
import re
import requests
from pyquery import PyQuery


class GPStoreWebApi(object):
    def __init__(self, hl='en', gl=None, proxies=None, verify=None):
        # language code
        self.hl = hl
        # country code
        self.gl = gl

        if proxies:
            self.proxies = proxies
        else:
            self.proxies = None

        if verify:
            self.verify = verify
        else:
            self.verify = False

        self.re_nbp = re.compile(r"var nbp='(.*)\\n';var")

        pass

    def get_accept_language(self):
        if self.gl:
            long_lang = "%s-%s" % (self.hl, self.gl)
        else:
            long_lang = self.hl
        return "%s,%s;q=1.0" % (long_lang, self.hl)

    def search(self, search, limit=None):
        results = []
        nbp = None
        if not isinstance(limit, (int, long)) or limit < 0:
            limit = 2 ** 32 - 1
        while True:
            data = self.send_search_request(search, nbp)
            if not data:
                break
            apps, nbp = self.parse_search_results(data)
            logging.info("Count:%s" % len(apps))
            if apps:
                results += apps
            if len(results) >= limit:
                results = results[:limit]
                break
            if not nbp:
                logging.info("NBP is None")
                break
        return results

    @staticmethod
    def fix_href(href=''):
        if href.startswith('//'):
            return 'https:' + href
        else:
            return href

    @staticmethod
    def fix_number(number, number_type='int'):
        try:
            pattern = '[^-+eE0-9\.]'
            num = re.sub(pattern, '', number)
            if number_type == 'int':
                return int(num)
            else:
                return float(num)
        except Exception as e:
            logging.info("fix_number:Error:\t%s" % ([number, e]))

    def app_detail(self, package_name):
        data = self.send_app_detail_request(package_name)
        if not data:
            logging.error("Get App Detail Failed!")
            return None
        return self.parse_app_detail_results(data)

    def parse_app_detail_results(self, text):
        results = {}
        try:
            root_pq = PyQuery(text)
            pq = root_pq('div.main-content')
            app_title = pq('div.id-app-title').text()
            app_category = pq('a.document-subtitle.category').text()
            developer_name = pq('a.document-subtitle.primary').text()
            href = pq('a.document-subtitle.primary').attr('href')
            if '?id=' in href:
                pre, suf = href.split("?id=", 1)
                developer = urllib.unquote_plus(suf)
            else:
                developer = ''
            icon_image = self.fix_href(pq('img.cover-image').attr('src'))
            full_screenshot = []
            for img in pq('img.full-screenshot').items():
                img_src = self.fix_href(img.attr('src'))
                full_screenshot.append(img_src)
            description = pq('div.details-section.description.simple.contains-text-link.apps-secondary-color' + \
                             ' > div > div > div > div').text()

            # review content
            reviews = []
            for review in pq('div.single-review').items():
                author_name = review('span.author-name').text()
                review_date = review('span.review-date').text()
                review_text = review('div.review-body').text()

                review_rating = review('div.current-rating').attr('style')
                review_rating = self.fix_number(review_rating, 'float') / 20

                reviews.append({
                    'author_name': author_name,
                    'date': review_date,
                    'rating': review_rating,
                    'review': review_text,
                })

            score = pq('div.score').text()

            review_num = pq('span.reviews-num').text()

            #
            numDownloads = root_pq('div.content[itemprop="numDownloads"]').text()
            # print numDownloads
            numDownloads = re.split(r'[^-+eE,\.0-9]', numDownloads, 1)[0]
            softwareVersion = root_pq('div.content[itemprop="softwareVersion"]').text()
            five_star_number = pq('div.rating-bar-container.five span.bar-number').text()
            four_star_number = pq('div.rating-bar-container.four span.bar-number').text()
            three_star_number = pq('div.rating-bar-container.three span.bar-number').text()
            two_star_number = pq('div.rating-bar-container.two span.bar-number').text()
            one_star_number = pq('div.rating-bar-container.one span.bar-number').text()
            results = {
                'title': app_title,
                'category': app_category,
                'developer_name': developer_name,
                'developer': developer,
                'icon': icon_image,
                'screenshot': full_screenshot,
                'description': description,
                'score': self.fix_number(score),
                'review_num': self.fix_number(review_num),
                'softwareVersion': softwareVersion,
                'downloads': self.fix_number(numDownloads),
                'five_star_number': self.fix_number(five_star_number),
                'four_star_number': self.fix_number(four_star_number),
                'three_star_number': self.fix_number(three_star_number),
                'two_star_number': self.fix_number(two_star_number),
                'one_star_number': self.fix_number(one_star_number),
                'reviews': reviews
            }
        except Exception as e:
            logging.error("%s::parse_app_detail_results():\t%s" % (self.__class__.__name__, e))
        return results

    def send_app_detail_request(self, package_name):
        text = None
        try:
            url = 'https://play.google.com/store/apps/details?'
            url += urllib.urlencode({
                'id': package_name
            })

            logging.info("Url:\t%s" % url)

            headers = {
                "origin": "https://play.google.com",
                "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "accept-language": self.get_accept_language(),
                "cache-control": "no-cache",
                "authority": "play.google.com",
                "pragma": "no-cache",
                "x-chrome-uma-enabled": "1",
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/55.0.2883.87 Safari/537.36",
            }
            resp = requests.get(url, headers=headers, proxies=self.proxies, verify=self.verify)
            if not resp or resp.status_code >= 400:
                logging.error("%s:send_app_detail_request():Bad Response:\t%s" % (self.__class__.__name__, [url, resp]))
            else:
                text = resp.text
        except Exception as e:
            logging.error("%s:send_app_detail_request():\t%s" % (self.__class__.__name__, e))
        finally:
            return text

    def developer_detail(self, developer):
        pass

    def parse_search_results(self, text):
        results = []
        nbp = None
        try:
            pq = PyQuery(text)
            app_list = pq('div.card.no-rationale.apps')
            for app in app_list.items():
                try:
                    package = app.attr('data-docid')
                    app_name = app('a.title').attr('title')
                    developer_name = app('a.subtitle').attr('title')
                    href = app('a.subtitle').attr('href')
                    if '?id=' not in href:
                        logging.warning("Skip:%s" % app)
                        continue
                    pre, suf = href.split("?id=", 1)
                    developer = urllib.unquote_plus(suf)
                    large_cover_image = 'https:' + app('img.cover-image').attr('data-cover-large')
                    small_cover_image = 'https:' + app('img.cover-image').attr('data-cover-small')
                    price = app('span.display-price:last').text()
                    results.append({
                        'package': package,
                        'app_name': app_name,
                        'developer': developer,
                        'developer_name': developer_name,
                        'large_cover_image': large_cover_image,
                        'small_cover_image': small_cover_image,
                        'price': price,
                    })
                except Exception as e:
                    logging.error("GPStoreWebApi::parse_search_results():\t%s" % e)
                    traceback.print_exc()

            script = pq('script:last').html()
            m = None
            if script:
                m = self.re_nbp.search(script)
            if m:
                nbp_text = m.group(1)
                nbp = json.loads(nbp_text.decode("unicode-escape"))
                # print "NBP:\t%s" % nbp
        except Exception as e:
            logging.error("%s:parse_search_results():\t%s" % (self.__class__.__name__, e))
            traceback.print_exc()
        logging.info("Apps COUNT:\t%s" % len(results))
        return results, nbp

    def send_search_request(self, search, nbp=None, category='apps'):
        logging.info("%s::send_search_request().PARAM:%s\n" % (search.__class__.__name__, [search, nbp]))

        if isinstance(search, unicode):
            search = search.encode('utf-8')

        is_nbp = False
        if nbp and isinstance(nbp, (list, tuple)):
            is_nbp = True
            url = "https://play.google.com/store/apps/collection/search_results_cluster_apps?authuser=0"
        else:
            url = "https://play.google.com/store/search?"
            params = {
                'authuser': '0',
                'c': category,
                'q': search,
                'hl': self.hl,
            }
            if self.gl:
                params['gl'] = self.gl
            url += urllib.urlencode(params)

        headers = {
            "origin": "https://play.google.com",
            "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "accept-language": self.get_accept_language(),
            "cache-control": "no-cache",
            "authority": "play.google.com",
            "pragma": "no-cache",
            "x-chrome-uma-enabled": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/55.0.2883.87 Safari/537.36",
            "referer": "https://play.google.com/store/search?" + urllib.urlencode({
                'q': search, 'hl': self.hl, 'c': 'apps'
            })
        }

        logging.info("%s\nGPStoreWebApi:send_search_request():\t%s" % ('=' * 20, [url, headers]))
        text = None
        try:
            if is_nbp:
                form = urllib.urlencode({
                    'start': nbp[3],
                    'num': nbp[2],
                    'numChildren': nbp[4],
                    'pagTok': nbp[1],
                    'clp': nbp[6],
                    'pagtt': nbp[7],
                    'cctcss': 'square-cover',
                    'cllayout': 'NORMAL',
                    'ipf': 1,
                    'xhr': 1,
                })
                logging.info("%s::send_search_request():Form:\t%s" % (self.__class__.__name__, form))
                resp = requests.post(url, headers=headers, proxies=self.proxies, verify=self.verify, data=form)
            else:
                resp = requests.get(url, headers=headers, proxies=self.proxies, verify=self.verify)
            if not resp or resp.status_code >= 400:
                logging.error("GPStoreWebApi:send_search_request():\t%s" % [url, resp])
            else:
                text = resp.text
        except Exception as e:
            logging.exception("GPStoreWebApi:send_search_request():\t%s" % e)
            traceback.print_exc()
        finally:
            return text


#########


def init_log():
    # set up logging to file - see previous section for more details
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='/media/ram/parse_cc.log',
                        filemode='a')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)


if __name__ == '__main__':
    import sys

    reload(sys)
    sys.setdefaultencoding('utf-8')
    init_log()

    proxies = {
        'http': 'http://127.0.0.1:8118',
        'https': 'http://127.0.0.1:8118',
    }

    g = GPStoreWebApi('zh')
    # r = g.search('weather', 5)
    r = g.app_detail('com.whatsapp')
    print '=' * 40
    print json.dumps(r, ensure_ascii=False, indent=4).encode('utf-8')
    print len(r)
