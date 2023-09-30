import geomuda

gd=geomuda.GeoData('/var/data.csv')
multigeolayer=gd.to_multigeolayer()
multigeolayer.to_geojson()
