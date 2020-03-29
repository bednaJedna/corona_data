# Coronavirus data overview

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Used API](#api)
- [Special Thanks](#thanks)
- [Authors](#authors)

## About <a name = "about"></a>

Simple interactive table overview of Coronavirus data per country. Data refreshes via API call once per hour. That does not mean, that data are updated on the data source side as well.

Heat map of the confirmed cases is available now, but it is not refreshed automatically. Data are provided semi-daily, so it is not needed so much.

Line plot chart of the confirmed cases together with daily changes is available now. Again, due to semi-daily update, data refresh is not automatic.

News tab is now available. Displays Top Headlines provided by https://newsapi.org/. You need to generate your own API key and implement it in the _api.py_. This tab uses Dash DataTable component. URL links are currently not clickable directly - doublick on them and go to to the site via right mouse button option.

## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Have Python 3.+ and some modern browser installed.

### Installing

1. Run "[sudo] python setup.py install" in the shell with admin privileges

## Usage <a name = "usage"></a>

1. Run "python run.py"
2. Wait for init of the app - open provided link from the console in the browser
3. Profit

## Used API <a name = "api"></a>

Heat map Data are fetched from https://coronavirus-19-api.herokuapp.com/countries

Lineplot Data are fetched from https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv

News data are fetched using https://newsapi.org/

## Special thanks <a name = "thanks"></a>

Thank god for <a href="https://pandas.pydata.org/" target="_blank">pandas</a> and <a href="https://dash.plotly.com/" target="_blank">Dash</a>.

You can do awesome things with those.

## Authors <a name="authors"></a>

bednaJedna (sometimes pushing as dzcxs6c, since he can be a not very bright one when messing with Git config ... :/)
