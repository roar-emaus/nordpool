import json
import plotly
plotly.io.orca.config.executable = '/home/roar/projects/nordpool/__pypackages__/3.9/bin/orca'
import plotly.graph_objects as go


with open('data/elspot/day_price.html') as f:
    data = json.load(f)
    rows = data['data']['Rows']
    time_series = {col['Name']: [[], []] for col in rows[0]['Columns']}
    for row in rows:
        t = row['StartTime']
        if row['IsExtraRow']:
            break
        columns = row['Columns']
        for col in columns:
            time_series[col['Name']][0].append(t)
            time_series[col['Name']][1].append(float(col['Value'].replace(',','.')))


fig = go.Figure()
areas = ['Oslo', 'Molde']
for area in areas:
    area_data = time_series[area]
    fig.add_trace(
        go.Scatter(x=area_data[0], y=area_data[1], mode="lines+markers",  name=area)
    )
fig.update_traces(line_shape='hv', selector=dict(type='scatter'))
fig.update_layout(
    title="Morgendages ELSpot priser", xaxis_title="CEST", yaxis_title="NOK/MWh"
)
fig.write_html("morgendagens.html")
fig.write_image('morgendagens.png', width=1920, height=1080)
