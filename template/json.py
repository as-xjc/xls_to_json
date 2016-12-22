# -*- coding: utf-8 -*-

import json

def write(file_path, proto):
	with open(file_path, 'w', encoding = 'utf8') as f:
		text = json.dumps(proto.getData(), indent=4, sort_keys=True, ensure_ascii=False)
		f.write(text)

		return True

	return False
