from typing import Any, Dict, List

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import pandas as p
from pandas.api.types import is_string_dtype
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

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
    id="visualWrapper",
    children=[
        html.Div(
            id="sliderWrapper",
            children=[],
            style={"marginTop": "10px", "marginBottom": "40px"},
        ),
        html.Div(id="mapWrapper", children=[],),
        html.Div(
            id="plotUnitWrapper",
            children=[
                html.Div(
                    id="dropdownWrapper",
                    children=[],
                    style={"marginTop": "10px", "marginBottom": "40px"},
                ),
                html.Div(id="linePlotWrapper", children=[]),
            ],
        ),
    ],
    style={"display": "flex", "flexDirection": "column", "justifyContent": "center"},
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
    data = p.DataFrame.from_dict(data)
    columns: List[str] = data.columns[3:]
    return dcc.Slider(
        id="mapSlider",
        min=0,
        max=len(columns) - 1,
        step=1,
        value=len(columns) - 1,
        marks={
            i: {"label": label, "style": {"writingMode": "vertical-rl"}}
            for i, label in enumerate(columns)
        },
    )


def prep_map_data(data: Any, col: int) -> Any:
    data = p.DataFrame.from_dict(data)
    desc_cols: Any = data.iloc[:, :3]
    # col + 3 => because when doing slider, we had to cut away first three columns
    data_col: Any = data.iloc[:, col + 3]
    data = p.concat([desc_cols, data_col], axis=1)
    data.columns = ["Country", "Lat", "Long", "ConfirmedCases"]
    return data


def map_(data: Any) -> Any:
    fig: Any = go.Figure(
        go.Densitymapbox(
            name="Confirmed",
            lat=data.Lat,
            lon=data.Long,
            z=data.ConfirmedCases,
            radius=40,
            hovertext=list(data.Country),
            hoverinfo="all",
        )
    )
    fig.update_layout(
        mapbox_style="carto-positron", mapbox_center_lon=25, mapbox_center_lat=41
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(mapbox={"zoom": 2})

    # this works, but it looks ugly :( will stick to density map
    # just for the better looks :)
    # fig: Any = px.scatter_geo(
    #     data,
    #     lat=data.Lat,
    #     lon=data.Long,
    #     color=data.ConfirmedCases,
    #     hover_name=data.Country,
    #     size=data.ConfirmedCases,
    #     projection="kavrayskiy7",
    #     scope="world",
    #     size_max=40,
    #     width=1920,
    #     height=720,
    # )
    return dcc.Graph(id="heatMap", figure=fig)


def dropdown(countries: List[str]) -> Any:
    return dcc.Dropdown(
        id="countrySelector",
        options=[{"label": country, "value": country} for country in countries],
        value=["Czechia"],
        multi=True,
        persistence=True,
        persistence_type="local",
    )


def line_plot(data: Any) -> Any:
    diff_data: Any = data.diff(axis=1)
    diff_x: List[str] = diff_data.columns[1:]
    x: List[str] = data.columns[1:]

    fig: Any = make_subplots(specs=[[{"secondary_y": True}]])
    for row in data.iterrows():
        fig.add_trace(
            go.Scatter(
                x=x, y=row[1][1:], name=f"Total count: {row[0]}", line={"width": 4}
            ),
            secondary_y=False,
        )
    for drow in diff_data.iterrows():
        fig.add_trace(
            go.Bar(
                x=diff_x, y=drow[1][1:], name=f"Daily change: {drow[0]}", opacity=0.6
            ),
            secondary_y=True,
        )
    fig.update_layout(
        title="Confirmed Coronavirus Cases Development",
        xaxis_title="Day",
        yaxis_title="Confirmed Cases: Total Count",
        showlegend=True,
    )
    fig.update_yaxes(title_text="Confirmed Cases: Daily Change", secondary_y=True)

    return dcc.Graph(id="linePlot", figure=fig)


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
    [
        Input("mapSlider", "value"),
        Input("mapDataStorage", "data"),
        Input("tabs", "value"),
        Input("sliderWrapper", "children"),
    ],
)
def render_map(value: int, data: dict, tab_name: str, slider_wrap_child: Any) -> Any:
    if (data is not None) and (tab_name == "tab-2") and (slider_wrap_child is not []):
        data = prep_map_data(data, value)
        return map_(data)
    else:
        PreventUpdate()


@app.callback(
    Output("dropdownWrapper", "children"),
    [Input("mapDataStorage", "data"), Input("tabs", "value"),],
)
def create_dropdown(data: dict, tab: str) -> Any:
    if (data is not None) and (tab == "tab-2"):
        countries_list: Any = p.DataFrame.from_dict(data).groupby(
            "Country/Region"
        ).sum().reset_index().iloc[:, 0]
        return dropdown(countries_list)
    else:
        PreventUpdate


@app.callback(
    Output("linePlotWrapper", "children"),
    [
        Input("countrySelector", "value"),
        Input("tabs", "value"),
        Input("mapDataStorage", "data"),
        Input("dropdownWrapper", "children"),
    ],
)
def render_line_plot(
    dropdown_val: List[str], tab_val: str, data: Any, dropdown_wrap: dict
):
    if (
        (dropdown_val is not [])
        and (tab_val == "tab-2")
        and (data is not None)
        and (dropdown_wrap is not [])
    ):
        data = p.DataFrame.from_dict(data)
        data = (
            p.concat([data.iloc[:, 0], data.iloc[:, 3:]], axis=1)
            .groupby("Country/Region")
            .sum()
            .reset_index()
        )
        data = data.set_index(data.iloc[:, 0], drop=False)
        data = data.rename(columns={"Country/Region": "Country"})
        rows: List[Any] = data.loc[dropdown_val]
        return line_plot(rows)

    else:
        PreventUpdate
