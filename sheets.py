from datetime import datetime

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

ROW_TITLES = ['timestamp', 'temperature']

SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']


def get_date_worksheet(spreadsheet, time):
    worksheet_names = [w.title for w in spreadsheet.worksheets()]

    sheet_name = time.strftime('%Y_%m')
    if not sheet_name in worksheet_names:
        spreadsheet.add_worksheet(sheet_name, 1000, len(ROW_TITLES))
        worksheet = spreadsheet.worksheet(sheet_name)
        worksheet.append_row(ROW_TITLES)
    else:
        worksheet = spreadsheet.worksheet(sheet_name)
    return worksheet


def append_data(worksheet, time, data):
    worksheet.append_row([time.timestamp()] + data)


def read_data(worksheet):
    df_data = pd.DataFrame(worksheet.get_all_records())
    df_data.timestamp = df_data.timestamp.apply(datetime.fromtimestamp)
    return df_data


if __name__ == '__main__':
    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', SCOPE)

    gc = gspread.authorize(credentials)
    ss = gc.open('Smart Home')

    now = datetime.now()
    wks = get_date_worksheet(ss, now)
    append_data(wks, now, [21])
    df = read_data(wks)

    print(df)
