from flask import Flask, request, session, redirect, url_for, abort, render_template, flash
import collections
import math
import operator
import time
import ast

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MySecRetKey'

imagelinks = {}
contentimagelist = []
collaborativeimagelist = []
hybridimagelist = []
def fetchimage(id):
	global contentimagelist,collaborativeimagelist,hybridimagelist
	contentimagelist = []
	collaborativeimagelist = []
	hybridimagelist = []
	searchphrase = 'User Id =  '+id
	content = {}
	collaborative = {}
	hybrid = {}
	with open("output.txt", "r") as ins:
	    for line in ins:
	    	if searchphrase in line:
	    		content = dict(ast.literal_eval(next(ins)))
	    		collaborative = dict(ast.literal_eval(next(ins)))
	    		hybrid = dict(ast.literal_eval(next(ins)))
	for keys in content.keys():   
		name = keys
		final = ""
		if "," in name:
			namearr = name.split(",")
			temp = namearr[1].split(" ")
			final = temp[1]+"+"+namearr[0]
		else:
			 namearr = name.split(" ")
			 for i in range(0,len(namearr)-1):
			 	if namearr[i][0] == "(":
			 		continue
			 	else:
			 		final = final+namearr[i]+"+"
			 final = final[0:-1]
		final = final.replace(" ", "+")
		if final in imagelinks:
			contentimagelist.append(imagelinks[final])
	for keys in collaborative.keys():   
		name = keys
		final = ""
		if "," in name:
			namearr = name.split(",")
			temp = namearr[1].split(" ")
			final = temp[1]+"+"+namearr[0]
		else:
			 namearr = name.split(" ")
			 for i in range(0,len(namearr)-1):
			 	if namearr[i][0] == "(":
			 		continue
			 	else:
			 		final = final+namearr[i]+"+"
			 final = final[0:-1]
		final = final.replace(" ", "+")
		if final in imagelinks:
			collaborativeimagelist.append(imagelinks[final])
	for keys in hybrid.keys():   
		name = keys
		final = ""
		if "," in name:
			namearr = name.split(",")
			temp = namearr[1].split(" ")
			final = temp[1]+"+"+namearr[0]
		else:
			 namearr = name.split(" ")
			 for i in range(0,len(namearr)-1):
			 	if namearr[i][0] == "(":
			 		continue
			 	else:
			 		final = final+namearr[i]+"+"
			 final = final[0:-1]
		final = final.replace(" ", "+")
		if final in imagelinks:
			hybridimagelist.append(imagelinks[final])

@app.route('/')
def homepage():
	fetchimage('211')
	return render_template('index.html',hybridimagelist=hybridimagelist)

@app.route('/userpage', methods=['GET', 'POST'])
def userpage():
	global contentimagelist, hybridimagelist,collaborativeimagelist
	if request.method == 'POST':
		session['userid'] = request.form['userid']
		fetchimage(request.form['userid'])
		if(len(contentimagelist)==0 and len(collaborativeimagelist)==0 and len(hybridimagelist)==0):
			return render_template('404.html')
		if(len(hybridimagelist)<4):
			hybridimagelist = collaborativeimagelist
		return render_template('homepage.html',contentimagelist=contentimagelist, collaborativeimagelist=collaborativeimagelist, hybridimagelist=hybridimagelist)

if __name__ == '__main__':
	with open("links.txt", "r") as ins:
		for line in ins:
			temp = line.split("|")
			if temp[0] not in imagelinks:
				imagelinks[temp[0]] = temp[1]
	app.run(debug=True)