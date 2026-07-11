import os
import sys
import time

import psycopg2


def main() -> int:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL no esta configurado.", flush=True)
        return 1

    attempts = int(os.environ.get("DB_WAIT_ATTEMPTS", "60"))
    delay = float(os.environ.get("DB_WAIT_DELAY_SECONDS", "2"))

    for attempt in range(1, attempts + 1):
        try:
            connection = psycopg2.connect(database_url)
            connection.close()
            print("Base de datos disponible.", flush=True)
            return 0
        except psycopg2.OperationalError as exc:
            print(
                f"Esperando base de datos ({attempt}/{attempts}): {exc}",
                flush=True,
            )
            time.sleep(delay)

    print("La base de datos no estuvo disponible a tiempo.", flush=True)
    return 1


if __name__ == "__main__":
    sys.exit(main())
