import os
import clickhouse_connect
from dotenv import load_dotenv

import urllib3
import requests
import requests.adapters

load_dotenv()

CLICKHOUSE_HOST = os.environ.get("CLICKHOUSE_HOST", "localhost")
CLICKHOUSE_HTTP_PORT = int(os.environ.get("CLICKHOUSE_HTTP_PORT", 8123))
CLICKHOUSE_USER = os.environ.get("CLICKHOUSE_USER")
CLICKHOUSE_PASSWORD = os.environ.get("CLICKHOUSE_PASSWORD")
CLICKHOUSE_RAW_TABLE = "raw_api_responses"
DATA_URL = "http://api.open-notify.org/astros.json"


http_session = requests.Session()
retries_atapter = requests.adapters.HTTPAdapter(
    max_retries=urllib3.Retry(total=5, status_forcelist=[429, 500, 502, 503, 504])
)
http_session.mount("http://", retries_atapter)


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
            id UInt8,
            raw_json JSON
        )
        ENGINE = ReplacingMergeTree
        ORDER BY id
        """
    )


def request() -> requests.Response:
    response = http_session.get(DATA_URL, timeout=30)
    response.raise_for_status()
    return response


def insert_raw(_id: int, data: dict) -> None:
    ensure_raw_table()
    client.insert(
        CLICKHOUSE_RAW_TABLE,
        [[_id, data]],
        column_names=["id", "raw_json"],
    )


if __name__ == "__main__":
    response = request()
    data = response.json()
    for i, row in enumerate(data["people"]):
        insert_raw(i, row)
    client.command(f"OPTIMIZE TABLE {CLICKHOUSE_RAW_TABLE} FINAL;")
