# -*- coding: utf-8 -*-
# @Author	: luobo
# @Contact	: helloluobo@126.com
# @Date		: 2019/8/16
# @File		: xml_helper
# @Desc		:
from xml.dom import minidom


class XMLElement(object):
	def __init__(self, name, attr):
		self.name = name
		self.attr = attr
		self.children = []

	def parse(self):
		ele = minidom.Element(self.name)
		for name, value in self.attr.items():
			ele.setAttribute(name, value)
		for child in self.children:
			dom_ele = child.parse()
			ele.appendChild(dom_ele)
		return ele

	def set_children(self, children):
		self.children = children

class ResElement(XMLElement):
	RES_ELEMENT_DICT = {}
	def __init__(self, tag_name, attr_name):
		super(ResElement, self).__init__(tag_name, {"Name": attr_name})
		if tag_name == "Project":
			self.on_project_element()

	def on_project_element(self):
		self.attr["Type"] = "Layer"

	@classmethod
	def register_res_element(cls, suffix, tag_name):
		cls.RES_ELEMENT_DICT[suffix] = tag_name

	@classmethod
	def create_res_element(cls, res_name):
		idx = res_name.rfind(".")
		suffix = ""
		if idx > 0:     # is file
			suffix = res_name[idx + 1:]
		tag_name = cls.RES_ELEMENT_DICT.get(suffix)
		if tag_name:
			return cls(tag_name, res_name)
		else:
			print("Error: No Element is found with suffix", suffix)
			return None


def register_elements():
	ele_dict = {
		"Folder": [""],
		"Image": ["png", "jpg"],
		"File": ["ico", "json"],
		"TTF": ["ttf", "ttc"],
		"Fnt": ["fnt"],
		"PlistParticleFile": ["plist"],
		"Project": ["csd"],
	}
	for tag_name, suffix_list in ele_dict.items():
		for suffix in suffix_list:
			ResElement.RES_ELEMENT_DICT[suffix] = tag_name

def get_element(res_name):
	return ResElement.create_res_element(res_name)


def load_template(filepath):
	dom_tree = minidom.parse(filepath)
	return dom_tree

register_elements()
