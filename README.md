# data-ingest
Minimal ETL pipeline for loading data from the [STRATZ GraphQL API](https://stratz.com/api) into a local Postgres server. So far, mostly just queries related to Aghanim's Labyrinth are implemented.

`queries/` stores GraphQL queries used to request data.

`schemas/` stores schemas to initialize the local database.

## Usage
- Create a venv if desired, and install dependencies
```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```
- Create a `.env` file to store your STRATZ API Key and database credentials:
```.env
STRATZ_APIKEY={YOUR_API_KEY}
POSTGRES_PASS={DB_PASS}
POSTGRES_PORT={PORT (5342 is the default)}
```

`main.py` currently defaults to Aghanim's Labyrinth matches.
```
python main.py {MAX_REQUESTS}
```
