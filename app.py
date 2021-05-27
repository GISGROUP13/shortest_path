from flask import Flask, render_template, request
import folium

app = Flask(__name__)


@app.route('/',methods=["GET","POST"])
def index():

    if request.method == "POST":
        distance = float(request.form['distance'])
        time = float(request.form['time'])

        nodes = []
        for i in range(3):
            lat = distance+i*10
            lon = time + i*10
            nodes.append([lat,lon])


        map = folium.Map(
            location=[distance, time]
        )

        for i in range(3):
            folium.Marker(
                location=[nodes[i][0],nodes[i][1]],
                popup="<i>Marker here</i>"
            ).add_to(map)


        folium.PolyLine(nodes,
                        color='red',
                        weight=2,
                        opacity=1).add_to(map)
        # 45.52336, -122.6750
        return map._repr_html_()

    return render_template('index.html')

if __name__ == '__main__':
    app.run()

