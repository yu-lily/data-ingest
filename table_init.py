from sql_client import SQLClient

class TableInitializer(SQLClient):

    def __init__(self):
        super().__init__()
    
    def initialize_tables(self, destroy_existing_tables: bool = False, schema_fname: str = "./schemas/aghs_schema.sql"):
        if destroy_existing_tables:
            # #Destroy existing tables
            print("Dropping tables")
            self.cur.execute("""DROP TABLE IF EXISTS matches CASCADE;""")
            self.cur.execute("""DROP TABLE IF EXISTS players CASCADE;""")
            self.cur.execute("""DROP TABLE IF EXISTS playerDepthList CASCADE;""")
            self.cur.execute("""DROP TABLE IF EXISTS playerBlessings CASCADE;""")
            self.cur.execute("""DROP TABLE IF EXISTS depthList CASCADE;""")
            self.cur.execute("""DROP TABLE IF EXISTS ascenionAbilities CASCADE;""")
            self.cur.execute("""DROP TABLE IF EXISTS abilityConstants CASCADE;""")
            self.conn.commit()

        #Get all tables
        self.cur.execute("""SELECT table_name
        FROM information_schema.tables
        WHERE table_schema='public'
        AND table_type='BASE TABLE';""")

        tables = self.cur.fetchall()
        print(f'Existing tables: {tables}')

        #Create tables
        if ('matches',) not in tables:
            
            print("Creating tables")
            self.cur.execute(open(schema_fname, "r").read())
            self.conn.commit()