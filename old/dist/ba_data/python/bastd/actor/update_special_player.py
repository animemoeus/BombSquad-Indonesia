# Run this script with crontab, etc to update special_player list automatically

import os
import requests
import json
import time

def main():
	dir_path = os.path.dirname(os.path.realpath(__file__))

	admin_list = json.loads(requests.get('https://bombsquad.my.id/stats/get_admin/').text)['admin_list']
	kaizoku_ou_list = json.loads(requests.get('https://bombsquad.my.id/stats/get_kaizoku_ou/').text)['kaizoku_ou_list']
	yonkou_list = json.loads(requests.get('https://bombsquad.my.id/stats/get_yonkou/').text)['yonkou_list']


	with open(f'{dir_path}/special_player.py') as file:
		s = [row for row in file]
		s[0] = 'admin_list = ' + str(admin_list) + '\n'
		s[1] = 'kaizoku_ou_list = ' + str(kaizoku_ou_list) + '\n'
		s[2] = 'yonkou_list = ' + str(yonkou_list) + '\n'
		
		f = open(f'{dir_path}/special_player.py','w') 
		for updates in s:
			f.write(updates)
		f.close()

if __name__ == '__main__':
	while True:
		try:
			main()
			print('Special Player List Updated')
		except:
			print('Failed To Update Special Player List')
	
		time.sleep(600)