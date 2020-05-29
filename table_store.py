#!/usr/bin/env python
# coding:utf8
"""
使用阿里云的 tablestore 存储
"""
from tablestore import OTSClient, Row, Condition, RowExistenceExpectation, OTSClientError, OTSServiceError

from secret_config import *


def save_predict(time, symbol, percent):
    """

    :param time:
    :param symbol:
    :param percent:
    :return:
    """
    end_point = "https://deep-trade.cn-hangzhou.ots.aliyuncs.com"
    instance_name = "deep-trade"
    table_name = "t_singal"

    ots_client = OTSClient(end_point, table_store_access_key, table_store_access_secret, instance_name)
    primary_key = [('day', time), ('symbol', symbol)]
    attribute_columns = [('percent', percent)]
    row = Row(primary_key, attribute_columns)
    condition = Condition(RowExistenceExpectation.EXPECT_NOT_EXIST)

    try:
        # 调用put_row方法，如果没有指定ReturnType，则return_row为None。
        consumed, return_row = ots_client.put_row(table_name, row, condition)

        # 打印出此次请求消耗的写CU。
        print('put row succeed, consume %s write cu.' % consumed.write)
        # 客户端异常，一般为参数错误或者网络异常。
    except OTSClientError as e:
        print(
            "put row failed, http_status:%d, error_message:%s" % (e.get_http_status(), e.get_error_message()))
        # 服务端异常，一般为参数错误或者流控错误。
    except OTSServiceError as e:
        print(
            "put row failed, http_status:%d, error_code:%s, error_message:%s, request_id:%s" % (
                e.get_http_status(), e.get_error_code(), e.get_error_message(), e.get_request_id()))


if __name__ == '__main__':
    save_predict(2020052910, "btc", 1)
