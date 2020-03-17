from typing import Any, Dict, List

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output

from src.api import get_all_countries_data

external_stylesheets: List[str] = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
cell_style_cond: List[Any] = [{"if": {"column_id": "country"}, "textAlign": "left"}]
data_style_cond: List[Any] = [
    {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)",},
    {
        "if": {"filter_query": '{country} eq "Czechia"'},
        "backgroundColor": "#3D9970",
        "color": "white",
    },
]
cell_style: Dict[str, str] = {"textAlign": "center"}
header_style: Dict[str, str] = {
    "backgroundColor": "rgb(230, 230, 230)",
    "fontWeight": "bold",
    "textAlign": "center",
}

app: Any = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def get_data_table() -> Any:
    data: Any = get_all_countries_data()
    return dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i} for i in data.columns],
        data=data.to_dict("records"),
        filter_action="native",
        sort_action="native",
        column_selectable="multi",
        style_cell=cell_style,
        style_cell_conditional=cell_style_cond,
        style_data_conditional=data_style_cond,
        style_header=header_style,
    )


app.layout = html.Div(
    id="mainWrapper",
    children=[
        html.Div(id="tableWrapper", children=[],),
        html.Div(
            id="helperWrapper",
            children=[
                dcc.Interval(
                    id="interval-component", interval=(60 * 10 * 1000), n_intervals=0
                )
            ],
        ),
    ],
)


@app.callback(
    Output("tableWrapper", "children"), [Input("interval-component", "n_intervals")]
)
def update_data(n: int) -> Any:
    return get_data_table()
