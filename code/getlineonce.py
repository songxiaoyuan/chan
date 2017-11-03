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
		self._parting_array = []#保存顶底信息，包括从顶底开始对应的macd的和，顶开始保存macd负值，底开始保存macd正值
		self._listkmsg_array = []
		self._penmsg_list=[]#保存笔信息，开始，结束,starttime,overtime，macd
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

		#######中枢相关变量#######
		self.zs_index=0#目前中枢个数

		self.zs_now_upvalue=0#中枢上界
		self.zs_now_downvalue=0#中枢下界
		self.zs_now_uptime=''#中枢上届时间
		self.zs_now_downtime=''#中枢下届时间
		self.zs_now_dir=0#中枢方向,0向下，1向上
		self.zs_now_zoushilist=[]#进入中枢的走势【begin,over,time,macd面积】
		self.zs_now_penlist=[]

		self.zs_last_upvalue=0#中枢上界
		self.zs_last_downvalue=0#中枢下界
		self.zs_last_uptime=''#中枢上届时间
		self.zs_last_downtime=''#中枢下届时间
		self.zs_last_dir=0#中枢方向
		self.zs_last_zoushilist=[]#进入中枢的走势【begin,over,time,macd面积】
		self.zs_last_penlist=[]
		#########################



		###############短周期变量###########
		#
		self._k_bar_tick_short= 0
		self._k_period_short = 120
		self._open_price_short = 0
		self._close_price_short = 0
		self._high_price_short = 0
		self._low_price_short = 0

		self._parting_array_short = []#保存顶底信息，包括从顶底开始对应的macd的和，顶开始保存macd负值，底开始保存macd正值
		self._penmsg_short_list=[]#保存笔信息，开始，结束，结束时间，macd
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
			config_file = "../config/"+str(self._k_period)+"/"+str(self._config_file)
			bf.get_config_info(quick_ema_array,slow_ema_array,self._diff_array,
				self._lastlastk_array,self._lastk_array,midkone_array,dd_val_array,dd_dir_array,
			    config_file)

			path = "../kdata/"+str(self._k_period)+"/"+self._instrumentid+"_zhongshu.txt"
			self.get_zhongshu_msg(path)

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
			penpath= "../kdata/"+str(self._k_period)+"/"+self._instrumentid+"_penmsg.csv"
			self._penmsg_list=bf.read_data_from_csv(penpath)
			if len(self._penmsg_list)==1 and int((self._penmsg_list[0])[0])==0:
				self._penmsg_list=[]
			print 'this is  read pengmsg    ',self._penmsg_list
		if self._now_bar_num_short ==0:
			print "this is init function " + str(self._config_file_short)
			quick_ema_array = []
			slow_ema_array = []
			midkone_array = []
			dd_val_array = []
			dd_dir_array = []
			config_file = "../config/"+str(self._k_period_short)+"/"+str(self._config_file_short)
			bf.get_config_info(quick_ema_array,slow_ema_array,self._diff_array_short,
				self._lastlastk_array_short,self._lastk_array_short,midkone_array,dd_val_array,dd_dir_array,
			    config_file)
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
	def get_zhongshu_msg(self,path):
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
			self.zs_now_upvalue=float(splitline[0])
			self.zs_now_uptime=splitline[1]
			self.zs_now_downvalue=float(splitline[2])
			self.zs_now_downtime=splitline[3]
			self.zs_now_dir=int(splitline[4])
			self.zs_now_zoushilist.append(float((splitline[5].split('_'))[0]))
			self.zs_now_zoushilist.append(float((splitline[5].split('_'))[1]))
			self.zs_now_zoushilist.append(int((splitline[5].split('_'))[2]))
			self.zs_now_zoushilist.append(splitline[5].split('_')[3])
			self.zs_now_zoushilist.append(float((splitline[5].split('_'))[4]))
			self.zs_now_zoushilist.append(splitline[5].split('_')[5])

		if len(lines)>1:
			splitline=lines[-1].split(',')
			self.zs_now_upvalue=float(splitline[0])
			self.zs_now_uptime=splitline[1]
			self.zs_now_downvalue=float(splitline[2])
			self.zs_now_downtime=splitline[3]
			self.zs_now_dir=int(splitline[4])
			self.zs_now_zoushilist.append(float((splitline[5].split('_'))[0]))
			self.zs_now_zoushilist.append(float((splitline[5].split('_'))[1]))
			self.zs_now_zoushilist.append(int((splitline[5].split('_'))[2]))
			self.zs_now_zoushilist.append(splitline[5].split('_')[3])
			self.zs_now_zoushilist.append(float((splitline[5].split('_'))[4]))
			self.zs_now_zoushilist.append(splitline[5].split('_')[5])

			splitline=lines[-2].split(',')
			self.zs_last_upvalue=float(splitline[0])
			self.zs_last_uptime=splitline[1]
			self.zs_last_downvalue=float(splitline[2])
			self.zs_last_downtime=splitline[3]
			self.zs_last_dir=int(splitline[4])
			self.zs_last_zoushilist.append(float((splitline[5].split('_'))[0]))
			self.zs_last_zoushilist.append(float((splitline[5].split('_'))[1]))
			self.zs_last_zoushilist.append(int((splitline[5].split('_'))[2]))
			self.zs_last_zoushilist.append(splitline[5].split('_')[3])
			self.zs_last_zoushilist.append(float((splitline[5].split('_'))[4]))
			self.zs_last_zoushilist.append(splitline[5].split('_')[5])

	def __del__(self):
		print "this is the over function and save the config file"
		self.over_fun()

		path = "../config/" + str(self._k_period)+"/"+str(self._config_file)
		bf.write_config_info(self._quick_ema,self._slow_ema,
			self._diff_array,self._dea_period,
			self._lastlastk_array,self._lastk_array,self._midkone,self._dd_value,self._dd_dir,path)


		path = "../config/" + str(self._k_period_short)+"/"+str(self._config_file_short)
		#print "haha   ",self._diff_array_short
		bf.write_config_info(self._quick_ema_short,self._slow_ema_short,
			self._diff_array_short,self._dea_period_short,
			self._lastlastk_array_short,self._lastk_array_short,self._midkone_short,self._dd_value_short,self._dd_dir_short,path)
		#print self._penmsg_list
		self.write_data_to_file()


	def findpen(self,longorshort):
		if longorshort==1:
			if len(self._parting_array)<2:
				return
			if (len(self._penmsg_list)==0) or (len(self._penmsg_list)>0 and (self._parting_array[-2])[1]!=(self._penmsg_list[-1])[0]):#有一对顶底 or 新的一笔
				templist=[]
				templist.append((self._parting_array[-2])[1])#self._parting_array=[time,lastprice,1,macd]
				#self._penmsg_list[startvalue,overvalue,dddir,starttime,macd,overtime]  dddirs=1:笔方向向上   dddir=0:比方向向下
				templist.append((self._parting_array[-1])[1])
				if (self._parting_array[-2])[1]<(self._parting_array[-1])[1]:#向上的一笔
					templist.append(1)
				else:
					templist.append(0)
				templist.append((self._parting_array[-2])[0])
				
				templist.append((self._parting_array[-2])[3])
				templist.append((self._parting_array[-1])[0])
				self._penmsg_list.append(templist)
			elif len(self._penmsg_list)>0 and (self._parting_array[-2])[1]==(self._penmsg_list[-1])[0] and (self._parting_array[-1])[1]!=(self._penmsg_list[-1])[1]:#笔的结束位置变化
				(self._penmsg_list[-1])[1]=(self._parting_array[-1])[1]
				(self._penmsg_list[-1])[4]=(self._penmsg_list[-1])[4]+(self._parting_array[-1])[3]

				
			
			
		# self.zs_now_upvalue=0#中枢上界
		# self.zs_now_downvalue=0#中枢下界
		# self.zs_now_uptime=''#中枢上届时间
		# self.zs_now_downtime=''#中枢下届时间
		# self.zs_now_dir=0#中枢方向,0向下，1向上
		# self.zs_now_zoushilist=[]#进入中枢的走势【begin,over,starttime,overtime,macd面积】
		# self.zs_now_penlist=[]
	# def pendirdowncover(pre_pen_list,behind_pen_list):#判断向下两笔是否有重重迭
	# 	if pre_pen_list[0]<behind_pen_list[1]:
	# 		return false 
	# def pendirdowncover(pre_pen_list,behind_pen_list):#判断向上两笔是否有重重迭
	# 	if pre_pen_list[0]>behind_pen_list[1]:
	# 		return false 			

	def findzhongshu(self,longorshort):
		if longorshort==1:
			
			self.findpen(1)
			if len(self._penmsg_list)==0:#没有笔
				return
			if len(self._penmsg_list)==1:#只有一笔，判断中枢方向,这个方向需要提前给
				#print self._penmsg_list
				self.zs_now_dir=1-(self._penmsg_list[0])[2]
				return 
			if len(self._penmsg_list)<4:#至少要有4笔，才能确定中枢
				return

			#if len(self._penmsg_list)%2==0:#新添加两笔判断一次,这可能有问题
			if self.zs_now_upvalue==0:#如果现在没有中枢，生成新中枢
				print 'dir   ',self.zs_now_dir,'  ',self._penmsg_list[-3],'   ',self._penmsg_list[-1]
				if self.zs_now_dir==1:#中枢方向向上
					if (self._penmsg_list[-3])[1]>(self._penmsg_list[-1])[0]  and (self._penmsg_list[-3])[0]<(self._penmsg_list[-1])[1] and (self._penmsg_list[-3])[2]==self.zs_now_dir and (self._penmsg_list[-1])[2]==self.zs_now_dir :#判断是否有交集
						if (self._penmsg_list[-3])[1]>(self._penmsg_list[-1])[1]:#中书上界2
							self.zs_now_upvalue=(self._penmsg_list[-1])[1]
							self.zs_now_uptime=(self._penmsg_list[-1])[5]

						else:
							self.zs_now_upvalue=(self._penmsg_list[-3])[1]
							self.zs_now_uptime=(self._penmsg_list[-3])[5]

						if (self._penmsg_list[-3])[0]>(self._penmsg_list[-1])[0]:#中书下界
							self.zs_now_downvalue=(self._penmsg_list[-3])[0]
							self.zs_now_downtime=(self._penmsg_list[-3])[3]
						else:
							self.zs_now_downvalue=(self._penmsg_list[-1])[0]
							self.zs_now_downtime=(self._penmsg_list[-1])[3]
						self.zs_now_zoushilist=self._penmsg_list[-4]#这个地方有问题，macd的值需要改变!!!!!!!!!!!!!!!!!!!!!!!!!!!
						print "upupupupupup"
						ret=''
						ret=str(self.zs_now_upvalue)+','+self.zs_now_uptime+','+str(self.zs_now_downvalue)+','+self.zs_now_downtime+','+str(self.zs_now_dir)+','+str(self.zs_now_zoushilist[0])+'_'+str(self.zs_now_zoushilist[1])+'_'+str(self.zs_now_zoushilist[2])+'_'+str(self.zs_now_zoushilist[3])+'_'+str(self.zs_now_zoushilist[4])+'_'+str(self.zs_now_zoushilist[5])+'\n'

						path = "../kdata/"+str(self._k_period)+"/"+self._instrumentid+"_zhongshu.txt"
						print "has come here 1"
						bf.write_zhongshu(ret,path)

					else:
						pass
						######进入中枢一笔的macd需要修改
				else:#中枢方向向下
					
					if (self._penmsg_list[-3])[1]<(self._penmsg_list[-1])[0]  and (self._penmsg_list[-3])[0]>(self._penmsg_list[-1])[1] and (self._penmsg_list[-3])[2]==self.zs_now_dir and (self._penmsg_list[-1])[2]==self.zs_now_dir :#判断是否有交集
						if (self._penmsg_list[-3])[0]>(self._penmsg_list[-1])[0]:#中书上界
							self.zs_now_upvalue=(self._penmsg_list[-1])[0]
							self.zs_now_uptime=(self._penmsg_list[-1])[3]
						else:
							self.zs_now_upvalue=(self._penmsg_list[-3])[0]
							self.zs_now_uptime=(self._penmsg_list[-3])[3]

						if (self._penmsg_list[-3])[1]>(self._penmsg_list[-1])[1]:#中书下界
							self.zs_now_downvalue=(self._penmsg_list[-3])[1]
							self.zs_now_downtime=(self._penmsg_list[-3])[5]
						else:
							self.zs_now_downvalue=(self._penmsg_list[-1])[1]
							self.zs_now_downtime=(self._penmsg_list[-1])[5]
						self.zs_now_zoushilist=self._penmsg_list[-4]#这个地方有问题，macd的值需要改变!!!!!!!!!!!!!!!!!!!!!!!!!!!!


						ret=''
						ret=str(self.zs_now_upvalue)+','+self.zs_now_uptime+','+str(self.zs_now_downvalue)+','+self.zs_now_downtime+','+str(self.zs_now_dir)+','+str(self.zs_now_zoushilist[0])+'_'+str(self.zs_now_zoushilist[1])+'_'+str(self.zs_now_zoushilist[2])+'_'+str(self.zs_now_zoushilist[3])+'_'+str(self.zs_now_zoushilist[4])+'_'+str(self.zs_now_zoushilist[5])+'\n'
						print "downdowndowndowndown"
						path = "../kdata/"+str(self._k_period)+"/"+self._instrumentid+"_zhongshu.txt"
						print "has come here 2"
						bf.write_zhongshu(ret,path)

					else:
						pass
						######进入中枢一笔的macd需要修改
			else:#如果现在已经有中枢，判断和中枢同向的笔和中枢的关系
				if self.zs_now_dir==1:#中枢方向向上
					if (self._penmsg_list[-1])[1]<self.zs_now_downvalue and (self._penmsg_list[-1])[2]==self.zs_now_dir:#最后一笔没有回到中枢，中枢方向没有改变
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

						self.zs_now_upvalue=0
						self.zs_now_downvalue=0
						self.zs_now_zoushilist=self._penmsg_list[-2]
					elif (self._penmsg_list[-1])[0]>self.zs_now_upvalue and (self._penmsg_list[-1])[2]==self.zs_now_dir:#最后一笔没有回到中枢，中枢方向改变
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


						self.zs_now_upvalue=0
						self.zs_now_downvalue=0
						self.zs_now_dir=0#改变中枢方向
						self.zs_now_zoushilist=self._penmsg_list[-3]
				else:#中枢方向乡下
					if (self._penmsg_list[-1])[1]>self.zs_now_upvalue and (self._penmsg_list[-1])[2]==self.zs_now_dir:#最后一笔没有回到中枢，中枢方向没有改变
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

						self.zs_now_upvalue=0
						self.zs_now_downvalue=0
						self.zs_now_zoushilist=self._penmsg_list[-2]

					elif (self._penmsg_list[-1])[0]<self.zs_now_downvalue and (self._penmsg_list[-1])[2]==self.zs_now_dir:#最后一笔没有回到中枢，中枢方向改变
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

						self.zs_now_upvalue=0
						self.zs_now_downvalue=0
						self.zs_now_dir=1#改变中枢方向
						self.zs_now_zoushilist=self._penmsg_list[-3]





				

			#中枢高低点赋值
				


				


		
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

	def get_dea_val(self,longorshort):
		if longorshort==1:
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
		if longorshort==0:
			l = len(self._diff_array_short)
			sum_val = 0
			if l < self._dea_period_short:
				for x in xrange(0,l):
					sum_val += self._diff_array_short[x]
				ret = sum_val/l
				return ret
			else:
				left = l - self._dea_period_short
				for x in xrange(left,l):
					sum_val += self._diff_array_short[x]
				ret = sum_val/self._dea_period_short
				return ret

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
					self._parting_array.append([time,lastprice,1,0])#最后一个数据是macd的值
					return 1
				tmp = self._parting_array[-1]
				if tmp[2] ==1:
					if tmp[1] > lastprice:
						return 0
					else:
						tmp[0] = time
						tmp[1] = lastprice
						tmp[2] = 1
						tmp[3]=(self._parting_array[-1])[3]
						self._parting_array[-1] = tmp
						#self.dd_valueanddir_list
				elif tmp[2] == -1:
					if tmp[1] >= lastprice:
						return 0
					else:
						tmp1 = [time,lastprice,1,0]
						self._parting_array.append(tmp1)
			elif parting == -1:
				#lastprice = float(line[LOW])
				lastprice = float((updonglist[-2])[1])
				if len(self._parting_array) ==0:
					self._parting_array.append([time,lastprice,-1,0])
					return 1
				tmp = self._parting_array[-1]
				if tmp[2] ==1:
					if tmp[1] <= lastprice:
						return 0
					else:
						tmp1 = [time,lastprice,-1,0]
						self._parting_array.append(tmp1)
				elif tmp[2] == -1:
					if tmp[1] <= lastprice:
						return 0
					else:
						tmp[0] = time
						tmp[1] = lastprice
						tmp[2] = -1
						tmp[3]=(self._parting_array[-1])[3]
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
					self._parting_array_short.append([time,lastprice,1,0])
					return 1
				tmp = self._parting_array_short[-1]
				if tmp[2] ==1:
					if tmp[1] > lastprice:
						return 0
					else:
						tmp[0] = time
						tmp[1] = lastprice
						tmp[2] = 1
						tmp[3]=(self._parting_array_short[-1])[3]
						self._parting_array_short[-1] = tmp
				elif tmp[2] == -1:
					if tmp[1] >= lastprice:
						return 0
					else:
						tmp1 = [time,lastprice,1,0]
						self._parting_array_short.append(tmp1)
			elif parting == -1:
				#lastprice = float(line[LOW])
				lastprice = float((updonglist[-2])[1])
				if len(self._parting_array_short) ==0:
					self._parting_array_short.append([time,lastprice,-1,0])
					return 1
				tmp = self._parting_array_short[-1]
				if tmp[2] ==1:
					if tmp[1] <= lastprice:
						return 0
					else:
						tmp1 = [time,lastprice,-1,0]
						self._parting_array_short.append(tmp1)
				elif tmp[2] == -1:
					if tmp[1] <= lastprice:
						return 0
					else:
						tmp[0] = time
						tmp[1] = lastprice
						tmp[2] = -1
						tmp[3]=(self._parting_array_short[-1])[3]
						self._parting_array_short[-1] = tmp
			else:
				return 0


	def get_md_line(self,line,longorshort):

		#####长周期计算
		if longorshort==1:
			pass
			self._lastprice = float(line[LASTPRICE])
			self._time = line[DATE]+" "+line[TIME]
			kmesg = self.create_k(self._time,self._lastprice,1)
			if len(kmesg) ==0:
				return 
			else:
				# get one k line
				self.mergek(kmesg,1)
				self.get_merge_line(self._listkmsg_array,self._updonglist,1)
				# caculate the macd
				diff_val = self.get_diff_val(self._lastprice,1)
				self._diff_array.append(diff_val)
				dea_val = self.get_dea_val(1)
				tmp = [self._time,diff_val,dea_val]
				tmpbar=2*(diff_val-dea_val)
				if len(self._parting_array)!=0 and (self._parting_array[-1])[2]==-1:#由底开始的一笔
					if tmpbar>0:
						(self._parting_array[-1])[3]=(self._parting_array[-1])[3]+tmpbar
				if len(self._parting_array)!=0 and (self._parting_array[-1])[2]==1:#由顶开始的一笔
					if tmpbar<0:
						(self._parting_array[-1])[3]=(self._parting_array[-1])[3]+tmpbar

				self._macd_array.append(tmp)
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
				dea_val = self.get_dea_val(0)
				tmp = [self._time_short,diff_val,dea_val]
				tmpbar=2*(diff_val-dea_val)
				if len(self._parting_array_short)!=0 and (self._parting_array_short[-1])[2]==-1:#由底开始的一笔
					if tmpbar>0:
						(self._parting_array_short[-1])[3]=(self._parting_array_short[-1])[3]+tmpbar
				if len(self._parting_array_short)!=0 and (self._parting_array_short[-1])[2]==1:#由顶开始的一笔
					if tmpbar<0:
						(self._parting_array_short[-1])[3]=(self._parting_array_short[-1])[3]+tmpbar

				self._macd_array_short.append(tmp)
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


def main():
	date1 = [20171016,20171017,20171018,20171019,20171020]
	date2 = [20171023,20171024]
	date3 = [20171016]
	date = date1+date2
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
				
				getline_obj.findzhongshu(1)
			# data = getline_obj.get_line_data()
			# path = '../kdata/'+instrumentId + '_' + str(day) + '_total.csv'
			# bf.write_data_to_csv(data,path)


if __name__=='__main__': 
	main()