import json
import os

curpath = os.path.dirname(__file__)
data_path = curpath + "/../../data"
print(data_path)

files = os.listdir(data_path)
for file in files:
    filepath = os.path.join(data_path, file)
    data = json.load(open(filepath))
    if 20 > len(data['chartlist']):
        continue
    recent_20_day = data['chartlist'][-20:]
    vols = [t['volume'] for t in recent_20_day]
    prices = [t['close'] for t in recent_20_day]
    highs = [t['high'] for t in recent_20_day]

    today_price = prices[-1]
    yester_price = prices[-2]

    if highs[-1] <= today_price and today_price >= max(prices[:-1]) and  yester_price < max(prices[:-1]):
        print(filepath.split("/")[-1])
