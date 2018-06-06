from datetime import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

ROW_TITLES = ['Datetime', 'Type', 'Name', 'CO2', 'Humidity',
              'Noise', 'Pressure', 'Temperature', 'Setpoint']

SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']


def get_date_worksheet(spreadsheet, time):
    worksheet_names = [w.title for w in spreadsheet.worksheets()]

    sheet_name = time.strftime('%Y_%m')
    if sheet_name not in worksheet_names:
        spreadsheet.add_worksheet(sheet_name, 1000, len(ROW_TITLES))
        worksheet = spreadsheet.worksheet(sheet_name)
        worksheet.append_row(ROW_TITLES)
    else:
        worksheet = spreadsheet.worksheet(sheet_name)
    return worksheet


def append_data(worksheet, data):
    worksheet.append_row(data)


def get_current_worksheet(date=None):
    client_secret = '/home/pi/source/smart_home/client_secret.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(client_secret, SCOPE)

    gc = gspread.authorize(credentials)
    ss = gc.open('Smart Home')

    if date is None:
        date = datetime.now()
    return get_date_worksheet(ss, date)
