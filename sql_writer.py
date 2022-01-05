from sql_client import SQLClient
import os
import numpy as np
import pandas as pd

class SQLWriter(SQLClient):
    def __init__(self):
        super().__init__()

        if not os.path.exists('./tmp'):
            os.mkdir('./tmp')

    def write_to_sql(self):
        tables = ['matches', 'players', 'playerdepthlist', 'playerblessings', 'depthlist', 'ascensionabilities']
        for table in tables:
            #Create temporary table with copy of schema
            self.cur.execute(f"""
                CREATE TEMP TABLE tmp_{table} 
                ON COMMIT DROP
                AS
                SELECT * 
                FROM {table}
                WITH NO DATA;
            """)

            self.cur.copy_from(open(f'./tmp/{table}.csv'), f"tmp_{table}", sep=',', null='NULL')

            #Insert data into table
            self.cur.execute(f"""
                INSERT INTO {table}
                SELECT * 
                FROM tmp_{table}
                ON CONFLICT DO NOTHING;
            """)

        self.conn.commit()


    def write_to_csv(self, matches: list):
        self.matches = matches
        #Handle matches
        def to_csv_wrapper(df, fpath):
            df.to_csv(fpath, index=False, float_format = '%.0f', header=False, na_rep='NULL')

        df = pd.DataFrame(self.matches)
        df = df.drop(['players', 'depthList'], axis=1)
        df['startDateTime'] = pd.to_datetime(df['startDateTime'], unit='s')
        df['endDateTime'] = pd.to_datetime(df['endDateTime'], unit='s')
        #Make bool lowercase if needed
        to_csv_wrapper(df, './tmp/matches.csv')
        del df

        player_dfs = []
        for match in self.matches:
            player_dfs.append(pd.DataFrame(match['players']))
        player_df = pd.concat(player_dfs) 
        player_df = player_df.drop(['depthList', 'blessings'], axis=1)

        for i in range(6):
            col = f'item{i}Id'
            player_df[col] = player_df[col].replace(['None', 'nan'], np.nan)
            
        player_df['neutral0Id'] = player_df['neutral0Id'].replace(['None', 'nan'], np.nan)
        player_df['neutralItemId'] = player_df['neutralItemId'].replace(['None', 'nan'], np.nan)

        to_csv_wrapper(player_df, './tmp/players.csv')
        del player_df

        player_depthlist_rows = []
        for match in self.matches:
            row = {}
            row['matchId'] = match['id']
            for player in match['players']:
                row['playerSlot'] = player['playerSlot']
                row['depth'] = 0
                row['steamAccountId'] = player['steamAccountId']
                if player['depthList']:
                    for depth_item in player['depthList']:
                        ser = pd.concat([pd.Series(row), pd.Series(depth_item)])
                        player_depthlist_rows.append(ser)
                        row['depth'] += 1

        player_depthlist_df = pd.concat(player_depthlist_rows, axis=1).T
        to_csv_wrapper(player_depthlist_df, './tmp/playerdepthlist.csv')
        del player_depthlist_df

        player_blessings_rows = []
        for match in self.matches:
            row = {}
            row['matchId'] = match['id']
            for player in match['players']:
                row['playerSlot'] = player['playerSlot']
                row['steamAccountId'] = player['steamAccountId']
                if player['blessings']:
                    for blessing in player['blessings']:
                        ser = pd.concat([pd.Series(row), pd.Series(blessing)])
                        player_blessings_rows.append(ser)

        player_blessings_df = pd.concat(player_blessings_rows, axis=1).T
        to_csv_wrapper(player_blessings_df, './tmp/playerblessings.csv')
        del player_blessings_df

        depthlist_rows = []
        for match in self.matches:
            row = {}
            row['matchId'] = match['id']
            row['depth'] = 0
            if match['depthList']:
                for depth in match['depthList']:
                    ser = pd.concat([pd.Series(row), pd.Series(depth)])
                    depthlist_rows.append(ser)
                    row['depth'] += 1

        depthlist_df = pd.concat(depthlist_rows, axis=1).T
        depthlist_df = depthlist_df.drop(['ascensionAbilities'], axis=1)
        to_csv_wrapper(depthlist_df, './tmp/depthlist.csv')
        del depthlist_df

        ascensionabilities_rows = []
        for match in self.matches:
            row = {}
            row['matchId'] = match['id']
            row['depth'] = 0
            if match['depthList']:
                for depth in match['depthList']:
                    if depth['ascensionAbilities']:
                        for ascensionability in depth['ascensionAbilities']:
                            ser = pd.concat([pd.Series(row), pd.Series(ascensionability)])
                            ascensionabilities_rows.append(ser)
                    row['depth'] += 1

        ascensionabilities_df = pd.concat(ascensionabilities_rows, axis=1).T
        to_csv_wrapper(ascensionabilities_df, './tmp/ascensionabilities.csv')
        del ascensionabilities_df