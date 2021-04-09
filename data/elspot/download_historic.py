import os

template_url = 'https://www.nordpoolgroup.com/494bc9/globalassets/marketdata-excel-files/'
for year in range(2021, 2022):
    filename = f'elspot-prices_{year}_hourly_nok.xls'
    os.system(f'mv {filename} {filename}.bak')
    os.system(f'wget {template_url}{filename}')
    os.system(f'unoconv -f csv -o {year}.csv {filename}')

