#! /usr/bin/env python2
# -*- coding:utf-8 -*-
import os


def create_table_push_raw(tmp_sql_file, table_name):
    create_sql = '''
        CREATE TABLE IF NOT EXISTS `{table_name}` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `time` datetime NOT NULL,
            `client_time` datetime DEFAULT NULL,
            `arrival_time` datetime DEFAULT NULL,
            `client_id` varchar(255) DEFAULT NULL,
            `device_id` varchar(255) DEFAULT NULL,
            `country` varchar(5) NOT NULL,
            `ip_country` varchar(5)  NOT NULL,
            `sim_country` varchar(5)  NOT NULL,
            `lang` varchar(5) NOT NULL,
            `brand` varchar(20) NOT NULL,
            `model` varchar(100) NOT NULL,
            `os_version` varchar(20) NOT NULL,
            `app_type` varchar(20) NOT NULL,
            `push_count` int(10) unsigned NOT NULL,
            `msg_id` int(10) unsigned NOT NULL,
            `mid` int(10) unsigned NOT NULL,
            `push_type` varchar(20) NOT NULL,
            `fetch_img_status` tinyint(3) unsigned NOT NULL,
            `event_type` varchar(20) NOT NULL,
            `hash` char(64) NOT NULL,
            `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
            `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (`id`),
            UNIQUE KEY `hash` (`hash`),
            KEY `time` (`time`),
            KEY `country` (`country`),
            KEY `lang` (`lang`),
            KEY `brand` (`brand`),
            KEY `model` (`model`),
            KEY `os_version` (`os_version`),
            KEY `app_type` (`app_type`),
            KEY `push_count` (`push_count`),
            KEY `msg_id` (`msg_id`),
            KEY `mid` (`mid`),
            KEY `push_type` (`push_type`),
            KEY `fetch_img_status` (`fetch_img_status`),
            KEY `event_type` (`event_type`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    '''.format(table_name=table_name)

    if not tmp_sql_file:
        return create_sql

    with open(tmp_sql_file, 'a') as f:
        f.write(create_sql)


def create_table_store_raw(tmp_sql_file, table_name):
    create_sql = '''
        CREATE TABLE IF NOT EXISTS `{table_name}` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `time` datetime NOT NULL,
          `client_time` datetime DEFAULT NULL,
          `arrival_time` datetime DEFAULT NULL,
          `client_id` varchar(255) DEFAULT NULL,
          `device_id` varchar(255) DEFAULT NULL,
          `country` varchar(5)  NOT NULL,
          `ip_country` varchar(5)  NOT NULL,
          `sim_country` varchar(5)  NOT NULL,
          `lang` varchar(5)  NOT NULL,
          `brand` varchar(20)  NOT NULL,
          `model` varchar(100)  NOT NULL,
          `os_version` varchar(20)  NOT NULL,
          `app_type` varchar(20)  NOT NULL,
          `open_count` int(10) unsigned NOT NULL,
          `store_version` varchar(20)  NOT NULL,
          `store_item_type` varchar(20)  NOT NULL,
          `pkg_name` varchar(100)  NOT NULL,
          `event_type` varchar(20)  NOT NULL,
          `hash` char(64) NOT NULL,
          `created_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
          `updated_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          UNIQUE KEY `hash` (`hash`),
          KEY `time` (`time`),
          KEY `country` (`country`),
          KEY `lang` (`lang`),
          KEY `brand` (`brand`),
          KEY `model` (`model`),
          KEY `os_version` (`os_version`),
          KEY `app_type` (`app_type`),
          KEY `open_count` (`open_count`),
          KEY `store_version` (`store_version`),
          KEY `store_item_type` (`store_item_type`),
          KEY `pkg_name` (`pkg_name`),
          KEY `event_type` (`event_type`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    '''.format(table_name=table_name)

    if not tmp_sql_file:
        return create_sql

    with open(tmp_sql_file, 'a') as f:
        f.write(create_sql)


