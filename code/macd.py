# coding: utf-8
import sys, csv , operator  
#!/usr/bin/python
# -*- coding:utf8 -*-
import basic_fun as bf
import os
quicktime=120
slowtime=360
quick=12
slow=26
emadea=9
CLOSE_LASTPRICE = 1


class macd(object):
	"""docstring for macd"""
	def __init__(self):
		super(macd, self).__init__()
		self._quick_ema = 0
		self._slow_ema = 0
		self._quick_period = 12
		self._slow_period = 26
		self._now_bar_num = 0
		self._diff = 0
		self._dea = 0
		self._dea_period = 9
		self._diff_array = []

		self._config_file = 320

		if self._now_bar_num ==0:
			print "this is init function " + str(self._config_file)
			quick_ema_array = []
			slow_ema_array = []
			config_file = "../config/"+str(self._config_file)
			bf.get_config_info(quick_ema_array,slow_ema_array,self._diff_array,config_file)
			if len(quick_ema_array)==0:
				self._quick_ema = 0
				self._slow_ema = 0 
			else:
				self._quick_ema = quick_ema_array[0]
				self._slow_ema = slow_ema_array[0]
				self._now_bar_num = 99


	def get_diff_val(self,lastprice):
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

	def get_md_line(self,line):
		self._now_bar_num +=1
		close_lastrpice = float(line[CLOSE_LASTPRICE])
		diff_val = self.get_diff_val(close_lastrpice)

		self._diff_array.append(diff_val)
		dea_val = self.get_dea_val()

		if len(line) >=7 :
			line[5] = round(diff_val,2)
			line[6] = round(dea_val,2)
		else:
			line.append(round(diff_val,2))
			line.append(round(dea_val,2))

		return line

def write_data_to_csv(result,filename):
	print "start to write the file "+filename
	csvfile = file(filename, 'wb')
	writer = csv.writer(csvfile)
 	writer.writerows(result)
	csvfile.close()

		
def read_data_from_csv(path):
	f = open(path,'rb')
	reader = csv.reader(f)
	ret = []
	for row in reader:
		# obj.get_md_data(row)
		ret.append(row)
	# only get the day data
	return ret

def main():
	date = [20171023]
	instrumentIds = ["rb1801"]
	for day in date:
		for instrumentId in instrumentIds:
			macd_obj = macd()
			ret = []
			path = '../kdata/'+instrumentId + '_' + str(day) + '.csv'
			data = read_data_from_csv(path)

			for line in data:
				tmp = macd_obj.get_md_line(line)
				ret.append(tmp)
			write_data_to_csv(ret,path)


if __name__=='__main__': 
	main()