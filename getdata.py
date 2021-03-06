__author__ = 'clbx'
import io
import csv
import csv
import os
import plotly
import pandas as pd
import numpy as np
import json
import plotly.graph_objs as go
from flask import Flask, render_template,request, redirect, url_for, make_response
from flask_uploads import UploadSet, IMAGES, configure_uploads
from urllib.request import urlopen
from werkzeug.utils import secure_filename

app = Flask(__name__)

'''
.
yes i know my code is nasty

'''

def getAvg(wave):
	total = 0;
	for i in range(len(wave)):
		total += wave[i]
	avg = total/len(wave)
	return avg


@app.route('/')
def index():
	return render_template('index.html', title='Home')


@app.route('/data', methods=["POST"])
def data_view():
	f = request.files['data_file']
	if not f:
		return "No file"

	stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
	readdata = csv.reader(stream)
	data = []
	for row in readdata:
		data.append(row)
	# We now have a 2D array that has all the values of the CSV
	# this can be referenced using data[y-1][x-1] in the csv

	#Count blinks and jar clenches
	prefix = "/muse/elements/"
	total_blinks = 0
	total_syl = 0
	battery = []
	for i in range(len(data)):
		if len(data[i]) == 39:    #Nessessary to prevent the OOB created by lists
			if data[i][38] == prefix + "blink":
				total_blinks += 1
			if data[i][38] == prefix + "jaw_clench":
				total_syl += 1
	for i in range(len(data))[1:]:
		if data[i][37] != "":
			battery.append(float(data[i][37]))
	print("Total Blinks: "+str(total_blinks))
	print("Total Syl: "+ str(total_syl))


	battMax = max(battery)

	battMin = min(battery)
	total_batt = round(battMax - battMin,4)

	#Now for graph stuff
	#Initilze our lists
	timestamps = []
	delta = []
	theta = []
	alpha = []
	beta = []
	gamma = []
	accX = []
	accY = []
	accZ = []


	dTP9 = []
	dAF7 = []
	dAF8 = []
	dTP10 = []

	tTP9 = []
	tAF7 = []
	tAF8 = []
	tTP10 = []

	aTP9 = []
	aAF7 = []
	aAF8 = []
	aTP10 = []

	bTP9 = []
	bAF7 = []
	bAF8 = []
	bTP10 = []

	gTP9 = []
	gAF7 = []
	gAF8 = []
	gTP10 = []



	#print(data[1][1])

	#Now get it
	for i in range(len(data))[1:]:
		timestampsTemp = data[i][0]
		timestampsTemp = timestampsTemp[10:]
		#print(timestampsTemp)
		if len(timestampsTemp) == 13:
			timestamps.append(timestampsTemp)
		#Delta
		if data[i][1] != "":
			dTP9.append(float(data[i][1]))
			dAF7.append(float(data[i][2]))
			dAF8.append(float(data[i][3]))
			dTP10.append(float(data[i][4]))
			deltaTemp = (float(data[i][1])+float(data[i][2])+float(data[i][3])+float(data[i][4]))/4
			delta.append(deltaTemp)
		#Theta
		if data[i][5] != "":
			tTP9.append(float(data[i][5]))
			tAF7.append(float(data[i][6]))
			tAF8.append(float(data[i][7]))
			tTP10.append(float(data[i][8]))
			thetaTemp = (float(data[i][5])+float(data[i][6])+float(data[i][7])+float(data[i][8]))/4
			theta.append(thetaTemp)
		#Alpha
		if data[i][9] != "":
			aTP9.append(float(data[i][9]))
			aAF7.append(float(data[i][10]))
			aAF8.append(float(data[i][11]))
			aTP10.append(float(data[i][12]))
			alphaTemp = (float(data[i][9])+float(data[i][10])+float(data[i][11])+float(data[i][12]))/4
			alpha.append(alphaTemp)
		#Beta
		if data[i][13] != "":
			bTP9.append(float(data[i][13]))
			bAF7.append(float(data[i][14]))
			bAF8.append(float(data[i][15]))
			bTP10.append(float(data[i][16]))
			betaTemp = (float(data[i][13])+float(data[i][14])+float(data[i][15])+float(data[i][16]))/4
			beta.append(betaTemp)
		#Gamma
		if data[i][17] != "":
			gTP9.append(float(data[i][17]))
			gAF7.append(float(data[i][18]))
			gAF8.append(float(data[i][19]))
			gTP10.append(float(data[i][20]))
			gammaTemp = (float(data[i][17])+float(data[i][18])+float(data[i][19])+float(data[i][20]))/4
			gamma.append(gammaTemp)
		if data[i][28] != "":
			accX.append(float(data[i][28]))
			accY.append(float(data[i][29]))
			accZ.append(float(data[i][30]))





	'''
	print(timestamps)
	print()
	print(delta)
	print()
	print(len(timestamps))
	print(len(delta))
	print(len(theta))
	print(len(alpha))
	print(len(beta))
	print(len(gamma))
	'''


	deltaAvg = round(getAvg(delta),3)
	thetaAvg = round(getAvg(theta),3)
	alphaAvg = round(getAvg(alpha),3)
	betaAvg = round(getAvg(beta),3)
	gammaAvg = round(getAvg(gamma),3)
	xAvg = round(getAvg(accX),3)
	yAvg = round(getAvg(accY),3)
	zAvg = round(getAvg(accZ),3)
	accelAvg = (xAvg + yAvg + zAvg)/3


	print("Accel Average" + str(accelAvg))

	testlist = [1,2,3,4,4,3,2,3,3,4,4,5,6,7,7,6,5,4,3,3,4,5,5,6,4]
	testtimes = ["0:00","0:15","0:30","0:45","1:00","1:15","1:30","1:45","2:00","2:15","2:30","2:45","3:00","3:15","3:30","3:45","4:00","4:15","4:30","4:45","5:0","4:45","5:00","5:15","5:30"]


	xGraph = go.Scatter(
		x = timestamps,
		y = accX,
		name = "X Accelerometer",
		line = dict(
			color = ('rgb(205, 12, 24)'),
			width = 4
		)
	)
	yGraph = go.Scatter(
		x = timestamps,
		y = accY,
		name = "Y Accelerometer",
		line = dict(
			color = ('rgb(22,96,167)'),
			width = 4
		)
	)
	zGraph = go.Scatter(
		x = timestamps,
		y = accZ,
		name = "Z Accelerometer",
		line = dict(
			color = ('rgb(45,198,22)'),
			width = 4
		)
	)



	thetaGraph = go.Scatter(
		x = timestamps,
		y = theta,
		name = "Theta Waves",
		line = dict(
			color = ('rgb(205, 12, 24)'),
			width = 4)
	)
	deltaGraph = go.Scatter(
		x = timestamps,
		y = delta,
		name = "Delta Waves",
		line = dict(
			color = ('rgb(22,96,167)'),
			width = 4)
	)
	alphaGraph = go.Scatter(
		x = timestamps,
		y = alpha,
		name = "Alpha Waves",
		line = dict(
			color = ('rgb(156,12,203)'),
			width = 4)
	)
	betaGraph = go.Scatter(
		x = timestamps,
		y = beta,
		name = "Beta Waves",
		line = dict(
			color = ('rgb(45,198,22)'),
			width = 4)
	)
	gammaGraph = go.Scatter(
		x = timestamps,
		y = beta,
		name = "Gamma Waves",
		line = dict(
			color = ('rgb(170,170,23)'),
			width = 4)
	)


	dTP9g = go.Scatter(
		x = timestamps,
		y = dTP9,
		name = "Delta TP9",
		line = dict(
			color = ('rgb(205, 12, 24)'),
			width = 4)
	)
	dAF7g = go.Scatter(
		x = timestamps,
		y = dAF7,
		name = "Delta AF7",
		line = dict(
			color = ('rgb(22,96,167)'),
			width = 4)
	)
	dAF8g = go.Scatter(
		x = timestamps,
		y = dAF8,
		name = "Delta AF8",
		line = dict(
			color = ('rgb(156,12,203)'),
			width = 4)
	)
	dTP10g = go.Scatter(
		x = timestamps,
		y = dTP10,
		name = "Delta TP10",
		line = dict(
			color = ('rgb(45,198,22)'),
			width = 4)
	)

	aTP9g = go.Scatter(
		x = timestamps,
		y = aTP9,
		name = "Alpha TP9",
		line = dict(
			color = ('rgb(205, 12, 24)'),
			width = 4)
	)
	aAF7g = go.Scatter(
		x = timestamps,
		y = aAF7,
		name = "Alpha AF7",
		line = dict(
			color = ('rgb(22,96,167)'),
			width = 4)
	)
	aAF8g = go.Scatter(
		x = timestamps,
		y = aAF8,
		name = "Alpha AF8",
		line = dict(
			color = ('rgb(156,12,203)'),
			width = 4)
	)
	aTP10g = go.Scatter(
		x = timestamps,
		y = aTP10,
		name = "Alpha TP10",
		line = dict(
			color = ('rgb(45,198,22)'),
			width = 4)
	)

	bTP9g = go.Scatter(
		x = timestamps,
		y = bTP9,
		name = "Beta TP9",
		line = dict(
			color = ('rgb(205, 12, 24)'),
			width = 4)
	)
	bAF7g = go.Scatter(
		x = timestamps,
		y = bAF7,
		name = "Beta AF7",
		line = dict(
			color = ('rgb(22,96,167)'),
			width = 4)
	)
	bAF8g = go.Scatter(
		x = timestamps,
		y = bAF8,
		name = "Beta AF8",
		line = dict(
			color = ('rgb(156,12,203)'),
			width = 4)
	)
	bTP10g = go.Scatter(
		x = timestamps,
		y = bTP10,
		name = "Beta TP10",
		line = dict(
			color = ('rgb(45,198,22)'),
			width = 4)
	)

	gTP9g = go.Scatter(
		x = timestamps,
		y = gTP9,
		name = "Gamma TP9",
		line = dict(
			color = ('rgb(205, 12, 24)'),
			width = 4)
	)
	gAF7g = go.Scatter(
		x = timestamps,
		y = gAF7,
		name = "Gamma AF7",
		line = dict(
			color = ('rgb(22,96,167)'),
			width = 4)
	)
	gAF8g = go.Scatter(
		x = timestamps,
		y = gAF8,
		name = "Gamma AF8",
		line = dict(
			color = ('rgb(156,12,203)'),
			width = 4)
	)
	gTP10g = go.Scatter(
		x = timestamps,
		y = gTP10,
		name = "Gamma TP10",
		line = dict(
			color = ('rgb(45,198,22)'),
			width = 4)
	)

	tTP9g = go.Scatter(
		x = timestamps,
		y = tTP9,
		name = "Theta TP9",
		line = dict(
			color = ('rgb(205, 12, 24)'),
			width = 4)
	)
	tAF7g = go.Scatter(
		x = timestamps,
		y = tAF7,
		name = "Theta AF7",
		line = dict(
			color = ('rgb(22,96,167)'),
			width = 4)
	)
	tAF8g = go.Scatter(
		x = timestamps,
		y = tAF8,
		name = "Theta AF8",
		line = dict(
			color = ('rgb(156,12,203)'),
			width = 4)
	)
	tTP10g = go.Scatter(
		x = timestamps,
		y = tTP10,
		name = "Theta TP10",
		line = dict(
			color = ('rgb(45,198,22)'),
			width = 4)
	)



	graphs = [
		dict(
			data=[thetaGraph, deltaGraph, alphaGraph, betaGraph,gammaGraph ],
			layout=dict(
				title='Brain Data'
			)
		),
		dict(
			data=[xGraph,yGraph,zGraph],
			layout=dict(
				title='Accelerometer Data'
			)
		),
		dict(
			data=[aTP9g,aAF7g,aAF8g,aTP10g],
			layout=dict(
				title='Alpha Brianwaves'
			)
		),
		dict(
			data=[bTP9g,bAF7g,bAF8g,bTP10g],
			layout=dict(
				title='Beta Brianwaves'
			)
		),
		dict(
			data=[dTP9g,dAF7g,dAF8g,dTP10g],
			layout=dict(
				title='Delta Brianwaves'
			)
		),
		dict(
			data=[gTP9g,gAF7g,gAF8g,gTP10g],
			layout=dict(
				title='Gamma Brianwaves'
			)
		),
		dict(
			data=[tTP9g,tAF7g,tAF8g,tTP10g],
			layout=dict(
				title='Theta Brianwaves'
			)
		),
	]



	accelMax = 10;
	alerts = []
	alertmax = 3;
	current = 0;
	'''
	Types:
	sucess = green
	warning = yellow
	danger = red
	'''

	# This part is super nasty, I know. Awful, but it's a workaround

	alertMatrix = []
	alertMatrix.append([])
	alertMatrix.append([])
	alertMatrix.append([])

	if(current < alertmax and accelAvg > accelMax):
		alertMatrix[current].append(str("danger"))
		alertMatrix[current].append(str("You're Moving too Much"))
		alertMatrix[current].append(str("Try to keep still to get the best results"))
		current += 1

	if(current < alertmax and alphaAvg > 1):
		alertMatrix[current].append(str("sucess"))
		alertMatrix[current].append(str("Your Alpha Waves are High"))
		alertMatrix[current].append(str("This means you are physically and mentally aware"))
		current += 1
	if(current < alertmax and alphaAvg < 0):
		alertMatrix[current].append(str("success"))
		alertMatrix[current].append(str("Your Alpha Waves are Low"))
		alertMatrix[current].append(str("This means you're out of it"))
		current += 1

	if(current < alertmax and betaAvg > 1):
		alertMatrix[current].append(str("sucess"))
		alertMatrix[current].append(str("Your Beta Waves are High"))
		alertMatrix[current].append(str("This means you are alert, attentive, and engaged in activity"))
		current+= 1
	if(current < alertmax and betaAvg < 0):
		alertMatrix[current].append(str("success"))
		alertMatrix[current].append(str("Your Beta Waves are Low"))
		alertMatrix[current].append(str("This means you are out of it"))
		current+= 1

	if(current < alertmax and deltaAvg > 1):
		alertMatrix[current].append(str("success"))
		alertMatrix[current].append(str("Your Delta Waves are High"))
		alertMatrix[current].append(str("This means you are relaxed"))
		current+= 1

	if(current < alertmax and gammaAvg > 1):
		alertMatrix[current].append(str("success"))
		alertMatrix[current].append(str("Your Gamma Waves are High"))
		alertMatrix[current].append(str("This means that your brain is working hard!"))
		current+= 1
	if(current < alertmax and gammaAvg < 0):
		alertMatrix[current].append(str("success"))
		alertMatrix[current].append(str("Your Gamma Waves are low"))
		alertMatrix[current].append(str("This can many many different things"))
		current+= 1

	if(current < alertmax and thetaAvg > 1):
		alertMatrix[current].append(str("success"))
		alertMatrix[current].append(str("Your Theta Waves are high"))
		alertMatrix[current].append(str("You're sleepy arn't you"))
		current+= 1




	ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
	graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)


	print(ids)
	print(ids[0])

	return render_template('index.html', title='Home',alertMatrix=alertMatrix, ids=ids, graphJSON=graphJSON,total_syl=total_syl, total_blinks=total_blinks, total_batt=total_batt,deltaAvg=deltaAvg, thetaAvg=thetaAvg, gammaAvg=gammaAvg, betaAvg=betaAvg, alphaAvg=alphaAvg, xAvg=xAvg, yAvg=yAvg,zAvg=zAvg)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
