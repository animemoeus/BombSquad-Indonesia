# Arter Tendean, Kinamang 1, 11 Agustus 2020

import threading
import json
import os
import requests

from . import secrets

# where our stats file and pretty html output will go

# get bombsquad directory

def update_account_info(account_id,account_kills=0,account_killed=0,account_scores=0,account_played=0,account_name=None,account_characters=None):

    data = {
        'account_id': account_id,
        'account_kills': account_kills,
        'account_killed': account_killed,
        'account_scores': account_scores,
        'account_played': account_played,
        'account_name': account_name,
        'account_characters': account_characters,
    }

    requests.get(secrets.stats_server_address,params=data)

def update(score_set):

    account_name = {}
    account_scores = {}
    account_kills = {}
    account_killed = {}
    account_characters = {}

    for player in score_set._player_records.keys():
        account_id = None
        try:
            account_id = score_set._player_records[player]._last_sessionplayer.get_account_id()
        except:
            pass

        if account_id is not None:
            account_kills.setdefault(account_id, 0)  # make sure exists
            account_kills[account_id] += score_set._player_records[player].accum_kill_count
            account_killed.setdefault(account_id,0)
            account_killed[account_id] += score_set._player_records[player].accum_killed_count
            account_scores.setdefault(account_id,0)
            account_scores[account_id] += score_set._player_records[player].accumscore
            account_name.setdefault(account_id,score_set._player_records[player].name)
            account_characters.setdefault(account_id,score_set._player_records[player].character)

    # Ok; now we've got a dict of account-ids and kills.
    # Now lets kick off a background thread to load existing scores
    # from disk, do display-string lookups for accounts that need them,
    # and write everything back to disk (along with a pretty html version)
    # We use a background thread so our server doesn't hitch while doing this.
    UpdateThread(account_kills,account_killed,account_scores,account_name,account_characters).start()


class UpdateThread(threading.Thread):
    def __init__(self, account_kills,account_killed,account_scores,account_name,account_characters):
        threading.Thread.__init__(self)
        self._account_kills = account_kills
        self._account_killed = account_killed
        self._account_scores = account_scores
        self._account_name = account_name
        self._account_characters = account_characters

    def run(self):
        for account_id, kill_count in self._account_kills.items():
            update_account_info(account_id=account_id,account_kills=kill_count)
        for account_id, killed_count in self._account_killed.items():
            update_account_info(account_id=account_id,account_killed=killed_count)
        for account_id, scores_count in self._account_scores.items():
            update_account_info(account_id=account_id,account_scores=scores_count)
        for account_id, character in self._account_characters.items():
            update_account_info(account_id=account_id,account_characters=character)
        for account_id, name in self._account_name.items():
            update_account_info(account_id=account_id,account_name=name)

        print('Player Stats Updated.')