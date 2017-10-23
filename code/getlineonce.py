# coding: utf-8
import sys, csv , operator  
#!/usr/bin/python
# -*- coding:utf8 -*-
import basic_fun as bf
import os

LASTPRICE = 4
DATE = 0
TIME = 20
HIGH = 2
LOW = 3


class getline(object):
	"""docstring for getline"""
	def __init__(self):
		super(getline, self).__init__()
		self._parting_array = []
		self._listkmsg_array = []
		self._k_bar_tick = 0
		self._k_period = 120
		self._open_price = 0
		self._close_price = 0
		self._high_price = 0
		self._low_price = 0


		self._lastlastk_array=[]#分型最左边k线
		self._lastk_array=[]#分型中间k线
		self._flag=0#0:方向向上，1：方向向下，合并方向
		self._midkone=4#顶底之间中间的标志位，大于3 k线跟数大于1
		self._updonglist = []

	def create_k(self,time,lastprice):
		self._k_bar_tick +=1
		if self._k_bar_tick ==1:
			self._open_price = lastprice
			self._close_price = lastprice
			self._high_price = lastprice
			self._low_price = lastprice
		elif self._k_bar_tick == self._k_period:
			tmp = []
			tmp.append(self._open_price)
			tmp.append(self._close_price)
			tmp.append(self._high_price)
			tmp.append(self._low_price)
			tmp.append(time)
			self._listkmsg_array.append(tmp)
			self._k_bar_tick = 0
			return tmp
		else:
			if lastprice > self._high_price:
				self._high_price = lastprice
			if lastprice < self._low_price:
				self._low_price = lastprice
		return []

	def merge(self,lastk,nowk,flag):
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

	def mergek(self,kmesg):
		if not self._lastlastk_array:
			self._lastlastk_array=kmesg
			self._updonglist.append(0)
			return
		if not self._lastk_array:
			self._lastk_array=kmesg
			self._updonglist.append(0)
			return
		#print lastk,lastlastk
		lastk = self._lastk_array
		lastlastk = self._lastlastk_array
		if float(lastk[2])>float(lastlastk[2]) and float(lastk[3])>float(lastlastk[3]):#前两根k线方向向上
			self._flag=0
		elif float(lastk[2])<float(lastlastk[2]) and float(lastk[3])<float(lastlastk[3]):#前两根k线方向向下
			self._flag=1
		elif float(lastk[2])>float(lastlastk[2]):
			self._flag=0
		else:
			self._flag=1
		if (float(kmesg[2])<=float(lastk[2]) and float(kmesg[3])>=float(lastk[3])) or (float(kmesg[2])>=float(lastk[2])and float(kmesg[3])<=float(lastk[3])):#当前k线需要和前一k线合并
			getmargek=self.merge(lastk,kmesg,self._flag)
			self._lastk_array=getmargek
			self._updonglist.append(0)
		else:
			if float(lastk[2])>float(kmesg[2]) and float(lastk[2])>float(lastlastk[2]) and float(lastk[3])>float(kmesg[3]) and float(lastk[3])>float(lastlastk[3]) and self._midkone>3:
				self._updonglist[-1]=1
				self._midkone=0
			if float(lastk[2])<float(kmesg[2]) and float(lastk[2])<float(lastlastk[2]) and float(lastk[3])<float(kmesg[3]) and float(lastk[3])<float(lastlastk[3]) and self._midkone>3:
				self._updonglist[-1]=-1
				self._midkone=0
			self._updonglist.append(0)
			self._lastlastk_array=lastk
			self._lastk_array=kmesg
			self._midkone=self._midkone+1

	def get_merge_line(self,listkmsg_array,updonglist):
		if len(listkmsg_array) != len(updonglist):
			print "the list of k mesg is not equal updonglist"
			return 
		if len(listkmsg_array) < 3:
			print "the list is small and not parting"
			return

		parting = float(updonglist[-2])
		line = listkmsg_array[-2]
		time = line[4]

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

	def get_md_line(self,line):
		lastprice = float(line[LASTPRICE])
		time = line[DATE]+" "+line[TIME]
		kmesg = self.create_k(time,lastprice)
		if len(kmesg) ==0:
			return 
		else:
			# get one k line
			self.mergek(kmesg)
			self.get_merge_line(self._listkmsg_array,self._updonglist)
		

	def get_line_data(self):
		ret = []
		for x in xrange(0,len(self._listkmsg_array)):
			tmp = self._listkmsg_array[x]
			tmp.append(self._updonglist[x])
			time = tmp[4]
			for line in self._parting_array:
				if line[0] == time:
					tmp.append(line[2])
					break
			if len(tmp) == 6:
				tmp.append(0)
			ret.append(tmp)
		return ret

def main():
	date = [20171023]
	instrumentIds = ["rb1801"]
	for day in date:
		for instrumentId in instrumentIds:
			getline_obj = getline()
			path = '../data/'+instrumentId + '_' + str(day) + '.csv'
			data = bf.read_data_from_csv(path)

			for line in data:
				tmp = getline_obj.get_md_line(line)
			data = getline_obj.get_line_data()
			path = '../kdata/'+instrumentId + '_' + str(day) + '_total.csv'
			bf.write_data_to_csv(data,path)


if __name__=='__main__': 
	main()