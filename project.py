from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import io

from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)

import sqlite3
conn=sqlite3.connect('../sensorsdata.db', check_same_thread = False)
curs=conn.cursor()

# Retrieve LAST data from database
def getLastData():
	for row in curs.execute("SELECT * FROM HCSR04_data ORDER BY timestamp DESC LIMIT 1"):
		time = str(row[0])
		dist = row[1]
	#conn.close()
	return time, dist


def getHistData (numSamples):
	curs.execute("SELECT * FROM HCSR04_data ORDER BY timestamp DESC LIMIT "+str(numSamples))
	data = curs.fetchall()
	dates = []
	dist = []
	for row in reversed(data):
		dates.append(row[0])
		dist.append(row[1])
	return dates, dist

def maxRowsTable():
	for row in curs.execute("select COUNT(dist) from  HCSR04_data"):
		maxNumberRows=row[0]
	return maxNumberRows

#initialize global variables
global numSamples
numSamples = maxRowsTable()
if (numSamples > 101):
	numSamples = 100


# main route 
@app.route("/")
def index():

	time, dist = getLastData()
	templateData = {
		'time' :  time,
		'dist' : dist,
		'numSamples'	: numSamples
	}

	return render_template('index.html', **templateData)


@app.route('/', methods=['POST'])
def my_form_post():
    global numSamples
    numSamples = int (request.form['numSamples'])
    numMaxSamples = maxRowsTable()
    if (numSamples > numMaxSamples):
        numSamples = (numMaxSamples-1)

    time, dist = getLastData()

    templateData = {
	'time'		: time,
      	'dist'		: dist,
      	'numSamples'	: numSamples
	}
    return render_template('index.html', **templateData)

@app.route('/plot/distance')
def plot_distance():
	times, dist = getHistData(numSamples)
	ys = dist
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Distance [cm]")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=False)
