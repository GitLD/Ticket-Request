#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'LuDi'

"""命令行火车票查看器

Usage:
	tickets [-gdtkz] <from> <to> <date>
	
Options:
	-h,--help	显示帮助菜单
	-g			高铁
	-d			动车
	-t			特快
	-k			快速
	-z			直达
	
Example:
	tickets 北京 上海 2016-10-10
	tickets -dg 成都 南京 2016-10-10	
"""
from docopt import docopt
from stations import stations
from prettytable import PrettyTable
from colorama import init, Fore
import requests
import re

init()

station_reverse = {v:k for k,v in stations.items()}
class TrainsCollection:
	header = u'车次 车站 时间 历时 商务座 一等座 二等座 高级软卧 软卧 动卧 硬卧 软座 硬座 无座 其他'.split()
	def __init__(self, available_trains, options):
		"""查询到的火车班次集合
		:param available_trains: 一个列表, 包含可获得的火车班次, 每个火车班次是一个字典
		:param options: 查询的选项, 如高铁, 动车, etc...
		"""
		self.available_trains = available_trains
		self.options = options

	def _get_duration(self, raw_train):
		duration = raw_train[10].replace(':',u'小时') + u'分'
		if duration.startswith('00'):
			return duration[4:]
		if duration.startswith('0'):
			return duration[1:]
		return duration

	@property
	def trains(self):
		for raw_train in self.available_trains:
			# train_data = re.findall(u'([a-zA-Z0-9]+)'
									# '\|([A-Z]{3})\|([A-Z]{3})'
									# '\|([A-Z]{3})\|([A-Z]{3})'
									# '\|([0-9]{2}\:[0-9]{2})'
									# '\|([0-9]{2}\:[0-9]{2})'
									# '\|([0-9]{2}\:[0-9]{2})'
									# ,raw_train)
			train_data = raw_train.split("|")
			train_no = train_data[3]
			initial = train_no[0].lower()
			if not self.options or initial in self.options:
				from_station_code = train_data[6]
				from_station_name = station_reverse[from_station_code]
				to_station_code = train_data[7]
				to_station_name = station_reverse[to_station_code]
				start_time = train_data[8]
				arrive_time = train_data[9]
				seat_num = train_data[-6:-17:-1]
				train = [
					train_no,
					'\n'.join([Fore.GREEN + from_station_name + Fore.RESET,
					Fore.RED + to_station_name +Fore.RESET]),
					'\n'.join([Fore.GREEN + start_time + Fore.RESET,
					Fore.RED + arrive_time + Fore.RESET]),
					self._get_duration(train_data),] + seat_num
				yield train
		
	def pretty_print(self):
		pt = PrettyTable()
		pt.padding_width = 0   # 填充宽度
		pt._set_field_names(self.header)
		for train in self.trains:
			pt.add_row(train)
		print(pt)

def cli():
	"""command-line interface"""
	arguments = docopt(__doc__)
	from_station = stations.get(arguments['<from>'])
	to_station = stations.get(arguments['<to>'])
	date = arguments['<date>']
	# 构建url
	url = ('https://kyfw.12306.cn/otn/leftTicket/query?'
		'leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&'
		'leftTicketDTO.to_station={}&purpose_codes=ADULT').format(
		date, from_station, to_station
		)
	# 获取参数（添加verify=False参数不验证证书）
	options = ''.join([
		key for key, value in arguments.items() if value is True
		])
	r = requests.get(url,verify=False)
	available_trains = r.json()['data']['result']
	TrainsCollection(available_trains, options).pretty_print()
if __name__ == '__main__':
	cli()