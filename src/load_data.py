import os
from dotenv import load_dotenv
import requests
import clickhouse_connect

load_dotenv()

CLICKHOUSE_HOST = os.environ.get("CLICKHOUSE_HOST", "localhost")
CLICKHOUSE_HTTP_PORT = int(os.environ.get("CLICKHOUSE_HTTP_PORT", 8123))
CLICKHOUSE_USER= os.environ.get("CLICKHOUSE_USER")
CLICKHOUSE_PASSWORD = os.environ.get("CLICKHOUSE_PASSWORD")

if not (CLICKHOUSE_PASSWORD and CLICKHOUSE_USER):
    raise ValueError("Clickhouse credentials are not specified")


client = clickhouse_connect.get_client(
    host=CLICKHOUSE_HOST,
    port=CLICKHOUSE_HTTP_PORT,
    username=CLICKHOUSE_USER,
    password=CLICKHOUSE_PASSWORD
)

def request() -> requests.Response:
    return requests.get("http://api.open-notify.org/astros.json")

def insert_raw(data: list):
    pass

if __name__ == "__main__":
    pass
