import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from datetime import datetime
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SPREADSHEET_ID = "*TOKEN*"

def main():
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('creds.json', SCOPES)
            credentials = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())

    try:
        service = build("sheets", 'v4', credentials=credentials)
        sheets = service.spreadsheets()

        return sheets

    except HttpError as ex:
        print(ex)

def calc():
    sheets = main()
    result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range="test!A1:B5").execute()
    values = result.get("values", [])
    num1 = values[0][0]
    num2 = values[0][1]
    result = int(num1) + int(num2)

    sheets.values().update(spreadsheetId=SPREADSHEET_ID, range="test!C1",
                           valueInputOption="USER_ENTERED", body={'values': [[result]]}).execute()

def get_value_direction_of_activity():
    sheets = main()
    result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range="Справочники!A1:A7").execute()
    values = result.get("values", [])
    dict_value_direction_of_activity = {}
    list_value = []

    for i in range(1,len(values)):
        list_value.append(values[i][0])

    dict_value_direction_of_activity[values[0][0]] = list_value

    return dict_value_direction_of_activity

def get_value_RP():
    sheets = main()
    result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range="Справочники!C1:C50").execute()
    values = result.get("values", [])
    dict_value_RP = {}
    list_value = []

    for i in range(1,len(values)):
        list_value.append(values[i][0])

    dict_value_RP[values[0][0]] = list_value

    return dict_value_RP

def set_date(date):
    sheets = main()
    i = 0
    count = 3
    range = ''
    while i == 0 :
        result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f"ДДС!C{count}").execute()
        values = result.get("values", [])
        if values == []:
            i = i + 1
        range = result['range']
        count = count + 1

    sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=range,
                           valueInputOption="USER_ENTERED", body={'values': [[str(date)]]}).execute()

def set_RP(date):
    sheets = main()
    i = 0
    count = 3
    range = ''
    while i == 0 :
        result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f"ДДС!D{count}").execute()
        values = result.get("values", [])
        if values == []:
            i = i + 1
        range = result['range']
        count = count + 1

    sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=range,
                           valueInputOption="USER_ENTERED", body={'values': [[str(date)]]}).execute()

def get_RP_for_ID(ID):
    try:
        sheets = main()
        i = 0
        count = 2
        range = ''
        result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f"Справочники!H1:I300").execute()
        values = result.get("values", [])
        for i in values:
            if i[0] == ID:
                return i[1]

        return 'not_valid'
    except Exception as ex:
        print(ex)
def set_sum(date):
    sheets = main()
    i = 0
    count = 3
    range = ''
    while i == 0 :
        result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f"ДДС!F{count}").execute()
        values = result.get("values", [])
        if values == []:
            i = i + 1
        range = result['range']
        count = count + 1
    date = date.split(' ')
    date = date[1]
    sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=range,
                           valueInputOption="USER_ENTERED", body={'values': [[str(date)]]}).execute()

def set_direction_of_activity(date):
    try:
        sheets = main()
        i = 0
        count = 3
        range = ''
        while i == 0 :
            result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f"ДДС!G{count}").execute()
            values = result.get("values", [])
            if values == []:
                i = i + 1
            range = result['range']
            count = count + 1
        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=range,
                               valueInputOption="USER_ENTERED", body={'values': [[str(date)]]}).execute()
    except Exception as ex:
        print(ex)

def set_comment(date):
    try:
        sheets = main()
        i = 0
        count = 3
        range = ''
        while i == 0 :
            result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f"ДДС!I{count}").execute()
            values = result.get("values", [])
            if values == []:
                i = i + 1
            range = result['range']
            count = count + 1
        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=range,
                               valueInputOption="USER_ENTERED", body={'values': [[str(date)]]}).execute()
    except Exception as ex:
        print(ex)

def set_article(date):
    sheets = main()
    i = 0
    count = 3
    range = ''
    while i == 0:
        result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f"ДДС!H{count}").execute()
        values = result.get("values", [])
        if values == []:
            i = i + 1
        range = result['range']
        count = count + 1
    sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=range,
                           valueInputOption="USER_ENTERED", body={'values': [[str(date)]]}).execute()


def update_table(date):
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    now_date = f"{currentYear}-{currentMonth}-{currentDay}"
    try:
        sheets = main()
        i = 0
        count = 3
        range = ''
        while i == 0 :
            result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f"ДДС!I{count}").execute()
            values = result.get("values", [])
            if values == []:
                i = i + 1
            range = result['range']
            count = count + 1
        count = count - 1
        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"ДДС!C{count}",
                               valueInputOption="USER_ENTERED", body={'values': [[str(now_date)]]}).execute()

        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"ДДС!D{count}",
                               valueInputOption="USER_ENTERED", body={'values': [[str(date['РП'])]]}).execute()

        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"ДДС!E{count}",
                               valueInputOption="USER_ENTERED", body={'values': [[str(date['ИД'])]]}).execute()

        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"ДДС!F{count}",
                               valueInputOption="USER_ENTERED", body={'values': [[str(date['Сумма'])]]}).execute()

        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"ДДС!G{count}",
                               valueInputOption="USER_ENTERED", body={'values': [[str(date['Направление'])]]}).execute()

        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"ДДС!H{count}",
                               valueInputOption="USER_ENTERED", body={'values': [[str(date['Статья'])]]}).execute()

        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"ДДС!I{count}",
                               valueInputOption="USER_ENTERED", body={'values': [[str(date['Комментарий'])]]}).execute()

    except Exception as ex:
        print(ex)

def valid(a):
    try:
        a = a.split('-')
        year = a[0]
        mouth = a[1]
        day = a[2]
        if 1900 < int(year) < 9999:
            if int(mouth) < 13:
                if int(day) < 32:
                    return 'valid'
                else:
                    return 'not_valid'
            else:
                return 'not_valid'

        else:
            return 'not_valid'
    except Exception as ex:
        return 'not_valid'