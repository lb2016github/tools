# -*- coding: utf-8 -*-
# @Author	: luobo
# @Contact	: helloluobo@126.com
# @Date		: 2019/8/16
# @File		: csd_parser
# @Desc		: 解析csb，返回必要的信息
import re

class CSDParser(object):
	def __init__(self, file_path):
		self.file_path = file_path
		self.res_set = set()

	def parse(self):
		with open(self.file_path, mode="r") as f:
			txt = "\n".join(f.readlines())
			rst = re.findall('Path=\".+?\..+?\"', txt, )
			for res_str in rst:
				res_path = res_str[6: -1]
				if len(res_path) > 0 and res_path not in self.res_set:
					self.res_set.add(res_path)

	def get_res_set(self):
		return self.res_set

if __name__ == "__main__":
	parser = CSDParser(r"G:\dts\lb\branches\dev_develop2\cocos\cocosstudio\csb\3teambattle_ability_greed.csd")
	parser.parse()

