import csv
import json
from typing import Any, Text

import pandas as p
import requests as r

API_BASE = "https://coronavirus-19-api.herokuapp.com/"
MAP_DATA = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"


def get_all_countries_data() -> Any:
    reurl: Text = f"{API_BASE}countries"
    result: Any = r.get(reurl)

    return p.read_json(json.dumps(result.json(), ensure_ascii=False))


def get_map_data() -> Any:
    return p.read_csv(MAP_DATA).iloc[:, 1:]


# if __name__ == "__main__":
#     data: Any = get_map_data()
#     print(data.head(10))
#     print(data.columns)
#     print(data.columns[3:])
#     desc_cols: Any = data.iloc[:, :3]
#     data_col: Any = data.iloc[:, len(data.columns) - 1]
#     data = p.concat([desc_cols, data_col], axis=1)
#     data.columns = ["Country", "Lat", "Long", "Confirmed Cases"]
#     print(data.head(10))
#     print(list(data.Country))
