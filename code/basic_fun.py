# -*- coding:utf8 -*-
import math
import csv

def get_ema_data(lastprice,pre_ema_val,period):
	# this is used to get the ema get ema data
	if period ==1:
		return lastprice
	tmp = float(((period -1)*pre_ema_val + 2*lastprice))/(period + 1)
	return tmp

def write_data_to_csv(data,path):
	csvfile = file(path, 'wb')
	writer = csv.writer(csvfile)
 	writer.writerows(data)
	csvfile.close()

def write_data_to_csv_add(data,path):
	csvfile = file('path', 'ab+')
	writer = csv.writer(csvfile)
 	writer.writerows(data)
	csvfile.close()
def write_txt(data,path):
	f = open(path,'a')
	f.write(data)
	f.close()
def read_data_from_csv(path):
	f = open(path,'rb')
	reader = csv.reader(f)
	ret = []
	for row in reader:
		# obj.get_md_data(row)
		ret.append(row)
	# only get the day data
	return ret

def write_config_info(long_position,short_position,_parting_array_last,zs_now_dir,zs_index,quick_ema,slow_ema,diff_array,dea_period,
	lastlastk_array,lastk_array,midkon,dd_val,dd_dir,config_path):
	config_file = open(str(config_path),"w")
	line0 = "zs_index:,"+str(zs_index)
	line00 = "zs_now_dir:,"+str(zs_now_dir)
	line000 = "long_position:,"+str(long_position)
	line0000 = "short_position:,"+str(short_position)
	

	line00000 = "outbar_parting_array_last:"
	for x in xrange(0,len(_parting_array_last)):
		line00000 = line00000 + "," + str(_parting_array_last[x])
	# line000000 = "inbar_parting_array_last:"
	# for x in xrange(0,len(_inbar_parting_array_last)):
	# 	line000000 = line000000 + "," + str(_inbar_parting_array_last[x])

	# line0000000 = "redmacdbar:,"+str(redmacdbar)
	# line00000000 = "greenmacdbar:,"+str(greenmacdbar)
	# line000000000 = "macd_bar_short_list:"
	# for x in xrange(0,len(macd_bar_short_list)):
	# 	line000000000 = line000000000 + "," + str(macd_bar_short_list[x])

	line1 = "quick_ema_val:,"+str(quick_ema)
	line2 = "slow_ema_val:,"+str(slow_ema)
	line3 = "diff_array:"
	left = len(diff_array) - dea_period
	if left<0:
		left = 0
	for i in xrange(left,len(diff_array)):
		line3 = line3 + "," + str(diff_array[i])
	line4 = "lastlastk_array:"
	# "dont save the k mesg time"
	for x in xrange(0,len(lastlastk_array)):
		line4 = line4 + "," + str(lastlastk_array[x])
	line5 = "lastk_array:"
	for x in xrange(0,len(lastk_array)):
		line5 = line5 + "," + str(lastk_array[x])
	line6 = "midkon:,"+str(midkon)
	line7 = "dd_val:,"+str(dd_val)
	line8 = "dd_dir:,"+str(dd_dir)
	write_lines = [line0+'\n',line00+'\n',line000+'\n',line0000+'\n',line00000+'\n',line1+'\n',line2+'\n',line3+'\n',line4+'\n',line5+'\n',line6+'\n',line7+'\n',line8]
	config_file.writelines(write_lines)
	config_file.close()
def get_zhongshu_msg(path,zs_now_upvalue,zs_now_downvalue,zs_now_uptime,zs_now_downtime,zs_now_dir,zs_now_zoushilist,
				zs_last_upvalue,zs_last_downvalue,zs_last_uptime,zs_last_downtime,zs_last_dir,zs_last_zoushilist):
	try:
		file = open(path)
	except Exception as e:
		file = open(path,"w")
		return
	lines = file.readlines()
	if len(lines)==0:
		return
	if len(lines)==1:
		splitline=lines[0].split(',')
		zs_now_upvalue=float(splitline[0])
		zs_now_uptime=splitline[1]
		zs_now_downvalue=float(splitline[2])
		zs_now_downtime=splitline[3]
		zs_now_dir=int(splitline[4])
		zs_now_zoushilist.append(float((splitline[5].split('_'))[0]))
		zs_now_zoushilist.append(float((splitline[5].split('_'))[1]))
		zs_now_zoushilist.append(int((splitline[5].split('_'))[2]))
		zs_now_zoushilist.append(splitline[5].split('_')[3])
		zs_now_zoushilist.append(float((splitline[5].split('_'))[4]))
		zs_now_zoushilist.append(float(splitline[5].split('_')[5]))
		zs_now_zoushilist.append(splitline[5].split('_')[6])

	if len(lines)>1:
		splitline=lines[-1].split(',')
		zs_now_upvalue=float(splitline[0])
		zs_now_uptime=splitline[1]
		zs_now_downvalue=float(splitline[2])
		zs_now_downtime=splitline[3]
		zs_now_dir=int(splitline[4])
		zs_now_zoushilist.append(float((splitline[5].split('_'))[0]))
		zs_now_zoushilist.append(float((splitline[5].split('_'))[1]))
		zs_now_zoushilist.append(int((splitline[5].split('_'))[2]))
		zs_now_zoushilist.append(splitline[5].split('_')[3])
		zs_now_zoushilist.append(float((splitline[5].split('_'))[4]))
		zs_now_zoushilist.append(float(splitline[5].split('_')[5]))
		zs_now_zoushilist.append(splitline[5].split('_')[6])

		splitline=lines[-2].split(',')
		zs_last_upvalue=float(splitline[0])
		zs_last_uptime=splitline[1]
		zs_last_downvalue=float(splitline[2])
		zs_last_downtime=splitline[3]
		zs_last_dir=int(splitline[4])
		zs_last_zoushilist.append(float((splitline[5].split('_'))[0]))
		zs_last_zoushilist.append(float((splitline[5].split('_'))[1]))
		zs_last_zoushilist.append(int((splitline[5].split('_'))[2]))
		zs_last_zoushilist.append(splitline[5].split('_')[3])
		zs_last_zoushilist.append(float((splitline[5].split('_'))[4]))
		zs_last_zoushilist.append(float((splitline[5].split('_'))[5]))
		zs_last_zoushilist.append(splitline[5].split('_')[6])





