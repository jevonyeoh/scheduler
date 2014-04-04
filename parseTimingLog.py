'''
Helper file to parse timing.log output into csv file.
'''

#!/usr/bin/python

import sys
import ast

if len(sys.argv) > 1:
	fname = sys.argv[1]

outfile = "timing.csv"

# properties that we want to output
requestSpecProperties = ["num_instances", "instance_type"]

def outputHeader():
	return "num_instances,instance_type_name,timing\n"

def extractFilterPropInfo(line):
	x = ast.literal_eval(line)
	return

def extractRequestSpecInfo(line):
	x = ast.literal_eval(line)
	# obtain necessary variables
	lineout = x.get("num_instances", "0")
	lineout = str(lineout) + "," + str(x["instance_type"]["name"]) + ","
	return lineout

def parseFile(filename):
	f = open(fname, 'r')
	fo = open(outfile, 'w')

	fo.write(outputHeader())

	readFilterProperties = False
	readRequestSpec = False
	readTiming = False

	lineToWrite = ""

	for i, line in enumerate(f):

		if readFilterProperties:
			readFilterProperties = False
		elif readRequestSpec:
			lineToWrite = lineToWrite + extractRequestSpecInfo(line) 
			readRequestSpec = False
		elif readTiming:
			lineToWrite = lineToWrite + line + "\n"
			# write line now since it's the last variable to check for
			fo.write(lineToWrite)
			lineToWrite = ""
			readTiming = False

		if line.strip() == "Filter properties":
			print "updating filter bool"
			readFilterProperties = True
		elif line.strip() == "Request spec":
			print "updating request bool"
			readRequestSpec = True
		elif line.strip() == "Time taken to schedule":
			readTiming = True

	f.close()
	fo.close()

if __name__ == "__main__":
	parseFile(fname)