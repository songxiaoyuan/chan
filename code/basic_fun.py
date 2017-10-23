# -*- coding:utf8 -*-
import math
import csv

def get_ema_data(lastprice,pre_ema_val,period):
	# this is used to get the ema get ema data
	if period ==1:
		return lastprice
	tmp = float(((period -1)*pre_ema_val + 2*lastprice))/(period + 1)
	return tmp

def write_data_to_csv(path,data):
	csvfile = file(path, 'wb')
	writer = csv.writer(csvfile)
 	writer.writerows(data)
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

def write_config_info(quick_ema,slow_ema,diff_array,dea_period,config_path):
	config_file = open(str(config_path),"w")
	line1 = "quick_ema_val:,"+str(quick_ema)
	line2 = "slow_ema_val:,"+str(slow_ema)
	line3 = "diff_array:"
	left = len(diff_array) - dea_period
	if left<0:
		left = 0
	for i in xrange(left,len(diff_array)):
		line3 = line3 + "," + str(diff_array[i])
	write_lines = [line1+'\n',line2+'\n',line3+'\n']
	config_file.writelines(write_lines)
	config_file.close()

def get_config_info(quick_ema_array,slow_ema_array,diff_array,config_path):
	try:
		config_file = open(config_path)
	except Exception as e:
		config_file = open(config_path,"w")
		return
	config_file = open(config_path)
	lines = config_file.readlines()
	for line in lines:
		if "quick_ema_val" in line:
			print "this is quick_ema_val"
			line = line.split(',')
			quick_ema_array.append(float(line[1].strip()))
		elif "slow_ema_val" in line:
			print "this is slow_ema_val"
			line = line.split(',')
			slow_ema_array.append(float(line[1].strip()))
			# print "the length of lastprice is: " + str(len(lastprice_array))
		elif "diff_array" in line:
			print "this is rsiarray"
			line = line.split(',')[1:]
			for tmp in line:
				diff_array.append(float(tmp.strip()))
		else:
			print "this is not the config line"
	config_file.close()

if __name__=='__main__': 
	print "this is basic fun like c++ so"