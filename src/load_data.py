import json
import os
from dotenv import load_dotenv
import requests
import clickhouse_connect

load_dotenv()

CLICKHOUSE_HOST = os.environ.get("CLICKHOUSE_HOST", "localhost")
CLICKHOUSE_HTTP_PORT = int(os.environ.get("CLICKHOUSE_HTTP_PORT", 8123))
CLICKHOUSE_USER = os.environ.get("CLICKHOUSE_USER")
CLICKHOUSE_PASSWORD = os.environ.get("CLICKHOUSE_PASSWORD")
CLICKHOUSE_RAW_TABLE = "raw_api_responses"
DATA_URL = "http://api.open-notify.org/astros.json"


if not (CLICKHOUSE_PASSWORD and CLICKHOUSE_USER):
    raise ValueError("Clickhouse credentials are not specified")

client = clickhouse_connect.get_client(
    host=CLICKHOUSE_HOST,
    port=CLICKHOUSE_HTTP_PORT,
    username=CLICKHOUSE_USER,
    password=CLICKHOUSE_PASSWORD,
)


def ensure_raw_table() -> None:
    client.command(
        f"""
        CREATE TABLE IF NOT EXISTS {CLICKHOUSE_RAW_TABLE} (
            raw_json String
        )
        ENGINE = MergeTree
        ORDER BY tuple()
        """
    )


def request() -> requests.Response:
    response = requests.get(DATA_URL, timeout=30)
    response.raise_for_status()
    return response


def insert_raw(data: dict) -> None:
    ensure_raw_table()
    client.insert(
        CLICKHOUSE_RAW_TABLE,
        [[str(data)]],
        column_names=["raw_json"],
    )


if __name__ == "__main__":
    response = request()
    data = response.json()
    for row in data["people"]:
        insert_raw(row)
