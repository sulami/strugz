def get_distances(plz, services):
    """Return a dict of services and their distance to a given PLZ"""

    distances = {}

    for service in services:
        dlon = abs(plz.lon - service.lon)
        dlat = abs(plz.lat - service.lat)

        kdlon = dlon * 71.5
        kdlat = dlat * 111.3

        distances[service] = round(sqrt(kdlon * kdlon + kdlat * kdlat), 2)

    return distances

