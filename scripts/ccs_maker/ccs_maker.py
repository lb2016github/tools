# -*- coding: utf-8 -*-
# @Author	: luobo
# @Contact	: helloluobo@126.com
# @Date		: 2019/8/16
# @File		: ccs_maker
# @Desc		: 创建ccs工程文件
import os

from ccs_maker import csd_parser


class CCSMaker(object):
	def __init__(self, root_dir, csd_root_dir, csd_name_list):
		self.root_dir = root_dir
		self.csd_root_dir = csd_root_dir
		self.csd_name_list = csd_name_list
		# ======= created data
		self.csd_parsers = []
		self._init_parsers()

	def _init_parsers(self):
		name_pattern = "|".join(self.csd_name_list)
		pattern = "(%s)\.csd"%name_pattern
		def on_match(root, name, is_file):
			if not is_file:
				return
			file_path = os.path.join(root, name)
			self.csd_parsers.append(csd_parser.CSDParser(file_path))

		from common import file_helper

		file_helper.walk_directory(self.csd_root_dir, pattern, on_match)

	def make(self):
		root_path_list = self._conver_path_to_list(self.root_dir)
		root_path_len = len(root_path_list)
		# get res set of ccs
		res_set = set()
		for parser in self.csd_parsers:
			parser.parse()
			res_set = res_set.union(parser.get_res_set())
			path_list = self._conver_path_to_list(parser.file_path)
			path_list = path_list[root_path_len:]
			csd_path = "/".join(path_list)
			if csd_path not in res_set:
				res_set.add(csd_path)
		# create xml node
		data_dict = {}
		for res in res_set:
			data_dict = self._add_path_to_dict(data_dict, res)
		print data_dict

	def _conver_path_to_list(self, path):
		path = path.replace("\\", "/")
		return path.split("/")

	def _add_path_to_dict(self, root, path):
		path_list = self._conver_path_to_list(path)
		cur_folder = root
		for i in xrange(len(path_list)):
			tmp = path_list[i]
			if tmp not in cur_folder:
				if tmp.find(".") > 0:   # is file
					cur_folder[tmp] = tmp
				else:
					cur_folder[tmp] = {}
			cur_folder = cur_folder[tmp]
		return root

	def _convert_folder_dict_to_xml_dict(self, folder_dict):
		from xml.etree import ElementTree
		root = ElementTree.Element("Solution")



if __name__ == "__main__":
	make = CCSMaker(r"G:\dts\lb\branches\dev_develop3\cocos\cocosstudio", r"G:\dts\lb\branches\dev_develop3\cocos\cocosstudio\csb", ["3teambattle_ability_greed"])
	make.make()