def get_config_info(long_position,short_position,_parting_array_last,zs_dir_array,zs_index_array,quick_ema_array,slow_ema_array,diff_array,
	lastlastk_array,lastk_array,midkone_array,dd_val_array,dd_dir_array,config_path):
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
		elif "zs_index" in line:
			
			line = line.split(',')
			zs_index_array.append(float(line[1].strip()))
			print "this is zs_index    ",zs_index_array[0]
		
		elif "zs_now_dir" in line:
			
			line = line.split(',')
			zs_dir_array.append(round(float(line[1].strip())))
			print "this is zs_dir_array    "
		elif "long_position" in line:
			
			line = line.split(',')
			long_position.append(round(float(line[1].strip())))
			print "this is long_position    "
		elif "short_position" in line:
			
			line = line.split(',')
			short_position.append(round(float(line[1].strip())))
			print "this is short_position    "
		elif "outbar_parting_array_last" in line:
			print "this is parting_array_last   ",line
			line = line.split(',')[1:]
			for tmp in line:
				_parting_array_last.append(tmp.strip())
		elif "slow_ema_val" in line:
			print "this is slow_ema_val"
			line = line.split(',')
			slow_ema_array.append(float(line[1].strip()))
			# print "the length of lastprice is: " + str(len(lastprice_array))
		elif "diff_array" in line:
			print "this is diff_array"
			line = line.split(',')[1:]
			for tmp in line:
				diff_array.append(float(tmp.strip()))
		elif "lastlastk_array" in line:
			print "this is lastlastk_array"
			line = line.split(',')[1:]
			index=len(line)
			for x in range(0,index-1):
				lastlastk_array.append(float(tmp.strip()))
			lastlastk_array.append(tmp.strip())
		elif "lastk_array" in line:
			print "this is lastk_array"
			line = line.split(',')[1:]
			index=len(line)
			for x in range(0,index-1):
				lastlastk_array.append(float(tmp.strip()))
			lastlastk_array.append(tmp.strip())
		elif "midkon" in line:
			print "this is midkon"
			line = line.split(',')[1:]
			for tmp in line:
				midkone_array.append(float(tmp.strip()))
		elif "dd_val" in line:
			print "this is dd_val"
			line = line.split(',')[1:]
			for tmp in line:
				dd_val_array.append(float(tmp.strip()))
		elif "dd_dir" in line:
			print "this is dd_dir"
			line = line.split(',')[1:]
			for tmp in line:
				dd_dir_array.append(float(tmp.strip()))
		else:
			print "this is not the config line"
	config_file.close()

if __name__=='__main__': 

# -*- coding:utf8 -*-
import math
import csv

def get_ema_data(lastprice,pre_ema_val,period):
	# this is used to get the ema get ema data
	if period ==1:
		return lastprice
	tmp = float(((period -1)*pre_ema_val + 2*lastprice))/(period + 1)
	return tmp

def write_data_to_csv(data,path):
	csvfile = file(path, 'wb')
	writer = csv.writer(csvfile)
 	writer.writerows(data)
	csvfile.close()

def write_data_to_csv_add(data,path):
	csvfile = file('path', 'ab+')
	writer = csv.writer(csvfile)
 	writer.writerows(data)
	csvfile.close()
def write_zhongshu(data,path):
	f = open(path,'a')
	f.write(data)
	f.close()
def read_data_from_csv(path):
	f = open(path,'rb')
	reader = csv.reader(f)
	ret = []
	for row in reader:
		# obj.get_md_data(row)
		ret.append(row)
	# only get the day data
	return ret

