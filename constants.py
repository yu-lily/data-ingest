import json
from query_handler import QueryHandler


class AbilityConstantsHandler(QueryHandler):
    def __init__(self) -> None:
        super().__init__()

        #Load GraphQL query
        with open(f'queries/ability_constants.txt', 'r') as f:
            self.query = f.read()

    def make_query(self) -> tuple:
        r = super().make_query(variables={})

        query_result = json.loads(r)
        abilities = query_result['data']['constants']['customAbilities']
        
        return abilities, None