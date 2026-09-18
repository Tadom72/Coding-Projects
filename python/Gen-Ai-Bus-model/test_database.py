"""Open flyonwheels.db and print all tables with their rows."""

import sqlite3
from pathlib import Path


def print_rows_as_table(table_name: str, rows: list[sqlite3.Row]) -> None:
	"""Print a list of sqlite rows as a text table with headers."""
	print(f"\n=== {table_name} ===")

	if not rows:
		print("(no rows)")
		return

	headers = list(rows[0].keys())
	string_rows = [
		[str(row[header]) if row[header] is not None else "NULL" for header in headers]
		for row in rows
	]
	column_widths = [
		max(len(header), *(len(row[index]) for row in string_rows))
		for index, header in enumerate(headers)
	]

	header_line = " | ".join(
		header.ljust(column_widths[index])
		for index, header in enumerate(headers)
	)
	separator_line = "-+-".join("-" * width for width in column_widths)

	print(header_line)
	print(separator_line)

	for row in string_rows:
		print(
			" | ".join(
				value.ljust(column_widths[index])
				for index, value in enumerate(row)
			)
		)


def dump_database(db_path: Path) -> None:
	"""Print every user table and all data rows in each table."""
	if not db_path.exists():
		raise FileNotFoundError(f"Database not found: {db_path}")

	with sqlite3.connect(db_path) as connection:
		connection.row_factory = sqlite3.Row
		cursor = connection.cursor()

		cursor.execute(
			"""
			SELECT name
			FROM sqlite_master
			WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
			ORDER BY name
			"""
		)
		tables = [row["name"] for row in cursor.fetchall()]

		if not tables:
			print("No user tables found in the database.")
			return

		for table_name in tables:
			cursor.execute(f"SELECT * FROM {table_name}")
			rows = cursor.fetchall()
			print_rows_as_table(table_name, rows)


def main() -> None:
	"""Locate flyonwheels.db in the same folder and dump its contents."""
	database_file = Path(__file__).with_name("flyonwheels.db")
	dump_database(database_file)


if __name__ == "__main__":
	main()
