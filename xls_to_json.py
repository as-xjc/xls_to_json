# -*- coding: utf-8 -*-

import sys
import xlrd
import re
import json
sys.path.append("..")
import encoding

def read_xls_head(xls_data, sheet):
	head = {}
	xls_data["head"] = head

	index = 0
	while sheet.cell(index, 0).value != "":
		key = sheet.cell(index, 0).value
		value = sheet.cell(index, 1).value
		head[key] = value
		index += 1

		if index > 20:
			return False 

	return True

def parse_struct(value):
	value = str(value)
	result = re.match(u'^(.*)\((.*)\)', value)
	if result:
		return result.group(1), result.group(2)
	else:
		return None, None

support_data_type = ("int", "float", "string", "map", "array", "bool")
def read_data_struct(xls_data, sheet):
	try:
		struct_line = int(xls_data["head"]["key_row"])
		struct_line -= 1
	except KeyError:
		return False

	if struct_line <= 1:
		return False

	struct = {}
	xls_data["struct"] = struct

	rows = sheet.row_values(struct_line)
	for i in range(0, len(rows)):
		value = rows[i]
		if value != "":
			key, data_type = parse_struct(value)
			if key and data_type:
				if not data_type in support_data_type:
					print("unknow type[%s] in (%d,%d)[%s]"%(data_type, struct_line, i, value))
					sys.exit(1)
				else:
					struct[i] = {"key":key, "type":data_type, "msg":value}

	return True

def parse_data(xls_data, x, y, value):
	try:
		structInfo = xls_data["struct"][y]
	except KeyError:
		return None, None, False

	data_value, ok = encoding.to_value(value, structInfo["type"])
	if ok:
		return structInfo["key"], data_value, True
	else:
		print("parse data error: (%d,%d)[%s][%s]"%(x, y, structInfo["msg"], value))
		sys.exit(1)

def need_parse(xls_data, y):
	try:
		tmp = xls_data["struct"][y]
		return len(tmp) > 0
	except KeyError:
		return False

def read_xls_data_line(xls_data, row_index, rows):
	result = {}
	for i in range(0, len(rows)):
		if not need_parse(xls_data, i):
			continue

		row_value = rows[i]
		key, value, ok = parse_data(xls_data, row_index, i, row_value)
		if ok:
			result[key] = value

	return result, True

def read_xls_data(xls_data, sheet):
	try:
		start_line = int(xls_data["head"]["start_row"])
		start_line -= 1
	except KeyError:
		return False

	if start_line <= 1:
		return False

	try:
		data_type = xls_data["head"]["data_type"]
		if data_type == "array":
			data_type = "array"
		else:
			data_type = "map"
	except KeyError:
		data_type = "map"

	for i in range(start_line, sheet.nrows):
		rows = sheet.row_values(i)
		result, isOk = read_xls_data_line(xls_data, i, rows)
		if isOk:
			if data_type == "array":
				xls_data["data"].append(result)
			else:
				key, value, ok = parse_data(xls_data, start_line, 0, rows[0])
				if ok:
					xls_data["data"][value] = result
				else:
					return False
		else:
			return False

	return True

def save_json(json_data, path):
	file = open(path, "w")
	file.write(json_data)
	file.close()


def usage():
	print("usage:")
	print("	python xls_to_json.py xls_path sheet_name to_json_path")

if __name__ == "__main__":
	if len(sys.argv) != 4:
		usage()
		sys.exit(1)

	xls_path, sheet_name, to_json_path = sys.argv[1:4]

	try:
		xls = xlrd.open_workbook(xls_path)
	except FileNotFoundError:
		print("can't open xls:%s"%(xls_path))
		sys.exit(1)

	try:
		sheet = xls.sheet_by_name(sheet_name)
	except xlrd.biffh.XLRDError:
		print("can't get sheet:%s"%(sheet_name))
		sys.exit(1)

	xls_data = {}
	if not read_xls_head(xls_data, sheet):
		print("read xls head fail")
		sys.exit(1)

	try:
		key = xls_data["head"]["data_type"]
		if key == "array":
			xls_data["data"] = []
		else:
			xls_data["data"] = {}
	except KeyError:
		xls_data["data"] = {}

	if not read_data_struct(xls_data, sheet):
		print("read struct fail")
		sys.exit(1)

	if read_xls_data(xls_data, sheet):
		json_data = json.dumps(xls_data["data"], indent=4, sort_keys=True, ensure_ascii=False)
		save_json(json_data, to_json_path)
	else:
		print("read xls data fail")
		sys.exit(1)
