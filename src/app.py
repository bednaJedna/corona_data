from typing import Any, Dict, List

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import pandas as p
import plotly.graph_objects as go

from src.api import get_all_countries_data, get_map_data

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
        html.Div(id="sliderWrapper", children=[]),
        html.Div(id="mapWrapper", children=[],),
    ],
    style={"display": "flex", "flexDirection": "column"},
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


def slider(data: Any) -> Any:
    data: Any = p.DataFrame.from_dict(data)
    columns: List[str] = data.columns[4:]
    return dcc.Slider(
        id="mapSlider",
        min=0,
        max=len(columns) - 1,
        step=1,
        value=len(columns) - 1,
        marks={i: label for i, label in enumerate(columns)},
    )


def prep_map_data(data: Any, col: int) -> Any:
    data: Any = p.DataFrame.from_dict(data)
    desc_cols: Any = data.iloc[:, :3]
    data_col: Any = data.iloc[:, col]
    data = p.concat([desc_cols, data_col], axis=1)
    data.columns = ["Country", "Lat", "Long", "ConfirmedCases"]
    return data


def map_(data: Any) -> Any:
    fig: Any = go.Figure(
        go.Densitymapbox(lat=data.Lat, lon=data.Long, z=data.ConfirmedCases, radius=50,)
    )
    fig.update_layout(
        mapbox_style="stamen-terrain", mapbox_center_lon=25, mapbox_center_lat=41
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(mapbox={"zoom": 2})
    return dcc.Graph(id="heatMap", figure=fig)


app.layout = html.Div(
    id="mainBodyWrapper",
    children=[
        html.Div(
            id="helperWrapper",
            children=[
                dcc.Interval(
                    id="interval-component", interval=(60 * 10 * 1000), n_intervals=0
                ),
                dcc.Store(id="mapDataStorage", storage_type="local"),
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


@app.callback(
    Output("mapDataStorage", "data"), [Input("tabs", "value")],
)
def update_map_data(value: str) -> Any:
    if value == "tab-2":
        return get_map_data().to_dict("records")
    else:
        PreventUpdate()


@app.callback(Output("sliderWrapper", "children"), [Input("mapDataStorage", "data")])
def create_slider(data: Any) -> Any:
    return slider(data)


@app.callback(
    Output("mapWrapper", "children"),
    [Input("mapSlider", "value"), Input("mapDataStorage", "data")],
)
def render_map(value: int, data: dict) -> Any:
    if data is not None:
        data: Any = prep_map_data(data, value)
        return map_(data)
    else:
        PreventUpdate()
