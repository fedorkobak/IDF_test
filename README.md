# IDF test

The test task from IFD technology.

Check:

- [The clickhouse configuration in](docker-compose.yml#L2-10).
- Python script for loading information and publishing to DB [`load_data.py`](src/load_data.py).
- The database initialisation:
    - [Deduplication strategy](src/sql_scripts/database.sql#L13-14).
    - [Materialized view for json parsing](src/sql_scripts/database.sql#L16-22).
- [DBT models](IDF_dbt/models).

## Deploy

For example use `.env`:

```bash
CLIKCHOUSE_HOST=localhost
CLICKHOUSE_USER=user
CLICKHOUSE_PASSWORD=password
CLICKHOUSE_HTTP_PORT=8123
```

Start the solution:

`docker compose up -d`

After a while check:

```bash
docker exec -it idf_test-click-1 bash
root@5e12ae8bef62:/# clickhouse-client

...

5e12ae8bef62 :) SHOW TABLES;

Query id: d44500b2-21d9-42f6-b46e-4424d04babf7

   ┌─name────────────────┐
1. │ astronauts_by_craft │
2. │ people              │
3. │ people_mv           │
4. │ raw_api_responses   │
5. │ stg_people          │
   └─────────────────────┘

5 rows in set. Elapsed: 0.003 sec. 

5e12ae8bef62 :) SELECT * FROM astronauts_by_craft;

SELECT *
FROM astronauts_by_craft

Query id: bd25fe8d-d68a-4153-8898-6021bd238d91

   ┌─craft────┬─astronaut_count─┬─astronaut_names───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┬──snapshot_loaded_at─┐
1. │ ISS      │               9 │ ['Matthew Dominick','Michael Barratt','Oleg Kononenko','Sunita Williams','Alexander Grebenkin','Jeanette Epps','Butch Wilmore','Tracy Caldwell Dyson','Nikolai Chub'] │ 2026-03-14 11:44:32 │
2. │ Tiangong │               3 │ ['Ye Guangfu','Li Cong','Li Guangsu']                                                                                                                                 │ 2026-03-14 11:44:33 │
   └──────────┴─────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴─────────────────────┘

2 rows in set. Elapsed: 0.004 sec. 

```
