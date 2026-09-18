"""Bus service model matching the services table in flyonwheels.db."""

import sqlite3
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any, Mapping


@dataclass
class BusService:
	"""Represents one row from the services table."""

	id: int
	name: str

	def get_id(self) -> int:
		"""Return the service id."""
		return self.id

	def set_id(self, id_value: int) -> None:
		"""Set the service id."""
		self.id = id_value

	def get_name(self) -> str:
		"""Return the service name."""
		return self.name

	def set_name(self, name: str) -> None:
		"""Set the service name."""
		self.name = name

	@classmethod
	def from_row(cls, row: Mapping[str, Any]) -> "BusService":
		"""Create a BusService from a dict-like SQLite row."""
		return cls(
			id=int(row["id"]),
			name=str(row["name"]),
		)


def print_table(headers: list[str], rows: list[tuple]) -> None:
	"""Print rows in a simple aligned table format."""
	if not rows:
		print("(no rows)")
		return

	column_widths = []
	for index, header in enumerate(headers):
		cell_width = max(len(header), *(len(str(row[index])) for row in rows))
		column_widths.append(cell_width)

	header_line = " | ".join(
		header.ljust(column_widths[index]) for index, header in enumerate(headers)
	)
	separator_line = "-+-".join("-" * width for width in column_widths)

	print(header_line)
	print(separator_line)
	for row in rows:
		print(
			" | ".join(
				str(value).ljust(column_widths[index])
				for index, value in enumerate(row)
			)
		)


def view_existing_services(connection: sqlite3.Connection) -> None:
	"""Display all services in the database."""
	cursor = connection.cursor()
	cursor.execute("SELECT id, name FROM services ORDER BY id")
	rows = cursor.fetchall()
	print_table(["id", "name"], [tuple(row) for row in rows])


def create_new_service(connection: sqlite3.Connection) -> None:
	"""Create a new service entry."""
	service_name = input("Enter new service name: ").strip()
	if not service_name:
		print("Service name cannot be empty.")
		return

	cursor = connection.cursor()
	cursor.execute("SELECT 1 FROM services WHERE name = ?", (service_name,))
	if cursor.fetchone() is not None:
		print("That service already exists.")
		return

	cursor.execute("INSERT INTO services (name) VALUES (?)", (service_name,))
	service_id = cursor.lastrowid

	cursor.execute(
		"SELECT id FROM bus_models ORDER BY seats ASC, id ASC LIMIT 2"
	)
	bus_models = cursor.fetchall()
	if len(bus_models) < 2:
		raise RuntimeError("At least two bus models are required in the database.")

	weekend_model_id = bus_models[0]["id"]
	workday_model_id = bus_models[1]["id"]

	cursor.execute(
		"""
		INSERT INTO physical_buses (bus_model_id, service_id, schedule_type)
		VALUES (?, ?, ?)
		""",
		(weekend_model_id, service_id, "weekend"),
	)
	weekend_bus_id = cursor.lastrowid

	cursor.execute(
		"""
		INSERT INTO physical_buses (bus_model_id, service_id, schedule_type)
		VALUES (?, ?, ?)
		""",
		(workday_model_id, service_id, "workday"),
	)
	workday_bus_id = cursor.lastrowid

	today = date.today()
	for day_offset in range(7):
		run_day = today + timedelta(days=day_offset)
		run_date = run_day.strftime("%Y-%m-%d")
		schedule_type = "weekend" if run_day.weekday() >= 5 else "workday"
		assigned_bus_id = weekend_bus_id if schedule_type == "weekend" else workday_bus_id
		cursor.execute(
			"""
			INSERT INTO runs (service_id, physical_bus_id, date)
			VALUES (?, ?, ?)
			""",
			(service_id, assigned_bus_id, run_date),
		)
	connection.commit()
	print(f"Service '{service_name}' created.")
