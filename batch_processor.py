from collections import deque
import json
import time
import os

from aghs_matches import AghsMatchesVars, AghsMatchesHandler
from sql_writer import SQLWriter


class BatchProcessor:
    def __init__(self):
        window_log_path = "./logs/window_log.json"
        if os.path.exists(window_log_path):
            with open(window_log_path, 'r') as f:
                self.window_log = json.load(f)
        else:
            self.window_log = {}

        self.aghs_matches_handler = AghsMatchesHandler()
        self.sql_writer = SQLWriter()

    def populate_queue(self, difficulties: list = ['APEXMAGE', 'GRANDMAGUS'], cutoff: int = None):
        AGHANIM_RELEASE = 1639533060
        CURRENT_TIME = int(time.time())
        WINDOW_SIZE = 18000 # 5 hours
        
        self.processing_queue = deque()

        if not cutoff:
            cutoff = CURRENT_TIME - 2 * WINDOW_SIZE

        for difficulty in difficulties:
            start_time = AGHANIM_RELEASE
            while start_time < cutoff:
                skip = 0
                #Check if window has been handled
                if difficulty in self.window_log.keys():
                    if start_time in self.window_log[difficulty].keys():
                        if self.window_log[difficulty][start_time]['reached_end']:
                            print(f'Window {start_time} has been handled')
                            start_time += WINDOW_SIZE
                            continue
                        else:
                            skip = self.window_log[difficulty][start_time]['processed']
                            print(f'Window {start_time} has been partially handled ({skip} already processed)')

                #Construct query variable object
                query_vars = AghsMatchesVars(
                    createdAfterDateTime=start_time,
                    createdBeforeDateTime=start_time + WINDOW_SIZE,
                    difficulty=difficulty,
                    take=100,
                    skip=skip
                )
                self.processing_queue.append(query_vars)

                start_time += WINDOW_SIZE

    def process_queue(self, cutoff: int = None):

        ctr = 0
        while len(self.processing_queue) > 0:
            timer_start = time.time()
            query_vars = self.processing_queue.popleft()
            print(f'Window {ctr}: {query_vars.difficulty} - {query_vars.createdAfterDateTime} to {query_vars.createdBeforeDateTime}, ', end = '')
            matches, next_query = self.aghs_matches_handler.make_query(query_vars)
            if next_query:
                self.processing_queue.append(next_query)
            timer_end = time.time()
            print(f'Processed {len(matches)} matches in {timer_end - timer_start:.2f} seconds')
            self.save_matches(matches)
            ctr += 1
            if cutoff and ctr >= cutoff:
                break

    def save_matches(self, matches: list):
        timer_start = time.time()
        if len(matches) > 0:
            self.sql_writer.write_to_csv(matches)
            self.sql_writer.write_to_sql()
        timer_end = time.time()
        print(f'Saved {len(matches)} matches in {timer_end - timer_start:.2f} seconds')