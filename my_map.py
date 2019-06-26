import folium
import csv


def color_producer(elevation):
    """Returns color name depending on the height of the volcanoe"""
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation < 3000:
        return "orange"
    else:
        return "red"

my_map = folium.Map(location=[38.9700012,-112.5009995], zoom_start=4)

fgv = folium.FeatureGroup(name="Volcanoes")
fgp = folium.FeatureGroup(name="Population")

with open("Volcanoes_USA.txt", newline="") as csvfile:
    volcanoes = csv.DictReader(csvfile)
    for row in volcanoes:
        lat, lon = map(float, [row["LAT"], row["LON"]])
        elev = float(row["ELEV"])
        color = color_producer(elev)
        #fg.add_child(folium.Marker(location=(lat, lon), popup=str(elev)+" m", icon=folium.Icon(color=color)))
        fgv.add_child(folium.CircleMarker(location=(lat, lon), radius=9, color="grey", fill=True,
        fill_color=color, fill_opacity=1, popup=str(elev)+" m"))

fgp.add_child(folium.GeoJson(open("world.json", "r", encoding="utf-8-sig").read(), 
                            style_function=lambda x: {"fillColor":"green" if x["properties"]["POP2005"] < 10000000
                            else "orange" if 10000000 <= x["properties"]["POP2005"] < 20000000 else "red"}))

my_map.add_child(fgv)
my_map.add_child(fgp)
my_map.add_child(folium.LayerControl())

my_map.save("my_map.html")
