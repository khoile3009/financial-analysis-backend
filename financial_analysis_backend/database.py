DATASET_TABLE_CREATE_QUERY = """
CREATE TABLE IF NOT EXISTS datasets (
    ID              SERIAL PRIMARY KEY,
    SYMBOL          VARCHAR(100),
    INTERVAL        VARCHAR(10),
    START_TIMESTAMP TIMESTAMPTZ,
    END_TIMESTAMP   TIMESTAMPTZ
);
"""

TICKER_PRICE_TABLE_CREATE_QUERY = """
CREATE TABLE IF NOT EXISTS ticker_price (
    TIME                TIMESTAMPTZ NOT NULL,
    SYMBOL              VARCHAR(100),
    ADJUSTED_CLOSE      DOUBLE PRECISION NULL,
    CLOSE               DOUBLE PRECISION NULL,
    OPEN                DOUBLE PRECISION NULL,
    HIGH                DOUBLE PRECISION NULL,
    LOW                 DOUBLE PRECISION NULL,
    VOLUME              DOUBLE PRECISION NULL
)
"""


class Database:
    def __init__(self, conn):
        self.conn = conn

    def create_dataset_table(self):
        with self.conn.cursor() as cursor:
            cursor.execute(DATASET_TABLE_CREATE_QUERY)
