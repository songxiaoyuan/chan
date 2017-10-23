# -*- coding:utf8 -*-
import cx_Oracle  
import csv
import shutil
import time
import os

import basic_fun as bf

CLOSE_LASTPRICE = 1

param_dict_pb = {"config_file":310}

param_dict_rb = {"config_file":320}

param_dic_ru = {"config_file":330}

param_dic_zn = {"config_file":340}

param_dic_i = {"config_file":350}

param_dic_ni = {"config_file":360}

param_dic_al = {"config_file":370}

param_dic_hc = {"config_file":380}

param_dic_cu = {"config_file":390}

param_dic_pp = {"config_file":400}

param_dic_v = {"config_file":410}

nameDict = {
	"rb1801":{"param":[param_dict_rb]},
	"ru1801":{"param":[param_dic_ru]},
	"zn1712":{"param":[param_dic_zn]},
	"cu1711":{"param":[param_dic_cu]},
	"hc1801":{"param":[param_dic_hc]},
	"i1801":{"param":[param_dic_i]},
	"ni1801":{"param":[param_dic_ni]},
	"al1712":{"param":[param_dic_al]},
	"pp1801":{"param":[param_dic_pp]},
	"v1801":{"param":[param_dic_v]},
	"pb1712":{"param":[param_dict_pb]}
}

class CreateConfig(object):
	"""docstring for macd"""
	def __init__(self,param_dic):
		super(CreateConfig, self).__init__()
		self._quick_ema = 0
		self._slow_ema = 0
		self._quick_period = 12
		self._slow_period = 26
		self._now_bar_num = 0
		self._diff = 0
		self._dea = 0
		self._dea_period = 9
		self._diff_array = []

		self._config_file = param_dic["config_file"]


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

	def __del__(self):
		print "this is the over function"
		path = "../config/" + str(self._config_file)
		bf.write_config_info(self._quick_ema,self._slow_ema
			,self._diff_array,self._dea_period,path)

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


def start_create_config(instrumentid,data):
	print "start create the config file of " + instrumentid
	if instrumentid not in nameDict:
		print "the instrument id " + instrumentid + " is not in the dict"
	for param in nameDict[instrumentid]["param"]:
		create_config_obj = CreateConfig(param)
		for row in data:
			create_config_obj.get_md_line(row)
			# tranfer the string to float

def main():
	data =[20171020]
	instrumentid_array = ["rb1801"]
	for item in data:
		for instrumentid in instrumentid_array:
			path = "../kdata/"+instrumentid+'_'+str(item)+'.csv'
			data = bf.read_data_from_csv(path)
			start_create_config(instrumentid,data)	

if __name__=='__main__':
	main()