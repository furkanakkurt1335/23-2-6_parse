from __future__ import print_function
from pprint import pprint

import os.path
from googleapiclient import discovery
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import dateparser
import unidecode
import re
import json

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('google_sheets_test/token.json'):
    creds = Credentials.from_authorized_user_file('google_sheets_test/token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'google_sheets_test/credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('google_sheets_test/token.json', 'w') as token:
        token.write(creds.to_json())

service = discovery.build('sheets', 'v4', credentials=creds)

def get_values(spreadsheet_id, sheet_range):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=sheet_range).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
        return None
    return values

def update_values(spreadsheet_id, sheet_range, values):
    batch_update_values_request_body = {
        # How the input data should be interpreted.
        'value_input_option': 'USER_ENTERED',  # TODO: Update placeholder value.

        # The new values to apply to the spreadsheet.
        #'data': [],  # TODO: Update placeholder value.
        'data': [
            {
            "range": sheet_range,
            "values": values
            },
        ]
        # TODO: Add desired entries to the request body.
    }

    request = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=batch_update_values_request_body)
    response = request.execute()

    # TODO: Change code below to process the `response` dict:
    pprint(response)

def parse_dates(raw_values):
    turkish_dates = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık", 
                        "Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara", 
                        "pazartesi", "salı", "çarşamba", "perşembe", "cuma", "cumartesi", "pazar",
                        "pzt", "sal", "çar", "per", "cum", "cmt", "pzr",
                        "paz", "sal", "çar", "per", "cum", "cmt", "paz",
                        "pzt", "sal", "çrş", "per", "cum", "cmt", "paz",
                        "paz", "sal", "çrş", "per", "cum", "cmt", "paz",
                        "paz", "sal", "çr", "per", "cum", "cmt", "paz",
                        "paz", "sal", "çr", "per", "cum", "cmt", "paz",]
    turkish_dates_lower = [date.lower() for date in turkish_dates]
    # convert turkish characters to non unicode characters in turkish_dates list
    turkish_dates_en = [unidecode.unidecode(date) for date in turkish_dates]
    turkish_dates_en_lower = [date.lower() for date in turkish_dates_en]

    turkish_dates_full = turkish_dates_lower + turkish_dates_en_lower

    dates = [["Teyit Tarihi"]]
    for i in range(len(raw_values)):
        raw_date = raw_values[i][0]
        raw_date_lower = raw_date.lower().replace("'", "").replace("saat: ","")
        date_as_list = []
        separator = ""
        for turkish_date in turkish_dates_full:
            date_as_list = raw_date_lower.split(turkish_date)
            if len(date_as_list) > 1:
                separator = turkish_date
                break

        
        # remove text from raw_date which are not date or time
        # we can use regex here
        # remove non numeric characters, except for . and : and / and - and space and ,
        if len(date_as_list) > 1:
            final_raw_date = re.sub(r'[^0-9\.\:\-\/\s\,]', '', date_as_list[0]) + separator + \
                re.sub(r'[^0-9\.\:\-\/\s\,]', '', date_as_list[1])
        else:
            final_raw_date = re.sub(r'[^0-9\.\:\-\/\s\,]', '', raw_date)

        parsed_date = dateparser.parse(final_raw_date)
        parsed_date_string = parsed_date.strftime("%d.%m.%Y, %H.%M") if parsed_date else "-"
        dates.append([parsed_date_string])
    return dates

def main():
    spreadsheet_id = 'UPDATE_HERE'  # TODO: Update placeholder value.
    sheet_name = "UPDATE_HERE" # name of ilce
    date_values_range = sheet_name + '!D2:D'
    raw_values = get_values(spreadsheet_id, sheet_name + '!D2:D')
    print(raw_values)
    dates = parse_dates(raw_values)
    date_values_update_range = sheet_name + '!E1:E'
    update_values(spreadsheet_id, date_values_update_range, dates)
    return None

if __name__ == '__main__':
    main()