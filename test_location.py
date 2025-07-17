import geocoder

g = geocoder.ip("me")

lat, long = g.latlng[0], g.latlng[1]

print(f"lat: {lat} long: {long}")

print(g.latlng)