import gnsspy as gp


rinex_file = "ISK41040.20O"
station = gp.read_obsFile(rinex_file)

print(station)
