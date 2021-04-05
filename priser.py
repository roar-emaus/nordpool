import csv
import numpy as np
import matplotlib.pyplot as plt


time_series = dict()
with open('data/elspot/2021.csv', 'r') as csvfile: 
    new_values = []
    market_prices = csv.reader(csvfile)
    # Finding headers
    for row in market_prices:
        if row[1] == 'Hours':
            headers = row[2:]
            break

    time_series = {h: [[], []] for h in headers}
    for j, row in enumerate(market_prices):
        date_str = row[0].split('-')
        date = f'{date_str[2]}-{date_str[1]}-{date_str[0]}'
        hour = row[1][:2]
        for i, h in enumerate(headers):
            v = row[i + 2]
            value = float(v.replace(',','.')) if v else float('nan')
            time_series[h][0].append(f'{date}T{hour}')
            time_series[h][1].append(value)


t = np.array(time_series['Oslo'][0], dtype='datetime64')
v = np.array(time_series['Oslo'][1])

plt.plot(t, v)
plt.show()
