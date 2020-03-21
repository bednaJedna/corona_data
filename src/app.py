from typing import Any, Dict, List

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

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

tab_sheet: Any = html.Div(
    id="tabsheetWrapper", children=[html.Div(id="tableWrapper", children=[],),],
)
tab_map: Any = html.Div(
    id="mapsheetWrapper",
    children=[
        html.Div(
            id="storageWrapper",
            children=[dcc.Store(id="mapDataStorage", storage_type="session"),],
        ),
        html.Div(id="mapWrapper", children=[],),
        html.Div(id="sliderWrapper", children=[]),
    ],
    style={"display": "flex", "flex-direction": "column"},
)

app: Any = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
)


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
    id="mainBodyWrapper",
    children=[
        html.Div(
            id="helperWrapper",
            children=[
                dcc.Interval(
                    id="interval-component", interval=(60 * 10 * 1000), n_intervals=0
                )
            ],
        ),
        html.Div(
            id="tabsWrapper",
            children=[
                dcc.Tabs(
                    id="tabs",
                    value="tab-1",
                    children=[
                        dcc.Tab(label="Datasheet", value="tab-1"),
                        dcc.Tab(label="Charts", value="tab-2"),
                    ],
                )
            ],
        ),
        html.Div(id="content", children=[]),
    ],
)


@app.callback(Output("content", "children"), [Input("tabs", "value")])
def render_content(value: str) -> Any:
    if value == "tab-1":
        return tab_sheet
    elif value == "tab-2":
        return tab_map


@app.callback(
    Output("tableWrapper", "children"),
    [Input("interval-component", "n_intervals"), Input("tabs", "value")],
)
def update_data(n: int, value: str) -> Any:
    if value == "tab-1":
        return get_data_table()
    else:
        PreventUpdate()
