from typing import Any, List, Dict

import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

from src.api import get_all_countries_data

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

data: Any = get_all_countries_data()

app: Any = dash.Dash(__name__, external_stylesheets=external_stylesheets)

cell_style: List[Any] = [
    {"if": {"column_id": c}, "textAlign": "left"} for c in ["Date", "Region"]
]
data_style: List[Any] = [
    {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)",}
]
header_style: Dict[str, str] = {
    "backgroundColor": "rgb(230, 230, 230)",
    "fontWeight": "bold",
}

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
                    style_cell_conditional=cell_style,
                    style_data_conditional=data_style,
                    style_header=header_style,
                )
            ],
        ),
        html.Div(
            id="helperWrapper",
            children=[
                dcc.Interval(
                    id="interval-component", interval=(10 * 60 * 1000), n_intervals=0
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
        style_cell_conditional=cell_style,
        style_data_conditional=data_style,
        style_header=header_style,
    )
