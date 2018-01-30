#! /usr/bin/env python2
# -*- coding:utf-8 -*-
import argparse
import logging
import os
import uuid
import datetime
import subprocess
import time
import pytz
import re


def parse_args(task_list, duration_list=()):
    """
    :return: datetime_from , type datatime : 起始时间
              datetime_end , type datetime : 结束时间
              task_type ,  string : 任务类型
    """
    parser = argparse.ArgumentParser(description='Ads Data Crawler.')
    parser.add_argument("--task", type=str, dest="task", required=True, choices=task_list, help="")

    if duration_list:
        parser.add_argument("--duration", type=str, dest="duration", required=False, default=duration_list[0],
                            choices=duration_list,
                            help="time unit size for summary metrics: [ daily , hourly ].")
    parser.add_argument("--from", type=str, dest="from_date", required=False,
                        help="the datetime from which  crawler start;\nformatter 2016-01-01:02")
    parser.add_argument("--to", type=str, dest="to_date", required=False, default=None,
                        help="the datetime which  crawler end;\nformatter 2016-01-01:02")
    parser.add_argument("--days", type=int, dest="days", required=False, default=None,
                        help="the datetime which  crawler end;\nformatter 10")
    parser.add_argument("hours", type=int, nargs='?', default=0,
                        help="How many recently days or with --from <DATE> "
                             "means how many days after <date> \n")

    args = parser.parse_args()
    pattern = "\d{4}\-\d{2}\-\d{2}:\d{02}"

    if not duration_list:
        args.duration = None

    m_list = []
    for m in [args.to_date, args.days, args.hours]:
        if m:
            m_list.append(m)
    if len(m_list) > 1:
        print "options `--to` `--days` `hours` cannot used together!"
        parser.print_help()
        exit(1)
    if args.hours == 0:
        args.hours = 1

    datetime_start = None
    datetime_end = None
    if args.from_date:
        if not re.match(pattern, args.from_date):
            print "--from in bad format,(%s);should be [ 2016-01-01:00 ] " % args.from_date
            parser.print_help()
            exit(3)
        else:
            datetime_start = datetime.datetime.strptime(args.from_date, "%Y-%m-%d:%H")
            if args.to_date:
                if not re.match(pattern, args.to_date):
                    print "--to in bad format,(%s);should be [ 2016-01-01:00 ] " % args.from_date
                    parser.print_help()
                    exit(4)
                else:
                    datetime_end = datetime.datetime.strptime(args.to_date, "%Y-%m-%d:%H")
            elif args.hours:
                time_delta = datetime.timedelta(hours=args.hours)
                datetime_end = datetime_start + time_delta
            elif args.days:
                time_delta = datetime.timedelta(days=args.days)
                datetime_end = datetime_start + time_delta
            else:
                print "miss param `to`, `days`, `hours`"
                parser.print_help()
                exit(2)

    else:
        datetime_end = datetime.datetime.utcnow()
        if args.days:
            datetime_start = datetime_end - datetime.timedelta(days=args.days)
        elif args.hours:
            datetime_start = datetime_end - datetime.timedelta(hours=args.hours)
        else:
            print "miss param `to`, `days`, `hours`"
            parser.print_help()
            exit(2)

    # check datetime_start & datetime_end
    if datetime_start < datetime_end:
        return datetime_start, datetime_end, args.task, args.duration
    else:
        return datetime_end, datetime_start, args.task, args.duration


def init_log(log_file, debug=False):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=log_file,
                        filemode='a')
    if debug:
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)


def make_file_name(prefix=None, suffix=None):
    if not prefix:
        prefix = '/tmp/'
    if suffix and isinstance(suffix, (str, unicode)):
        suffix = time.strftime(suffix, time.gmtime())
    if not suffix:
        suffix = str(uuid.uuid4()).replace("-", "")
    return '%s%s' % (prefix, suffix)


def download_from_s3(s3, base_path, tm, save_prefix):
    if not isinstance(tm, datetime.datetime):
        logging.error("[download_from_s3]:Bad Param Type `tm`!")
        return None
    key_path = base_path + tm.strftime('/%Y/%m/%d/%H/')
    key_path = key_path.replace('//', '/')
    logging.info("key_path:%s" % key_path)
    print key_path
    s3_key_list = s3.ls_dir(key_path)
    print s3_key_list
    save_file_list = []
    for s3_key in s3_key_list:
        file_name = os.path.basename(s3_key)
        save_file = '%s/%s' % (save_prefix, file_name)
        stat = s3.download(s3_key, save_file)
        if not stat:
            logging.critical("[FAIL]S3 Download Key fail:[%s,%s]" % (s3_key, save_file))
            continue
        save_file_list.append(save_file)
    return save_file_list


