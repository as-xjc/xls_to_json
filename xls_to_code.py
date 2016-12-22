# -*- coding: utf-8 -*-

import sys
import xlrd
import re
import encoding
import language as lang
import prototype

def read_xls_head(proto, sheet):
	index = 0
	while sheet.cell(index, 0).value != '':
		row = sheet.row_values(index)
		key = row[0]
		list = []
		for i in range(1, len(row)):
			value = row[i]
			if value == '':
				continue

			list.append(value)

		if len(list) == 1:
			proto.setArg(key, list[0])
		else:
			proto.setArg(key, list)

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

def read_data_struct(proto, sheet):
	try:
		which = proto.getArg('struct_row')
		struct_line = int(proto.getArg(which))
		struct_line -= 1
	except KeyError:
		return False

	if struct_line <= 1:
		return False

	rows = sheet.row_values(struct_line)
	for i in range(0, len(rows)):
		value = rows[i]
		if value != '':
			key, data_type = parse_struct(value)
			if key and data_type:
				if encoding.is_supported(data_type):
					proto.addType(i, key, data_type, value)
				else:
					print('unknow type[%s] in (%d,%d)[%s]'%(data_type, struct_line, i, value))
					sys.exit(1)

	return True

def parse_data(proto, x, y, value):
	try:
		structInfo = proto.getType(y)
	except KeyError:
		return None, None, False

	data_value, ok = encoding.to_value(value, structInfo['type'])
	if ok:
		return structInfo['name'], data_value, True
	else:
		print('parse data error: (%d,%d)[%s][%s]'%(x, y, structInfo['content'], value))
		sys.exit(1)

def need_parse(proto, y):
	try:
		tmp = proto.getType(y)
		return len(tmp) > 0
	except KeyError:
		return False

def read_xls_data_line(proto, row_index, rows):
	result = {}
	for i in range(0, len(rows)):
		if not need_parse(proto, i):
			continue

		row_value = rows[i]
		key, value, ok = parse_data(proto, row_index, i, row_value)
		if ok:
			result[key] = value

	return result, True

def read_xls_data(proto, sheet):
	try:
		start_line = int(proto.getArg('start_row'))
		start_line -= 1
	except KeyError:
		return False

	if start_line <= 1:
		return False

	try:
		data_type = proto.getArg('data_type')
		if data_type == 'array':
			data_type = 'array'
		else:
			data_type = 'map'
	except KeyError:
		data_type = 'map'

	for i in range(start_line, sheet.nrows):
		rows = sheet.row_values(i)
		result, isOk = read_xls_data_line(proto, i, rows)
		if isOk:
			if data_type == 'array':
				proto.addData(i, result)
			else:
				key, value, ok = parse_data(proto, start_line, 0, rows[0])
				if ok:
					proto.addData(value, result)
				else:
					return False
		else:
			return False

	return True

def usage():
	print('usage:')
	print('	python xls_to_json.py xls_path sheet_name to_code_path language struct_row')

if __name__ == '__main__':
	if len(sys.argv) != 6:
		usage()
		sys.exit(1)

	xls_path, sheet_name, to_json_path, language, struct_row = sys.argv[1:6]

	try:
		xls = xlrd.open_workbook(xls_path)
	except FileNotFoundError:
		print('can\'t open xls:%s'%(xls_path))
		sys.exit(1)

	try:
		sheet = xls.sheet_by_name(sheet_name)
	except xlrd.biffh.XLRDError:
		print('can\'t get sheet:%s'%(sheet_name))
		sys.exit(1)

	proto = prototype.Prototype()
	if not read_xls_head(proto, sheet):
		print('read xls head fail')
		sys.exit(1)

	proto.setArg('language', language)
	proto.setArg('xls_path', xls_path)
	proto.setArg('struct_row', struct_row)
	#proto.printArgs()

	proto.setDataType(proto.getArg('data_type'))

	if not read_data_struct(proto, sheet):
		print('read struct fail')
		sys.exit(1)

	#proto.printTypes()

	if read_xls_data(proto, sheet):
		#proto.printData()
		lang.write(to_json_path, proto)
	else:
		print('read xls data fail')
		sys.exit(1)
