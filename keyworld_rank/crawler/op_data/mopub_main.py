#!/usr/bin/python
# -*- coding:utf-8 -*-
import json

import config
import toolkit
import logging
import argparse
import datetime
import re
import uuid
import time
import os
from MopubApi import MopubApi
import hashlib
import traceback


def parse_args():
    mopub_task = config.mopub_task_list.keys()
    parser = argparse.ArgumentParser(description='Ads Data Crawler.')
    parser.add_argument("--from", type=str, dest="from_date", required=False,
                        help="the datetime from which  crawler start;\nformatter 2016-01-01")
    parser.add_argument("--task", type=str, dest="task", required=True, choices=mopub_task, help="")
    parser.add_argument("days", type=int, nargs='?', default=0,
                        help="How many recently days or with --from <DATE> "
                             "means how many days after <date> \n")

    args = parser.parse_args()
    pattern = "\d{4}\-\d{2}\-\d{2}"

    if args.from_date:
        if not re.match(pattern, args.from_date):
            print "--from in bad format,(%s);should be [ 2016-01-01 ] " % args.from_date
            parser.print_help()
            exit(-1)
        else:
            datetime_start = datetime.datetime.strptime(args.from_date, "%Y-%m-%d")
            time_delta = datetime.timedelta(days=args.days)
            datetime_end = datetime_start + time_delta
            if datetime_start < datetime_end:
                return datetime_start, datetime_end, args.task
            else:
                return datetime_end, datetime_start, args.task
    else:
        if args.days < 0:
            print "days used as recently days,must be >= 0"
            print parser.print_help()
            exit(-1)
        datetime_end = datetime.datetime.utcnow()
        time_delta = datetime.timedelta(days=args.days)
        datetime_from = datetime_end - time_delta
        return datetime_from, datetime_end, args.task


def gen_sql_file_name():
    return "/tmp/%s.sql" % str(uuid.uuid4()).replace("-", "")


def safe_type_float(number):
    try:
        return float(number)
    except:
        return 0.0


def safe_type_int(number):
    try:
        return int(number)
    except:
        return 0


def safe_type_str(val, length=None):
    if not (isinstance(val, (unicode, str))):
        return ''
    val = val.replace(r"'", r"''")
    if isinstance(length, int):
        val = val[:length]
    return val


def compute_hash(model, field_list):
    m = {}
    for key in field_list:
        val = model.get(key, '')
        m[key] = val
    j = json.dumps(m)
    hash_val = hashlib.sha1(j).hexdigest()
    return hash_val


def main_loop(task_type, sql_file_name, start_time):
    global app
    time_str = time.strftime('%Y-%m-%d', time.gmtime(start_time))
    task_config = config.mopub_task_list[task_type]
    table_name = task_config["table_name"]
    field_list = task_config["field_list"]
    unique_list = task_config['unique_list']
    account_list = config.mopub_account_list.keys()
    for account in account_list:
        api_key = config.mopub_account_list[account]['api_key']
        report_key = config.mopub_account_list[account]['report_key']

        data = MopubApi(api_key, report_key).fetch_report(time_str)

        if not data:
            logging.error("main:mopub.fetch_report.No_Data:"
                          "[task:%s,appid:%s,time:%sfield_list:%s]" % (
                              task_type, account, time_str, field_list)
                          )
            continue
        sql_list = []
        for model in data:
            # insert some info
            model["account"] = account
            model["platform"] = "mopub"
            model['country'] = safe_type_str(model.get('country', '00'), 2)

            model['appname'] = safe_type_str(model['appname'], 100)
            model['placement'] = safe_type_str(model['placement'], 255)

            model['request'] = safe_type_int(model['request'])
            model['filled'] = 0
            model['impression'] = safe_type_int(model['impression'])
            model['click'] = safe_type_int(model['click'])
            model['filled_rate'] = 0
            model['ctr'] = safe_type_float(model['ctr'])
            model['ecpm'] = 0
            model['revenue'] = safe_type_float(model['revenue'])

            for key in ['app_id', 'creative_id', 'creative', 'priority', 'order_id', 'line_item',
                        'line_item_type', 'device', 'segment', 'adunit_id', 'segment_id',
                        'os', 'order', 'conversions']:
                model[key] = safe_type_str(model.get(key, '00'), 32)

            hash_key = compute_hash(model, unique_list)
            model['hash'] = hash_key

            model_field_list = field_list + ["date", "appname", "platform"]
            unique_model_field_list = list(set(model_field_list))
            sql = toolkit.gen_save_sql(table_name, model=model, field_list=unique_model_field_list,
                                       unique_key=model_field_list)
            if sql:
                sql_list.append(sql)
            else:
                logging.error("main:gen_save_sql.Fail:"
                              "[table_name:%s, model=%s, field_list=%s]" % (
                                  task_type, model, field_list)
                              )
        # print sql_list
        app["total_count"] += len(sql_list)
        with open(sql_file_name, 'a') as f:
            if not sql_list:
                return
            big_sql = "\n".join(sql_list)
            # print "big_sql:", big_sql
            f.write(big_sql)


def main():
    global app
    datetime_from, datetime_end, task_type = parse_args()
    task_config = config.mopub_task_list[task_type]
    detail_log_file = task_config["detail_log_file"]
    clean_sql_file = task_config["clean_sql_file"]
    app["statics_log_file"] = task_config["statics_log_file"]

    init_logging(detail_log_file)

    sql_file_name = gen_sql_file_name()
    logging.info("main.sql_file_name.%s" % sql_file_name)

    p = toolkit.datetime_to_timestamp(datetime_from)
    g_stop_time = toolkit.datetime_to_timestamp(datetime_end)
    while p <= g_stop_time:
        main_loop(task_type, sql_file_name, p)
        p += 1 * 24 * 3600

    # 执行 SQL
    mysql_config = config.mysql_config
    toolkit.execute_mysql_sql(
        mysql_config['host'],
        mysql_config['port'],
        mysql_config["user"],
        mysql_config["passwd"],
        mysql_config["dbname"],
        sql_file_name)
    # END
    if clean_sql_file:
        os.remove(sql_file_name)
    else:
        logging.info("keep the tmp sql file @ %s" % sql_file_name)
    return


def init_logging(logfile):
    debug_mode = config.debug_mode
    current_date_string = toolkit.get_current_string_for_file_name(True)[0:10]
    log_file = "%s_%s.log" % (logfile, current_date_string)
    toolkit.init_log(log_file, debug_mode)


# global

app = {
    "total_count": 0,
    "statics_log_file": None,
    'mysql_connection': None,
    'mysql_write_count': 0,
    'mysql_max_count': 100,
    'success_count': 0,
    'fail_count': 0,
    'total': 0,
    'cpu_time': 0,
    'real_time': 0,
}

if __name__ == "__main__":
    start_time = time.time()
    start_clock = time.clock()
    main()  # 入口
    stop_time = time.time()
    stop_clock = time.clock()
    msg = "=" * 20
    msg += "\n%s\n" % time.strftime("%Y-%m-%d\t%H:%M:%S GMT", time.gmtime())
    msg += "实际花费时间: %0.2f秒\n" % (stop_time - start_time)
    msg += "处理器时间  : %0.2f秒\n" % (stop_clock - start_clock)
    msg += "记录总数    : %s\n" % app["total_count"]
    with open(app["statics_log_file"], 'a') as f:
        f.write(msg)
