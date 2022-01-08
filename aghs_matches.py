import os
import json
from query_handler import QueryHandler

from dataclasses import dataclass

@dataclass
class AghsMatchesVars:
    createdAfterDateTime: int
    createdBeforeDateTime: int
    difficulty: str
    take: int
    skip: int

class AghsMatchesHandler(QueryHandler):
    def __init__(self) -> None:
        super().__init__()

        #Load GraphQL query
        with open(f'queries/aghs_matches.txt', 'r') as f:
            self.query = f.read()

        #Initialize window log
        window_log_path = "./logs/window_log.json"
        if os.path.exists(window_log_path):
            with open(window_log_path, 'r') as f:
                self.window_log = json.load(f)
        else:
            self.window_log = {}


    def make_query(self, query_vars: AghsMatchesVars) -> tuple:
        r = super().make_query(variables=query_vars.__dict__)

        query_result = json.loads(r)
        matches = query_result['data']['stratz']['page']['aghanim']['matches']
        
        reached_end = len(matches) < query_vars.take
        total_processed = len(matches) + query_vars.skip
        self.log_window(query_vars.difficulty, query_vars.createdAfterDateTime, reached_end, total_processed)
        
        if reached_end:
            next_query = None
        else:
            next_query = AghsMatchesVars(
                createdAfterDateTime=query_vars.createdAfterDateTime,
                createdBeforeDateTime=query_vars.createdBeforeDateTime,
                difficulty=query_vars.difficulty,
                take=query_vars.take,
                skip=query_vars.skip + query_vars.take
            )
        return matches, next_query

    def log_window(self, diff, start_time, reached_end, total_processed):
        if diff not in self.window_log.keys():
            self.window_log[diff] = {}
        self.window_log[diff][start_time] = {
            'reached_end': reached_end,
            'processed': total_processed
        }
        with open('./logs/window_log.json', 'w') as f:
            json.dump(self.window_log, f)