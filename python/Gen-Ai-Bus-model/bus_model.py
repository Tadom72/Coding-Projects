"""Bus model matching the bus_models table in flyonwheels.db."""

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class BusModel:
	"""Represents one row from the bus_models table."""

	id: int
	name: str
	seats: int

	def get_id(self) -> int:
		"""Return the bus model id."""
		return self.id

	def set_id(self, id_value: int) -> None:
		"""Set the bus model id."""
		self.id = id_value

	def get_name(self) -> str:
		"""Return the bus model name."""
		return self.name

	def set_name(self, name: str) -> None:
		"""Set the bus model name."""
		self.name = name

	def get_seats(self) -> int:
		"""Return the number of seats."""
		return self.seats

	def set_seats(self, seats: int) -> None:
		"""Set the number of seats."""
		self.seats = seats

	@classmethod
	def from_row(cls, row: Mapping[str, Any]) -> "BusModel":
		"""Create a BusModel from a dict-like SQLite row."""
		return cls(
			id=int(row["id"]),
			name=str(row["name"]),
			seats=int(row["seats"]),
		)
