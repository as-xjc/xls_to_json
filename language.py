# -*- coding: utf-8 -*-

import template.json as tjson
import template.lua as tlua

def write(file_path, proto):
	language = proto.getArg('language')
	if language == 'json':
		return tjson.write(file_path, proto)
	elif language == 'lua':
		return tlua.write(file_path, proto)

	return False
