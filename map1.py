import folium
import pandas

data = pandas.read_csv("Vendors.csv")
#extracting columns out of data
lat = list(data["LAT"])
lon = list(data["LON"])
Num = list(data["VendorNum"])
vname = list(data["VendorName"])
TYPE = list(data["TYPE"])

def namegroup(TYPE):
    if TYPE == 'local':
        return 'green'
    elif TYPE == 'Mid':
        return 'orange'
    else:
        return 'red'

map = folium.Map(location=[50, -100], zoom_start = 4, tiles = "Mapbox Bright")

fgv = folium.FeatureGroup(name = "Vendors")

#use zip function when going through multiple items
#radius is size of circles
#for tags like before, use folium.Marker and get rid of fill_color, radius, opacity, fill
for lt, ln, num, vn, tp in zip(lat, lon, Num, vname, TYPE):
    fgv.add_child(folium.Marker(location=[lt,ln], radius = 6, popup= "Vendor Name " + str(vname) + " ," + str(Num), color = namegroup(TYPE)))

# fgp = folium.FeatureGroup(name = "Population")
# #GeoJson is a format of Json
# #style expects lambda functions
# fgp.add_child(folium.GeoJson(data=open('world.json','r', encoding='utf-8-sig').read(),
# style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 else 'blue' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgv)
# map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save("Map1.html")
