# -*- coding: utf-8 -*-

import template.json as tjson
import template.lua as tlua

def write(file_path, write_data):
	language = write_data['head']['language']
	if language == 'json':
		return tjson.write(file_path, write_data)
	elif language == 'lua':
		return tlua.write(file_path, write_data)

	return False
