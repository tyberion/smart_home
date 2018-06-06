#!/opt/berryconda3/bin/python

import pandas as pd
from datetime import datetime
from sheets import get_current_worksheet, append_data, ROW_TITLES
from honeywell import get_honeywell_temps
from fetch_netatmo import netatmo_data


def read_data(date=None):
    worksheet = get_current_worksheet(date=date)
    df_data = pd.DataFrame(worksheet.get_all_records())
    df_data.Datetime = df_data.Datetime.apply(datetime.fromtimestamp)
    return df_data


def measure_data():
    hdata = get_honeywell_temps()
    ndata = netatmo_data()
    data = pd.concat([hdata, ndata])

    return data[ROW_TITLES]


def write_data(data):
    worksheet = get_current_worksheet()
    data.Datetime = data.Datetime.apply(datetime.timestamp)
    for _, row in data.iterrows():
        append_data(worksheet, row.fillna('NaN').values.tolist())


if __name__ == '__main__':
    data = measure_data()
    write_data(data)
