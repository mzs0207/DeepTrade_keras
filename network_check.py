#!/usr/bin/env python
# coding:utf8
"""
网络检测
"""

import os
import time

from messenger import Messenger


def ping():
    ''' ping 主备网络 '''
    result = os.system(u"ping -c 3 www.bitmex.com")
    # result = os.system(u"ping www.baidu.com -n 3")
    if result == 0:
        print("A网正常")
    else:
        print("网络故障")
    return result


def run():
    """

    :return:
    """
    message = Messenger()
    while True:
        try:
            r = ping()
            if r != 0:
                message.send("ping bitmex.com 不通")
        except Exception as e:
            print(e)
        time.sleep(60)


if __name__ == "__main__":
    run()