def write_config_info(quick_ema,slow_ema,diff_array,dea_period,
	lastlastk_array,lastk_array,midkon,dd_val,dd_dir,config_path):
	config_file = open(str(config_path),"w")
	line1 = "quick_ema_val:,"+str(quick_ema)
	line2 = "slow_ema_val:,"+str(slow_ema)
	line3 = "diff_array:"
	left = len(diff_array) - dea_period
	if left<0:
		left = 0
	for i in xrange(left,len(diff_array)):
		line3 = line3 + "," + str(diff_array[i])
	line4 = "lastlastk_array:"
	# "dont save the k mesg time"
	for x in xrange(0,len(lastlastk_array)-1):
		line4 = line4 + "," + str(lastlastk_array[x])
	line5 = "lastk_array:"
	for x in xrange(0,len(lastk_array)-1):
		line5 = line5 + "," + str(lastk_array[x])
	line6 = "midkon:,"+str(midkon)
	line7 = "dd_val:,"+str(dd_val)
	line8 = "dd_dir:,"+str(dd_dir)
	write_lines = [line1+'\n',line2+'\n',line3+'\n',line4+'\n',line5+'\n',line6+'\n',line7+'\n',line8]
	config_file.writelines(write_lines)
	config_file.close()
def get_zhongshu_msg(path,zs_now_upvalue,zs_now_downvalue,zs_now_uptime,zs_now_downtime,zs_now_dir,zs_now_zoushilist,
				zs_last_upvalue,zs_last_downvalue,zs_last_uptime,zs_last_downtime,zs_last_dir,zs_last_zoushilist):
	try:
		file = open(path)
	except Exception as e:
		file = open(path,"w")
		return
	lines = file.readlines()
	if len(lines)==0:
		return
	if len(lines)==1:
		splitline=lines[0].split(',')
		zs_now_upvalue=float(splitline[0])
		zs_now_uptime=splitline[1]
		zs_now_downvalue=float(splitline[2])
		zs_now_downtime=splitline[3]
		zs_now_dir=int(splitline[4])
		zs_now_zoushilist.append(float((splitline[5].split('_'))[0]))
		zs_now_zoushilist.append(float((splitline[5].split('_'))[1]))
		zs_now_zoushilist.append(int((splitline[5].split('_'))[2]))
		zs_now_zoushilist.append(splitline[5].split('_')[3])
		zs_now_zoushilist.append(float((splitline[5].split('_'))[4]))
		zs_now_zoushilist.append(splitline[5].split('_')[5])

	if len(lines)>1:
		splitline=lines[-1].split(',')
		zs_now_upvalue=float(splitline[0])
		zs_now_uptime=splitline[1]
		zs_now_downvalue=float(splitline[2])
		zs_now_downtime=splitline[3]
		zs_now_dir=int(splitline[4])
		zs_now_zoushilist.append(float((splitline[5].split('_'))[0]))
		zs_now_zoushilist.append(float((splitline[5].split('_'))[1]))
		zs_now_zoushilist.append(int((splitline[5].split('_'))[2]))
		zs_now_zoushilist.append(splitline[5].split('_')[3])
		zs_now_zoushilist.append(float((splitline[5].split('_'))[4]))
		zs_now_zoushilist.append(splitline[5].split('_')[5])

		splitline=lines[-2].split(',')
		zs_last_upvalue=float(splitline[0])
		zs_last_uptime=splitline[1]
		zs_last_downvalue=float(splitline[2])
		zs_last_downtime=splitline[3]
		zs_last_dir=int(splitline[4])
		zs_last_zoushilist.append(float((splitline[5].split('_'))[0]))
		zs_last_zoushilist.append(float((splitline[5].split('_'))[1]))
		zs_last_zoushilist.append(int((splitline[5].split('_'))[2]))
		zs_last_zoushilist.append(splitline[5].split('_')[3])
		zs_last_zoushilist.append(float((splitline[5].split('_'))[4]))
		zs_last_zoushilist.append(splitline[5].split('_')[5])





def get_config_info(quick_ema_array,slow_ema_array,diff_array,
	lastlastk_array,lastk_array,midkone_array,dd_val_array,dd_dir_array,config_path):
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
			print "this is diff_array"
			line = line.split(',')[1:]
			for tmp in line:
				diff_array.append(float(tmp.strip()))
		elif "lastlastk_array" in line:
			print "this is lastlastk_array"
			line = line.split(',')[1:]
			for tmp in line:
				lastlastk_array.append(float(tmp.strip()))
		elif "lastk_array" in line:
			print "this is lastk_array"
			line = line.split(',')[1:]
			for tmp in line:
				lastk_array.append(float(tmp.strip()))
		elif "midkon" in line:
			print "this is midkon"
			line = line.split(',')[1:]
			for tmp in line:
				midkone_array.append(float(tmp.strip()))
		elif "dd_val" in line:
			print "this is dd_val"
			line = line.split(',')[1:]
			for tmp in line:
				dd_val_array.append(float(tmp.strip()))
		elif "dd_dir" in line:
			print "this is dd_dir"
			line = line.split(',')[1:]
			for tmp in line:
				dd_dir_array.append(float(tmp.strip()))
		else:
			print "this is not the config line"
	config_file.close()

if __name__=='__main__': 
	print "this is basic fun like c++ so"