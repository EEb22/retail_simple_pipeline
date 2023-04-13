import os

from utils.db import DBConnection


def get_warehouse_creds() -> DBConnection:
    return DBConnection(
        db=os.getenv('WAREHOUSE_DB', ''),
        user=os.getenv('WAREHOUSE_USER', ''),
        password=os.getenv('WAREHOUSE_PASSWORD', ''),
        host=os.getenv('WAREHOUSE_HOST', ''),
        port=int(os.getenv('WAREHOUSE_PORT', 5432)),
    )
