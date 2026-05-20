import swisseph as swe
import pandas as pd
from datetime import datetime, timedelta
import pytz
import json
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google credentials
creds_json=json.loads(os.environ['GOOGLE_CREDENTIALS'])

with open("creds.json","w") as f:
    json.dump(creds_json,f)

scope=[
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]

creds=ServiceAccountCredentials.from_json_keyfile_name(
"creds.json",
scope
)

client=gspread.authorize(creds)

sheet=client.open_by_key(
os.environ['SHEET_ID']
)

worksheet=sheet.sheet1

tz=pytz.timezone('Asia/Kolkata')

today=datetime.now(tz)

start=tz.localize(
datetime(
today.year,
today.month,
today.day,
9,
15
)
)

end=tz.localize(
datetime(
today.year,
today.month,
today.day,
15,
30
)
)

planets={
"Sun":swe.SUN,
"Moon":swe.MOON,
"Mercury":swe.MERCURY,
"Venus":swe.VENUS,
"Mars":swe.MARS,
"Jupiter":swe.JUPITER,
"Saturn":swe.SATURN,
"Uranus":swe.URANUS,
"Neptune":swe.NEPTUNE,
"Pluto":swe.PLUTO
}

data=[]

header=["TIME"]+list(planets.keys())

data.append(header)

current=start

while current<=end:

    utc=current.astimezone(
    pytz.utc
    )

    jd=swe.julday(
    utc.year,
    utc.month,
    utc.day,
    utc.hour+utc.minute/60
    )

    row=[current.strftime("%H:%M")]

    for name,p in planets.items():

        pos=swe.calc_ut(
        jd,
        p
        )

        degree=round(
        pos[0][0],
        4
        )

        row.append(degree)

    data.append(row)

    current += timedelta(minutes=5)

worksheet.clear()

worksheet.update(
"A1",
data
)

print("Planet Data Updated")
