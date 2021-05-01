import json

import numpy as np
import plotly.graph_objects as go


with open("data/elspot/day_price.html") as f:
    data = json.load(f)
    rows = data["data"]["Rows"]
    time_series = {col["Name"]: [[], []] for col in rows[0]["Columns"]}
    for row in rows:
        t = row["StartTime"]
        if row["IsExtraRow"]:
            break
        columns = row["Columns"]
        for col in columns:
            time_series[col["Name"]][0].append(t)
            time_series[col["Name"]][1].append(
                float(col["Value"].replace(" ", "").replace(",", "."))
            )


fig = go.Figure()
areas = ["Oslo", "Molde"]
annotation_kwargs = dict(
    xref="x",
    yref="y",
    showarrow=True,
    font=dict(family="Courier New, monospace", size=16, color="#ffffff"),
    align="center",
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    arrowcolor="#636363",
    ax=20,
    ay=-30,
    bordercolor="#c7c7c7",
    borderwidth=2,
    borderpad=4,
    bgcolor="#ff7f0e",
    opacity=0.8,
)

for area in areas:
    area_data = time_series[area]
    x = area_data[0]
    y = area_data[1]

    fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", name=area))

    i_max = np.argmax(y)
    i_min = np.argmin(y)

    fig.add_annotation(
        x=x[i_max],
        y=y[i_max],
        text=f"{area} max={y[i_max]}",
        **annotation_kwargs
    )
    fig.add_annotation(
            x=x[i_min],
            y=y[i_min],
            text=f"{area} min={y[i_min]}",
            **annotation_kwargs
            )

fig.update_traces(line_shape="hv", selector=dict(type="scatter"))
fig.update_layout(
    title="Morgendages ELSpot priser", xaxis_title="CEST", yaxis_title="NOK/MWh"
)
fig.write_html("morgendagens.html")


if False:
    import plotly

    plotly.io.orca.config.executable = (
        "/home/roar/projects/nordpool/__pypackages__/3.9/bin/orca"
    )
    fig.write_image("morgendagens.png", width=1920, height=1080)
