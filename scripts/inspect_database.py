"""Show fictional repair rows locally; do not publish output with real customer data."""

import os
import sqlite3
from pathlib import Path


def main():
    path = Path(os.getenv("DATABASE_PATH", "data/repairs.db"))
    if not path.is_file():
        print(f"Database not found: {path}. Run the API and create a request first.")
        raise SystemExit(1)
    with sqlite3.connect(path) as connection:
        for row in connection.execute(
            "SELECT id, customer_name, bicycle_type, service_type, status, created_at "
            "FROM repair_requests ORDER BY id DESC LIMIT 20"
        ):
            print(row)


if __name__ == "__main__":
    main()
