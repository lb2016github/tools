# -*- coding: utf-8 -*-
# @Author	: luobo
# @Contact	: helloluobo@126.com
# @Date		: 2019/8/16
# @File		: xml_helper
# @Desc		:
from xml.etree import ElementTree

ATTRIBUTES = "_ATTRIBUTE"
TEXT = "_TEXT"
NAME = "_NAME"
CHILDREN = "_CHILDREN"

# return node list
def parse_dict_to_xml(parent, data_dict):
	attr_dict = data_dict.get(ATTRIBUTES, {})
	text = data_dict.get(TEXT, "")
	name = data_dict.get(NAME, "")
	children = data_dict.get(CHILDREN, {})
	ele = ElementTree.SubElement(parent, name, attrib=attr_dict).text = text
	for child in children:
		parse_dict_to_xml(ele, child)
	return parent


class XMLElement(object):
	def __init__(self, name, attr, text):
		self.name = name
		self.attr = attr
		self.text = text
		self.children = []
		self.parent = None

	def parse(self, parent=None):
		if parent is None:
			ele = ElementTree.Element(self.name, attrib=self.attr)
		else:
			ele = ElementTree.SubElement(parent, self.name, attrib=self.attr)
		ele.text = self.text
		for child in self.children:
			child.parse(ele)
		return ele

class FolderElement(XMLElement):
	pass



