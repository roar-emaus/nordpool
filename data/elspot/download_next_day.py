import os


data_url = 'https://www.nordpoolgroup.com/api/marketdata/page/23?currency=NOK,NOK,EUR,EUR'
os.system(f'wget {data_url} -O day_price.html')
