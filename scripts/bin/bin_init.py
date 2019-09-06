# -*- coding: utf-8 -*-
# @Author	: luobo
# @Contact	: helloluobo@126.com
# @Date		: 2019/9/6
# @File		: bin_init
# @Desc		:
import os
cur_path = os.path.abspath(__file__)
script_dir = os.path.join(os.path.dirname(cur_path), "..")
# add path
import sys
sys.path.append(script_dir)
import init

