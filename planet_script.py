from datetime import datetime
import pytz

tz = pytz.timezone('Asia/Kolkata')
now = datetime.now(tz)

print("Mumbai Time:")
print(now)
print("GitHub Working Successfully")
