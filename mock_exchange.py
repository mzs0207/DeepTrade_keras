#!/usr/bin/env python
# coding:utf8
"""
模拟交易所
"""
import json
import datetime

import ccxt

from messenger import Messenger


class MockExchange(object):
    """

    """

    def __init__(self):
        """

        """
        self.exchange = ccxt.bitmex()
        self.messager = Messenger()
        self.config = {}
        self.config_file = "config.json"
        self.load_config()

    def load_config(self):
        """
        加载运行中产生的数据
        :return:
        """
        with open(self.config_file) as f:
            self.config = json.load(f)

    def save_config(self):
        """
        保存运行过程中产生的数据
        :return:
        """
        print(self.config)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, sort_keys=True, indent=4, separators=(",", ":"))

    def get_last_price(self):
        """

        :return:
        """
        return self.exchange.fetch_ticker("BTC/USD")['last']

    def buy(self, price, volume):
        """

        :param price:
        :param volume:
        :return:
        """
        self.config["money"] -= price * volume
        self.config["btc"] += volume
        op = "{0} buy {2} at {1}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), price, volume)
        self.config["history"].append(op)
        self.messager.send(op)

    def sell(self, price, volume):
        """

        :param price:
        :param volume:
        :return:
        """
        self.config["money"] += price * volume
        self.config["btc"] -= volume
        op = "{0} sell {2} at {1}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), price, volume)
        self.config["history"].append(op)
        self.messager.send(op)

    def trade(self, position):
        """

        :param position: 仓位比例
        :return:
        """
        price = self.get_last_price()
        hold_value = self.config['btc'] * price
        total_value = self.config['money'] + hold_value
        need_value = total_value * position

        if need_value > hold_value:
            volume = (need_value - hold_value) / price
            print("volume:{0}, hold_value:{1},need_value:{2},price:{3},position:{4}".format( volume, hold_value, need_value,
                  price, position))
            self.buy(price, volume)
        if need_value < hold_value:
            volume = (hold_value - need_value) / price
            print("volume:{0}, hold_value:{1},need_value:{2},price:{3},position:{4}".format( volume, hold_value, need_value,
                  price, position))
            self.sell(price, volume)
        self.save_config()


if __name__ == '__main__':
    m = MockExchange()
    m.trade(0)
