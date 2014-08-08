# -*- coding: utf-8 -*-

def to_int(value):
	if isinstance(value, str):
		value = value.strip()

		if value == "":
			return 0, True

	try:
		return int(value), True
	except ValueError:
		try:
			return int(float(value)), True
		except ValueError:
			return 0, False

def to_float(value):	
	if isinstance(value, str):
		value = value.strip()

		if value == "":
			return 0.0, True

	try:
		return float("%.4f"%float(value)), True
	except ValueError:
		return 0.0, False

def to_string(value):	
	if value == None:
		return "", True

	if isinstance(value, str):
		value = value.strip()
	else:
		value = str(value)
	return value, True

def to_bool(value):
	if isinstance(value, str):
		value = value.strip()
		value = value.lower()
		if value == "false" or value == u"否" or value == "no":
			return False, True

		elif value == "true" or value == u"是" or value == "yes":
			return True, True

	elif isinstance(value, int):
		return value != 0, True

	elif isinstance(value, float):
		return value != 0.0, True

	elif isinstance(value, bool):
		return value, True

	return False, False


strip_value_table = {
u"，":u",",
#u"＂":u"\"",
u"｛":u"{",
u"｝":u"}",
u"（":u"(",
u"）":u")",
u"［":u"[",
u"］":u"]",
}

def strip_value(value):
	value = value.strip()
	for k, v in strip_value_table.items():
		value = value.replace(k, v)
	return value 

def to_array(value):
	if not isinstance(value, str):
		value = str(value)

	array_data = "[" + value + "]"
	array_data = strip_value(array_data)
	try:
		return eval(array_data), True
	except SyntaxError:
		return [], False

def to_map(value):
	if not isinstance(value, str):
		value = str(value)

	map_data = "{" + value + "}"
	map_data = strip_value(map_data)
	try:
		return eval(map_data), True
	except SyntaxError:
		return {}, False

def to_value(value, value_type):
	value_type = value_type.strip()
	value_type = value_type.lower()

	if value_type == "int":
		return to_int(value)

	elif value_type == "float":
		return to_float(value)

	elif value_type == "map":
		return to_map(value)

	elif value_type == "array":
		return to_array(value)

	elif value_type == "bool":
		return to_bool(value)

	elif value_type == "string":
		return to_string(value)

	else:
		return None, False
