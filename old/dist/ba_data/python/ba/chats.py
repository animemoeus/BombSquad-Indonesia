import _ba

import json
import threading
import requests

from . import secrets

def get_player_list():

	player_list = list()

	for player in _ba.get_game_roster():
		if player['client_id'] == -1:
			pass
		else:
			info = {
				'name': json.loads(player['spec_string'])['n'],
				'client_id': player['client_id'],
				'account_id': player['account_id']
			}

			player_list.append(info)

	return player_list


def save(msg,client_id):
	player_list = get_player_list()

	for player in player_list:
		if player['client_id'] == client_id:
			message_info = {
				'from': player['name'],
				'message': msg,
				'account_id': player['account_id']
			}

			try:
				SaveChat(player['name'],msg,player['account_id']).start()
			except:
				print('Failed To Update Chat')


class SaveChat(threading.Thread):
	def __init__(self,name,message,account_id):
		threading.Thread.__init__(self)
		self.name = name
		self.message = message
		self.account_id = account_id

	def run(self):
		requests.get(secrets.chat_server_address,
					params={'name':self.name,'message':self.message,'account_id':self.account_id})