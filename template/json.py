# -*- coding: utf-8 -*-

import json

def write(file_path, write_data):
	with open(file_path, 'w') as f:
		text = json.dumps(write_data['data'], indent=4, sort_keys=True, ensure_ascii=False)
		f.write(text)

		return True

	return False
