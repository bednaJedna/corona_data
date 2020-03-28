import csv
import json
from typing import Any, Text

import pandas as p
import requests as r

API_BASE = "https://coronavirus-19-api.herokuapp.com/"
MAP_DATA = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"


def get_all_countries_data() -> Any:
    reurl: Text = f"{API_BASE}countries"
    result: Any = r.get(reurl)

    return p.read_json(json.dumps(result.json(), ensure_ascii=False))


def get_map_data() -> Any:
    data: Any = p.read_csv(MAP_DATA)
    data["Province/State"] = data["Province/State"].where(
        data["Province/State"].notna(), "", axis=0
    )
    data["Province/State"] = data["Province/State"].str.cat(
        data["Country/Region"], sep=" "
    )

    china: Any = data.loc[(data["Country/Region"] == "China")]
    china = china.set_index(china["Province/State"], drop=False)

    g_china = china.groupby("Country/Region").sum().reset_index()
    g_china["Lat"] = china.at["Hubei China", "Lat"]
    g_china["Long"] = china.at["Hubei China", "Long"]
    g_china = g_china.rename(columns={"Country/Region": "Province/State"})

    data = data.append(g_china, ignore_index=True)

    return p.concat([data.iloc[:, 0], data.iloc[:, 2:]], axis=1)
