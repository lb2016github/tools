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

def publish_csb(res_dir, csd_name_list, ccs_file_name, cocos_dir, output_dir, open=False):
	res_dir = res_dir
	target_path = os.path.join(res_dir, "../%s"%ccs_file_name)
	ccs_maker = CCSMaker(res_dir, res_dir, csd_name_list, target_path)
	ccs_maker.make()
	cocos_tool_path = os.path.join(cocos_dir, "Cocos.Tool.exe")
	cmd = "%s publish -f %s -o %s -d Serializer_FlatBuffers"%(cocos_tool_path, target_path, output_dir)
	os.system(cmd)
	if open:
		open_ccs(cocos_dir, target_path)

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
	parser.add_argument("--open", default=False, type=bool, help="Open the project")

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
	open = args.open

	if args.command == "make_ccs":
		make_ccs(res_dir, csd_name_list, ccs_file_name, cocos_dir, open)
	elif args.command == "publish":
		out_dir = args.out_dir
		if not out_dir:
			out_dir = os.path.join(res_dir, "../output_dir")
		publish_csb(res_dir, csd_name_list, ccs_file_name, cocos_dir, out_dir, open)


if __name__ == "__main__":
	parser = init_parser()
	args = parser.parse_args()
	run(args)

