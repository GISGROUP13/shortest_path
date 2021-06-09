from WEBMAP import app
from WEBMAP.forms import CalculationForm
from flask import Flask, render_template, request
import folium
from collections import defaultdict
import csv
import geojson


@app.route('/')
def index():
    return render_template('index.html', title='HOME')

@app.route('/about')
def about():
    return render_template('about.html', title='ABOUT')

@app.route('/calculate', methods=['GET','POST'])
def calculate():

    if request.method == "POST":
        distance0 = float(request.form['start1'])
        time0 = float(request.form['start2'])

        distance = int(distance0)
        time = int(time0)
        datastring = 'C:\\Users\\PINAR\\Desktop\\road.geojson'

        with open(datastring) as f:
            gj = geojson.load(f)
        features = gj['features']

        class Graph():
            def __init__(self):
                self.edges = defaultdict(list)
                self.weights = {}

            def add_edge(self, from_node, to_node, weight):
                # Note: assumes edges are bi-directional
                self.edges[from_node].append(to_node)
                self.edges[to_node].append(from_node)
                self.weights[(from_node, to_node)] = weight
                self.weights[(to_node, from_node)] = weight

        graph = Graph()

        edges = []
        coords = {}
        nodes = []
        with open('C:\\Users\\PINAR\\Desktop\\used.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                edges.append((row['STARTID'], row['ENDID'], row['LENGTH']))
                if (row['XCoord'], row['YCoord']) not in coords:
                    coords[row['STARTID']] = (row['XCoord'], row['YCoord'])

        for edge in edges:
            graph.add_edge(*edge)

        def dijsktra(graph, initial, end):
            # shortest paths is a dict of nodes
            # whose value is a tuple of (previous node, weight)
            shortest_paths = {initial: (None, 0)}
            current_node = initial
            visited = set()

            while current_node != end:
                visited.add(current_node)
                destinations = graph.edges[current_node]
                weight_to_current_node = shortest_paths[current_node][1]

                for next_node in destinations:
                    # print(type(graph.weights[(current_node, next_node)]))
                    # print(type(weight_to_current_node))
                    weight = float(graph.weights[(current_node, next_node)]) + weight_to_current_node
                    if next_node not in shortest_paths:
                        shortest_paths[next_node] = (current_node, weight)
                    else:
                        current_shortest_weight = shortest_paths[next_node][1]
                        if current_shortest_weight > weight:
                            shortest_paths[next_node] = (current_node, weight)

                next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
                if not next_destinations:
                    return "Route Not Possible"
                # next node is the destination with the lowest weight
                current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

            # Work back through destinations in shortest path
            path = []
            while current_node is not None:
                path.append(current_node)
                next_node = shortest_paths[current_node][0]
                current_node = next_node
            # Reverse path
            path = path[::-1]
            return path

        for k in range(len(dijsktra(graph, str(distance), str(time)))):
            nodes.append(coords[dijsktra(graph, str(distance), str(time))[k]])

        # print(dijsktra(graph, str(distance), str(time)))
        # print(nodes)
        a = len(dijsktra(graph, str(distance), str(time)))
        map_node = []
        for i in range(a):
            map_node.append((float(nodes[i][1]), float(nodes[i][0])))

        map_node2 = []
        for i in range(a):
            map_node2.append((float(nodes[i][0]), float(nodes[i][1])))


        lines = []
        for i in range(len(features)):
            leng = len(features[i]['geometry']['coordinates'][0])

            for j in range(len(map_node2)):
                if j != len(map_node2) - 1:
                    if list(map("{:.4f}".format, features[i]['geometry']['coordinates'][0][0])) == list(
                            map("{:.4f}".format, list(map_node2[j]))) and list(
                            map("{:.4f}".format, features[i]['geometry']['coordinates'][0][leng - 1])) == list(
                            map("{:.4f}".format, list(map_node2[j + 1]))):
                        lines.append(features[i])
                        print('yes')
                else:
                    if list(map("{:.4f}".format, features[i]['geometry']['coordinates'][0][0])) == list(
                            map("{:.4f}".format, list(map_node2[j]))) and list(
                            map("{:.4f}".format, features[i]['geometry']['coordinates'][0][leng - 1])) == list(
                            map("{:.4f}".format, list(map_node2[j]))):
                        lines.append(features[i])
                        print('yes')

        start_x = map_node[0][0]
        start_y = map_node[0][1]
        m1 = folium.Map(
            location=[start_x, start_y], zoom_start=15
        )

        icon_ur1 = 'https://cdn1.bbcode0.com/uploads/2021/6/9/70b14c922f7020a1615e92abf2b62f90-full.png'
        icon = folium.features.CustomIcon(icon_ur1, icon_size=(30,30))
        folium.Marker(
                location=[start_x, start_y],
                popup="<i>Start Point</i>",
                icon= icon
            ).add_to(m1)

        stop_x = map_node[-1][0]
        stop_y = map_node[-1][1]

        icon_ur1 = 'https://cdn1.bbcode0.com/uploads/2021/6/9/70b14c922f7020a1615e92abf2b62f90-full.png'
        icon = folium.features.CustomIcon(icon_ur1, icon_size=(30,30))
        folium.Marker(
            location=[stop_x, stop_y],
            popup="<i>Target Point</i>",
            icon=icon
        ).add_to(m1)


        style_function = lambda x: {
            'color': 'red',
            'weight': 4.5
        }

        for k in range(len(lines)):
            folium.GeoJson(lines[k], style_function=style_function).add_to(m1)


        # folium.PolyLine(map_node,
        #                 color='red',
        #                 weight=2,
        #                 opacity=1).add_to(m1)
        # # (45.52336, -122.6750)
        return m1._repr_html_()

    form = CalculationForm()
    return render_template('calculate.html', title='CALCULATE', form=form)

