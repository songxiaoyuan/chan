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


daystartime=9*3600
pausestartime=10*3600+15*60
pauseendtime=10*3600+30*60
middayendtime=11*3600+30*60
affternornstartime=13*3600+30*60
affternornendtime=15*3600

nightstarttime=21*3600
nightendtime=23*3600

timesub=60
class getline(object):
	"""docstring for getline"""
	def __init__(self,param_dict):
		super(getline, self).__init__()


		#交易时间
		


		self._parting_array = []#保存顶底信息，包括从顶底开始对应的macd的和，顶开始保存macd负值，底开始保存macd正值
		self._listkmsg_array = []
		self._penmsg_list=[]#[startvalue,overvalue,dddir,starttime,macd红，macd绿,overtime]  dddirs=1:笔方向向上   dddir=0:比方向向下
		self._penmsgforxianduan_list=[]#用来保存还未生成线段时的笔信息
		self.xianduan_list=[]#[startvalue,overvalue,dddir,starttime,macd红，macd绿,overtime]  dddirs=1:线段方向向上   dddir=0:线段方向向上 
		self._k_bar_tick = 0
		self._k_period = 600
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

		self._nowbar_array=[]#正在形成的k线
		self._midkone=4#顶底之间中间的标志位，大于3 k线跟数大于1
		self._updonglist = []

		self._penmsg_listchangeflag=0#判断penmsg_list是否改变  0:没有变化  1：添加新一笔或修改最后一笔信息



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

		self._config_file = 220
		self.long_position=0#多单仓位 0有 1 无
		self.short_position=0#空单仓位 0有 1 无

		#######中枢相关变量#######
		self.zs_index=0#目前中枢个数
		print "init value==0!!!!!!!!"
		self.zs_now_upvalue=0#中枢上界
		self.zs_now_downvalue=0#中枢下界
		self.zs_now_uptime=''#中枢上届时间
		self.zs_now_downtime=''#中枢下届时间
		self.zs_now_dir=0#中枢方向,0向下，1向上
		self.zs_now_zoushilist=[]#进入中枢的走势【begin,over,timebegin,macd红，macd绿，timeend】
		#self.zs_now_penlist=[]

		self.zs_last_upvalue=0#中枢上界
		self.zs_last_downvalue=0#中枢下界
		self.zs_last_uptime=''#中枢上届时间
		self.zs_last_downtime=''#中枢下届时间
		self.zs_last_dir=0#中枢方向
		self.zs_last_zoushilist=[]#进入中枢的走势【begin,over,timebegin,macd红，macd绿，timeend】
		self.zs_last_penlist=[]
		#########################



		###############短周期变量###########
		#
		#
		#
		self.zs_index_short=0
		self.zs_now_dir_short=0
		self._penmsg_short_list=[]#[startvalue,overvalue,dddir,starttime,macd红，macd绿,overtime]  dddirs=1:笔方向向上   dddir=0:比方向向下
		self._penmsg_listchangeflag_short=0#判断penmsg_list是否改变  0:没有变化  1：添加新一笔或修改最后一笔信息
		self._k_bar_tick_short= 0
		self._k_period_short = 120
		self._open_price_short = 0
		self._close_price_short = 0
		self._high_price_short = 0
		self._low_price_short = 0

		self._parting_array_short = []#保存顶底信息，包括从顶底开始对应的macd的和，顶开始保存macd负值，底开始保存macd正值
		
		self.xianduan_short_list=[]#[startvalue,overvalue,dddir,starttime,macd红，macd绿,overtime]  dddirs=1:线段方向向上   dddir=0:线段方向向上
		self._listkmsg_array_short = []
		self._lastprice_short = 0
		self._time_short = 0

		self._instrumentid_short = param_dict["instrumentId"]
		self._date_short = param_dict["date"]

		self._dd_value_short=0#顶底value
		self._dd_dir_short=0#1：顶  -1：低
		self._lastlastk_array_short=[]#分型最左边k线
		self._lastk_array_short=[]#分型中间k线
		self._midkone_short=4#顶底之间中间的标志位，大于3 k线跟数大于1
		self._updonglist_short = []

		
		


		#######中枢相关变量#######
		self.zs_index_short=0#目前中枢个数
		print "init value==0!!!!!!!!"
		self.zs_now_upvalue_short=0#中枢上界
		self.zs_now_downvalue_short=0#中枢下界
		self.zs_now_uptime_short=''#中枢上届时间
		self.zs_now_downtime_short=''#中枢下届时间
		self.zs_now_dir_short=0#中枢方向,0向下，1向上
		self.zs_now_zoushilist_short=[]#进入中枢的走势【begin,over,timebegin,macd红，macd绿，timeend】
		#self.zs_now_penlist=[]

		self.zs_last_upvalue_short=0#中枢上界
		self.zs_last_downvalue_short=0#中枢下界
		self.zs_last_uptime_short=''#中枢上届时间
		self.zs_last_downtime_short=''#中枢下届时间
		self.zs_last_dir_short=0#中枢方向
		self.zs_last_zoushilist_short=[]#进入中枢的走势【begin,over,timebegin,macd红，macd绿，timeend】
		self.zs_last_penlist_short=[]
		#########################


		# macd mesg
		self._quick_ema_short = 0
		self._slow_ema_short = 0
		self._quick_period_short = 12
		self._slow_period_short = 26
		self._now_bar_num_short = 0
		self._diff_short = 0
		self._dea_short = 0
		self._dea_period_short = 9
		self._diff_array_short = []

		self._macd_array_short = []

		self._config_file_short = 220
		##############短周期变量结束###############


		if self._now_bar_num ==0:
			print "this is init function " + str(self._config_file)
			quick_ema_array = []
			slow_ema_array = []
			midkone_array = []
			dd_val_array = []
			dd_dir_array = []
			zs_index_array=[]
			zs_now_dir_array=[]
			long_position_list=[]
			short_position_list=[]
			_parting_array_temp=[]
			config_file = "../config/"+str(self._k_period)+"/"+str(self._config_file)
			bf.get_config_info(long_position_list,short_position_list,_parting_array_temp,zs_now_dir_array,zs_index_array,quick_ema_array,slow_ema_array,self._diff_array,
				self._lastlastk_array,self._lastk_array,midkone_array,dd_val_array,dd_dir_array,
			    config_file)
			if len(_parting_array_temp)!=0:
				(self._parting_array).append(_parting_array_temp)
			print 'get_configinfo   ',self._parting_array
			
			

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
				self.zs_index=zs_index_array[0]
				self.zs_now_dir=zs_now_dir_array[0]
				self.long_position=long_position_list[0]
				self.short_position=short_position_list[0]

			path = "../kdata/"+str(self._k_period)+"/"+self._instrumentid+"_zhongshu.txt"
			self.get_zhongshu_msg(path)
			print 'now self.zs_index  ',self.zs_index,'   zhongshu dir   ',self.zs_now_dir
			penpath= "../kdata/"+str(self._k_period)+"/"+self._instrumentid+"_penmsg.csv"
			self._penmsg_list=bf.read_data_from_csv(penpath)
			print self._penmsg_list
			if float((self._penmsg_list[0])[0])==0:
				self._penmsg_list=[]
			print 'this is  read pengmsg    ',self._penmsg_list
		if self._now_bar_num_short ==0:
			print "this is init function " + str(self._config_file_short)
			quick_ema_array = []
			slow_ema_array = []
			midkone_array = []
			dd_val_array = []
			dd_dir_array = []
			zs_index_short_array=[]
			zs_now_dir_short_array=[]
			long_position_short_list=[]
			short_position_short_list=[]
			_parting_array_temp=[]
			config_file = "../config/"+str(self._k_period_short)+"/"+str(self._config_file_short)
			bf.get_config_info(long_position_short_list,short_position_short_list,_parting_array_temp,zs_now_dir_short_array,zs_index_short_array,quick_ema_array,slow_ema_array,self._diff_array_short,
				self._lastlastk_array_short,self._lastk_array_short,midkone_array,dd_val_array,dd_dir_array,
			    config_file)
			if len(_parting_array_temp)!=0:
				pass
				(self._parting_array_short).append(_parting_array_temp)
			print 'get_configinfo   ',self._parting_array_short
		# self.zs_now_upvalue=0#中枢上界
		# self.zs_now_downvalue=0#中枢下界
		# self.zs_now_uptime=''#中枢上届时间
		# self.zs_now_downtime=''#中枢下届时间
		# self.zs_now_dir=0#中枢方向,0向下，1向上
		# self.zs_now_zoushilist=[]#进入中枢的走势【begin,over,time,macd面积】
		# 
		# # self.zs_last_upvalue=0#中枢上界
		# self.zs_last_downvalue=0#中枢下界
		# self.zs_last_uptime=''#中枢上届时间
		# self.zs_last_downtime=''#中枢下届时间
		# self.zs_last_dir=0#中枢方向
		# self.zs_last_zoushilist=[]#进入中枢的走势【begin,over,time,macd面积】
			# path = "../kdata/"+str(self._k_period)+"/"+self._instrumentid+"_zhongshu.txt"
			# bf.get_zhongshu_msg(path,self.zs_now_upvalue,self.zs_now_downvalue,self.zs_now_uptime,self.zs_now_downtime,self.zs_now_dir,self.zs_now_zoushilist,self.zs_last_upvalue,self.zs_last_downvalue,self.zs_last_uptime,self.zs_last_downtime,self.zs_last_dir,self.zs_last_zoushilist)

			if len(quick_ema_array)==0:
				self._quick_ema_short = 0
				self._slow_ema_short= 0 
				self._midkone_short = 4
			else:
				self._quick_ema_short = quick_ema_array[0]
				self._slow_ema_short = slow_ema_array[0]
				self._now_bar_num_short = 99
				self._midkone_short = midkone_array[0]
				self._dd_value_short = dd_val_array[0]
				self._dd_dir_short = dd_dir_array[0]
				self.zs_index_short=zs_index_short_array[0]
				self.zs_now_dir_short=zs_now_dir_short_array[0]

			path = "../kdata/"+str(self._k_period_short)+"/"+self._instrumentid+"_zhongshu.txt"
			self.get_zhongshu_msg_short(path)#####################################这个函数没有改
			#print 'now self.zs_index  ',self.zs_index,'   zhongshu dir   ',self.zs_now_dir
			penpath= "../kdata/"+str(self._k_period_short)+"/"+self._instrumentid+"_penmsg.csv"
			self._penmsg_short_list=bf.read_data_from_csv(penpath)
			if float((self._penmsg_short_list[0])[0])==0:
				self._penmsg_short_list=[]
			#print 'this is  read pengmsg    ',self._penmsg_list
	#[startvalue,overvalue,dddir,starttime,macd红，macd绿,overtime]  dddirs=1:笔方向向上   dddir=0:比方向向下
	#
	#
	# daystartime=9*3600
	# pausestartime=10*3600+15*60
	# pauseendtime=10*3600+30*60
	# middayendtime=11*3600+30*60
	# affternornstartime=13*3600+30*60
	# affternornendtime=15*3600

	# nightstarttime=21*3600
	# nightendtime=23*3600
	def changetime(self,timetochange):
		temp_timelist=timetochange.split(' ')
		day=int(temp_timelist[0])
		timelist=temp_timelist[1].split(':')
		hour=int(timelist[0])
		minute=int(timelist[1])
		second=int(timelist[2])

		return day,hour*3600+minute*60+second
		
	def equaltime(self,long_day,short_day,long_time,short_time):
		if long_day==short_day and abs(long_time-short_time)<300:
			return True
		if long_day!=short_day:
			if long_day>short_day and short_time<nightendtime and long_time>daystartime:
				if nightendtime-short_time+long_time-daystartime<300:
					return True
			elif long_day<short_day and long_time<nightendtime and short_time>daystartime:
				if nightendtime-long_time+short_time-daystartime<300:
					return True
		return False
				
			
	#[startvalue,overvalue,dddir,starttime,macd红，macd绿,overtime]  dddirs=1:笔方向向上   dddir=0:比方向向下
	def qujiantao(self,longtimepenmsg):
		long_startime=longtimepenmsg[3]
		long_startimeday,long_starttimetime=self.changetime(long_startime)
		if self.zs_now_dir_short==self.zs_last_dir_short and self.zs_now_dir_short!=round(float(longtimepenmsg[2])):
			short_startimeday_last,short_startimetime_last=self.changetime(self.zs_last_zoushilist_short[3])
			timetf=self.equaltime(long_startimeday,short_startimeday_last,long_starttimetime,short_startimetime_last)
			if timetf==True:
				if round(float(self.self.zs_now_zoushilist_short[2]))==1:
					abs(float(self.self.zs_now_zoushilist_short[4]))>abs(float((self._penmsg_short_list[-1])[4]))
					return True
				if round(float(self.self.zs_now_zoushilist_short[2]))==0:
					abs(float(self.self.zs_now_zoushilist_short[5]))>abs(float((self._penmsg_short_list[-1])[5]))
		else:
			return False
	def open_long(self,lastprice,time):
		enterzhongshu_pen_macd=0
		lastpen_macd=0		
		if len(self.zs_last_zoushilist)!=0 and len(self.zs_now_zoushilist)!=0:
			
			if self.zs_now_dir==self.zs_last_dir and self.zs_now_dir==1 and abs(float(self.zs_now_zoushilist[5]))>abs(float((self._penmsg_list[-1])[5])):
				print 'long_msg    ',self.zs_index,' ',self.zs_now_dir,' ',self.zs_last_dir,' ',self.zs_now_zoushilist[5],' ',(self._penmsg_list[-1])[5]
				print 'long----   ',lastprice,'    ',time
				if self.qujiantao(self._penmsg_list[-1])==True:#向下一笔，盘整背驰，开多条件
					ret='open_long_first  ,  '+time+' ,  '+str(lastprice)+'\n'
					path = "../kdata/"+str(self._k_period)+"/"+self._instrumentid+"_tradeposition.txt"
					bf.write_txt(ret,path)
				#self.long_position=1	


	# tmp[0] = time
	# 					tmp[1] = lastprice
	# 					tmp[2] = 1
	# 					tmp[3]=(self._parting_array[-1])[3]
	# 					tmp[4]=(self._parting_array[-1])[4]
	# 					tmp[5]=0
	# 					self._parting_array[-1] = tmp
	def exit_long(self,lastprice,time):	
		if self.long_position==1:
			if float(lastprice)<float((self._parting_array[-1])[1]):
				self.long_position=0
				ret='exit_long  ,  '+time+' ,  '+str(lastprice)+'\n'
				path = "../kdata/"+str(self._k_period)+"/"+self._instrumentid+"_tradeposition.txt"
				bf.write_txt(ret,path)
			elif round(float((self._parting_array[-1])[2]))==1:#现在有顶
				self.long_position=0
				ret='exit_long  ,  '+time+' ,  '+str(lastprice)+'\n'
				path = "../kdata/"+str(self._k_period)+"/"+self._instrumentid+"_tradeposition.txt"
				bf.write_txt(ret,path)
		
	def open_short(self,lastprice,time):
		enterzhongshu_pen_macd=0
		lastpen_macd=0
		if len(self.zs_last_zoushilist)!=0 and len(self.zs_now_zoushilist)!=0 and self.zs_now_dir==self.zs_last_dir and self.zs_now_dir==0 and abs(float(self.zs_now_zoushilist[4]))>abs(float((self._penmsg_list[-1])[4])):
			print 'short_msg    ',self.zs_index,' ',self.zs_now_dir,' ',self.zs_last_dir,' ',self.zs_now_zoushilist[4],' ',(self._penmsg_list[-1])[4]
			print 'short----   ',lastprice,'    ',time
			if self.qujiantao(self._penmsg_list[-1])==True:#向下一笔，盘整背驰，开多条件
				ret='open_short_first  ,  '+time+' ,  '+str(lastprice)+'\n'
				path = "../kdata/"+str(self._k_period)+"/"+self._instrumentid+"_tradeposition.txt"
				bf.write_txt(ret,path)
				#self.short_position=1
	def exit_short(self,lastprice,time):	
		if self.short_position==1:
			if float(lastprice)>float((self._parting_array[-1])[1]):
				self.short_position=0
				ret='exit_short  ,  '+time+' ,  '+str(lastprice)+'\n'
				path = "../kdata/"+str(self._k_period)+"/"+self._instrumentid+"_tradeposition.txt"
				bf.write_txt(ret,path)
			elif round(float((self._parting_array[-1])[2]))==-1:#现在有di
				self.short_position=0
				ret='exit_short  ,  '+time+' ,  '+str(lastprice)+'\n'
				path = "../kdata/"+str(self._k_period)+"/"+self._instrumentid+"_tradeposition.txt"
				bf.write_txt(ret,path)

	def get_zhongshu_msg(self,path):
		try:
			file = open(path)
		except Exception as e:
			file = open(path,"w")
			return
		lines = file.readlines()
		if len(lines)==0 or self.zs_index==0:
			return
		if self.zs_index==1:
			#self._penmsg_list[startvalue,overvalue,dddir,starttime,macd红，macd绿,overtime]  dddirs=1:笔方向向上   dddir=0:比方向向下
			splitline=lines[-1].split(',')
			self.zs_now_upvalue=float(splitline[0])
			self.zs_now_uptime=splitline[1]
			self.zs_now_downvalue=float(splitline[2])
			self.zs_now_downtime=splitline[3]
			self.zs_now_dir=round(float(splitline[4]))
			#self.zs_now_dir=int(splitline[4])
			self.zs_now_zoushilist.append(float((splitline[5].split('_'))[0]))
			self.zs_now_zoushilist.append(float((splitline[5].split('_'))[1]))
			self.zs_now_zoushilist.append(int((splitline[5].split('_'))[2]))
			self.zs_now_zoushilist.append(splitline[5].split('_')[3])
			self.zs_now_zoushilist.append(float((splitline[5].split('_'))[4]))
			self.zs_now_zoushilist.append(float((splitline[5].split('_'))[5]))
			self.zs_now_zoushilist.append(splitline[5].split('_')[6])

		if self.zs_index>1:
			splitline=lines[-1].split(',')
			self.zs_now_upvalue=float(splitline[0])
			self.zs_now_uptime=splitline[1]
			self.zs_now_downvalue=float(splitline[2])
			self.zs_now_downtime=splitline[3]
			self.zs_now_dir=round(float(splitline[4]))
			self.zs_now_zoushilist.append(float((splitline[5].split('_'))[0]))
			self.zs_now_zoushilist.append(float((splitline[5].split('_'))[1]))
			self.zs_now_zoushilist.append(int((splitline[5].split('_'))[2]))
			self.zs_now_zoushilist.append(splitline[5].split('_')[3])
			self.zs_now_zoushilist.append(float((splitline[5].split('_'))[4]))
			self.zs_now_zoushilist.append(float((splitline[5].split('_'))[5]))
			self.zs_now_zoushilist.append(splitline[5].split('_')[6])

			splitline=lines[-2].split(',')
			self.zs_last_upvalue=float(splitline[0])
			self.zs_last_uptime=splitline[1]
			self.zs_last_downvalue=float(splitline[2])
			self.zs_last_downtime=splitline[3]
			self.zs_last_dir=round(float(splitline[4]))
			self.zs_last_zoushilist.append(float((splitline[5].split('_'))[0]))
			self.zs_last_zoushilist.append(float((splitline[5].split('_'))[1]))
			self.zs_last_zoushilist.append(int((splitline[5].split('_'))[2]))
			self.zs_last_zoushilist.append(splitline[5].split('_')[3])
			self.zs_last_zoushilist.append(float((splitline[5].split('_'))[4]))
			self.zs_last_zoushilist.append(float((splitline[5].split('_'))[5]))
			self.zs_last_zoushilist.append(splitline[5].split('_')[6])
		print 'read zhongshu hahahah  ',self.zs_now_upvalue,'   ',self.zs_now_uptime,'   ',self.zs_now_downvalue,'   ',self.zs_now_downtime,'   ',self.zs_now_dir,'   ',self.zs_now_zoushilist
	def get_zhongshu_msg_short(self,path):
		try:
			file = open(path)
		except Exception as e:
			file = open(path,"w")
			return
		lines = file.readlines()
		if len(lines)==0 or self.zs_index_short==0:
			return
		if self.zs_index_short==1:
			#self._penmsg_list[startvalue,overvalue,dddir,starttime,macd红，macd绿,overtime]  dddirs=1:笔方向向上   dddir=0:比方向向下
			splitline=lines[-1].split(',')
			self.zs_now_upvalue_short=float(splitline[0])
			self.zs_now_uptime_short=splitline[1]
			self.zs_now_downvalue_short=float(splitline[2])
			self.zs_now_downtime_short=splitline[3]
			self.zs_now_dir_short=round(float(splitline[4]))
			#self.zs_now_dir=int(splitline[4])
			self.zs_now_zoushilist_short.append(float((splitline[5].split('_'))[0]))
			self.zs_now_zoushilist_short.append(float((splitline[5].split('_'))[1]))
			self.zs_now_zoushilist_short.append(int((splitline[5].split('_'))[2]))
			self.zs_now_zoushilist_short.append(splitline[5].split('_')[3])
			self.zs_now_zoushilist_short.append(float((splitline[5].split('_'))[4]))
			self.zs_now_zoushilist_short.append(float((splitline[5].split('_'))[5]))
			self.zs_now_zoushilist_short.append(splitline[5].split('_')[6])

		if self.zs_index_short>1:
			splitline=lines[-1].split(',')
			self.zs_now_upvalue_short=float(splitline[0])
			self.zs_now_uptime_short=splitline[1]
			self.zs_now_downvalue_short=float(splitline[2])
			self.zs_now_downtime_short=splitline[3]
			self.zs_now_dir_short=round(float(splitline[4]))
			self.zs_now_zoushilist_short.append(float((splitline[5].split('_'))[0]))
			self.zs_now_zoushilist_short.append(float((splitline[5].split('_'))[1]))
			self.zs_now_zoushilist_short.append(int((splitline[5].split('_'))[2]))
			self.zs_now_zoushilist_short.append(splitline[5].split('_')[3])
			self.zs_now_zoushilist_short.append(float((splitline[5].split('_'))[4]))
			self.zs_now_zoushilist_short.append(float((splitline[5].split('_'))[5]))
			self.zs_now_zoushilist_short.append(splitline[5].split('_')[6])

			splitline=lines[-2].split(',')
			self.zs_last_upvalue_short=float(splitline[0])
			self.zs_last_uptime_short=splitline[1]
			self.zs_last_downvalue_short=float(splitline[2])
			self.zs_last_downtime_short=splitline[3]
			self.zs_last_dir_short=round(float(splitline[4]))
			self.zs_last_zoushilist_short.append(float((splitline[5].split('_'))[0]))
			self.zs_last_zoushilist_short.append(float((splitline[5].split('_'))[1]))
			self.zs_last_zoushilist_short.append(int((splitline[5].split('_'))[2]))
			self.zs_last_zoushilist_short.append(splitline[5].split('_')[3])
			self.zs_last_zoushilist_short.append(float((splitline[5].split('_'))[4]))
			self.zs_last_zoushilist_short.append(float((splitline[5].split('_'))[5]))
			self.zs_last_zoushilist_short.append(splitline[5].split('_')[6])
		print 'read zhongshu hahahah  ',self.zs_now_upvalue_short,'   ',self.zs_now_uptime_short,'   ',self.zs_now_downvalue_short,'   ',self.zs_now_downtime_short,'   ',self.zs_now_dir_short,'   ',self.zs_now_zoushilist_short
	def savemsg(self):
		print "this is the over function and save the config file"
		#self.over_fun()
		print 'save self._parting_array is   ',self._parting_array,'  self._parting_array_short  ',self._parting_array_short
		path = "../config/" + str(self._k_period)+"/"+str(self._config_file)

		bf.write_config_info(self.long_position,self.short_position,self._parting_array[-1],self.zs_now_dir,self.zs_index,self._quick_ema,self._slow_ema,
			self._diff_array,self._dea_period,
			self._lastlastk_array,self._lastk_array,self._midkone,self._dd_value,self._dd_dir,path)


		path = "../config/" + str(self._k_period_short)+"/"+str(self._config_file_short)
		#print "haha   ",self._diff_array_short
		bf.write_config_info(self.long_position,self.short_position,self._parting_array_short[-1],self.zs_now_dir_short,self.zs_index_short,self._quick_ema_short,self._slow_ema_short,
			self._diff_array_short,self._dea_period_short,
			self._lastlastk_array_short,self._lastk_array_short,self._midkone_short,self._dd_value_short,self._dd_dir_short,path)
		#print self._penmsg_list
		self.write_data_to_file()
	#self.xianduan_list=[]#[startvalue,overvalue,dddir,starttime,macd红，macd绿,overtime,lastpenstarttime,xianduanoverflagvalue]  dddirs=1:线段方向向上   dddir=0:线段方向向xia
	#self._penmsgforxianduan_list=[]#用来保存还未生成线段时的笔信息
	def findxianduan(self,longorshort):
		if longorshort==1:
			if len(self.xianduan_list)==0 and len(self._penmsg_list)<3:
				return
			if len(self.xianduan_list)==0 and len(self._penmsg_list)==3:#第一个线段
				
				xianduan_temp=[]
				xianduan_temp.append(float((self._penmsg_list[0])[0]))#startvalue
				xianduan_temp.append(float((self._penmsg_list[2])[1]))#overvalue
				if (self._penmsg_list[0])[2]==1:
					xianduan_temp.append(1)#dddir
				else:
					xianduan_temp.append(0)#dddir
				xianduan_temp.append((self._penmsg_list[0])[3])#starttime
				xianduan_temp.append(float((self._penmsg_list[0])[4])+float((self._penmsg_list[1])[4])+float((self._penmsg_list[2])[4]))#macd红
				xianduan_temp.append(float((self._penmsg_list[0])[5])+float((self._penmsg_list[1])[5])+float((self._penmsg_list[2])[5]))#macd绿
				xianduan_temp.append((self._penmsg_list[2])[6])#overtime
				xianduan_temp.append((self._penmsg_list[2])[3])#lastpenstarttime
				xianduan_temp.append((self._penmsg_list[-3])[1])#xianduanoverflagvalue
				self.xianduan_list.append(xianduan_temp)
			elif len(self.xianduan_list)!=0:#如果已经有线段
				if (self._penmsg_list[-1])[0]==(self.xianduan_list[-1])[7] and float((self.xianduan_list[-1])[1])!=float((self._penmsg_list[-1])[1]):#没有新的一笔,最后一笔结束位置发生改变
					(self.xianduan_list[-1])[1]=float((self._penmsg_list[-1])[1])
					(self.xianduan_list[-1])[6]=float((self._penmsg_list[-1])[6])
				elif (self._penmsg_list[-1])[0]!=(self.xianduan_list[-1])[7]:#有新的一笔
					if round(float((self.xianduan_list[-1])[2]))==1 and round(float((self._penmsg_list[-1])[2]))==1:#线段方向向上 and 最后一笔方向向上
						if (self._penmsg_list[-1])[2]==1:
							pass

	def findpen(self,longorshort):
		if longorshort==1:
			#print 'updong  msg !!!!!!  ',self._parting_array
			#print 'pen change  hahah1 !!!!!    ',self._penmsg_list
			if len(self._parting_array)<2 and len(self._penmsg_list)==0:
				return

			if (len(self._penmsg_list)==0) or (len(self._penmsg_list)>0 and len(self._parting_array)>=2 and float((self._parting_array[-2])[1])!=float((self._penmsg_list[-1])[0])):#有一对顶底 or 新的一笔
				templist=[]
				templist.append((self._parting_array[-2])[1])#self._parting_array=[time,lastprice,1,macd]
				#self._penmsg_list[startvalue,overvalue,dddir,starttime,macd红，macd绿,overtime]  dddirs=1:笔方向向上   dddir=0:比方向向下
				templist.append((self._parting_array[-1])[1])
				if float((self._parting_array[-2])[1])<float((self._parting_array[-1])[1]):#向上的一笔
					templist.append(1)
				else:
					templist.append(0)
				templist.append((self._parting_array[-2])[0])
				
				templist.append((self._parting_array[-2])[3])#macd 红
				templist.append((self._parting_array[-2])[4])#macd 绿
				templist.append((self._parting_array[-1])[0])
				self._penmsg_list.append(templist)
				self._penmsg_listchangeflag=1
			#elif len(self._penmsg_list)>0 and float((self._parting_array[-2])[1])==float((self._penmsg_list[-1])[0]) and float((self._parting_array[-1])[1])!=float((self._penmsg_list[-1])[1]):#笔的结束位置变化
			elif len(self._penmsg_list)>0 and len(self._parting_array)>=1:
				#print "492!!!!!!    ",self._parting_array,"      ",self._penmsg_list
				if ((int((self._penmsg_list[-1])[2])==1 and float((self._parting_array[-1])[1])>float((self._penmsg_list[-1])[1]))  or (int((self._penmsg_list[-1])[2])==0 and float((self._parting_array[-1])[1])<float((self._penmsg_list[-1])[1]))):
					(self._penmsg_list[-1])[1]=(self._parting_array[-1])[1]
					(self._penmsg_list[-1])[4]=float((self._penmsg_list[-1])[4])+float((self._parting_array[-1])[3])#macd 红
					(self._penmsg_list[-1])[5]=float((self._penmsg_list[-1])[5])+float((self._parting_array[-1])[4])#macd 绿
					(self._penmsg_list[-1])[6]=(self._parting_array[-1])[0]
					self._penmsg_listchangeflag=1
		if longorshort==0:
			#print 'updong  msg !!!!!!  ',self._parting_array
			#print 'pen change  hahah1 !!!!!    ',self._penmsg_list
			if len(self._parting_array_short)<2 and len(self._penmsg_short_list)==0:
				return

			if (len(self._penmsg_short_list)==0) or (len(self._penmsg_short_list)>0 and len(self._parting_array_short)>=2 and float((self._parting_array_short[-2])[1])!=float((self._penmsg_short_list[-1])[0])):#有一对顶底 or 新的一笔
				templist=[]
				templist.append((self._parting_array_short[-2])[1])#self._parting_array=[time,lastprice,1,macd]
				#self._penmsg_list[startvalue,overvalue,dddir,starttime,macd红，macd绿,overtime]  dddirs=1:笔方向向上   dddir=0:比方向向下
				templist.append((self._parting_array_short[-1])[1])
				if float((self._parting_array_short[-2])[1])<float((self._parting_array_short[-1])[1]):#向上的一笔
					templist.append(1)
				else:
					templist.append(0)
				templist.append((self._parting_array_short[-2])[0])
				
				templist.append((self._parting_array_short[-2])[3])#macd 红
				templist.append((self._parting_array_short[-2])[4])#macd 绿
				templist.append((self._parting_array_short[-1])[0])
				self._penmsg_short_list.append(templist)
				self._penmsg_listchangeflag_short=1
			#elif len(self._penmsg_list)>0 and float((self._parting_array[-2])[1])==float((self._penmsg_list[-1])[0]) and float((self._parting_array[-1])[1])!=float((self._penmsg_list[-1])[1]):#笔的结束位置变化
			elif len(self._penmsg_short_list)>0 and len(self._parting_array_short)>=1:
				if ((int((self._penmsg_short_list[-1])[2])==1 and float((self._parting_array_short[-1])[1])>float((self._penmsg_short_list[-1])[1]))  or (int((self._penmsg_short_list[-1])[2])==0 and float((self._parting_array_short[-1])[1])<float((self._penmsg_short_list[-1])[1]))):
					(self._penmsg_short_list[-1])[1]=(self._parting_array_short[-1])[1]
					(self._penmsg_short_list[-1])[4]=float((self._penmsg_short_list[-1])[4])+float((self._parting_array_short[-1])[3])#macd 红
					(self._penmsg_short_list[-1])[5]=float((self._penmsg_short_list[-1])[5])+float((self._parting_array_short[-1])[4])#macd 绿
					(self._penmsg_short_list[-1])[6]=(self._parting_array_short[-1])[0]
					self._penmsg_listchangeflag_short=1				

	def findzhongshu_short(self,longorshort):
		if longorshort==0:		
			self.findpen(0)
			if len(self._penmsg_short_list)==0:#没有笔
				return
			if len(self._penmsg_short_list)==1 and self.zs_index_short==0:#只有一笔，判断中枢方向,这个方向需要提前给
				#print self._penmsg_list
				self.zs_now_dir_short=1-(self._penmsg_short_list[0])[2]
				return 
			if len(self._penmsg_short_list)<4:#至少要有4笔，才能确定中枢
				return
			if self.zs_index_short==0 and self._penmsg_listchangeflag_short==1:#如果现在没有中枢，生成新中枢
				self._penmsg_listchangeflag_short=0

				if self.zs_now_dir_short==1:#中枢方向向上
					if  float((self._penmsg_short_list[-3])[0])<float((self._penmsg_short_list[-1])[1]) and int((self._penmsg_short_list[-3])[2])==self.zs_now_dir_short and int((self._penmsg_short_list[-1])[2])==self.zs_now_dir_short :#判断是否有交集
						#(self._penmsg_list[-3])[1]>(self._penmsg_list[-1])[0]  and
						if float((self._penmsg_short_list[-3])[1])>float((self._penmsg_short_list[-1])[1]):#中书上界2
							self.zs_now_upvalue_short=(self._penmsg_short_list[-1])[1]
							self.zs_now_uptime_short=(self._penmsg_short_list[-1])[6]

						else:
							self.zs_now_upvalue_short=(self._penmsg_short_list[-3])[1]
							self.zs_now_uptime_short=(self._penmsg_short_list[-3])[6]

						if float((self._penmsg_short_list[-3])[0])>float((self._penmsg_short_list[-1])[0]):#中书下界
							self.zs_now_downvalue_short=(self._penmsg_short_list[-3])[0]
							self.zs_now_downtime_short=(self._penmsg_short_list[-3])[3]
						else:
							self.zs_now_downvalue_short=(self._penmsg_short_list[-1])[0]
							self.zs_now_downtime_short=(self._penmsg_short_list[-1])[3]


						if len(self.zs_now_zoushilist_short)==0:#之前没有进入中枢的笔，此处进入中枢的笔开始赋值
							
							self.zs_now_zoushilist_short.append((self._penmsg_short_list[-4])[0])
							self.zs_now_zoushilist_short.append((self._penmsg_short_list[-4])[1])
							self.zs_now_zoushilist_short.append((self._penmsg_short_list[-4])[2])
							self.zs_now_zoushilist_short.append((self._penmsg_short_list[-4])[3])
							tempbarred=float((self._penmsg_short_list[-4])[4])
							tempbargreen=float((self._penmsg_short_list[-4])[5])
							self.zs_now_zoushilist_short.append(tempbarred)
							self.zs_now_zoushilist_short.append(tempbargreen)
							self.zs_now_zoushilist_short.append((self._penmsg_short_list[-4])[6])
						else:#之前有进入中枢的笔，此处修改进入中枢结束，和macd值
							self.zs_now_zoushilist_short[1]=(self._penmsg_short_list[-4])[1]
							self.zs_now_zoushilist_short[4]=float(self.zs_now_zoushilist_short[4])+float((self._penmsg_short_list[-4])[4])
							self.zs_now_zoushilist_short[5]=float(self.zs_now_zoushilist_short[5])+float((self._penmsg_short_list[-4])[5])
							self.zs_now_zoushilist_short[6]=(self._penmsg_short_list[-4])[6]

						print "upupupupupup"
						ret=''
						print self.zs_now_zoushilist_short
						ret=str(self.zs_now_upvalue_short)+','+self.zs_now_uptime_short+','+str(self.zs_now_downvalue_short)+','+self.zs_now_downtime_short+','+str(self.zs_now_dir_short)+','+str(self.zs_now_zoushilist_short[0])+'_'+str(self.zs_now_zoushilist_short[1])+'_'+str(self.zs_now_zoushilist_short[2])+'_'+str(self.zs_now_zoushilist_short[3])+'_'+str(self.zs_now_zoushilist_short[4])+'_'+str(self.zs_now_zoushilist_short[5])+'_'+str(self.zs_now_zoushilist_short[6])+'\n'
						self.zs_index_short=self.zs_index_short+1
						path = "../kdata/"+str(self._k_period_short)+"/"+self._instrumentid+"_zhongshu.txt"
						print "has come here 1"
						bf.write_txt(ret,path)

					elif float((self._penmsg_short_list[-3])[0])>=float((self._penmsg_short_list[-1])[1]) and int((self._penmsg_short_list[-3])[2])==self.zs_now_dir_short and int((self._penmsg_short_list[-1])[2])==self.zs_now_dir_short :
						#self._penmsg_list[startvalue,overvalue,dddir,starttime,macd红，macd绿,overtime]  dddirs=1:笔方向向上   dddir=0:比方向向下
						#print "zoushilist      ",self.zs_now_zoushilist_short
						
						if len(self.zs_now_zoushilist_short)==0:#之前没有进入中枢的笔，此处进入中枢的笔开始赋值
							
							self.zs_now_zoushilist_short.append((self._penmsg_short_list[-4])[0])
							self.zs_now_zoushilist_short.append((self._penmsg_short_list[-4])[1])
							self.zs_now_zoushilist_short.append((self._penmsg_short_list[-4])[2])
							self.zs_now_zoushilist_short.append((self._penmsg_short_list[-4])[3])
							tempbarred=float((self._penmsg_short_list[-4])[4])+float((self._penmsg_short_list[-3])[4])
							tempbargreen=float((self._penmsg_short_list[-4])[5])+float((self._penmsg_short_list[-3])[5])
							self.zs_now_zoushilist_short.append(tempbarred)
							self.zs_now_zoushilist_short.append(tempbargreen)
							self.zs_now_zoushilist_short.append((self._penmsg_short_list[-4])[6])
						else:#之前有进入中枢的笔，此处修改进入中枢结束，和macd值
						 	self.zs_now_zoushilist_short[1]=(self._penmsg_short_list[-4])[1]


							self.zs_now_zoushilist_short[4]=float(self.zs_now_zoushilist_short[4])+float((self._penmsg_short_list[-4])[4])+float((self._penmsg_short_list[-3])[4])
							self.zs_now_zoushilist_short[5]=float(self.zs_now_zoushilist_short[5])+float((self._penmsg_short_list[-4])[5])+float((self._penmsg_short_list[-3])[5])
						 	self.zs_now_zoushilist_short[6]=(self._penmsg_short_list[-4])[6]
						 	print "_penmsg_list hahahha  upup!!!!!!!!     ",self._penmsg_short_list
						######进入中枢一笔的macd需要修改
				else:#中枢方向向下
					
					if float((self._penmsg_short_list[-3])[0])>float((self._penmsg_short_list[-1])[1]) and int((self._penmsg_short_list[-3])[2])==self.zs_now_dir_short and int((self._penmsg_short_list[-1])[2])==self.zs_now_dir_short :#判断是否有交集,有交集
						#self._penmsg_list[startvalue,overvalue,dddir,starttime,macd红，macd绿,overtime]  dddirs=1:笔方向向上   dddir=0:比方向向下
						if float((self._penmsg_short_list[-3])[0])>float((self._penmsg_short_list[-1])[0]):#中书上界
							self.zs_now_upvalue_short=(self._penmsg_short_list[-1])[0]
							self.zs_now_uptime_short=(self._penmsg_short_list[-1])[3]
						else:
							self.zs_now_upvalue_short=(self._penmsg_short_list[-3])[0]
							self.zs_now_uptime_short=(self._penmsg_short_list[-3])[3]

						if float((self._penmsg_short_list[-3])[1])>float((self._penmsg_short_list[-1])[1]):#中书下界
							self.zs_now_downvalue_short=(self._penmsg_short_list[-3])[1]
							self.zs_now_downtime_short=(self._penmsg_short_list[-3])[6]
						else:
							self.zs_now_downvalue_short=(self._penmsg_short_list[-1])[1]
							self.zs_now_downtime_short=(self._penmsg_short_list[-1])[6]

						if len(self.zs_now_zoushilist_short)==0:#之前没有进入中枢的笔，此处进入中枢的笔开始赋值
							
							self.zs_now_zoushilist_short.append((self._penmsg_short_list[-4])[0])
							self.zs_now_zoushilist_short.append((self._penmsg_short_list[-4])[1])
							self.zs_now_zoushilist_short.append((self._penmsg_short_list[-4])[2])
							self.zs_now_zoushilist_short.append((self._penmsg_short_list[-4])[3])
							tempbarred=float((self._penmsg_short_list[-4])[4])
							tempbargreen=float((self._penmsg_short_list[-4])[5])
							self.zs_now_zoushilist_short.append(tempbarred)
							self.zs_now_zoushilist_short.append(tempbargreen)
							self.zs_now_zoushilist_short.append((self._penmsg_short_list[-4])[6])
						else:#之前有进入中枢的笔，此处修改进入中枢结束，和macd值
							self.zs_now_zoushilist_short[1]=(self._penmsg_short_list[-4])[1]
							self.zs_now_zoushilist_short[4]=float(self.zs_now_zoushilist_short[4])+float((self._penmsg_short_list[-4])[4])
							self.zs_now_zoushilist_short[5]=float(self.zs_now_zoushilist_short[5])+float((self._penmsg_short_list[-4])[5])
							self.zs_now_zoushilist_short[6]=(self._penmsg_short_list[-4])[6]
							print "_penmsg_list hahahha  upup!!!!!!!!     ",self._penmsg_short_list



						ret=''
						ret=str(self.zs_now_upvalue_short)+','+self.zs_now_uptime_short+','+str(self.zs_now_downvalue_short)+','+self.zs_now_downtime_short+','+str(self.zs_now_dir_short)+','+str(self.zs_now_zoushilist_short[0])+'_'+str(self.zs_now_zoushilist_short[1])+'_'+str(self.zs_now_zoushilist_short[2])+'_'+str(self.zs_now_zoushilist_short[3])+'_'+str(self.zs_now_zoushilist_short[4])+'_'+str(self.zs_now_zoushilist_short[5])+'_'+str(self.zs_now_zoushilist_short[6])+'\n'
						print "downdowndowndowndown"
						self.zs_index_short=self.zs_index_short+1
						path = "../kdata/"+str(self._k_period_short)+"/"+self._instrumentid+"_zhongshu.txt"
						print "has come here 2"
						bf.write_txt(ret,path)

					elif float((self._penmsg_short_list[-3])[0])<=float((self._penmsg_short_list[-1])[1]) and int((self._penmsg_short_list[-3])[2])==self.zs_now_dir_short and int((self._penmsg_short_list[-1])[2])==self.zs_now_dir_short :#判断是否有交集，没有交集	
						if len(self.zs_now_zoushilist_short)==0:#之前没有进入中枢的笔，此处进入中枢的笔开始赋值
							
							self.zs_now_zoushilist_short.append((self._penmsg_short_list[-4])[0])
							self.zs_now_zoushilist_short.append((self._penmsg_short_list[-4])[1])
							self.zs_now_zoushilist_short.append((self._penmsg_short_list[-4])[2])
							self.zs_now_zoushilist_short.append((self._penmsg_short_list[-4])[3])
							tempbarred=float((self._penmsg_short_list[-4])[4])+float((self._penmsg_short_list[-3])[4])
							tempbargreen=float((self._penmsg_short_list[-4])[5])+float((self._penmsg_short_list[-3])[5])
							self.zs_now_zoushilist_short.append(tempbarred)
							self.zs_now_zoushilist_short.append(tempbargreen)
							self.zs_now_zoushilist_short.append((self._penmsg_short_list[-4])[6])
						else:#之前有进入中枢的笔，此处修改进入中枢结束，和macd值
						 	self.zs_now_zoushilist_short[1]=(self._penmsg_short_list[-4])[1]
						 	self.zs_now_zoushilist_short[4]=float(self.zs_now_zoushilist_short[4])+float((self._penmsg_short_list[-4])[4])+float((self._penmsg_short_list[-3])[4])
							self.zs_now_zoushilist_short[5]=float(self.zs_now_zoushilist_short[5])+float((self._penmsg_short_list[-4])[5])+float((self._penmsg_short_list[-3])[5])
						 	self.zs_now_zoushilist_short[6]=(self._penmsg_short_list[-4])[6]
			elif self.zs_index_short==1 and self._penmsg_listchangeflag_short==1:#如果现在已经有中枢，判断和中枢同向的笔和中枢的关系
				self._penmsg_listchangeflag_short=0
				if self.zs_now_dir_short==1:#中枢方向向上
					if float((self._penmsg_short_list[-1])[1])<self.zs_now_downvalue_short and int((self._penmsg_short_list[-1])[2])==self.zs_now_dir_short:#最后一笔没有回到中枢，中枢方向没有改变
						print "leave zhongshu no change   ",self.zs_now_upvalue_short, '  ',self.zs_now_downvalue_short, '  ',self.zs_now_dir_short, '  ',self.zs_now_uptime_short, '  ',self.zs_now_downtime_short, '  ',self.zs_now_zoushilist_short
						self.zs_last_upvalue_short=self.zs_now_upvalue_short
						self.zs_last_downvalue_short=self.zs_now_downvalue_short
						self.zs_last_dir_short=self.zs_now_dir_short
						self.zs_last_uptime_short=self.zs_now_uptime_short
						self.zs_last_downtime_short=self.zs_now_downtime_short
						self.zs_last_zoushilist_short=self.zs_now_zoushilist_short

						temp_penlist=[]
						temp_penlist.append(self._penmsg_short_list[-2])
						temp_penlist.append(self._penmsg_short_list[-1])
						self._penmsg_short_list=temp_penlist

						self.zs_index_short=0
						self.zs_now_upvalue_short=0
						self.zs_now_downvalue_short=0
						#self.zs_now_zoushilist_short=self._penmsg_list[-2]
						self.zs_now_zoushilist_short=[]
						print 'self.zs_now_zoushilist_short!!!!   ',self.zs_now_zoushilist_short
						print 'exit zhongshu    ',self._penmsg_short_list
					elif float((self._penmsg_short_list[-1])[0])>self.zs_now_upvalue_short and int((self._penmsg_short_list[-1])[2])==self.zs_now_dir_short:#最后一笔没有回到中枢，中枢方向改变
						print "leave zhongshu  change  ",self.zs_now_upvalue_short, '  ',self.zs_now_downvalue_short, '  ',self.zs_now_dir_short, '  ',self.zs_now_uptime_short, '  ',self.zs_now_downtime_short, '  ',self.zs_now_zoushilist_short
						self.zs_last_upvalue_short=self.zs_now_upvalue_short
						self.zs_last_downvalue_short=self.zs_now_downvalue_short
						self.zs_last_dir_short=self.zs_now_dir_short
						self.zs_last_uptime_short=self.zs_now_uptime_short
						self.zs_last_downtime_short=self.zs_now_downtime_short
						self.zs_last_zoushilist_short=self.zs_now_zoushilist_short
						temp_penlist=[]
						temp_penlist.append(self._penmsg_short_list[-3])
						temp_penlist.append(self._penmsg_short_list[-2])
						temp_penlist.append(self._penmsg_short_list[-1])
						self._penmsg_short_list=temp_penlist

						self.zs_index_short=0
						self.zs_now_upvalue_short=0
						self.zs_now_downvalue_short=0
						self.zs_now_dir_short=0#改变中枢方向
						#self.zs_now_zoushilist_short=self._penmsg_list[-3]
						self.zs_now_zoushilist_short=[]
				else:#中枢方向乡下
					
					if float((self._penmsg_short_list[-1])[1])>self.zs_now_upvalue_short and int((self._penmsg_short_list[-1])[2])==self.zs_now_dir_short:#最后一笔没有回到中枢，中枢方向没有改变
						print "leave zhongshu  down  no change",self.zs_now_upvalue_short, '  ',self.zs_now_downvalue_short, '  ',self.zs_now_dir_short, '  ',self.zs_now_uptime_short, '  ',self.zs_now_downtime_short, '  ',self.zs_now_zoushilist_short
						self.zs_last_upvalue_short=self.zs_now_upvalue_short
						self.zs_last_downvalue_short=self.zs_now_downvalue_short
						self.zs_last_dir_short=self.zs_now_dir_short
						self.zs_last_uptime_short=self.zs_now_uptime_short
						self.zs_last_downtime_short=self.zs_now_downtime_short
						self.zs_last_zoushilist_short=self.zs_now_zoushilist_short

						self.zs_index_short=0
						temp_penlist=[]
						temp_penlist.append(self._penmsg_short_list[-2])
						temp_penlist.append(self._penmsg_short_list[-1])
						self._penmsg_short_list=temp_penlist

						self.zs_now_upvalue_short=0
						self.zs_now_downvalue_short=0
						#self.zs_now_zoushilist_short=self._penmsg_list[-2]
						self.zs_now_zoushilist_short=[]

					elif float((self._penmsg_short_list[-1])[0])<self.zs_now_downvalue_short and int((self._penmsg_short_list[-1])[2])==self.zs_now_dir_short:#最后一笔没有回到中枢，中枢方向改变
						print "leave zhongshu  down  change",self.zs_now_upvalue_short, '  ',self.zs_now_downvalue_short, '  ',self.zs_now_dir_short, '  ',self.zs_now_uptime_short, '  ',self.zs_now_downtime_short, '  ',self.zs_now_zoushilist_short
						self.zs_last_upvalue_short=self.zs_now_upvalue_short
						self.zs_last_downvalue_short=self.zs_now_downvalue_short
						self.zs_last_dir_short=self.zs_now_dir_short
						self.zs_last_uptime_short=self.zs_now_uptime_short
						self.zs_last_downtime_short=self.zs_now_downtime_short
						self.zs_last_zoushilist_short=self.zs_now_zoushilist_short

						self.zs_index_short=0
						temp_penlist=[]
						temp_penlist.append(self._penmsg_short_list[-3])
						temp_penlist.append(self._penmsg_short_list[-2])
						temp_penlist.append(self._penmsg_short_list[-1])
						self._penmsg_short_list=temp_penlist

						self.zs_now_upvalue_short=0
						self.zs_now_downvalue_short=0
						self.zs_now_dir_short=1#改变中枢方向
						self.zs_now_zoushilist_short=[]
		return


	def findzhongshu(self,longorshort):
		if longorshort==1:		
			self.findpen(1)
			if len(self._penmsg_list)==0:#没有笔
				return
			if len(self._penmsg_list)==1 and self.zs_index==0:#只有一笔，判断中枢方向,这个方向需要提前给
				#print self._penmsg_list
				self.zs_now_dir=1-(self._penmsg_list[0])[2]
				return 
			if len(self._penmsg_list)<4:#至少要有4笔，才能确定中枢
				return
			if self.zs_index==0 and self._penmsg_listchangeflag==1:#如果现在没有中枢，生成新中枢
				self._penmsg_listchangeflag=0

				if self.zs_now_dir==1:#中枢方向向上
					if  float((self._penmsg_list[-3])[0])<float((self._penmsg_list[-1])[1]) and int((self._penmsg_list[-3])[2])==self.zs_now_dir and int((self._penmsg_list[-1])[2])==self.zs_now_dir :#判断是否有交集
						#(self._penmsg_list[-3])[1]>(self._penmsg_list[-1])[0]  and
						if float((self._penmsg_list[-3])[1])>float((self._penmsg_list[-1])[1]):#中书上界2
							self.zs_now_upvalue=(self._penmsg_list[-1])[1]
							self.zs_now_uptime=(self._penmsg_list[-1])[6]

						else:
							self.zs_now_upvalue=(self._penmsg_list[-3])[1]
							self.zs_now_uptime=(self._penmsg_list[-3])[6]

						if float((self._penmsg_list[-3])[0])>float((self._penmsg_list[-1])[0]):#中书下界
							self.zs_now_downvalue=(self._penmsg_list[-3])[0]
							self.zs_now_downtime=(self._penmsg_list[-3])[3]
						else:
							self.zs_now_downvalue=(self._penmsg_list[-1])[0]
							self.zs_now_downtime=(self._penmsg_list[-1])[3]


						if len(self.zs_now_zoushilist)==0:#之前没有进入中枢的笔，此处进入中枢的笔开始赋值
							
							self.zs_now_zoushilist.append((self._penmsg_list[-4])[0])
							self.zs_now_zoushilist.append((self._penmsg_list[-4])[1])
							self.zs_now_zoushilist.append((self._penmsg_list[-4])[2])
							self.zs_now_zoushilist.append((self._penmsg_list[-4])[3])
							tempbarred=float((self._penmsg_list[-4])[4])
							tempbargreen=float((self._penmsg_list[-4])[5])
							self.zs_now_zoushilist.append(tempbarred)
							self.zs_now_zoushilist.append(tempbargreen)
							self.zs_now_zoushilist.append((self._penmsg_list[-4])[6])
						else:#之前有进入中枢的笔，此处修改进入中枢结束，和macd值
							self.zs_now_zoushilist[1]=(self._penmsg_list[-4])[1]
							self.zs_now_zoushilist[4]=float(self.zs_now_zoushilist[4])+float((self._penmsg_list[-4])[4])
							self.zs_now_zoushilist[5]=float(self.zs_now_zoushilist[5])+float((self._penmsg_list[-4])[5])
							self.zs_now_zoushilist[6]=(self._penmsg_list[-4])[6]

						print "upupupupupup"
						ret=''
						print self.zs_now_zoushilist
						ret=str(self.zs_now_upvalue)+','+self.zs_now_uptime+','+str(self.zs_now_downvalue)+','+self.zs_now_downtime+','+str(self.zs_now_dir)+','+str(self.zs_now_zoushilist[0])+'_'+str(self.zs_now_zoushilist[1])+'_'+str(self.zs_now_zoushilist[2])+'_'+str(self.zs_now_zoushilist[3])+'_'+str(self.zs_now_zoushilist[4])+'_'+str(self.zs_now_zoushilist[5])+'_'+str(self.zs_now_zoushilist[6])+'\n'
						self.zs_index=self.zs_index+1
						path = "../kdata/"+str(self._k_period)+"/"+self._instrumentid+"_zhongshu.txt"
						print "has come here 1"
						bf.write_txt(ret,path)

					elif float((self._penmsg_list[-3])[0])>=float((self._penmsg_list[-1])[1]) and int((self._penmsg_list[-3])[2])==self.zs_now_dir and int((self._penmsg_list[-1])[2])==self.zs_now_dir :
						#self._penmsg_list[startvalue,overvalue,dddir,starttime,macd红，macd绿,overtime]  dddirs=1:笔方向向上   dddir=0:比方向向下
						#print "zoushilist      ",self.zs_now_zoushilist
						
						if len(self.zs_now_zoushilist)==0:#之前没有进入中枢的笔，此处进入中枢的笔开始赋值
							
							self.zs_now_zoushilist.append((self._penmsg_list[-4])[0])
							self.zs_now_zoushilist.append((self._penmsg_list[-4])[1])
							self.zs_now_zoushilist.append((self._penmsg_list[-4])[2])
							self.zs_now_zoushilist.append((self._penmsg_list[-4])[3])
							tempbarred=float((self._penmsg_list[-4])[4])+float((self._penmsg_list[-3])[4])
							tempbargreen=float((self._penmsg_list[-4])[5])+float((self._penmsg_list[-3])[5])
							self.zs_now_zoushilist.append(tempbarred)
							self.zs_now_zoushilist.append(tempbargreen)
							self.zs_now_zoushilist.append((self._penmsg_list[-4])[6])
						else:#之前有进入中枢的笔，此处修改进入中枢结束，和macd值
						 	self.zs_now_zoushilist[1]=(self._penmsg_list[-4])[1]


							self.zs_now_zoushilist[4]=float(self.zs_now_zoushilist[4])+float((self._penmsg_list[-4])[4])+float((self._penmsg_list[-3])[4])
							self.zs_now_zoushilist[5]=float(self.zs_now_zoushilist[5])+float((self._penmsg_list[-4])[5])+float((self._penmsg_list[-3])[5])
						 	self.zs_now_zoushilist[6]=(self._penmsg_list[-4])[6]
						 	print "_penmsg_list hahahha  upup!!!!!!!!     ",self._penmsg_list
						######进入中枢一笔的macd需要修改
				else:#中枢方向向下
					
					if float((self._penmsg_list[-3])[0])>float((self._penmsg_list[-1])[1]) and int((self._penmsg_list[-3])[2])==self.zs_now_dir and int((self._penmsg_list[-1])[2])==self.zs_now_dir :#判断是否有交集,有交集
						#self._penmsg_list[startvalue,overvalue,dddir,starttime,macd红，macd绿,overtime]  dddirs=1:笔方向向上   dddir=0:比方向向下
						if float((self._penmsg_list[-3])[0])>float((self._penmsg_list[-1])[0]):#中书上界
							self.zs_now_upvalue=(self._penmsg_list[-1])[0]
							self.zs_now_uptime=(self._penmsg_list[-1])[3]
						else:
							self.zs_now_upvalue=(self._penmsg_list[-3])[0]
							self.zs_now_uptime=(self._penmsg_list[-3])[3]

						if float((self._penmsg_list[-3])[1])>float((self._penmsg_list[-1])[1]):#中书下界
							self.zs_now_downvalue=(self._penmsg_list[-3])[1]
							self.zs_now_downtime=(self._penmsg_list[-3])[6]
						else:
							self.zs_now_downvalue=(self._penmsg_list[-1])[1]
							self.zs_now_downtime=(self._penmsg_list[-1])[6]

						if len(self.zs_now_zoushilist)==0:#之前没有进入中枢的笔，此处进入中枢的笔开始赋值
							
							self.zs_now_zoushilist.append((self._penmsg_list[-4])[0])
							self.zs_now_zoushilist.append((self._penmsg_list[-4])[1])
							self.zs_now_zoushilist.append((self._penmsg_list[-4])[2])
							self.zs_now_zoushilist.append((self._penmsg_list[-4])[3])
							tempbarred=float((self._penmsg_list[-4])[4])
							tempbargreen=float((self._penmsg_list[-4])[5])
							self.zs_now_zoushilist.append(tempbarred)
							self.zs_now_zoushilist.append(tempbargreen)
							self.zs_now_zoushilist.append((self._penmsg_list[-4])[6])
						else:#之前有进入中枢的笔，此处修改进入中枢结束，和macd值
							self.zs_now_zoushilist[1]=(self._penmsg_list[-4])[1]
							self.zs_now_zoushilist[4]=float(self.zs_now_zoushilist[4])+float((self._penmsg_list[-4])[4])
							self.zs_now_zoushilist[5]=float(self.zs_now_zoushilist[5])+float((self._penmsg_list[-4])[5])
							self.zs_now_zoushilist[6]=(self._penmsg_list[-4])[6]
							print "_penmsg_list hahahha  upup!!!!!!!!     ",self._penmsg_list



						ret=''
						ret=str(self.zs_now_upvalue)+','+self.zs_now_uptime+','+str(self.zs_now_downvalue)+','+self.zs_now_downtime+','+str(self.zs_now_dir)+','+str(self.zs_now_zoushilist[0])+'_'+str(self.zs_now_zoushilist[1])+'_'+str(self.zs_now_zoushilist[2])+'_'+str(self.zs_now_zoushilist[3])+'_'+str(self.zs_now_zoushilist[4])+'_'+str(self.zs_now_zoushilist[5])+'_'+str(self.zs_now_zoushilist[6])+'\n'
						print "downdowndowndowndown"
						self.zs_index=self.zs_index+1
						path = "../kdata/"+str(self._k_period)+"/"+self._instrumentid+"_zhongshu.txt"
						print "has come here 2"
						bf.write_txt(ret,path)

					elif float((self._penmsg_list[-3])[0])<=float((self._penmsg_list[-1])[1]) and int((self._penmsg_list[-3])[2])==self.zs_now_dir and int((self._penmsg_list[-1])[2])==self.zs_now_dir :#判断是否有交集，没有交集	
						if len(self.zs_now_zoushilist)==0:#之前没有进入中枢的笔，此处进入中枢的笔开始赋值
							
							self.zs_now_zoushilist.append((self._penmsg_list[-4])[0])
							self.zs_now_zoushilist.append((self._penmsg_list[-4])[1])
							self.zs_now_zoushilist.append((self._penmsg_list[-4])[2])
							self.zs_now_zoushilist.append((self._penmsg_list[-4])[3])
							tempbarred=float((self._penmsg_list[-4])[4])+float((self._penmsg_list[-3])[4])
							tempbargreen=float((self._penmsg_list[-4])[5])+float((self._penmsg_list[-3])[5])
							self.zs_now_zoushilist.append(tempbarred)
							self.zs_now_zoushilist.append(tempbargreen)
							self.zs_now_zoushilist.append((self._penmsg_list[-4])[6])
						else:#之前有进入中枢的笔，此处修改进入中枢结束，和macd值
						 	self.zs_now_zoushilist[1]=(self._penmsg_list[-4])[1]
						 	self.zs_now_zoushilist[4]=float(self.zs_now_zoushilist[4])+float((self._penmsg_list[-4])[4])+float((self._penmsg_list[-3])[4])
							self.zs_now_zoushilist[5]=float(self.zs_now_zoushilist[5])+float((self._penmsg_list[-4])[5])+float((self._penmsg_list[-3])[5])
						 	self.zs_now_zoushilist[6]=(self._penmsg_list[-4])[6]
			elif self.zs_index==1 and self._penmsg_listchangeflag==1:#如果现在已经有中枢，判断和中枢同向的笔和中枢的关系
				self._penmsg_listchangeflag=0
				if self.zs_now_dir==1:#中枢方向向上
					if float((self._penmsg_list[-1])[1])<self.zs_now_downvalue and int((self._penmsg_list[-1])[2])==self.zs_now_dir:#最后一笔没有回到中枢，中枢方向没有改变
						print "leave zhongshu no change   ",self.zs_now_upvalue, '  ',self.zs_now_downvalue, '  ',self.zs_now_dir, '  ',self.zs_now_uptime, '  ',self.zs_now_downtime, '  ',self.zs_now_zoushilist
						self.zs_last_upvalue=self.zs_now_upvalue
						self.zs_last_downvalue=self.zs_now_downvalue
						self.zs_last_dir=self.zs_now_dir
						self.zs_last_uptime=self.zs_now_uptime
						self.zs_last_downtime=self.zs_now_downtime
						self.zs_last_zoushilist=self.zs_now_zoushilist

						temp_penlist=[]
						temp_penlist.append(self._penmsg_list[-2])
						temp_penlist.append(self._penmsg_list[-1])
						self._penmsg_list=temp_penlist

						self.zs_index=0
						self.zs_now_upvalue=0
						self.zs_now_downvalue=0
						#self.zs_now_zoushilist=self._penmsg_list[-2]
						self.zs_now_zoushilist=[]
						print 'self.zs_now_zoushilist!!!!   ',self.zs_now_zoushilist
						print 'exit zhongshu    ',self._penmsg_list
					elif float((self._penmsg_list[-1])[0])>self.zs_now_upvalue and int((self._penmsg_list[-1])[2])==self.zs_now_dir:#最后一笔没有回到中枢，中枢方向改变
						print "leave zhongshu  change  ",self.zs_now_upvalue, '  ',self.zs_now_downvalue, '  ',self.zs_now_dir, '  ',self.zs_now_uptime, '  ',self.zs_now_downtime, '  ',self.zs_now_zoushilist
						self.zs_last_upvalue=self.zs_now_upvalue
						self.zs_last_downvalue=self.zs_now_downvalue
						self.zs_last_dir=self.zs_now_dir
						self.zs_last_uptime=self.zs_now_uptime
						self.zs_last_downtime=self.zs_now_downtime
						self.zs_last_zoushilist=self.zs_now_zoushilist
						temp_penlist=[]
						temp_penlist.append(self._penmsg_list[-3])
						temp_penlist.append(self._penmsg_list[-2])
						temp_penlist.append(self._penmsg_list[-1])
						self._penmsg_list=temp_penlist

						self.zs_index=0
						self.zs_now_upvalue=0
						self.zs_now_downvalue=0
						self.zs_now_dir=0#改变中枢方向
						#self.zs_now_zoushilist=self._penmsg_list[-3]
						self.zs_now_zoushilist=[]
				else:#中枢方向乡下
					
					if float((self._penmsg_list[-1])[1])>self.zs_now_upvalue and int((self._penmsg_list[-1])[2])==self.zs_now_dir:#最后一笔没有回到中枢，中枢方向没有改变
						print "leave zhongshu  down  no change",self.zs_now_upvalue, '  ',self.zs_now_downvalue, '  ',self.zs_now_dir, '  ',self.zs_now_uptime, '  ',self.zs_now_downtime, '  ',self.zs_now_zoushilist
						self.zs_last_upvalue=self.zs_now_upvalue
						self.zs_last_downvalue=self.zs_now_downvalue
						self.zs_last_dir=self.zs_now_dir
						self.zs_last_uptime=self.zs_now_uptime
						self.zs_last_downtime=self.zs_now_downtime
						self.zs_last_zoushilist=self.zs_now_zoushilist

						self.zs_index=0
						temp_penlist=[]
						temp_penlist.append(self._penmsg_list[-2])
						temp_penlist.append(self._penmsg_list[-1])
						self._penmsg_list=temp_penlist

						self.zs_now_upvalue=0
						self.zs_now_downvalue=0
						#self.zs_now_zoushilist=self._penmsg_list[-2]
						self.zs_now_zoushilist=[]

					elif float((self._penmsg_list[-1])[0])<self.zs_now_downvalue and int((self._penmsg_list[-1])[2])==self.zs_now_dir:#最后一笔没有回到中枢，中枢方向改变
						print "leave zhongshu  down  change",self.zs_now_upvalue, '  ',self.zs_now_downvalue, '  ',self.zs_now_dir, '  ',self.zs_now_uptime, '  ',self.zs_now_downtime, '  ',self.zs_now_zoushilist
						self.zs_last_upvalue=self.zs_now_upvalue
						self.zs_last_downvalue=self.zs_now_downvalue
						self.zs_last_dir=self.zs_now_dir
						self.zs_last_uptime=self.zs_now_uptime
						self.zs_last_downtime=self.zs_now_downtime
						self.zs_last_zoushilist=self.zs_now_zoushilist

						self.zs_index=0
						temp_penlist=[]
						temp_penlist.append(self._penmsg_list[-3])
						temp_penlist.append(self._penmsg_list[-2])
						temp_penlist.append(self._penmsg_list[-1])
						self._penmsg_list=temp_penlist

						self.zs_now_upvalue=0
						self.zs_now_downvalue=0
						self.zs_now_dir=1#改变中枢方向
						self.zs_now_zoushilist=[]
		return

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
		#print "haha1"
		self.mergek(tmp,1)
		#print "haha2"
		self.get_merge_line(self._listkmsg_array,self._updonglist,1)
		#print "haha3"
		diff_val = self.get_diff_val(self._lastprice,1)
		#print "haha4"
		self._diff_array.append(diff_val)
		dea_val = self.get_dea_val(1)
		tmp = [self._time,diff_val,dea_val]
		self._macd_array.append(tmp)


		#########短周期
		tmp = []
		tmp.append(self._open_price_short)
		tmp.append(self._close_price_short)
		tmp.append(self._high_price_short)
		tmp.append(self._low_price_short)
		tmp.append(self._time_short)
		self._listkmsg_array_short.append(tmp)
		#print "haha5"
		self.mergek(tmp,0)
		#print "haha6"
		self.get_merge_line(self._listkmsg_array_short,self._updonglist_short,0)
		#print "haha7"
		diff_val = self.get_diff_val(self._lastprice_short,0)
		self._diff_array_short.append(diff_val)
		#print "haha8"
		dea_val = self.get_dea_val(0)
		tmp = [self._time_short,diff_val,dea_val]
		self._macd_array_short.append(tmp)

	def get_diff_val(self,lastprice,longorshort):
		if longorshort==1:
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
		if longorshort==0:
			self._now_bar_num_short +=1
			if self._now_bar_num_short < self._quick_period_short:
				tmp = float((self._now_bar_num_short - 1) * self._quick_ema_short + 2 * lastprice)/(self._now_bar_num_short + 1)
			else:
				tmp = float((self._quick_period_short - 1) * self._quick_ema_short + 2 * lastprice)/(self._quick_period_short + 1)
			self._quick_ema_short = tmp

			if self._now_bar_num_short < self._slow_period_short:
				tmp = float((self._now_bar_num_short - 1) * self._slow_ema_short + 2 * lastprice)/(self._now_bar_num_short + 1)
			else:
				tmp = float((self._slow_period_short - 1) * self._slow_ema_short + 2 * lastprice)/(self._slow_period_short + 1)
			self._slow_ema_short = tmp
			return self._quick_ema_short - self._slow_ema_short

	def get_dea_val(self,diff_val,longorshort):
		# if longorshort==1:
		# 	l = len(self._diff_array)
		# 	sum_val = 0
		# 	if l < self._dea_period:
		# 		for x in xrange(0,l):
		# 			sum_val += self._diff_array[x]
		# 		ret = sum_val/l
		# 		return ret
		# 	else:
		# 		left = l - self._dea_period
		# 		for x in xrange(left,l):
		# 			sum_val += self._diff_array[x]
		# 		ret = sum_val/self._dea_period
		# 		return ret
		# if longorshort==0:
		# 	l = len(self._diff_array_short)
		# 	sum_val = 0
		# 	if l < self._dea_period_short:
		# 		for x in xrange(0,l):
		# 			sum_val += self._diff_array_short[x]
		# 		ret = sum_val/l
		# 		return ret
		# 	else:
		# 		left = l - self._dea_period_short
		# 		for x in xrange(left,l):
		# 			sum_val += self._diff_array_short[x]
		# 		ret = sum_val/self._dea_period_short
		# 		return ret
		if longorshort==1:
			self._dea = float((self._dea_period - 1) * self._dea + 2 * diff_val)/(self._dea_period + 1)
			return self._dea
		if longorshort==0:
			self._dea_short = float((self._dea_period_short - 1) * self._dea_short + 2 * diff_val)/(self._dea_period_short + 1)
			return self._dea_short

	def create_k(self,time,lastprice,p_periodflag):#1长周期，0短周期
		if p_periodflag==1:
			pass
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
		if p_periodflag==0:
			pass
			self._k_bar_tick_short +=1
			self._close_price_short= lastprice
			if self._k_bar_tick_short==1:
				self._open_price_short= lastprice
				self._close_price_short = lastprice
				self._high_price_short = lastprice
				self._low_price_short = lastprice
			elif self._k_bar_tick_short == self._k_period_short:
				tmp = []
				tmp.append(self._open_price_short)
				tmp.append(self._close_price_short)
				tmp.append(self._high_price_short)
				tmp.append(self._low_price_short)
				tmp.append(time)
				self._listkmsg_array_short.append(tmp)
				self._k_bar_tick_short = 0
				return tmp
			else:
				if lastprice > self._high_price_short:
					self._high_price_short = lastprice
				if lastprice < self._low_price_short:
					self._low_price_short = lastprice
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

	def mergek(self,kmesg,longorshort):
		if longorshort==1:
			templist=[0,0]
			if not self._lastlastk_array:
				self._lastlastk_array=kmesg
				self._updonglist.append(templist)
				return
			if not self._lastk_array:
				self._lastk_array=kmesg
				self._updonglist.append(templist)
				return
		#print lastk,lastlastk
			lastk = self._lastk_array
			lastlastk = self._lastlastk_array
			#print lastk
			#print lastlastk
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
				self._updonglist.append(templist)
			else:
				if float(lastk[2])>float(kmesg[2]) and float(lastk[2])>float(lastlastk[2]) and float(lastk[3])>float(kmesg[3]) and float(lastk[3])>float(lastlastk[3]) and self._midkone>3:
					if self._dd_dir==0 or (self._dd_dir==1 and lastk[2]>self._dd_value) or self._dd_dir==-1:
						if len(self._updonglist)==0:#在前一个文件
							templist=[]
							templist.append(1)
							templist.append(lastk[2])
							self._updonglist.append(templist)
							self._lastlastk_array=lastk
							self._lastk_array=kmesg
							self._midkone=1
							self._dd_dir=1
							self._dd_value=lastk[2]
							return

						((self._updonglist)[-1])[0]=1
						((self._updonglist)[-1])[1]=lastk[2]
						self._midkone=0
						self._dd_dir=1
						self._dd_value=lastk[2]


				if float(lastk[2])<float(kmesg[2]) and float(lastk[2])<float(lastlastk[2]) and float(lastk[3])<float(kmesg[3]) and float(lastk[3])<float(lastlastk[3]) and self._midkone>3:
					if self._dd_dir==0 or (self._dd_dir==-1 and lastk[3]<self._dd_value) or self._dd_dir==1:
						if len(self._updonglist)==0:#在前一个文件
							templist=[]
							templist.append(-1)
							templist.append(lastk[3])
							self._updonglist.append(templist)
							self._lastlastk_array=lastk
							self._lastk_array=kmesg
							self._midkone=1
							self._dd_dir=-1
							self._dd_value=lastk[3]
							return

						((self._updonglist)[-1])[0]=-1
						((self._updonglist)[-1])[1]=lastk[3]
					#self._updonglist[-1]=-1
						self._midkone=0
						self._dd_dir=-1
						self._dd_value=lastk[3]
				self._updonglist.append(templist)
				self._lastlastk_array=lastk
				self._lastk_array=kmesg
				self._midkone=self._midkone+1
		if longorshort==0:
			templist=[0,0]
			if not self._lastlastk_array_short:
				self._lastlastk_array_short=kmesg
				self._updonglist_short.append(templist)
				return
			if not self._lastk_array_short:
				self._lastk_array_short=kmesg
				self._updonglist_short.append(templist)
				return

			lastk = self._lastk_array_short
			lastlastk = self._lastlastk_array_short
			#print lastk
			#print lastlastk
			if float(lastk[2])>float(lastlastk[2]) and float(lastk[3])>float(lastlastk[3]):#前两根k线方向向上
				self._flag_short=0
			elif float(lastk[2])<float(lastlastk[2]) and float(lastk[3])<float(lastlastk[3]):#前两根k线方向向下
				self._flag_short=1
			elif float(lastk[2])>float(lastlastk[2]):
				self._flag_short=0
			else:
				self._flag_short=1
			
			if (float(kmesg[2])<=float(lastk[2]) and float(kmesg[3])>=float(lastk[3])) or (float(kmesg[2])>=float(lastk[2])and float(kmesg[3])<=float(lastk[3])):#当前k线需要和前一k线合并
				getmargek=self.merge(lastk,kmesg,self._flag_short)
				self._lastk_array_short=getmargek
				self._updonglist_short.append(templist)
				
			else:
				if float(lastk[2])>float(kmesg[2]) and float(lastk[2])>float(lastlastk[2]) and float(lastk[3])>float(kmesg[3]) and float(lastk[3])>float(lastlastk[3]) and self._midkone_short>3:
					if self._dd_dir_short==0 or (self._dd_dir_short==1 and lastk[2]>self._dd_value_short) or self._dd_dir_short==-1:
						if len(self._updonglist_short)==0:#在前一个文件
							templist=[]
							templist.append(1)
							templist.append(lastk[2])
							self._updonglist_short.append(templist)
							self._lastlastk_array_short=lastk
							self._lastk_array_short=kmesg
							self._midkone_short=1
							self._dd_dir_short=1
							self._dd_value_short=lastk[2]
							return

						((self._updonglist_short)[-1])[0]=1
						((self._updonglist_short)[-1])[1]=lastk[2]
						self._midkone_short=0
						self._dd_dir_short=1
						self._dd_value_short=lastk[2]
						#print "haha13"

				if float(lastk[2])<float(kmesg[2]) and float(lastk[2])<float(lastlastk[2]) and float(lastk[3])<float(kmesg[3]) and float(lastk[3])<float(lastlastk[3]) and self._midkone_short>3:
					if self._dd_dir_short==0 or (self._dd_dir_short==-1 and lastk[3]<self._dd_value_short) or self._dd_dir_short==1:
						if len(self._updonglist_short)==0:#在前一个文件
							templist=[]
							templist.append(-1)
							templist.append(lastk[3])
							self._updonglist_short.append(templist)
							self._lastlastk_array_short=lastk
							self._lastk_array_short=kmesg
							self._midkone_short=1
							self._dd_dir_short=-1
							self._dd_value_short=lastk[3]
							return

						((self._updonglist_short)[-1])[0]=-1
						((self._updonglist_short)[-1])[1]=lastk[3]
					#self._updonglist[-1]=-1
						self._midkone_short=0
						self._dd_dir_short=-1
						self._dd_value_short=lastk[3]
				self._updonglist_short.append(templist)
				self._lastlastk_array_short=lastk
				self._lastk_array_short=kmesg
				self._midkone_short=self._midkone_short+1	
	
				
			

		
	def get_merge_line(self,listkmsg_array,updonglist,longorshort):
		if longorshort==1:
			if len(listkmsg_array) != len(updonglist):
				print "the list of k mesg is not equal updonglist"
				return 
			if len(listkmsg_array) < 3:
				print "the list is small and not parting"
				return
			#print updonglist
			parting = float((updonglist[-2])[0])
			line = listkmsg_array[-2]
			time = line[4]

			if parting == 0:
				return 0
			elif parting ==1:
				#lastprice = float(line[HIGH])
				lastprice = float((updonglist[-2])[1])#保存顶底值
				if len(self._parting_array) ==0:
					self._parting_array.append([time,lastprice,1,0,0,0])#最后一个数据标记是否使用过0：没有使用  1 使用过
					return 1
				tmp = self._parting_array[-1]
				if round(float(tmp[2])) ==1:
					if float(tmp[1]) > lastprice:
						return 0
					else:
						tmp[0] = time
						tmp[1] = lastprice
						tmp[2] = 1
						tmp[3]=(self._parting_array[-1])[3]
						tmp[4]=(self._parting_array[-1])[4]
						tmp[5]=0
						self._parting_array[-1] = tmp
						#self.dd_valueanddir_list
				elif round(float(tmp[2])) == -1:
					if float(tmp[1]) >= lastprice:
						return 0
					else:
						tmp1 = [time,lastprice,1,0,0,0]
						self._parting_array.append(tmp1)
			elif parting == -1:
				#lastprice = float(line[LOW])
				lastprice = float((updonglist[-2])[1])
				if len(self._parting_array) ==0:
					self._parting_array.append([time,lastprice,-1,0,0,0])
					return 1
				tmp = self._parting_array[-1]
				if round(float(tmp[2])) ==1:
					if float(tmp[1]) <= lastprice:
						return 0
					else:
						tmp1 = [time,lastprice,-1,0,0,0]
						self._parting_array.append(tmp1)
				elif round(float(tmp[2])) == -1:
					if float(tmp[1]) <= lastprice:
						return 0
					else:
						tmp[0] = time
						tmp[1] = lastprice
						tmp[2] = -1
						tmp[3]=(self._parting_array[-1])[3]
						tmp[4]=(self._parting_array[-1])[4]
						tmp[5]=0
						self._parting_array[-1] = tmp
			else:
				return 0
		if longorshort==0:
			if len(listkmsg_array) != len(updonglist):
				print "the list of k mesg is not equal updonglist"
				return 
			if len(listkmsg_array) < 3:
				print "the list is small and not parting"
				return
			#print updonglist
			parting = float((updonglist[-2])[0])
			line = listkmsg_array[-2]
			time = line[4]

			if parting == 0:
				return 0
			elif parting ==1:
				#lastprice = float(line[HIGH])
				lastprice = float((updonglist[-2])[1])#保存顶底值
				if len(self._parting_array_short) ==0:
					self._parting_array_short.append([time,lastprice,1,0,0,0])
					return 1
				tmp = self._parting_array_short[-1]
				if round(float(tmp[2])) ==1:
					if float(tmp[1]) > lastprice:
						return 0
					else:
						#print self._parting_array_short
						tmp[0] = time
						tmp[1] = lastprice
						tmp[2] = 1
						tmp[3]=(self._parting_array_short[-1])[3]
						tmp[4]=(self._parting_array_short[-1])[4]
						self._parting_array_short[-1] = tmp
				elif round(float(tmp[2])) == -1:
					if float(tmp[1]) >= lastprice:
						return 0
					else:
						tmp1 = [time,lastprice,1,0,0,0]
						self._parting_array_short.append(tmp1)
			elif parting == -1:
				#lastprice = float(line[LOW])
				lastprice = float((updonglist[-2])[1])
				if len(self._parting_array_short) ==0:
					self._parting_array_short.append([time,lastprice,-1,0,0,0])
					return 1
				tmp = self._parting_array_short[-1]
				if round(float(tmp[2])) ==1:
					if float(tmp[1]) <= lastprice:
						return 0
					else:
						tmp1 = [time,lastprice,-1,0,0,0]
						self._parting_array_short.append(tmp1)
				elif round(float(tmp[2])) == -1:
					if float(tmp[1]) <= lastprice:
						return 0
					else:
						tmp[0] = time
						tmp[1] = lastprice
						tmp[2] = -1
						tmp[3]=(self._parting_array_short[-1])[3]
						tmp[4]=(self._parting_array_short[-1])[4]
						self._parting_array_short[-1] = tmp
			else:
				return 0

	#self._nowbar_array=[]#正在形成的k线
	def get_doing_bar(self,lastprice):#得到正在形成的k线
		if len(self._nowbar_array)==0:
			self._nowbar_array.append(1)
			self._nowbar_array.append(lastprice)#最高价
			self._nowbar_array.append(lastprice)#最低价
			return
		if self._nowbar_array[0]<=self._k_period:
			self._nowbar_array[0]=self._nowbar_array[0]+1
			if lastprice>self._nowbar_array[1]:
				self._nowbar_array[1]=lastprice
			if lastprice<self._nowbar_array[2]:
				self._nowbar_array[2]=lastprice

	def get_md_line(self,line,longorshort):

		
		#####长周期计算
		if longorshort==1:
			pass
			self._lastprice = float(line[LASTPRICE])
			self._time = line[DATE]+" "+line[TIME]
			kmesg = self.create_k(self._time,self._lastprice,1)
			#self.get_doing_bar(self._lastprice)


			#self.exit_long(self._lastprice,self._time)
			#self.exit_short(self._lastprice,self._time)
			if len(kmesg) ==0:
				return 
			else:
				# get one k line
				self.mergek(kmesg,1)
				self.get_merge_line(self._listkmsg_array,self._updonglist,1)
				# caculate the macd
				diff_val = self.get_diff_val(self._lastprice,1)
				self._diff_array.append(diff_val)
				dea_val = self.get_dea_val(diff_val,1)
				tmp = [self._time,diff_val,dea_val]
				tmpbar=2*(diff_val-dea_val)
				if tmpbar>=0 and len(self._parting_array)!=0:
					(self._parting_array[-1])[3]=float((self._parting_array[-1])[3])+tmpbar
				elif tmpbar<0 and len(self._parting_array)!=0:
					(self._parting_array[-1])[4]=float((self._parting_array[-1])[4])+tmpbar
				# if len(self._parting_array)!=0 and (self._parting_array[-1])[2]==-1:#由底开始的一笔
				# 	if tmpbar>0:
				# 		(self._parting_array[-1])[3]=(self._parting_array[-1])[3]+tmpbar
				# if len(self._parting_array)!=0 and (self._parting_array[-1])[2]==1:#由顶开始的一笔
				# 	if tmpbar<0:
				# 		(self._parting_array[-1])[3]=(self._parting_array[-1])[3]+tmpbar
				#print 'macd   ',tmpbar,'  updownmsg   ',self._parting_array

				self._macd_array.append(tmp)
				self.findzhongshu(1)
				#self.open_long(self._lastprice,self._time)
				#self.open_short(self._lastprice,self._time)
				self.open_long(self._lastprice,self._time)
				self.open_short(self._lastprice,self._time)
				return
		############
		#
		#######短周期计算
		if longorshort==0:
			pass
			self._lastprice_short = float(line[LASTPRICE])
			self._time_short = line[DATE]+" "+line[TIME]
			kmesg = self.create_k(self._time_short,self._lastprice_short,0)

			if len(kmesg) ==0:
				return 
			else:
				# get one k line
				self.mergek(kmesg,0)
				self.get_merge_line(self._listkmsg_array_short,self._updonglist_short,0)
				# caculate the macd
				diff_val = self.get_diff_val(self._lastprice_short,0)
				self._diff_array_short.append(diff_val)
				dea_val = self.get_dea_val(diff_val,0)
				tmp = [self._time_short,diff_val,dea_val]
				tmpbar=2*(diff_val-dea_val)
				#print "short macd !!!!!  ",self._parting_array_short
				if tmpbar>=0 and len(self._parting_array_short)!=0:
					(self._parting_array_short[-1])[3]=float((self._parting_array_short[-1])[3])+tmpbar
				elif tmpbar<0 and len(self._parting_array_short)!=0:
					(self._parting_array_short[-1])[4]=float((self._parting_array_short[-1])[4])+tmpbar

				self._macd_array_short.append(tmp)
				self.findzhongshu_short(0)
				return
		

		#
		#
		

	def write_data_to_file(self):

		#######写长周期
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
			tmp.append(self._macd_array[x][1])
			tmp.append(self._macd_array[x][2])
			time = tmp[4]
			for line in self._parting_array:
				if line[0] == time:
					tmp.append(line[2])
					break
			if len(tmp) == 6:
				tmp.append(0)
			ret.append(tmp)
		path = "../kdata/"+str(self._k_period)+"/"+self._instrumentid+"_"+str(self._date)+".csv"
		bf.write_data_to_csv(ret,path)


		path = "../kdata/"+str(self._k_period)+"/"+self._instrumentid+"_penmsg.csv"
		print "write penmasg    ",self._penmsg_list
		bf.write_data_to_csv(self._penmsg_list,path)
		#######写短周期
		ret = []
		if len(self._listkmsg_array_short) !=  len(self._updonglist_short):
			print "len(self._listkmsg_array) !=  len(self._updonglist)"
			return
		if len(self._listkmsg_array_short) !=  len(self._macd_array_short):
			print "len(self._listkmsg_array) !=  len(self._macd_array)"
			return
		for x in xrange(0,len(self._listkmsg_array_short)):
			tmp = self._listkmsg_array_short[x]
			tmp.append(self._updonglist_short[x])
			tmp.append(self._macd_array_short[x][1])
			tmp.append(self._macd_array_short[x][2])
			time = tmp[4]
			for line in self._parting_array_short:
				if line[0] == time:
					tmp.append(line[2])
					break
			if len(tmp) == 6:
				tmp.append(0)
			ret.append(tmp)
		path = "../kdata/"+str(self._k_period_short)+"/"+self._instrumentid_short+"_"+str(self._date_short)+".csv"
		bf.write_data_to_csv(ret,path)

		path = "../kdata/"+str(self._k_period_short)+"/"+self._instrumentid_short+"_penmsg.csv"
		print "write penmasg_short    ",self._penmsg_short_list
		bf.write_data_to_csv(self._penmsg_short_list,path)


def main():
	date1 = [20171016,20171017,20171018,20171019,20171020]
	#date2 = [20171023,20171024]
	date2 = [20171023,20171024,20171025,20171026,20171027,20171030,20171031,20171101,20171102,20171103,20171106,20171107,20171108,20171109,20171110]
	date3 = [20171016,20171017,20171018,20171019]
	date = date1+date2
	#date = date3
	instrumentIds = ["rb1801"]
	i=0
	for day in date:
		for instrumentId in instrumentIds:
			print "~~~~~~~~~"+str(day)

			param_dict = {"instrumentId":instrumentId,"date":day}
			getline_obj = getline(param_dict)
			path = '../data/'+instrumentId + '_' + str(day) + '.csv'
			data = bf.read_data_from_csv(path)

			for line in data:
				tmp = getline_obj.get_md_line(line,1)
				tmp = getline_obj.get_md_line(line,0)
				
				
			# data = getline_obj.get_line_data()
			# path = '../kdata/'+instrumentId + '_' + str(day) + '_total.csv'
			# bf.write_data_to_csv(data,path)
			getline_obj.savemsg()


if __name__=='__main__': 
	main()