# coding: utf-8
import sys, csv , operator  
#!/usr/bin/python
# -*- coding:utf8 -*-
import basic_fun as bf
import os

PARTING = 7
TIME = 4
HIGH = 2
LOW = 3


class getline(object):
	"""docstring for getline"""
	def __init__(self):
		super(getline, self).__init__()
		self._parting_array = []


	def get_md_line(self,line):
		parting = float(line[PARTING])
		time = line[TIME]
		
		if parting == 0:
			return 0
		elif parting ==1:
			lastprice = float(line[HIGH])
			if len(self._parting_array) ==0:
				self._parting_array.append([time,lastprice,1])
				return 1
			tmp = self._parting_array[-1]
			if tmp[2] ==1:
				if tmp[1] > lastprice:
					return 0
				else:
					tmp[0] = time
					tmp[1] = lastprice
					tmp[2] = 1
					self._parting_array[-1] = tmp
			elif tmp[2] == -1:
				if tmp[1] >= lastprice:
					return 0
				else:
					tmp1 = [time,lastprice,1]
					self._parting_array.append(tmp1)
		elif parting == -1:
			lastprice = float(line[LOW])
			if len(self._parting_array) ==0:
				self._parting_array.append([time,lastprice,1])
				return 1
			tmp = self._parting_array[-1]
			if tmp[2] ==1:
				if tmp[1] <= lastprice:
					return 0
				else:
					tmp1 = [time,lastprice,-1]
					self._parting_array.append(tmp1)
			elif tmp[2] == -1:
				if tmp[1] <= lastprice:
					return 0
				else:
					tmp[0] = time
					tmp[1] = lastprice
					tmp[2] = -1
					self._parting_array[-1] = tmp
		else:
			return 0

	def get_line_data(self):
		return self._parting_array

def main():
	date = [20171023]
	instrumentIds = ["rb1801"]
	for day in date:
		for instrumentId in instrumentIds:
			getline_obj = getline()
			path = '../kdata/'+instrumentId + '_' + str(day) + '.csv'
			data = bf.read_data_from_csv(path)

			for line in data:
				tmp = getline_obj.get_md_line(line)
			data = getline_obj.get_line_data()
			path = '../kdata/'+instrumentId + '_' + str(day) + '_line.csv'
			bf.write_data_to_csv(data,path)


if __name__=='__main__': 
	main()