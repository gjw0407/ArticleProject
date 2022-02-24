import datetime
from background_task import background

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", __file__)
import django
django.setup()


@background(schedule=60)
def notify_user():
    print("Notified")

notify_user(3, datetime.datetime.now() + datetime.timedelta(minutes=2))

print("haha")

for i in range(1000000000):
    pass

print("hoho")
