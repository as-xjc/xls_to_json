# -*- coding: utf-8 -*-

import json
import io
import re

tab = '  '

custom_area_start = u'-- ========== custom your code area start ==========\n'
custom_area_end = u'-- ========== custom your code area end ==========\n'

def _insert(stream, index, value):
	stream.write(tab*index)
	stream.write(value)

def _encoderValue(stream, lua_data):
	if isinstance(lua_data, str):
		stream.write('"')
		stream.write(lua_data)
		stream.write('"')

	elif isinstance(lua_data, bool):
		if lua_data:
			stream.write('false')
		else:
			stream.write('true')

	elif isinstance(lua_data, int):
		stream.write(str(lua_data))
		
	elif isinstance(lua_data, float):
		stream.write(str(lua_data))

	else:
		stream.write('nil')

def _encoderList(stream, index, lua_data):
	index = index + 1
	i = 1
	for v in lua_data:
		_insert(stream, index, '[')
		_encoderValue(stream, i)
		_insert(stream, 0, '] = ')

		if isinstance(v, dict):
			_insert(stream, 0, '{\n')
			_encoderDict(stream, index+1, v)
			_insert(stream, index, '},\n')

		elif isinstance(v, list):
			_insert(stream, 0, '{\n')
			_encoderList(stream, index+1, v)
			_insert(stream, index, '},\n')

		else:
			_encoderValue(stream, v)
			stream.write(',\n')

		i = i + 1

def _encoderDict(stream, index, lua_data):
	index = index + 1
	for k, v in lua_data.items():
		_insert(stream, index, '[')
		_encoderValue(stream, k)
		_insert(stream, 0, '] = ')

		if isinstance(v, dict):
			stream.write('{\n')
			_encoderDict(stream, index+1, v)
			_insert(stream, index, '},\n')

		elif isinstance(v, list):
			stream.write('{\n')
			_encoderList(stream, index+1, v)
			_insert(stream, index, '},\n')

		else:
			_encoderValue(stream, v)
			stream.write(',\n')

def _inserHead(stream, write_data):
	stream.write('--[[\n')
	stream.write('xls path: %s'%write_data['head']['xls_path'])
	stream.write('\n]]--\n\n')

def _encoderLua(write_data, custom_code):
	stream = io.StringIO()

	_inserHead(stream, write_data)

	lua_data = write_data['data']
	stream.write('local hander = {}\n\n')
	stream.write('local __data__ = {\n')
	if isinstance(lua_data, dict):
		_encoderDict(stream, 0, lua_data)

	elif isinstance(lua_data, list):
		_encoderDict(stream, 0, lua_data)

	stream.write('}\n\n')

	stream.write(
'''function hander.getData()
	return __data__
end\n\n''')

	stream.write(custom_area_start)
	if len(custom_code):
		stream.write(custom_code)
	stream.write(custom_area_end)

	stream.write('\n\nreturn hander')
	text = stream.getvalue()
	stream.close()
	return text

def _getCustomCode(text):
	if len(text) < 1:
		return ''

	engine = re.compile(u'%s(.*?)%s'%(custom_area_start, custom_area_end), re.DOTALL)
	result = engine.findall(text)
	if len(result):
		return result[0]
	else:
		return ''

def write(file_path, write_data):
	try:
		with open(file_path, 'r+', encoding = 'utf8') as f:
			oldText = f.read()
	except:
		oldText = ''

	with open(file_path, 'w', encoding = 'utf8') as f:
		custom_code = _getCustomCode(oldText)
		text = _encoderLua(write_data, custom_code)
		f.write(text)
		return True

	return False
