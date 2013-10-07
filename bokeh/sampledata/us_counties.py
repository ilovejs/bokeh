'''
This modules exposes geometry data for Unites States. It exposes a dictionary 'data' which is
indexed by the two-tuple containing (state_id, county_id) and has the following dictionary as the
associated value:

    data[(1,1)]['name']
    data[(1,1)]['lats']
    data[(1,1)]['lons']

'''
import csv
import xml.etree.cElementTree as et
from os.path import dirname, join

nan = float('NaN')

data = {}
with open(join(dirname(__file__), 'US_Counties.csv')) as f:
    f.next()
    reader = csv.reader(f, delimiter=',', quotechar='"')
    for row in reader:
        name, dummy, dummy, dummy, geometry, dummy, dummy, dummy, dummy, state_id, county_id, dummy, dummy = row
        xml = et.fromstring(geometry)
        lats = []
        lons = []
        for i, poly in enumerate(xml.findall('.//outerBoundaryIs/LinearRing/coordinates')):
            if i > 0:
                lats.append(nan)
                lons.append(nan)
            coords = (c.split(',')[:2] for c in poly.text.split())
            lat, lon = zip(*[(float(lat), float(lon)) for lon, lat in coords])
            lats.extend(lat)
            lons.extend(lon)
        data[(int(state_id), int(county_id))] = {
            'name' : name,
            'lats' : lats,
            'lons' : lons,
        }