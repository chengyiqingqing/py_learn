#! /usr/bin/env python2
# -*- coding:utf-8 -*-
import os
import sys
import datetime
import logging
import config
import common
import create_table


def update_dimension_enum(origin_table_name, target_table_name, dimension_name, category):
    if dimension_name == 'global':
        return None
    sql = '''
        INSERT IGNORE INTO  `{target_table_name}` (
                `category`,`dimension_name`,`dimension_value`
            )
            SELECT DISTINCT '{category}', '{dimension_name}',`{dimension_name}`
            FROM `{origin_table_name}`;
    '''.format(origin_table_name=origin_table_name,
               target_table_name=target_table_name,
               dimension_name=dimension_name,
               category=category)

    return sql


def compute_dimension_enum(origin_table_name, target_table_name, dimension_name_list, category):
    sql_list = []
    for dimension_name in dimension_name_list:
        sql = update_dimension_enum(origin_table_name, target_table_name, dimension_name, category)
        sql_list.append(sql)
    return sql_list


def update_metric(origin_table_name, summary_table_name,
                  p_time, duration, event_type,
                  dimension_1_name, dimension_2_name, metric_name):
    # p_time is datetime.datetime
    # start of time range
    t_start = ''
    # end of time range
    t_end = ''
    # the time for summary
    t_time = ''

    if duration == 'hour':
        t_time = p_time.strftime('%Y-%m-%d %H:00:00')
        t_start = t_time
        t_end = p_time.strftime('%Y-%m-%d %H:59:59')
    elif duration == 'day':
        t_time = p_time.strftime('%Y-%m-%d 00:00:00')
        t_start = t_time
        t_end = p_time.strftime('%Y-%m-%d 23:59:59')
    else:
        logging.error('update_metric():bad param `duration`:[%s]' % duration)
        return None

    # handle dimension_name is global

    if dimension_1_name == 'global':
        dimension_1_value = " 'global' "
    else:
        dimension_1_value = " `%s` " % dimension_1_name

    if dimension_2_name == 'global':
        dimension_2_value = " 'global' "
    else:
        dimension_2_value = " `%s` " % dimension_2_name

    # handle uv or not
    if metric_name == 'uv':
        distinct_value = ' distinct '
    else:
        distinct_value = ''

    insert_empty_sql = '''
        INSERT IGNORE INTO `{summary_table_name}` (
                `time`,
                `dimension_1_name`,
                `dimension_2_name`,
                `dimension_1_value`,
                `dimension_2_value` 
            )
            SELECT distinct '{time}',
                '{dimension_1_name}',
                '{dimension_2_name}',
                {dimension_1_value},
                {dimension_2_value}
            FROM `{origin_table_name}`
            WHERE `time` >= '{t_start}' AND `time` <= '{t_end}';
    '''.format(origin_table_name=origin_table_name,
               summary_table_name=summary_table_name,
               time=t_time,
               t_start=t_start,
               t_end=t_end,
               dimension_1_name=dimension_1_name,
               dimension_2_name=dimension_2_name,
               dimension_1_value=dimension_1_value,
               dimension_2_value=dimension_2_value,
               metric_name=metric_name,
               )

    update_summary_sql = '''
        UPDATE `{summary_table_name}`  as A,
            (
                SELECT '{time}' as time,
                    '{dimension_1_name}' as `dimension_1_name`,
                    '{dimension_2_name}' as `dimension_2_name`,
                    `dimension_1_value`,
                    `dimension_2_value`,
                    count(A.`client_id`) as metric
                FROM (
                        SELECT {distinct} `client_id` as `client_id`,
                                {dimension_1_value} as `dimension_1_value`,
                                {dimension_2_value} as `dimension_2_value`
                        FROM  `{origin_table_name}`
                        WHERE `time` >= '{t_start}' AND `time` <= '{t_end}'
                                AND `event_type` = '{event_type}'
                    ) as A
                GROUP BY `dimension_1_value`, `dimension_2_value`
            )as B
        SET A.`{metric_name}` = B.`metric`
        WHERE   A.`dimension_1_name` = B.`dimension_1_name` AND
                A.`dimension_1_value` = B.`dimension_1_value` AND
                A.`dimension_2_name` = B.`dimension_2_name` AND
                A.`dimension_2_value` = B.`dimension_2_value` AND
                A.`time` = B.`time` ; 
    '''.format(
        origin_table_name=origin_table_name,
        summary_table_name=summary_table_name,
        time=t_time,
        t_start=t_start,
        t_end=t_end,
        dimension_1_name=dimension_1_name,
        dimension_2_name=dimension_2_name,
        dimension_1_value=dimension_1_value,
        dimension_2_value=dimension_2_value,
        metric_name=metric_name,
        event_type=event_type,
        distinct=distinct_value
    )

    return insert_empty_sql + '\n' + update_summary_sql + '\n'


