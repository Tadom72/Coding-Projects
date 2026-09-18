"""User model matching the users table in flyonwheels.db."""

import hashlib
import sqlite3
from dataclasses import dataclass
from typing import Any, Mapping


def hash_password(raw_password: str) -> str:
	"""Return a SHA-256 hash for a plaintext password."""
	return hashlib.sha256(raw_password.encode("utf-8")).hexdigest()


def login(connection: sqlite3.Connection) -> "User | None":
	"""Authenticate a user by username and password."""
	username = input("Username: ").strip()
	password = input("Password: ").strip()
	password_hash = hash_password(password)

	cursor = connection.cursor()
	cursor.execute(
		"""
		SELECT id, username, password, admin
		FROM users
		WHERE username = ? AND password = ?
		""",
		(username, password_hash),
	)
	row = cursor.fetchone()

	if row is None:
		print("Login failed: invalid username or password.")
		return None

	user = User.from_row(row)
	print(f"Welcome back, {user.username}!")
	return user


def create_user(connection: sqlite3.Connection) -> None:
	"""Create a new non-admin user account."""
	username = input("Choose a username: ").strip()
	if not username:
		print("Username cannot be empty.")
		return

	password = input("Choose a password: ").strip()
	if not password:
		print("Password cannot be empty.")
		return

	cursor = connection.cursor()
	cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
	if cursor.fetchone() is not None:
		print("That username already exists.")
		return

	password_hash = hash_password(password)
	cursor.execute(
		"INSERT INTO users (username, password, admin) VALUES (?, ?, ?)",
		(username, password_hash, False),
	)
	connection.commit()
	print(f"Account created for '{username}'.")


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


def view_user_tickets(connection: sqlite3.Connection, user: "User") -> None:
	"""Display all tickets owned by the current user."""
	cursor = connection.cursor()
	cursor.execute(
		"""
		SELECT
			tickets.id,
			tickets.number,
			runs.date,
			services.name AS service_name
		FROM tickets
		JOIN runs ON runs.id = tickets.run_id
		JOIN services ON services.id = runs.service_id
		WHERE tickets.user_id = ?
		ORDER BY runs.date, tickets.id
		""",
		(user.id,),
	)
	rows = cursor.fetchall()
	print_table(["ticket_id", "number", "date", "service"], [tuple(row) for row in rows])


@dataclass
class User:
	"""Represents one row from the users table."""

	id: int
	username: str
	password: str
	admin: bool

	def get_id(self) -> int:
		"""Return the user id."""
		return self.id

	def set_id(self, id_value: int) -> None:
		"""Set the user id."""
		self.id = id_value

	def get_username(self) -> str:
		"""Return the username."""
		return self.username

	def set_username(self, username: str) -> None:
		"""Set the username."""
		self.username = username

	def get_password(self) -> str:
		"""Return the password hash."""
		return self.password

	def set_password(self, password: str) -> None:
		"""Set the password hash."""
		self.password = password

	def get_admin(self) -> bool:
		"""Return whether this user has admin privileges."""
		return self.admin

	def set_admin(self, admin: bool) -> None:
		"""Set whether this user has admin privileges."""
		self.admin = admin

	@classmethod
	def from_row(cls, row: Mapping[str, Any]) -> "User":
		"""Create a User from a dict-like SQLite row."""
		return cls(
			id=int(row["id"]),
			username=str(row["username"]),
			password=str(row["password"]),
			admin=bool(row["admin"]),
		)
