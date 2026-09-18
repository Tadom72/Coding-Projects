"""Ticket model matching the tickets table in flyonwheels.db."""

from datetime import date
import sqlite3
from dataclasses import dataclass
from typing import Any, Mapping, TYPE_CHECKING

from bus_run import view_future_bus_runs

if TYPE_CHECKING:
	from user import User


def get_run_capacity(connection: sqlite3.Connection, run_id: int) -> int | None:
	"""Return total seat capacity for a run based on its assigned bus model."""
	cursor = connection.cursor()
	cursor.execute(
		"""
		SELECT bus_models.seats
		FROM runs
		JOIN physical_buses ON physical_buses.id = runs.physical_bus_id
		JOIN bus_models ON bus_models.id = physical_buses.bus_model_id
		WHERE runs.id = ?
		""",
		(run_id,),
	)
	row = cursor.fetchone()
	if row is None:
		return None
	return int(row["seats"])


def get_tickets_sold_for_run(connection: sqlite3.Connection, run_id: int) -> int:
	"""Return the total number of tickets already sold for a run."""
	cursor = connection.cursor()
	cursor.execute(
		"""
		SELECT COALESCE(SUM(number), 0) AS sold_count
		FROM tickets
		WHERE run_id = ?
		""",
		(run_id,),
	)
	row = cursor.fetchone()
	return int(row["sold_count"])


def get_available_seats_for_run(connection: sqlite3.Connection, run_id: int) -> int | None:
	"""Return remaining seats for a run."""
	capacity = get_run_capacity(connection, run_id)
	if capacity is None:
		return None
	sold = get_tickets_sold_for_run(connection, run_id)
	return max(0, capacity - sold)


def decrease_available_seats(available_seats: int, tickets_sold: int) -> int:
	"""Return updated remaining seats after selling tickets."""
	return max(0, available_seats - tickets_sold)


def buy_tickets(connection: sqlite3.Connection, user: "User") -> None:
	"""Buy tickets for a future run."""
	today = date.today().isoformat()
	runs = view_future_bus_runs(connection)
	if not runs:
		print("No future runs are available right now.")
		return

	print("Select a run by its list number (1 = first row).")
	run_selection_text = input("Enter run number: ").strip()
	quantity_text = input("How many tickets would you like to buy? ").strip()

	if not run_selection_text.isdigit() or not quantity_text.isdigit():
		print("Run number and ticket quantity must be numbers.")
		return

	run_selection = int(run_selection_text)
	if run_selection < 1 or run_selection > len(runs):
		print("Invalid run number selected.")
		return

	run_id = int(runs[run_selection - 1][0])
	quantity = int(quantity_text)
	if quantity <= 0:
		print("Ticket quantity must be greater than zero.")
		return

	cursor = connection.cursor()
	cursor.execute(
		"""
		SELECT id
		FROM runs
		WHERE id = ? AND date >= ?
		""",
		(run_id, today),
	)
	if cursor.fetchone() is None:
		print("Invalid run number selected.")
		return

	available_seats = get_available_seats_for_run(connection, run_id)
	if available_seats is None:
		print("Could not determine seat capacity for this run.")
		return

	if quantity > available_seats:
		print(
			f"Not enough available seats. Requested {quantity}, only {available_seats} left."
		)
		return

	confirmation = input("Press Enter to confirm booking, or type esc to cancel: ").strip().lower()
	if confirmation == "esc":
		print("Booking cancelled.")
		return

	cursor.execute(
		"INSERT INTO tickets (user_id, run_id, number) VALUES (?, ?, ?)",
		(user.id, run_id, quantity),
	)
	connection.commit()
	remaining_seats = decrease_available_seats(available_seats, quantity)
	print("Booking confirmed!")
	print(f"Seats remaining on this run: {remaining_seats}.")


@dataclass
class Ticket:
	"""Represents one row from the tickets table."""

	id: int
	user_id: int
	run_id: int
	number: int

	def get_id(self) -> int:
		"""Return the ticket id."""
		return self.id

	def set_id(self, id_value: int) -> None:
		"""Set the ticket id."""
		self.id = id_value

	def get_user_id(self) -> int:
		"""Return the user id linked to this ticket."""
		return self.user_id

	def set_user_id(self, user_id: int) -> None:
		"""Set the user id linked to this ticket."""
		self.user_id = user_id

	def get_run_id(self) -> int:
		"""Return the run id linked to this ticket."""
		return self.run_id

	def set_run_id(self, run_id: int) -> None:
		"""Set the run id linked to this ticket."""
		self.run_id = run_id

	def get_number(self) -> int:
		"""Return the ticket count for the run."""
		return self.number

	def set_number(self, number: int) -> None:
		"""Set the ticket count for the run."""
		self.number = number

	@classmethod
	def from_row(cls, row: Mapping[str, Any]) -> "Ticket":
		"""Create a Ticket from a dict-like SQLite row."""
		return cls(
			id=int(row["id"]),
			user_id=int(row["user_id"]),
			run_id=int(row["run_id"]),
			number=int(row["number"]),
		)
