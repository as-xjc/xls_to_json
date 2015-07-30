# -*- coding: utf-8 -*-

import template.json as tjson

def write(file_path, write_data):
	language = write_data['head']['language']
	if language == 'json':
		return tjson.write(file_path, write_data)

	return False
