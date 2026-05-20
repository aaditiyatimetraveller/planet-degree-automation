import os
import json
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pytz

# GitHub Secret पढ़ना
creds_json = json.loads(os.environ['GOOGLE_CREDENTIALS'])

with open("creds.json","w") as f:
    json.dump(creds_json,f)

scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "creds.json",
    scope
)

client = gspread.authorize(creds)

sheet_id = os.environ['SHEET_ID']

sheet = client.open_by_key(sheet_id)

worksheet = sheet.sheet1

tz = pytz.timezone("Asia/Kolkata")

now = datetime.now(tz)

data = [
    ["Time","Status"],
    [now.strftime("%d-%m-%Y %H:%M:%S"),"Connected Successfully"]
]

worksheet.clear()
worksheet.update("A1",data)

print("Google Sheet Updated")
