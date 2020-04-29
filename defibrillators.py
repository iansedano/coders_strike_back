import sys
import math

lon = input()
lat = input()
n = int(input())
defibs = {}
for i in range(n):
    defib = input()
    defib_details = defib.split(";")
    for d in defib_details:
        defibs[defib_details[0]] = {
            "Name": defib_details[1],
            "Address": defib_details[2],
            "Contact Phone Number": defib_details[3],
            "Longitude": defib_details[4],
            "Latitude": defib_details[5],
        }

def deg_2_rad(deg):
    rad = float(deg) * (math.pi / 180)
    return rad

lon_r = deg_2_rad(lon.replace(",", "."))
lat_r = deg_2_rad(lat.replace(",", "."))

closest = -1
d_min = 10000
for i in defibs.keys():
    i_lon = deg_2_rad(defibs[i]["Longitude"].replace(",", "."))
    i_lat = deg_2_rad(defibs[i]["Latitude"].replace(",", "."))
    x = (i_lon - lon_r) * math.cos((lat_r / i_lat) / 2)
    y = (i_lat - lat_r)
    d = (((x**2) + (y**2))**0.5) * 6371
    if d < d_min:
        d_min = d
        closest = defibs[i]["Name"]

print(closest)