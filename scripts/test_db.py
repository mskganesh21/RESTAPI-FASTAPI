import asyncio

import asyncpg


async def main() -> None:
    base = dict(user="postgres", password="root", host="localhost", port=5432)

    print("1) Testing login to default 'postgres' database...")
    try:
        conn = await asyncpg.connect(database="postgres", **base)
        print("   OK - password and server are fine")
        rows = await conn.fetch(
            "SELECT datname FROM pg_database WHERE datname = 'notescrud'"
        )
        if rows:
            print("   OK - database 'notescrud' exists")
        else:
            print("   MISSING - database 'notescrud' does not exist")
            print("   Fix: CREATE DATABASE notescrud;")
        await conn.close()
    except Exception as exc:
        print(f"   FAILED: {type(exc).__name__}: {exc}")
        return

    print("2) Testing connection to 'notescrud' database...")
    try:
        conn = await asyncpg.connect(database="notescrud", **base)
        print("   OK - can connect to notescrud")
        await conn.close()
    except Exception as exc:
        print(f"   FAILED: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    asyncio.run(main())
