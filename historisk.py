import csv
import plotly.graph_objects as go


time_series = dict()
years = list(range(2015, 2022))
for year in years:
    with open(f"data/elspot/{year}.csv", "r") as csvfile:
        new_values = []
        market_prices = csv.reader(csvfile)
        # Finding headers
        for row in market_prices:
            if row[1] == "Hours":
                headers = row[2:]
                break
        for h in headers:
            if h not in time_series:
                time_series[h] = [[], []]
        for j, row in enumerate(market_prices):
            date_str = row[0].split("-")
            date = f"{date_str[2]}-{date_str[1]}-{date_str[0]}"
            hour = row[1][:2]
            for i, h in enumerate(headers):
                v = row[i + 2]
                value = float(v.replace(",", ".")) if v else float("nan")
                time_series[h][0].append(f"{date}T{hour}")
                time_series[h][1].append(value)


fig = go.Figure()
areas = ['Oslo', 'Molde']
for area in areas:
    area_data = time_series[area]
    fig.add_trace(
        go.Scatter(x=area_data[0], y=area_data[1], mode="lines", name=area)
    )
fig.update_traces(line_shape='hv', selector=dict(type='scatter'))
fig.update_layout(
    title="EL spot priser", xaxis_title="CEST", yaxis_title="NOK/MWh"
)
fig.write_html("historisk.html")
