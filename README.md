# Coronavirus data overview

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Used API](#api)

## About <a name = "about"></a>

Simple interactive table overview of Coronavirus data per country. Data refreshes via API call once per hour. That does not mean, that data are updated on the data source side as well.

Heat map of the confirmed cases is also available now, but it is not refreshed automatically. Data are provided semi-daily, so it is not needed so much.

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

Data are fetched from https://coronavirus-19-api.herokuapp.com/countries
