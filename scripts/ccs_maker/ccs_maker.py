# -*- coding: utf-8 -*-
# @Author	: luobo
# @Contact	: helloluobo@126.com
# @Date		: 2019/8/16
# @File		: ccs_maker
# @Desc		: 创建ccs工程文件
import os
import csd_parser
import xml_helper


class CCSMaker(object):
	def __init__(self, root_dir, csd_root_dir, csd_name_list, target_path):
		self.root_dir = root_dir
		self.csd_root_dir = csd_root_dir
		self.csd_name_list = csd_name_list
		self.target_path = target_path  # target file path
		# ======= created data
		self.csd_parsers = []
		self._init_parsers()

	def _init_parsers(self):
		name_pattern = "|".join(self.csd_name_list)
		pattern = "^.+\.csd"
		def on_match(root, name, is_file):
			if not is_file:
				return
			if name not in self.csd_name_list:
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

		# load template
		import os
		temp_path = os.path.join(g.res_dir, "ui.ccs")
		dom_tree = xml_helper.load_template(temp_path)
		root_folder = dom_tree.getElementsByTagName("RootFolder")[0]
		# update res
		def _convert_res_dict_to_elements(data):
			rst = []
			for res_name, sub_data in data.items():
				ele = xml_helper.get_element(res_name)
				if isinstance(sub_data, dict):
					ele.set_children(_convert_res_dict_to_elements(sub_data))
				rst.append(ele)
			rst.sort(key=lambda key: key.name)
			return rst
		elements = _convert_res_dict_to_elements(data_dict)
		for ele in elements:
			dom_ele = ele.parse()
			if dom_ele:
				root_folder.appendChild(dom_ele)
		with open(self.target_path, mode="w") as f:
			dom_tree.writexml(f, indent="\t", newl="\n")

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





if __name__ == "__main__":
	import init, g
	print g.script_dir
	print g.res_dir
	root_dir = r"G:\dts\lb\branches\dev_develop3\cocos\cocosstudio"
	ccs_dir = os.path.join(root_dir, "csb")
	csd_list = []
	target_file = "tmp.ccs"
	print ccs_dir
	from common import file_helper
	def on_match(root, file_name, is_file):
		csd_list.append(file_name)
	file_helper.walk_directory(ccs_dir, "^.+\.csd", on_match=on_match)
	make = CCSMaker(root_dir, ccs_dir, csd_list, target_file)
	make.make()

