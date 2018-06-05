import pandas as pd
from datetime import datetime

import netatmo
from credentials import (NETATMO_ID, NETATMO_PASSWORD, NETATMO_SECRET,
                         NETATMO_STATION_ID, NETATMO_USERNAME)


def netatmo_data():
    # credentials as parameters
    ws = netatmo.WeatherStation(
        {'client_id': NETATMO_ID,
         'client_secret': NETATMO_SECRET,
         'username': NETATMO_USERNAME,
         'password': NETATMO_PASSWORD,
         'default_station': NETATMO_STATION_ID,
         })
    ws.get_data()
    module = ws.devices[0]
    module_data = [module['dashboard_data']] + [m['dashboard_data'] for m in module['modules']]
    data = pd.DataFrame(module_data)
    data['Datetime'] = data.time_utc.apply(datetime.fromtimestamp)
    # data['module_name'] = [module['module)name']0
    data['Name'] = [module['module_name']] + [m['module_name'] for m in module['modules']]
    data['Type'] = 'Netatmo'

    return data[['Datetime', 'Type', 'Name', 'CO2', 'Humidity', 'Noise', 'Pressure', 'Temperature']]


if __name__ == '__main__':
    mdata = netatmo_data()
