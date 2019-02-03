from logic import *
import datetime

log_file = Logging("log.xlsx")
now = datetime.datetime.now()
log_file.write_new_entry(now.strftime("%Y-%m-%d"), now.strftime("%H:%M"), "Coding")
log_file.save()

