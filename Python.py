import csv
import pygal
import numpy as np
from datetime import datetime
from pygal.style import Style
from flask import Flask, request, render_template

custom_style = Style(
  background='transparent',
  plot_background='transparent',
  foreground='#3067AA',
  foreground_strong='#3067AA',
  foreground_subtle='#3067AA',
  opacity='1',
  opacity_hover='1',
  colors=('#FFFFFF', '#E8537A', '#E95355', '#E87653', '#E89B53'))

app = Flask(__name__, static_folder='docs/_build/html/_static',template_folder='docs/_build/html')
@app.route('/', methods=['POST'])
def result():
    time = (request.form['time'])
    deviceID = (request.form['deviceID'])
    stage = (request.form['stage'])
    print(time+" "+deviceID+" "+stage)
    with open(r'/home/server1/static/StageData.csv','a') as csvFile:
        writer = csv.writer(csvFile)
        data = time+"@"+deviceID+"@"+ stage +"@"
        writer.writerow(data.split("@"))
    csvFile.close()
    return 'Received'

@app.route('/live')
def hello():
    month = (datetime.now().month) - 1
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    with open('/home/server1/static/StageData.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        rowCount = sum(1 for row in reader)
        print (rowCount)
    csvFile.close()

    with open('/home/server1/static/StageData.csv', 'r') as f:
        dataPoints = []
        mycsv = csv.reader(f)
        mycsv = list(mycsv)
        lastUpdate = mycsv[rowCount-1][0]
        location = mycsv[rowCount-1][1]
        current = mycsv[rowCount-1][2]
        battery = float(mycsv[rowCount-1][3])
        x = rowCount-100
        while x < rowCount-1:
            try:
                dataPoints.append(int(mycsv[x][2]))
            except ValueError:
                dataPoints.append(0)
            x=x+1
    #print (dataPoints)
    csvFile.close()
    graph = pygal.Line(height=210, show_legend=False, dots_size=1.5, style=custom_style)
    #graph.x_labels = months[month-5:month]
    #print(months[month-5:month])
    graph.add('Stage', dataPoints)
    graph_data = graph.render_data_uri()
    #print (graph_data)
    if battery >= 3.3:
        battery = 'Asset1.png'

    elif battery >= 3.25:
        battery = 'Asset2.png'

    elif battery >= 3.20:
        battery = 'Asset3.png'

    elif battery >= 3.15:
        battery = 'Asset4.png'

    elif battery >= 3.10:
        battery = 'Asset2.png'

    elif battery >= 3.05:
        battery = 'Asset6.png'
    return render_template('site.html', graph_data = graph_data, location = location, lastUpdate = lastUpdate, current = current, battery = battery)

#app = Flask(__name__, static_url_path='/home/server1/static/')
@app.route('/docs')
def root():
    return render_template('index.html')
