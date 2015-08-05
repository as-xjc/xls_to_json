# -*- coding: utf-8 -*-

import json
import io

tab = ' '

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

def __encoder(lua_data):
	stream = io.StringIO()
	stream.write('return \n')
	stream.write('{\n')
	if isinstance(lua_data, dict):
		_encoderDict(stream, 0, lua_data)

	elif isinstance(lua_data, list):
		_encoderDict(stream, 0, lua_data)

	stream.write('}\n')

	text = stream.getvalue()
	stream.close()
	return text

def write(file_path, write_data):
	with open(file_path, 'w', encoding = 'utf8') as f:
		f.write('--[[\n')
		f.write('xls path: %s'%write_data['head']['xls_path'])
		f.write('\n]]--\n\n')

		text = __encoder(write_data['data'])
		f.write(text)
		return True

	return False
