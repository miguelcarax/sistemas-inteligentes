# Proyeccion Mercator
# http://wiki.openstreetmap.org/wiki/Mercator

import math

def merc_x(lon):
  r_major=6378137.000
  return r_major*math.radians(lon)

def merc_y(lat):
  if lat>89.5:lat=89.5
  if lat<-89.5:lat=-89.5
  r_major=6378137.000
  r_minor=6356752.3142
  temp=r_minor/r_major
  eccent=math.sqrt(1-temp**2)
  phi=math.radians(lat)
  sinphi=math.sin(phi)
  con=eccent*sinphi
  com=eccent/2
  con=((1.0-con)/(1.0+con))**com
  ts=math.tan((math.pi/2-phi)/2)/con
  y=0-r_major*math.log(ts)
  return y

#Distancia entre dos punto geograficos.
#Se obtiene sus proyecciones Mercator
#y la distancia euclidea entre ellas
def dist(p1lon,p1lat,p2lon,p2lat):
	x1=merc_x(p1lon)
	x2=merc_x(p2lon)
	y1=merc_y(p1lat)
	y2=merc_y(p2lat)
	return math.sqrt((x1-x2)**2+(y1-y2)**2)
