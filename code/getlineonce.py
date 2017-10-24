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
	def __init__(self,param_dict):
		super(getline, self).__init__()
		self._parting_array = []
		self._listkmsg_array = []
		self._k_bar_tick = 0
		self._k_period = 120
		self._open_price = 0
		self._close_price = 0
		self._high_price = 0
		self._low_price = 0

		self._lastprice = 0
		self._time = 0

		self._instrumentid = param_dict["instrumentId"]
		self._date = param_dict["date"]

		self._dd_value=0#顶底value
		self._dd_dir=0#1：顶  -1：低
		self._lastlastk_array=[]#分型最左边k线
		self._lastk_array=[]#分型中间k线
		self._midkone=4#顶底之间中间的标志位，大于3 k线跟数大于1
		self._updonglist = []

		



		# macd mesg
		self._quick_ema = 0
		self._slow_ema = 0
		self._quick_period = 12
		self._slow_period = 26
		self._now_bar_num = 0
		self._diff = 0
		self._dea = 0
		self._dea_period = 9
		self._diff_array = []

		self._macd_array = []

		self._config_file = 320

		if self._now_bar_num ==0:
			print "this is init function " + str(self._config_file)
			quick_ema_array = []
			slow_ema_array = []
			midkone_array = []
			dd_val_array = []
			dd_dir_array = []
			config_file = "../config/"+str(self._config_file)
			bf.get_config_info(quick_ema_array,slow_ema_array,self._diff_array,
				self._lastlastk_array,self._lastk_array,midkone_array,dd_val_array,dd_dir_array,
			    config_file)
			if len(quick_ema_array)==0:
				self._quick_ema = 0
				self._slow_ema = 0 
				self._midkone = 4
			else:
				self._quick_ema = quick_ema_array[0]
				self._slow_ema = slow_ema_array[0]
				self._now_bar_num = 99
				self._midkone = midkone_array[0]
				self._dd_value = dd_val_array[0]
				self._dd_dir = dd_dir_array[0]

	def __del__(self):
		print "this is the over function and save the config file"
		self.over_fun()
		path = "../config/" + str(self._config_file)
		bf.write_config_info(self._quick_ema,self._slow_ema,
			self._diff_array,self._dea_period,
			self._lastlastk_array,self._lastk_array,self._midkone,self._dd_value,self._dd_dir,path)

		self.write_data_to_file()

	def over_fun(self):
		# save the last k mesg
		tmp = []
		tmp.append(self._open_price)
		tmp.append(self._close_price)
		tmp.append(self._high_price)
		tmp.append(self._low_price)
		tmp.append(self._time)
		self._listkmsg_array.append(tmp)

		# mergek and create the parting
		self.mergek(tmp)
		self.get_merge_line(self._listkmsg_array,self._updonglist)

		diff_val = self.get_diff_val(self._lastprice)
		self._diff_array.append(diff_val)
		dea_val = self.get_dea_val()
		tmp = [self._time,diff_val,dea_val]
		self._macd_array.append(tmp)

	def get_diff_val(self,lastprice):
		self._now_bar_num +=1
		if self._now_bar_num < self._quick_period:
			tmp = float((self._now_bar_num - 1) * self._quick_ema + 2 * lastprice)/(self._now_bar_num + 1)
		else:
			tmp = float((self._quick_period - 1) * self._quick_ema + 2 * lastprice)/(self._quick_period + 1)
		self._quick_ema = tmp

		if self._now_bar_num < self._slow_period:
			tmp = float((self._now_bar_num - 1) * self._slow_ema + 2 * lastprice)/(self._now_bar_num + 1)
		else:
			tmp = float((self._slow_period - 1) * self._slow_ema + 2 * lastprice)/(self._slow_period + 1)
		self._slow_ema = tmp
		return self._quick_ema - self._slow_ema

	def get_dea_val(self):
		l = len(self._diff_array)
		sum_val = 0
		if l < self._dea_period:
			for x in xrange(0,l):
				sum_val += self._diff_array[x]
			ret = sum_val/l
			return ret
		else:
			left = l - self._dea_period
			for x in xrange(left,l):
				sum_val += self._diff_array[x]
			ret = sum_val/self._dea_period
			return ret

	def create_k(self,time,lastprice):
		self._k_bar_tick +=1
		self._close_price = lastprice
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
				if self._dd_dir==0 or (self._dd_dir==1 and lastk[1]>self._dd_value) or self._dd_dir==-1:
					if len(self._updonglist) ==0:
						self._updonglist.append(1)
					else:
						self._updonglist[-1]=1
					self._midkone=0
					self._dd_dir=1
					self._dd_value=lastk[1]


			if float(lastk[2])<float(kmesg[2]) and float(lastk[2])<float(lastlastk[2]) and float(lastk[3])<float(kmesg[3]) and float(lastk[3])<float(lastlastk[3]) and self._midkone>3:
				if self._dd_dir==0 or (self._dd_dir==-1 and lastk[1]<self._dd_value) or self._dd_dir==1:
					if len(self._updonglist) ==0:
						self._updonglist.append(-1)
					else:
						self._updonglist[-1]=-1
					self._midkone=0
					self._dd_dir=-1
					self._dd_value=lastk[1]
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
		self._lastprice = float(line[LASTPRICE])
		self._time = line[DATE]+" "+line[TIME]
		kmesg = self.create_k(self._time,self._lastprice)
		if len(kmesg) ==0:
			return 
		else:
			# get one k line
			self.mergek(kmesg)
			self.get_merge_line(self._listkmsg_array,self._updonglist)
			# caculate the macd
			diff_val = self.get_diff_val(self._lastprice)
			self._diff_array.append(diff_val)
			dea_val = self.get_dea_val()
			tmp = [self._time,diff_val,dea_val]
			self._macd_array.append(tmp)
		

	def write_data_to_file(self):
		ret = []
		if len(self._listkmsg_array) !=  len(self._updonglist):
			print "len(self._listkmsg_array) !=  len(self._updonglist)"
			return
		if len(self._listkmsg_array) !=  len(self._macd_array):
			print "len(self._listkmsg_array) !=  len(self._macd_array)"
			return
		for x in xrange(0,len(self._listkmsg_array)):
			tmp = self._listkmsg_array[x]
			tmp.append(self._updonglist[x])
			# tmp.append(round(self._macd_array[x][1],2))
			# tmp.append(round(self._macd_array[x][2],2))
			time = tmp[4]
			for line in self._parting_array:
				if line[0] == time:
					tmp.append(line[2])
					break
			if len(tmp) == 6:
				tmp.append(0)
			ret.append(tmp)
		path = "../kdata/"+self._instrumentid+"_"+str(self._date)+".csv"
		bf.write_data_to_csv(ret,path)

def main():
	date1 = [20171016,20171017,20171018,20171019,20171020]
	date2 = [20171023,20171024]
	date = date1 + date2
	instrumentIds = ["rb1801"]
	for day in date:
		for instrumentId in instrumentIds:
			param_dict = {"instrumentId":instrumentId,"date":day}
			getline_obj = getline(param_dict)
			path = '../data/'+instrumentId + '_' + str(day) + '.csv'
			data = bf.read_data_from_csv(path)

			for line in data:
				tmp = getline_obj.get_md_line(line)
			# data = getline_obj.get_line_data()
			# path = '../kdata/'+instrumentId + '_' + str(day) + '_total.csv'
			# bf.write_data_to_csv(data,path)


if __name__=='__main__': 
	main()