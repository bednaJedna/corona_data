from src.api import get_all_countries_data
import dash
import dash_table
from typing import Any


data: Any = get_all_countries_data()

app: Any = dash.Dash(__name__)

app.layout = dash_table.DataTable(
    id="table",
    columns=[{"name": i, "id": i} for i in data.columns],
    data=data.to_dict("records"),
    filter_action="native",
    sort_action="native",
    column_selectable="multi",
)

