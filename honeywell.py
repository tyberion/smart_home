import pandas as pd
from datetime import datetime
from evohomeclient2 import EvohomeClient

from credentials import HONEYWELL_PASSWORD, HONEYWELL_USERNAME


def get_honeywell_temps():
    client = EvohomeClient(HONEYWELL_USERNAME, HONEYWELL_PASSWORD)
    temperature = list(client.temperatures())[0]
    now = datetime.now()
    data = pd.DataFrame(temperature, index=[0])
    data = data.rename(columns={'temp': 'Temperature', 'name': 'Name', 'setpoint': 'Setpoint'})
    data['Datetime'] = now
    data['Type'] = 'Honeywell'
    return data[['Datetime', 'Type', 'Name', 'Temperature', 'Setpoint']]


if __name__ == '__main__':
    hdata = get_honeywell_temps()
