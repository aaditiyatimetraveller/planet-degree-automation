import swisseph as swe
from datetime import datetime, timedelta
import pytz
import json
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ==========================================
# GOOGLE CREDENTIALS
# ==========================================

creds_json=json.loads(
os.environ['GOOGLE_CREDENTIALS']
)

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


# ==========================================
# KUNDLI MATCH MODE
# ==========================================

swe.set_sid_mode(
swe.SIDM_LAHIRI
)


# ==========================================
# ===== EDIT ONLY THIS SECTION =====
# ==========================================

YEAR=2026
MONTH=5
DAY=22

START_HOUR=9
START_MINUTE=15

END_HOUR=15
END_MINUTE=30

INTERVAL_MINUTES=5

LATITUDE=18.9750
LONGITUDE=72.8258

TIMEZONE='Asia/Kolkata'

# ==========================================
# ===== STOP EDITING BELOW =====
# ==========================================


tz=pytz.timezone(TIMEZONE)

start=tz.localize(
datetime(
YEAR,
MONTH,
DAY,
START_HOUR,
START_MINUTE
)
)

end=tz.localize(
datetime(
YEAR,
MONTH,
DAY,
END_HOUR,
END_MINUTE
)
)

planets={

"Sun":swe.SUN,
"Moon":swe.MOON,
"Mercury":swe.MERCURY,
"Mars":swe.MARS,
"Jupiter":swe.JUPITER,
"Venus":swe.VENUS,
"Saturn":swe.SATURN,
"Rahu":swe.TRUE_NODE,
"Ketu":swe.TRUE_NODE,
"Uranus":swe.URANUS,
"Neptune":swe.NEPTUNE,
"Pluto":swe.PLUTO

}

data=[]

header=[
"TIME",
"Sun",
"Moon",
"Mercury",
"Mars",
"Jupiter",
"Venus",
"Saturn",
"Rahu",
"Ketu",
"Uranus",
"Neptune",
"Pluto"
]

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
    utc.hour + utc.minute/60
    )

    row=[
    current.strftime("%H:%M")
    ]

    for name,p in planets.items():

        pos=swe.calc_ut(
        jd,
        p,
        swe.FLG_SIDEREAL
        )

        degree=round(
        pos[0][0],
        4
        )

        if name=="Ketu":
            degree=(degree+180)%360

        row.append(
        degree
        )

    data.append(row)

    current += timedelta(
    minutes=INTERVAL_MINUTES
    )

worksheet.clear()

worksheet.update(
"A1",
data
)

print("Planet Data Updated Successfully")
