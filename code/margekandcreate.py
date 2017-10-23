# coding: utf-8
import sys, csv , operator  
#!/usr/bin/python
# -*- coding:utf8 -*-
import os
def writeToCsv(data,path):
	#csvFile = file('D:\\py\\py\\py\\cleanData_20170522_m1709C2750.csv','w')
	#writer = csv.writer(csvFile)
	#csvFile='D:\\py\\py\\py\\cleanData_20170522_m1709P2750.csv'
	with open(path, 'wb') as csvfile:
		spamwriter = csv.writer(csvfile,dialect='excel')
		for line in data:
			spamwriter.writerow(line)
def marge(lastk,nowk,flag):
	returnlist=nowk
	if flag==1:
		if float(lastk[2])>float(nowk[2]):
			returnlist[2]=float(nowk[2])
		else:
			returnlist[2]=float(lastk[2])

		if float(lastk[3])>float(nowk[3]):
			returnlist[3]=float(nowk[3])
		else:
			returnlist[3]=float(lastk[3])

	if flag==0:

		if float(lastk[2])>float(nowk[2]):
			returnlist[2]=float(lastk[2])
		else:
			returnlist[2]=float(nowk[2])

		if float(lastk[3])>float(nowk[3]):
			returnlist[3]=float(lastk[3])
		else:
			returnlist[3]=float(nowk[3])
	return returnlist


def margek(path):
	csvFile = file(path,'rb')
	reader = csv.reader(csvFile)
	nowk=[]
	updonglist=[]


	#需要保存到配置文件里的4个变量############
	lastlastk=[]#分型最左边k线
	lastk=[]#分型中间k线
	flag=0#0:方向向上，1：方向向下，合并方向
	midkone=4#顶底之间中间的标志位，大于3 k线跟数大于1
	##############################################
	#
	#
	#
	#
	for line in reader:
		if not lastlastk:
			lastlastk=line
			updonglist.append(0)
			continue
		if not lastk:
			lastk=line
			updonglist.append(0)
			continue
		#print lastk,lastlastk
		if float(lastk[2])>float(lastlastk[2]) and float(lastk[3])>float(lastlastk[3]):#前两根k线方向向上
			flag=0
		elif float(lastk[2])<float(lastlastk[2]) and float(lastk[3])<float(lastlastk[3]):#前两根k线方向向下
			flag=1
		elif float(lastk[2])>float(lastlastk[2]):
			flag=0
		else:
			flag=1
		if (float(line[2])<=float(lastk[2]) and float(line[3])>=float(lastk[3])) or (float(line[2])>=float(lastk[2])and float(line[3])<=float(lastk[3])):#当前k线需要和前一k线合并
			getmargek=marge(lastk,line,flag)
			lastk=getmargek
			updonglist.append(0)
		else:
			if float(lastk[2])>float(line[2]) and float(lastk[2])>float(lastlastk[2]) and float(lastk[3])>float(line[3]) and float(lastk[3])>float(lastlastk[3]) and midkone>3:
				updonglist[-1]=1
				midkone=0
			if float(lastk[2])<float(line[2]) and float(lastk[2])<float(lastlastk[2]) and float(lastk[3])<float(line[3]) and float(lastk[3])<float(lastlastk[3]) and midkone>3:
				updonglist[-1]=-1
				midkone=0
			updonglist.append(0)
			lastlastk=lastk
			lastk=line
			midkone=midkone+1
	#print updonglist,len(updonglist)
	i=0
	writeline=[]
	csvFile = file(path,'rb')
	reader = csv.reader(csvFile)
	for line in reader:
		line.append(updonglist[i])
		i=i+1
		writeline.append(line)
	# print writeline
	writeToCsv(writeline,path)
	
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
	fileList=printPath(1, '../kdata/')
	for x in fileList:
		filepath='../kdata/'+x
		margek(filepath)