def create_table_dimension_enum(tmp_sql_file, table_name):
    create_sql = '''
        CREATE TABLE IF NOT EXISTS `{table_name}` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `category` varchar(20) NOT NULL COMMENT 'eg:push,store',
          `dimension_name` varchar(20) NOT NULL,
          `dimension_value` varchar(100) NOT NULL,
          PRIMARY KEY (`id`),
          UNIQUE KEY `unique` (`category`, `dimension_name`, `dimension_value`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    '''.format(table_name=table_name)

    if not tmp_sql_file:
        return create_sql

    with open(tmp_sql_file, 'a') as f:
        f.write(create_sql)


def create_table_push_summary(tmp_sql_file, table_name):
    create_sql = '''
        CREATE TABLE IF NOT EXISTS `{table_name}` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `time` timestamp NULL DEFAULT NULL,
            `dimension_1_name` varchar(20) DEFAULT NULL COMMENT 'first dimension name',
            `dimension_1_value` varchar(100) DEFAULT NULL COMMENT 'first dimension value,',
            `dimension_2_name` varchar(20) DEFAULT NULL COMMENT 'second dimension name',
            `dimension_2_value` varchar(100) DEFAULT NULL COMMENT 'second dimension value',
            `pull_count` int(11) DEFAULT NULL COMMENT 'negative means value out of range',
            `pv` int(11) DEFAULT '0' COMMENT 'the total count of show message to user',
            `uv` int(11) DEFAULT '0' COMMENT 'unique user view count',
            `clicks` int(11) DEFAULT '0' COMMENT 'the count of user click message',
            `ctr` float DEFAULT '0' COMMENT 'click count divided by  pull count',
            PRIMARY KEY (`id`),
            UNIQUE KEY `unique` (`time`,`dimension_1_name`,`dimension_1_value`,`dimension_2_name`,`dimension_2_value`),
            KEY `time` (`time`),
            KEY `dimension_1_name` (`dimension_1_name`),
            KEY `dimension_1_value` (`dimension_1_value`),
            KEY `dimension_2_name` (`dimension_2_name`),
            KEY `dimension_2_value` (`dimension_2_value`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    '''.format(table_name=table_name)

    if not tmp_sql_file:
        return create_sql

    with open(tmp_sql_file, 'a') as f:
        f.write(create_sql)


def create_table_store_summary(tmp_sql_file, table_name):
    create_sql = '''
        CREATE TABLE IF NOT EXISTS `{table_name}` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `time` timestamp NULL DEFAULT NULL,
            `dimension_1_name` varchar(20) DEFAULT NULL COMMENT 'first dimension name',
            `dimension_1_value` varchar(100) DEFAULT NULL COMMENT 'first dimension value,',
            `dimension_2_name` varchar(20) DEFAULT NULL COMMENT 'second dimension name',
            `dimension_2_value` varchar(100) DEFAULT NULL COMMENT 'second dimension value',
            `pv` int(11) DEFAULT '0' COMMENT 'the total count of show message to user',
            `uv` int(11) DEFAULT '0' COMMENT 'unique user view count',
            `clicks` int(11) DEFAULT '0' COMMENT 'the count of user click message',
            `ctr` float DEFAULT '0' COMMENT 'click count divided by  pull count',
            PRIMARY KEY (`id`),
            UNIQUE KEY `unique` (`time`,`dimension_1_name`,`dimension_1_value`,`dimension_2_name`,`dimension_2_value`),
            KEY `time` (`time`),
            KEY `dimension_1_name` (`dimension_1_name`),
            KEY `dimension_1_value` (`dimension_1_value`),
            KEY `dimension_2_name` (`dimension_2_name`),
            KEY `dimension_2_value` (`dimension_2_value`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    '''.format(table_name=table_name)

    if not tmp_sql_file:
        return create_sql

    with open(tmp_sql_file, 'a') as f:
        f.write(create_sql)


if __name__ == '__main__':
    print create_table_store_raw(None, 'store_raw_20170522_13')
