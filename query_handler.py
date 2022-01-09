from abc import ABC, abstractmethod

import os
import time
import requests

ENDPOINT = "https://api.stratz.com/graphql"

class QueryHandler(ABC):
    def __init__(self, query_path: str = None) -> None:
        self.apikey = os.getenv('STRATZ_APIKEY')
        self.headers = {'Authorization': 'Bearer ' + self.apikey}

        if query_path:
            self.load_query(query_path)

    def load_query(self, query_path: str) -> None:
        with open(query_path, 'r') as f:
            self.query = f.read()

    def make_query(self, variables: dict = {}) -> str:
        r = requests.post(ENDPOINT, json={'query': self.query , 'variables': variables}, headers=self.headers)

        rl_s, rl_m, rl_h, rl_d = (r.headers['X-RateLimit-Remaining-Second'],
        r.headers['X-RateLimit-Limit-Minute'],
        r.headers['X-RateLimit-Limit-Hour'],
        r.headers['X-RateLimit-Limit-Day'])

        #Log that the request was made
        ts = int(time.time())
        log_fpath = './logs/api_call_log.csv'
        if not os.path.exists(log_fpath):
            with open(log_fpath, 'w') as f:
                f.write('timestamp,status_code,rl_sec,rl_min,rl_hr,rl_day\n')
        with open(log_fpath, 'a') as f:
            f.write(f"{ts},{r.status_code},{rl_s},{rl_m},{rl_h},{rl_d}\n")

        if r.status_code == 200:
            return r.text
        else:
            raise Exception(f"Query failed with status code: {r.status_code}, response: {r.text}")