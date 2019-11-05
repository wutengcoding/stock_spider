import json
import os
import math
import random

curpath = os.path.dirname(__file__)
data_path = curpath + "/../../data"
print(data_path)

files = os.listdir(data_path)

'''
    anchor表示锚定的是多少天之前的样本
'''
class Strategy:
    total_profit = 0
    total_share = 0

    def shuffle(self, position_tw=10):
        for i in range(100):
            file = random.choice(files)
            filepath = os.path.join(data_path, file)
            data = json.load(open(filepath))
            closes = [t['close'] for t in data['chartlist']]
            macds = [t['macd'] for t in data['chartlist']]
            if len(closes) > position_tw:
                buy_index = random.randint(0, len(closes)-1 - position_tw)
                if macds[buy_index] > 0:
                    self.total_profit = (closes[buy_index+position_tw] - closes[buy_index]) / closes[buy_index]
                    self.total_share += 1
                    print("stock id: {}, buy position: {}, sale position: {}".format(filepath.split("/")[-1], closes[buy_index], closes[buy_index+position_tw]))


    def method(self, ws=20, wait_ws=4, position_tw=3, anchor_index=10):
        for file in files:
            filepath = os.path.join(data_path, file)
            try:
                data = json.load(open(filepath))
            except:
                print("parse error ", filepath)
            # 选择anchor-index天前的样本
            anchor_data = data['chartlist'][:-anchor_index]
            if anchor_index == 0:
                anchor_data = data['chartlist']

            if len(anchor_data) <= ws + wait_ws + position_tw:
                continue

            train_tw, eval_tw = anchor_data[:-position_tw], anchor_data[-position_tw:]
            if position_tw == 0:    # not buy, just predict
                train_tw, eval_tw = anchor_data, []

            recent_ts_day = train_tw[-(ws+wait_ws): -wait_ws]
            vols = [t['volume'] for t in recent_ts_day]
            closes = [t['close'] for t in recent_ts_day]
            highs = [t['high'] for t in recent_ts_day]
            macd = [t['macd'] for t in recent_ts_day]

            train_vols = [t['volume'] for t in train_tw]
            train_closes = [t['close'] for t in train_tw]

            cur_close = closes[-1]
            yester_price = closes[-2]

            '''
                1. 当天close是盘中最高  highs[-1] <= cur_close
                2. 当天close是tw内最高    cur_close >= max(closes[:-1])
                3. 前1天close不是tw内最高  yester_price < max(closes[:-1])
                4. 3天后量不超过突破当天  max(train_vols[-last:]) < vols[-1]
                                    and abs(min(train_closes[-wait_ws:]) - cur_close) / cur_close <= 0.1\

            '''
            if cur_close >= max(closes[:-1]) \
                    and yester_price < max(closes[:-1]) \
                    and max(train_vols[-wait_ws:]) < vols[-1] \
                    and vols[-1] / max(vols[-5: -1]) >= 1.3 \
                    and macd[-1] > 0:
                # buy in close price
                if position_tw > 0:
                    buy_position = eval_tw[0]['open']
                    end_position = eval_tw[-1]['close']
                    cut_intime = False
                    for p in eval_tw:
                        # if p['close'] > buy_position and (p['close'] - buy_position) / buy_position >= 0.08:
                        #     self.total_profit += (p['close']-buy_position)/buy_position
                        #     self.total_share += 1
                        #     print('Reach profit', filepath.split("/")[-1], " profit is ", (p['close']-buy_position)/buy_position)
                        #     break
                        if p['close'] < buy_position and abs(p['close'] - buy_position) / buy_position >= 0.04:
                            self.total_profit += (p['close'] - buy_position) / buy_position
                            self.total_share += 1
                            print('Reach cut', filepath.split("/")[-1], " profit is ", (p['close'] - buy_position) / buy_position)
                            cut_intime = True
                            break

                    if not cut_intime:

                        self.total_profit += (end_position - buy_position) / buy_position
                        self.total_share += 1
                        print('Reach cut', filepath.split("/")[-1], " profit is ", (end_position - buy_position) / buy_position)

                else:
                    print(filepath.split("/")[-1])


strategy = Strategy()

def today_candiate():
    for wait_ws in range(3, 6):
        strategy.method(wait_ws=wait_ws, anchor_index=0, position_tw=0)
        print("Test index {} done".format(wait_ws))

def history_analysis():
    for anchor_index in range(1, 30):
        strategy.method(anchor_index=anchor_index)
        print("Test index {} done".format(anchor_index))

def shuffle():
    strategy.shuffle()

history_analysis()
# shuffle()
print(strategy.total_profit / strategy.total_share)