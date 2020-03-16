from typing import Any

import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

from src.api import get_all_countries_data

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

data: Any = get_all_countries_data()

app: Any = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    id="mainWrapper",
    children=[
        html.Div(
            id="tableWrapper",
            children=[
                dash_table.DataTable(
                    id="table",
                    columns=[{"name": i, "id": i} for i in data.columns],
                    data=data.to_dict("records"),
                    filter_action="native",
                    sort_action="native",
                    column_selectable="multi",
                )
            ],
        ),
        html.Div(
            id="helperWrapper",
            children=[
                dcc.Interval(
                    id="interval-component", interval=(60 * 60 * 1000), n_intervals=0
                )
            ],
        ),
    ],
)


@app.callback(
    Output("tableWrapper", "children"), [Input("interval-component", "n_intervals")]
)
def update_data(n_intervals: int) -> Any:
    data: Any = get_all_countries_data()
    return dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i} for i in data.columns],
        data=data.to_dict("records"),
        filter_action="native",
        sort_action="native",
        column_selectable="multi",
    )
