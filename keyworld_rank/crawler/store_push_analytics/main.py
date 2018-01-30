#! /usr/bin/env python2
# -*- coding:utf-8 -*-

import os
import os.path
import sys
import json
import parser
import logging
import datetime
import gzip

import config
import common
import create_table
from S3Helper import S3Helper


def main_loop(task, file_list):
    if not file_list or not isinstance(file_list, (list, tuple)):
        logging.error("[FAIL]main_loop():bad param[%s]" % file_list)
        return None
    else:
        logging.info('main_loop handle %s' % file_list)

    filter_event_list = task['filter_event_list']
    if not file_list:
        logging.error('main_loop():filter_event_list is empty')
        return None

    model_list = []
    parse_json = task['app']['parser_json']
    for local_file in file_list:
        try:
            with gzip.open(local_file, 'rb') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        js = json.loads(line)
                        event_type = js['event_type']
                        if event_type in filter_event_list:
                            model = parse_json(line)
                            if model and isinstance(model, dict):
                                model_list.append(model)
                    except Exception as e:
                        logging.exception('main_loop():json pre handle:Exception:[%s]' % e)
        except Exception as e:
            logging.exception('main_loop:Exception:[%s]' % e)

    # write data to tmp sql file
    sql_list = []
    field_list = task['field_list']
    table_name = task['app']['table_name']
    for m in model_list:
        sql = common.mysql_gen_save_sql(table_name, m, field_list, field_list)
        if not sql or not isinstance(sql, (unicode, str)):
            logging.error('gen sql failed for model:[%s]' % m)
            continue
        sql_list.append(sql)

    tmp_sql_file = task['app']['global_tmp_sql_file']
    with open(tmp_sql_file, 'a') as f:
        big_sql = '\n'.join(sql_list)
        f.write(big_sql)
        f.write('\n')
    return len(sql_list)


def main():
    global global_fail_count
    global global_success_count
    global global_file_list
    # parse args
    task_name_list = config.task_list.keys()
    start_time, stop_time, task_name, _ = common.parse_args(task_name_list)
    task = config.task_list[task_name]

    # init task app local data
    task['app'] = {}

    # init log
    common.init_log(task['log']['filename'],
                    task['log']['debug'])

    logging.info('======\n%s\n' %
                 datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z'))
    logging.info(" TASK [%s] START ..." % task_name)

    # init parser json function
    task['app']['parser_json'] = getattr(parser, task['parser_function_name'])

    # make tmp sql file
    _prefix = task['tmp_sql_file_name']
    _suffix = task['tmp_sql_file_name_suffix']
    global_tmp_sql_file = common.make_file_name(_prefix, _suffix)
    logging.info('Global Tmp Sql File:%s' % global_tmp_sql_file)
    # save global_tmp_sql_file to task .
    task['app']['global_tmp_sql_file'] = global_tmp_sql_file
    # delete old same name file
    common.delete_files(global_tmp_sql_file)

    # init s3 helper, download s3 file to local
    amazon_s3_auth = task['amazon_s3_auth']
    s3 = S3Helper(**amazon_s3_auth)

    aws_appid_list = task['aws_appid_list']
    tmp_local_file_dir = task['tmp_local_file_dir']

    keep_s3_file = task['keep_s3_file']

    # main loop
    # foreach time range
    p = start_time
    while p < stop_time:
        # prepare raw data table name
        _prefix = task['raw_data_table_name']
        _suffix = task['raw_data_table_name_suffix']
        _format_suffix = p.strftime(_suffix)
        table_name = '%s%s' % (_prefix, _format_suffix)
        # save table_name to task .
        task['app']['table_name'] = table_name

        # create table if not exits
        create_raw_data_table_function = task['create_raw_data_table_function']
        create_table_function = getattr(create_table, create_raw_data_table_function)
        create_table_function(global_tmp_sql_file, table_name)

        # foreach time range
        for aws_appid in aws_appid_list:
            key_path = 'awsma/events/%s/' % aws_appid
            local_s3_file_list = common.download_from_s3(s3, key_path, p, tmp_local_file_dir)
            #
            main_loop(task, local_s3_file_list)
            # delete local s3 files
            if not keep_s3_file:
                common.delete_files(local_s3_file_list)
        p += datetime.timedelta(hours=1)

    # exit()
    # 执行 SQL
    local_mysql_auth = config.local_mysql_auth

    common.execute_mysql_sql(
        local_mysql_auth['host'],
        local_mysql_auth['port'],
        local_mysql_auth['user'],
        local_mysql_auth['passwd'],
        local_mysql_auth['dbname'],
        global_tmp_sql_file
    )
    # END
    if os.path.exists(global_tmp_sql_file):
        if task['keep_sql_file']:
            logging.info("keep the tmp sql file @ %s" % global_tmp_sql_file)
        else:
            try:
                os.remove(global_tmp_sql_file)
            except Exception as e:
                logging.error("main():Delete the tmp sql file: %s:[%s]" % (global_tmp_sql_file, e))
    else:
        logging.warning("There is No tmp sql file:%s" % global_tmp_sql_file)

    return


# --------------
global_success_count = 0
global_fail_count = 0
global_table_list = []
global_file_list = []

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()
    # import parser
    # import config
    #
    # task = config.task_list['store']
    # p = parser.StoreAwsMAParser()
    # p = p.parser
    # task['app'] = {}
    # task['app']['parser_json'] = p
    # main_loop(task, ['./test.txt.gz'])
