import csv
import json
from datetime import datetime as dt
from pprint import PrettyPrinter
from typing import Any, Dict, Text

import pandas as p
import requests as r

from src.utils.private import NEWS_API_KEY

HEROKU_API_BASE = "https://coronavirus-19-api.herokuapp.com/"
NEWS_API_BASE = "https://newsapi.org/v2/everything"
MAP_DATA = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"


def _get_today() -> str:
    return dt.now().strftime("%Y-%m-%d")


def get_all_countries_data() -> Any:
    reurl: Text = f"{HEROKU_API_BASE}countries"
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


def get_news(
    q="COVID",
    from_=_get_today,
    sortBy="publishedAt",
    apiKey=NEWS_API_KEY,
    pageSize="10",
    page="1",
    language="en",
) -> Any:
    payload: Dict[str, str] = {
        "q": q,
        "from": from_,
        "sortBy": sortBy,
        "apiKey": apiKey,
        "pageSize": pageSize,
        "page": page,
        "language": language,
    }
    response: Any = r.get(NEWS_API_BASE, params=payload)

    return response.json()


if __name__ == "__main__":
    p: Any = PrettyPrinter(indent=2)
    p.pprint(get_news())
