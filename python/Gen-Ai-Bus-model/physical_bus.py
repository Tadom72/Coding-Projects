"""Physical bus model matching the physical_buses table in flyonwheels.db."""

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class PhysicalBus:
	"""Represents one row from the physical_buses table."""

	id: int
	bus_model_id: int
	service_id: int
	schedule_type: str

	def get_id(self) -> int:
		"""Return the physical bus id."""
		return self.id

	def set_id(self, id_value: int) -> None:
		"""Set the physical bus id."""
		self.id = id_value

	def get_bus_model_id(self) -> int:
		"""Return the bus model id."""
		return self.bus_model_id

	def set_bus_model_id(self, bus_model_id: int) -> None:
		"""Set the bus model id."""
		self.bus_model_id = bus_model_id

	def get_service_id(self) -> int:
		"""Return the service id."""
		return self.service_id

	def set_service_id(self, service_id: int) -> None:
		"""Set the service id."""
		self.service_id = service_id

	def get_schedule_type(self) -> str:
		"""Return the schedule type."""
		return self.schedule_type

	def set_schedule_type(self, schedule_type: str) -> None:
		"""Set the schedule type."""
		self.schedule_type = schedule_type

	@classmethod
	def from_row(cls, row: Mapping[str, Any]) -> "PhysicalBus":
		"""Create a PhysicalBus from a dict-like SQLite row."""
		return cls(
			id=int(row["id"]),
			bus_model_id=int(row["bus_model_id"]),
			service_id=int(row["service_id"]),
			schedule_type=str(row["schedule_type"]),
		)