def mysql_gen_save_sql(table, model, field_list, update_list):
    if not table or not isinstance(table, str):
        logging.error("gen_save_sql().table[%s] should be str()" % table)
        return None
    if not model or not isinstance(model, dict):
        logging.error("gen_save_sql().data[%s] should be dict()" % model)
        return None
    if not field_list or not isinstance(field_list, (list, tuple)):
        logging.error("gen_save_sql().field_list[%s] should be list()" % field_list)
        return None
    if not update_list or not isinstance(update_list, (list, tuple)):
        logging.error("gen_save_sql().unique_key[%s] should be list()" % update_list)
        return None

    # 拼接 insert 从句
    column_list = []
    value_list = []
    for field in field_list:
        if field not in model.keys():
            logging.warning("gen_save_sql():FIELD[%s] not in [%s]." % (field, model))
            continue
        column_list.append("`%s`" % field)
        value_list.append("'%s'" % model[field])
    column_sql = ",".join(column_list)
    value_sql = ",".join(value_list)

    # 拼接 UPDATE 从句
    # where_list = []
    # for key in update_list:
    #     if key not in model.keys():
    #         val = '00'
    #     else:
    #         val = model[key]
    #
    #     where_list.append("`%s`='%s'" % (key, val))
    # where_sql = ",".join(where_list)
    sql = " INSERT INTO `%s`(%s) VALUES(%s);" % \
          (table, column_sql, value_sql)
    # print "gen_save_sql:sql:", sql
    return sql


def run_command(command):
    try:
        p = subprocess.Popen(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE,
                             shell=True, env=os.environ)
        output, err = p.communicate()
        logging.info('run_command():output:\n%s\n' % output)
        logging.info('run_command():error :\n%s\n' % err)
        return output, err
    except Exception, e:
        logging.info('run_command exception: %s' % e)
        return False


def execute_mysql_sql(host, port, user, passwd, dbname, sql_file):
    cmd = "mysql --force --host=%s --port=%s --user=%s --password=%s %s < %s " % (
        host, port, user, passwd, dbname, sql_file)
    log_cmd = "mysql --force --host=%s --port=%s --user=%s --password=%s %s < %s " % (
        host, port, user, 'xxxx', dbname, sql_file)
    logging.info("execute_mysql_sql:CMD:%s" % log_cmd)
    run_command(cmd)


def execute_mysql_dump(host, port, user, passwd, dbname, table_name, result_file):
    cmd = "mysqldump --add-drop-database --host=%s --port=%s --user=%s --password=%s %s %s >> %s " % (
        host, port, user, passwd, dbname, table_name, result_file)
    log_cmd = "mysqldump --add-drop-database --host=%s --port=%s --user=%s --password=%s %s %s >> %s " % (
        host, port, user, 'xxxx', dbname, table_name, result_file)
    logging.info("execute_mysql_dump:CMD:%s" % log_cmd)
    run_command(cmd)


def get_pst_now():
    return get_time_now("US/Pacific")


def get_beijing_now():
    return get_time_now("Asia/Shanghai")


def get_time_now(tzname="UTC"):
    tz = pytz.timezone(tzname)
    dt = datetime.datetime.now(tz=tz)
    return dt.strftime("%Y%m%d")


def is_float(t):
    try:
        float(t)
        return True
    except:
        return False


def format_utc_time(t):
    try:
        t = float(t)
    except Exception as e:
        t = 1
    tm = time.gmtime(t)
    return time.strftime('%Y-%m-%d %H:%M:%S', tm)


def delete_files(file_list):
    if not file_list:
        logging.error('delete_files():EMPTY file list.')
        return None

    if isinstance(file_list, (unicode, str)):
        file_list = [file_list]
    elif not isinstance(file_list, (list, tuple)):
        logging.error('delete_files():param is bad type %s' % type(file_list))

    for f in file_list:
        try:
            os.remove(f)
            logging.info('[SUCCESS] delete file :%s' % f)
        except Exception as e:
            logging.exception('delete_files():delete file(%s) failed:[%s]' % (f, e))


if __name__ == '__main__':
    # print  format_utc_time('1')

    print make_file_name('', '_%Y.sql')
