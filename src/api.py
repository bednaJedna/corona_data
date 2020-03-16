import requests as r
import pandas as p
import json
from typing import Text, Any

API_BASE = "https://coronavirus-19-api.herokuapp.com/"


def get_all_countries_data() -> Any:
    reurl: Text = f"{API_BASE}countries"
    result: Any = r.get(reurl)

    return p.read_json(json.dumps(result.json(), ensure_ascii=False))


if __name__ == "__main__":
    print(get_all_countries_data())
