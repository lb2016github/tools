# -*- coding: utf-8 -*-
# @Author	: luobo
# @Contact	: helloluobo@126.com
# @Date		: 2019/9/6
# @File		: csb_publish
# @Desc		: cocos相关工具
import argparse
import os
import bin_init
from ccs_maker.ccs_maker import CCSMaker
import shutil

def publish_csb(res_dir, csd_name_list, ccs_file_name, cocos_dir, output_dir, open=False):
	"""
	发布csb
	:param res_dir: cocos里面res和csb所在目录
	:param csd_name_list: 需要发布的csd名字列表
	:param ccs_file_name: 生成的ccs文件名
	:param cocos_dir: cocosstudio的安装目录
	:param output_dir: 生成文件的输出目录
	:param open: 发布后，是否打开ccs工程
	:return:
	"""
	res_dir = res_dir
	target_path = os.path.join(res_dir, "../%s"%ccs_file_name)
	ccs_maker = CCSMaker(res_dir, res_dir, csd_name_list, target_path)
	ccs_maker.make()
	# clear output_dir
	print "Start clear output_dir: ", output_dir
	if os.path.exists(output_dir):
		shutil.rmtree(output_dir)
	# publish ccs
	print "Start publish ccs"
	cocos_tool_path = os.path.join(cocos_dir, "Cocos.Tool.exe")
	cmd = "%s publish -f %s -o %s -d Serializer_FlatBuffers -w"%(cocos_tool_path, target_path, output_dir)
	print "Start execute cmd", cmd
	os.system(cmd)
	# copy language res
	print "Start copy language res"
	copy_language_res(res_dir, output_dir)
	if open:
		open_ccs(cocos_dir, target_path)


def copy_language_res(res_dir, out_dir):
	"""
	拷贝多语言资源
	:param src_language_dir: 多语言资源
	:param out_dir:
	:return:
	"""
	print "=================Start copy language res==================="
	src_language_dir = "%s/res/ui1/language"%res_dir
	out_language_dir = "%s/res/ui1/language"%out_dir
	print out_language_dir
	# 检查是否有多语言资源输出
	if not os.path.exists(out_language_dir):
		return
	filenames = []
	for i in os.walk(out_language_dir):
		filenames.extend(i[2])

	def _get_rest_path(child_dir, parent_dir):
		abs_child_path = os.path.abspath(child_dir)
		abs_parent_path = os.path.abspath(parent_dir)
		if abs_parent_path not in abs_child_path:
			print "Error: %s is not child of %s" % (child_dir, parent_dir)
			return
		return abs_child_path[len(abs_parent_path) + 1:]
	for parent_dir, child_dirs, child_files in os.walk(src_language_dir):
		for file in child_files:
			if file in filenames:
				rest_path = _get_rest_path(parent_dir, src_language_dir)
				dst_dir = os.path.join(src_language_dir, rest_path)
				if not os.path.exists(dst_dir):
					os.mkdir(dst_dir)
				dst_path = os.path.join(dst_dir, file)
				src_path = os.path.join(parent_dir, file)
				print "copy: ", src_path, dst_path
				shutil.copy(src_path, dst_path)

def make_ccs(res_dir, csd_name_list, ccs_file_name, cocos_dir, open=False):
	res_dir = res_dir
	target_path = os.path.join(res_dir, "../%s"%ccs_file_name)
	ccs_maker = CCSMaker(res_dir, res_dir, csd_name_list, target_path)
	ccs_maker.make()
	if open:
		open_ccs(cocos_dir, target_path)

def open_ccs(cocos_dir, ccs_filepath):
	cmd = "%s/CocosStudio.exe %s"%(cocos_dir, ccs_filepath)
	os.system(cmd)

def init_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('--res_dir', help='direction of cocos res', required=True)
	parser.add_argument('--csd_dir', help="direction of csd files.")
	parser.add_argument('--cocos_dir', help='CocosStudio install path', required=True)
	parser.add_argument('--csd', nargs='+', help="csd list", default=[])
	parser.add_argument("--ccs", default="default", help="ccs file name")

	subparsers = parser.add_subparsers(dest="command", help="sub commands")

	subparsers.add_parser("make_ccs", help="make ccs file")

	publish_parser = subparsers.add_parser("publish", help="publish csb files")
	publish_parser.add_argument("--out_dir", help="output direction")

	return parser

def test():
	args = ['--res_dir', r'G:\g95na\cocos\ui\cocosstudio',
			 # '--csd_dir', r'G:\g95na\cocos\ui\cocos\cocosstudio\csb',
			 '--cocos_dir', r'D:\Develop\Cocos\CocosStudio',
			 '--csd', '1441_905.csd', 'mall_recommend_big_item_1411_905.csd',
			 '--ccs', 'auto.ccs',
			 'publish'
			 ]
	parser = init_parser()
	args = parser.parse_args(args)
	run(args)

def run(args):
	print args
	res_dir = args.res_dir
	cocos_dir = args.cocos_dir
	csd_name_list = args.csd
	ccs_file_name = args.ccs
	open = False

	if args.command == "make_ccs":
		make_ccs(res_dir, csd_name_list, ccs_file_name, cocos_dir, open)
	elif args.command == "publish":
		out_dir = args.out_dir
		if not out_dir:
			out_dir = os.path.join(res_dir, "../res")
		publish_csb(res_dir, csd_name_list, ccs_file_name, cocos_dir, out_dir, open)


if __name__ == "__main__":
	parser = init_parser()
	args = parser.parse_args()
	run(args)

