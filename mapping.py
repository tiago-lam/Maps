import folium
import pandas
from folium.plugins import FloatImage

def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

data = pandas.read_csv("maps/Volcanoes.txt")
lat = list(data['LAT'])
lon = list(data['LON'])
elev = list(data['ELEV'])
image_file = "assets/legend_redux_med.png"
html = """<h4>Volcano information:</h4>
Height: %s m
"""

#starting map
map = folium.Map(location=[38,-99], zoom_start=6, tiles="OpenStreetMap", min_zoom=2, max_zoom=8)

#volcanoes group
fgv = folium.FeatureGroup(name="Volcanoes")

#add markers to volcanoes locations
for lt, ln, el in zip(lat, lon, elev):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=6, popup=folium.Popup(html=html % str(el)),
                                            fill_color=color_producer(el), color='grey', fill_opacity=0.7))

#population group
#note lambda function to coloring map accoeding population
fgp = folium.FeatureGroup(name="Population")
map.add_child(fgp.add_child(folium.GeoJson(data=open('maps/world.json', 'r', encoding='utf-8-sig').read(),
                                          style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
                                                                    else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'})))

#add groups to map
map.add_child(fgv)
map.add_child(fgp)
#add control to switch groups on/off
map.add_child(folium.LayerControl(collapsed=False))

#add a legend to the screen
FloatImage(image_file, bottom=3, left=3).add_to(map)

#saves/generates map to the html specified in the parameter
map.save("index.html")

