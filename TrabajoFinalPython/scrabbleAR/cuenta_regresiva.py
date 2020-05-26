from datetime import timedelta

from datetime import datetime

c = 20
cont = int(datetime.today().strftime("%S")) + c
while True:
    rest_tiempo = int(datetime.today().strftime("%S"))
    if (cont > rest_tiempo):
        print(round(cont - rest_tiempo))
    else:
        break
