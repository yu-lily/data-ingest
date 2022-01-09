# data-ingest
Minimal ETL pipeline for loading data from the [STRATZ GraphQL API](https://stratz.com/api) into a local Postgres server.

`queries/` stores GraphQL queries used to request data.
`schemas/` stores schemas to initialize the local database.

So far, mostly just queries related to Aghanim's Labyrinth are implemented.
