from evohomeclient2 import EvohomeClient
import json
from credentials import HONEYWELL_PASSWORD, HONEYWELL_USERNAME
import pandas as pd

def get_honeywell_temps():
    client = EvohomeClient(HONEYWELL_USERNAME, HONEYWELL_PASSWORD)
    temperature = list(client.temperatures())[0]
    return pd.DataFrame(temperature, index=[0])

if __name__ == '__main__':

    df = get_honeywell_temps()
