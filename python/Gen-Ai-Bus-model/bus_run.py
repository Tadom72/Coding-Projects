"""Bus run model matching the runs table in flyonwheels.db."""

from datetime import date
import sqlite3
from dataclasses import dataclass
from typing import Any, Mapping


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


def view_future_bus_runs(connection: sqlite3.Connection) -> None:
	"""Display upcoming bus runs from today onward."""
	from ticket import get_available_seats_for_run

	today = date.today().isoformat()
	cursor = connection.cursor()
	cursor.execute(
		"""
		SELECT
			runs.id,
			runs.date,
			services.name AS service_name,
			physical_buses.schedule_type,
			bus_models.name AS bus_model,
			bus_models.seats
		FROM runs
		JOIN services ON services.id = runs.service_id
		JOIN physical_buses ON physical_buses.id = runs.physical_bus_id
		JOIN bus_models ON bus_models.id = physical_buses.bus_model_id
		WHERE runs.date >= ?
		ORDER BY runs.date, service_name, runs.id
		""",
		(today,),
	)
	runs = cursor.fetchall()
	rows = []
	for run in runs:
		available_seats = get_available_seats_for_run(connection, int(run["id"]))
		rows.append(
			(
				run["id"],
				run["date"],
				run["service_name"],
				run["schedule_type"],
				run["bus_model"],
				available_seats if available_seats is not None else "unknown",
			)
		)
	print_table(
		["run_id", "date", "service", "schedule", "bus_model", "seats_left"],
		rows,
	)
	return rows


@dataclass
class BusRun:
	"""Represents one row from the runs table."""

	id: int
	service_id: int
	physical_bus_id: int
	date: str

	def get_id(self) -> int:
		"""Return the run id."""
		return self.id

	def set_id(self, id_value: int) -> None:
		"""Set the run id."""
		self.id = id_value

	def get_service_id(self) -> int:
		"""Return the service id for this run."""
		return self.service_id

	def set_service_id(self, service_id: int) -> None:
		"""Set the service id for this run."""
		self.service_id = service_id

	def get_physical_bus_id(self) -> int:
		"""Return the assigned physical bus id."""
		return self.physical_bus_id

	def set_physical_bus_id(self, physical_bus_id: int) -> None:
		"""Set the assigned physical bus id."""
		self.physical_bus_id = physical_bus_id

	def get_date(self) -> str:
		"""Return the run date."""
		return self.date

	def set_date(self, run_date: str) -> None:
		"""Set the run date."""
		self.date = run_date

	@classmethod
	def from_row(cls, row: Mapping[str, Any]) -> "BusRun":
		"""Create a BusRun from a dict-like SQLite row."""
		return cls(
			id=int(row["id"]),
			service_id=int(row["service_id"]),
			physical_bus_id=int(row["physical_bus_id"]),
			date=str(row["date"]),
		)
