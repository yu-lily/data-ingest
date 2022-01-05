from abc import ABC, abstractmethod

import os
import time
import requests

ENDPOINT = "https://api.stratz.com/graphql"

class QueryHandler(ABC):
    def __init__(self) -> None:
        self.apikey = os.getenv('STRATZ_APIKEY')
        self.headers = {'Authorization': 'Bearer ' + self.apikey}

    def make_query(self, variables) -> str:
        r = requests.post(ENDPOINT, json={'query': self.query , 'variables': variables}, headers=self.headers)

        #Log that the request was made
        ts = int(time.time())
        log_fpath = './logs/api_call_log.txt'
        if not os.path.exists(log_fpath):
            open(log_fpath, 'w').close()
        with open(log_fpath, 'a') as f:
            f.write(f"{ts} {r.status_code}\n")

        if r.status_code == 200:
            return r.text
        else:
            raise Exception(f"Query failed with status code: {r.status_code}, response: {r.text}")