# Безопасный SQL Runner

Маленький скрипт: подключается к PostgreSQL, принимает SQL из консоли,
пропускает только SELECT, сам докидывает LIMIT 5 если его нет, и печатает
результат табличкой.

Без веб-сервера, без LLM — просто Python + PostgreSQL.

## Что умеет

- подключение к БД через `.env`
- только `SELECT` (и `WITH ... SELECT`)
- если нет `LIMIT` — добавляет `LIMIT 5`
- `DELETE` / `UPDATE` / прочее — отказ
- ошибки не роняют скрипт, просто пишутся в консоль

## Установка и запуск

```bash
git clone https://github.com/platonzhuman/code_baikal.git
cd code_baikal

python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# заполни DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

python main.py
```

После запуска:

```
Введите SQL-запрос:
```

Пример:

```
SELECT * FROM students
```

Если LIMIT нет — скрипт добавит его сам.

Если ввести:

```
DELETE FROM students
```

получишь:

```
Ошибка: разрешены только SELECT-запросы
```

## Требования

- Python 3.10+
- PostgreSQL
- зависимости из `requirements.txt` (`psycopg2-binary`, `python-dotenv`)

## Структура

```
main.py           — сам раннер
requirements.txt  — зависимости
.env.example      — пример конфига БД
README.md         — вот это
```

---

Автор: NoName ^_^  
platonzhuman@bk.ru
