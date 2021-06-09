from flask import Flask, render_template, request
import folium
from collections import defaultdict
import csv
import geojson



app = Flask(__name__)
app.config['SECRET_KEY']='mysecretkey'

from WEBMAP import routes