def update_summary_ctr(summary_table_name):
    sql = '''
        UPDATE `{summary_table_name}`
        SET `ctr` =  `clicks` / `pv`
        WHERE `clicks` IS NOT NULL AND `pv` IS NOT NULL AND `pv` > 0;           
    '''.format(summary_table_name=summary_table_name)
    return sql


def compute_store_summary(t_time, duration, origin_table_name, summary_table_name, dimension_1_name_list,
                          dimension_2_name_list, metric_name_list):
    # print "step into compute_store_summary()."
    sql_list = []
    for dimension_1_name in dimension_1_name_list:
        for dimension_2_name in dimension_2_name_list:
            for metric_name in metric_name_list:
                event_type = ''
                if metric_name == 'pv' or metric_name == 'uv':
                    if dimension_1_name in ['global', 'store_version']:
                        event_type = 'open_store'
                    elif dimension_1_name == 'store_item_type':
                        event_type = 'open_store_type'
                    else:
                        logging.error('compute_store_summary_daily():Cannot Compound [%s]' % [
                            metric_name, dimension_1_name, dimension_2_name])
                        continue
                elif metric_name == 'clicks':
                    event_type = 'click_to_gp'
                else:
                    logging.error('compute_store_summary_daily():Cannot Compound [%s]' % [
                        metric_name, dimension_1_name, dimension_2_name])
                    continue
                print metric_name, dimension_1_name, dimension_2_name
                sql = update_metric(origin_table_name=origin_table_name,
                                    summary_table_name=summary_table_name,
                                    p_time=t_time,
                                    duration=duration,
                                    event_type=event_type,
                                    dimension_1_name=dimension_1_name,
                                    dimension_2_name=dimension_2_name,
                                    metric_name=metric_name
                                    )
                sql_list.append(sql)
    return sql_list


def compute_push_summary(t_time, duration, origin_table_name, summary_table_name, dimension_1_name_list,
                         dimension_2_name_list, metric_name_list):
    # print "step into compute_store_summary()."
    sql_list = []
    for dimension_1_name in dimension_1_name_list:
        for dimension_2_name in dimension_2_name_list:
            for metric_name in metric_name_list:
                event_type = ''
                if metric_name == 'pull_count':
                    event_type = 'pull_msg'
                elif metric_name in ['pv', 'uv']:
                    event_type = 'show_msg'
                elif metric_name == 'clicks':
                    event_type = 'click_msg'
                else:
                    logging.error('compute_push_summary_daily():Cannot Compound [%s]' % [
                        metric_name, dimension_1_name, dimension_2_name])
                    continue
                sql = update_metric(origin_table_name=origin_table_name,
                                    summary_table_name=summary_table_name,
                                    p_time=t_time,
                                    duration=duration,
                                    event_type=event_type,
                                    dimension_1_name=dimension_1_name,
                                    dimension_2_name=dimension_2_name,
                                    metric_name=metric_name
                                    )
                sql_list.append(sql)
    return sql_list


