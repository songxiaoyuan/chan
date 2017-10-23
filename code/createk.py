# coding: utf-8
import sys, csv , operator  
#!/usr/bin/python
# -*- coding:utf8 -*-
import os

def writeToCsv(data,x):
	#csvFile = file('D:\\py\\py\\py\\cleanData_20170522_m1709C2750.csv','w')
	#writer = csv.writer(csvFile)
	csvFile='../kdata/'+x
	#csvFile='D:\\py\\py\\py\\cleanData_20170522_m1709P2750.csv'
	with open(csvFile, "wb") as f:  
		fileWriter = csv.writer(f, delimiter=',')  
		for row in data:  
			fileWriter.writerow(row)
def createk(path,ktime,x):
	csvFile = file(path,'rb')
	reader = csv.reader(csvFile)
	listkmsg=[]
	evekmsg=[]
	i=0
	openprice=0
	hightprice=0
	lowprice=0
	closeprice=0
	lastline=''
	for line in reader:
		lastline=line
		i=i+1
		if line[0]==0:
			continue
		if openprice==0:
			openprice=float(line[4])
			hightprice=float(line[4])
			lowprice=float(line[4])
		if float(line[4])>hightprice:
			hightprice=float(line[4])
		if float(line[4])<lowprice:
			lowprice=float(line[4])
		if i==ktime:
			closeprice=float(line[4])
			evekmsg.append(openprice)
			evekmsg.append(closeprice)
			evekmsg.append(hightprice)
			evekmsg.append(lowprice)
			evekmsg.append(line[0]+" "+line[20])
			listkmsg.append(evekmsg)
			openprice=0
			hightprice=0
			lowprice=0
			closeprice=0
			i=0
			evekmsg=[]
	if i<ktime:
		closeprice=float(lastline[4])
		evekmsg.append(openprice)
		evekmsg.append(closeprice)
		evekmsg.append(hightprice)
		evekmsg.append(lowprice)
		evekmsg.append(lastline[0]+" "+lastline[20])
		listkmsg.append(evekmsg)
	writeToCsv(listkmsg,x)	

def printPath(level, path):
	global allFileNum
	dirList = []
	fileList = []
	files = os.listdir(path)
	dirList.append(str(level))
	for f in files:
		if(os.path.isdir(path + '\\' + f)):
			if(f[0] == '.'):
				pass
			else:
 				dirList.append(f)
		if(os.path.isfile(path + '\\' + f)):
			fileList.append(f)
	i_dl = 0
	for dl in dirList:
		if(i_dl == 0):
			i_dl = i_dl + 1
		else:
			print '-' * (int(dirList[0])), dl
			printPath((int(dirList[0]) + 1), path + '\\' + dl)
	return fileList

if __name__=='__main__': 
	fileList=printPath(1, '../data')
	for x in fileList:
		longtime=600
		shorttime=120
		shortshorttime=20
		ktime=shorttime
		filepath='../data\\'+x
		createk(filepath,ktime,x)

	