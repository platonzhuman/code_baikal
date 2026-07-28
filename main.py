import os
import re
import sys

import psycopg2
from dotenv import load_dotenv
from psycopg2 import Error as PgError


def load_db_config():
    load_dotenv()
    cfg = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432"),
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
    }
    # без этих полей дальше смысла нет
    miss = [k for k, v in cfg.items() if not v]
    if miss:
        print("Не хватает переменных в .env:", ", ".join(miss))
        print("Скопируй .env.example -> .env и заполни")
        sys.exit(1)
    return cfg


def is_select(sql):
    clean = sql.strip().rstrip(";").strip()
    if not clean:
        return False
    # несколько запросов через ; — сразу нет
    if ";" in clean:
        return False
    return bool(re.match(r"(?is)^\s*(with\b.+\bselect\b|select\b)", clean))


def ensure_limit(sql, limit=5):
    clean = sql.strip().rstrip(";").strip()
    if re.search(r"(?i)\blimit\s+\d+", clean):
        return clean
    return f"{clean} LIMIT {limit}"


def print_table(columns, rows):
    if not columns:
        print("(пусто)")
        return

    data = []
    for row in rows:
        data.append(["NULL" if v is None else str(v) for v in row])

    widths = [len(c) for c in columns]
    for row in data:
        for i, cell in enumerate(row):
            if len(cell) > widths[i]:
                widths[i] = len(cell)

    def line(vals):
        return " | ".join(str(v).ljust(widths[i]) for i, v in enumerate(vals))

    print(line(columns))
    print("-+-".join("-" * w for w in widths))

    if not data:
        print("(нет строк)")
        return

    for row in data:
        print(line(row))


def run_query(conn, sql):
    cur = conn.cursor()
    try:
        cur.execute(sql)
        if cur.description is None:
            print("запрос ок, но строк нет")
            return
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
        print_table(cols, rows)
        print(f"\nстрок: {len(rows)}")
    finally:
        cur.close()


def main():
    cfg = load_db_config()

    try:
        sql = input("Введите SQL-запрос:\n").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nвыход")
        return

    if not sql:
        print("пустой запрос")
        return

    if not is_select(sql):
        print("Ошибка: разрешены только SELECT-запросы")
        return

    final_sql = ensure_limit(sql)
    if final_sql != sql.strip().rstrip(";").strip():
        print("(добавил LIMIT) ->", final_sql)

    try:
        conn = psycopg2.connect(**cfg)
    except PgError as e:
        print("не подключился к БД:", e)
        return

    try:
        run_query(conn, final_sql)
    except PgError as e:
        print("ошибка SQL:", e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