def main():
    duration_list = ['hour', 'day']
    # parse args
    task_name_list = config.task_list.keys()
    start_time, stop_time, task_name, duration = common.parse_args(task_name_list, duration_list)
    task = config.task_list[task_name]

    # init log
    common.init_log(task['log']['filename'],
                    task['log']['debug'])

    logging.info('======\n%s\n' %
                 datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z'))
    logging.info(" TASK [%s] START ..." % task_name)

    # init t_timedelta
    t_timedelta = 'hour'
    summary_suffix_format = '_%Y%m%d'
    if duration == 'hour':
        t_timedelta = datetime.timedelta(hours=1)
        summary_suffix_format = '_hourly_%Y%m%d'
    elif duration == 'day':
        t_timedelta = datetime.timedelta(days=1)
        summary_suffix_format = '_daily_%Y%m'
    else:
        logging.info('main():bad param `duration`:%s' % duration)
        return

    # make tmp sql file
    _prefix = task['tmp_summary_sql_file_name']
    _suffix = task['tmp_summary_sql_file_name_suffix']
    global_tmp_sql_file = common.make_file_name(_prefix, _suffix)
    logging.info('Global Tmp Sql File:%s' % global_tmp_sql_file)
    # delete old same name file
    common.delete_files(global_tmp_sql_file)

    summary_dimension_1_name_list = task['summary_dimension_1_name_list']
    summary_dimension_2_name_list = task['summary_dimension_2_name_list']
    summary_metric_name_list = task['summary_metric_name_list']

    # current module ref
    this_module = sys.modules[__name__]
    # create dimension table
    create_table.create_table_dimension_enum(global_tmp_sql_file, task['dimension_table_name'])
    # summary function
    create_summary_table_function = getattr(create_table, task['create_summary_table_function'])
    compute_summary_function = getattr(this_module, task['compute_summary_function'])

    # main loop
    # save summary_table_name
    dump_table_name_list = [task['dimension_table_name']]
    # foreach time range
    p = start_time
    sql_list = []
    while p < stop_time:
        # prepare origin_table_name
        _prefix = task['raw_data_table_name']
        _suffix = task['raw_data_table_name_suffix']
        _format_suffix = p.strftime(_suffix)
        origin_table_name = '%s%s' % (_prefix, _format_suffix)
        print 'origin_table_name', origin_table_name

        # prepare summary_table_name
        _prefix = task['summary_data_table_name']
        _format_suffix = p.strftime(summary_suffix_format)
        summary_table_name = '%s%s' % (_prefix, _format_suffix)
        # save summary_table_name
        dump_table_name_list.append(summary_table_name)

        # create summary table
        tmp_sql = create_summary_table_function(None, summary_table_name)
        sql_list.append(tmp_sql)

        # summary compute sql
        tmp_sql_list = compute_summary_function(p, duration,
                                                origin_table_name, summary_table_name,
                                                summary_dimension_1_name_list,
                                                summary_dimension_2_name_list,
                                                summary_metric_name_list
                                                )
        sql_list += tmp_sql_list

        # compute ctr
        tmp_sql = update_summary_ctr(summary_table_name)
        sql_list.append(tmp_sql)

        # extract dimension_enum
        category = task['category']
        dimension_name_list = list(set(summary_dimension_1_name_list + summary_dimension_2_name_list))
        tmp_sql_list = compute_dimension_enum(origin_table_name,
                                              task['dimension_table_name'],
                                              dimension_name_list,
                                              category
                                              )
        sql_list += tmp_sql_list

        # next
        p += t_timedelta
    # End While

    # filter duplication sql or None
    good_sql_list = []
    for sql in sql_list:
        if not sql or not isinstance(sql, (unicode, str)) \
                or sql in good_sql_list:
            continue
        good_sql_list.append(sql)

    # write sql to file
    with open(global_tmp_sql_file, 'a') as f:
        big_sql = '\n'.join(good_sql_list)
        f.write(big_sql)
        f.write('\n')

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

    # clean some files
    if os.path.exists(global_tmp_sql_file):
        if task['keep_summary_sql_file']:
            logging.info("keep the tmp sql file @ %s" % global_tmp_sql_file)
        else:
            try:
                os.remove(global_tmp_sql_file)
            except Exception as e:
                logging.error("main():Delete the tmp sql file: %s:[%s]" % (global_tmp_sql_file, e))
    else:
        logging.warning("There is No tmp sql file:%s" % global_tmp_sql_file)

    # dump to summary data to remote server
    _prefix = task['mysql_dump_file_name']
    _suffix_fmt = task['mysql_dump_file_name_suffix']
    dump_file_name = common.make_file_name(_prefix, _suffix_fmt)
    common.delete_files(dump_file_name)

    local_mysql_auth = config.local_mysql_auth
    dump_table_name_list = list(set(dump_table_name_list))

    # dump tables into dump file
    for dump_table_name in dump_table_name_list:
        common.execute_mysql_dump(
            local_mysql_auth['host'],
            local_mysql_auth['port'],
            local_mysql_auth['user'],
            local_mysql_auth['passwd'],
            local_mysql_auth['dbname'],
            dump_table_name,
            dump_file_name
        )

    # 执行 Dump SQL
    remote_mysql_auth = config.remote_mysql_auth
    common.execute_mysql_sql(
        remote_mysql_auth['host'],
        remote_mysql_auth['port'],
        remote_mysql_auth['user'],
        remote_mysql_auth['passwd'],
        remote_mysql_auth['dbname'],
        dump_file_name
    )

    if task['keep_mysql_dump_file']:
        logging.info("keep the Dump sql file @ %s" % global_tmp_sql_file)
    else:
        common.delete_files(dump_file_name)

    # End
    return


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()
