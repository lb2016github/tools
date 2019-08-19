# -*- coding: utf-8 -*-
# @Author	: luobo
# @Contact	: helloluobo@126.com
# @Date		: 2019/8/19
# @File		: init
# @Desc		:


def _set_dirs():
	import os, g
	cur_path = os.path.abspath(__file__)
	g.script_dir = os.path.dirname(cur_path)
	g.res_dir = os.path.join(g.script_dir, "../res")
	# add path
	import sys
	sys.path.append(g.script_dir)

_set_dirs()

