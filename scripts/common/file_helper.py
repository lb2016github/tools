# -*- coding: utf-8 -*-
# @Author	: luobo
# @Contact	: helloluobo@126.com
# @Date		: 2019/6/24
# @File		: file_helper
# @Desc		: 提供一些文件操作的接口

import os
import re
import argparse
import shutil
import logging


def walk_directory(directory, pattern, on_match):
	pattern = re.compile(pattern)
	for root, dirs, files in os.walk(directory, topdown=False):
		for name in files:
			if pattern.match(name):
				on_match(root, name, True)
		for name in dirs:
			if pattern.match(name):
				on_match(root, name, False)

def copy_file(src_dir, target_dir, name_pattern, debug=False):
	def _on_match(root, name, is_file):
		if is_file:
			src_path = os.path.join(root, name)
			dst_dir = root.replace(src_dir, target_dir, 1)
			if not os.path.exists(dst_dir):
				os.makedirs(dst_dir)
			logging.info("copy %s ---> %s"%(src_path, dst_dir))
			if not debug:
				shutil.copy(src_path, dst_dir)
	walk_directory(src_dir,  name_pattern, _on_match)

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--cmd", help="cmd name", type=str)
	parser.add_argument("-sub", "--sub_dir", help="sub directory", type=str)
	parser.add_argument("-s", "--src", help="src res directory", type=str)
	parser.add_argument("-d", "--dst", help="dest res directory", type=str)
	parser.add_argument("-p", "--pattern", help="name_pattern", type=str)
	parser.add_argument("-l", "--log", help="log file path", type=str)
	args = parser.parse_args()
	return args

def main():
	args = get_args()
	if args.log:
		logging.basicConfig(filename=args.log, filemode="a", level=logging.INFO)
	cmd = args.cmd
	if cmd == "copy_file":
		src_dir = args.src
		dst_dir = args.dst
		if args.sub_dir:
			src_dir = os.path.join(src_dir, args.sub_dir)
			dst_dir = os.path.join(dst_dir, args.sub_dir)
		copy_file(src_dir, dst_dir, args.pattern)

if __name__ == "__main__":
	main()

