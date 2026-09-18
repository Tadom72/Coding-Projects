"""Create and seed the flyonwheels SQLite database."""

import hashlib
import sqlite3
from datetime import date, timedelta
from pathlib import Path


DB_PATH = Path(__file__).with_name("flyonwheels.db")


def drop_existing_schema(cursor: sqlite3.Cursor) -> None:
	"""Remove any existing tables or compatibility views before rebuilding."""
	cursor.executescript(
		"""
		DROP VIEW IF EXISTS ticket;
		DROP VIEW IF EXISTS run;
		DROP VIEW IF EXISTS bus;
		DROP VIEW IF EXISTS service;
		DROP VIEW IF EXISTS user;

		DROP TABLE IF EXISTS tickets;
		DROP TABLE IF EXISTS runs;
		DROP TABLE IF EXISTS physical_buses;
		DROP TABLE IF EXISTS bus_models;
		DROP TABLE IF EXISTS services;
		DROP TABLE IF EXISTS users;
		"""
	)


def create_compatibility_views(cursor: sqlite3.Cursor) -> None:
	"""Expose singular table names expected by the tests."""
	cursor.executescript(
		"""
		CREATE VIEW user AS
		SELECT id, username, password, admin
		FROM users;

		CREATE VIEW service AS
		SELECT id, name
		FROM services;

		CREATE VIEW bus AS
		SELECT id, bus_model_id, service_id, schedule_type
		FROM physical_buses;

		CREATE VIEW run AS
		SELECT id, service_id, physical_bus_id, date
		FROM runs;

		CREATE VIEW ticket AS
		SELECT id, user_id, run_id, number
		FROM tickets;
		"""
	)


def hash_password(raw_password: str) -> str:
	"""Return a SHA-256 hex digest for the provided password."""
	return hashlib.sha256(raw_password.encode("utf-8")).hexdigest()


def create_schema(cursor: sqlite3.Cursor) -> None:
	"""Create database tables with required relationships."""
	cursor.executescript(
		"""
		PRAGMA foreign_keys = ON;

		CREATE TABLE users (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			username TEXT NOT NULL UNIQUE,
			password TEXT NOT NULL,
			admin BOOLEAN NOT NULL
		);

		CREATE TABLE services (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT NOT NULL UNIQUE
		);

		CREATE TABLE bus_models (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT NOT NULL UNIQUE,
			seats INTEGER NOT NULL
		);

		CREATE TABLE physical_buses (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			bus_model_id INTEGER NOT NULL,
			service_id INTEGER NOT NULL,
			schedule_type TEXT NOT NULL CHECK (schedule_type IN ('weekend', 'workday')),
			FOREIGN KEY (bus_model_id) REFERENCES bus_models(id),
			FOREIGN KEY (service_id) REFERENCES services(id)
		);

		CREATE TABLE runs (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			service_id INTEGER NOT NULL,
			physical_bus_id INTEGER NOT NULL,
			date TEXT NOT NULL,
			FOREIGN KEY (service_id) REFERENCES services(id),
			FOREIGN KEY (physical_bus_id) REFERENCES physical_buses(id)
		);

		CREATE TABLE tickets (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			user_id INTEGER NOT NULL,
			run_id INTEGER NOT NULL,
			number INTEGER NOT NULL,
			FOREIGN KEY (user_id) REFERENCES users(id),
			FOREIGN KEY (run_id) REFERENCES runs(id)
		);
		"""
	)


def seed_data(cursor: sqlite3.Cursor) -> None:
	"""Insert the required records into all tables."""
	cursor.execute(
		"INSERT INTO users (username, password, admin) VALUES (?, ?, ?)",
		("Bob", hash_password("pqr123#!"), True),
	)
	user_id = cursor.lastrowid

	service_names = [
		"Dublin to Kilkenny, 7pm",
		"Dublin to Letterkenny, 8am",
		"Dublin to Wicklow, 6pm",
	]
	service_ids = {}
	for service_name in service_names:
		cursor.execute("INSERT INTO services (name) VALUES (?)", (service_name,))
		service_ids[service_name] = cursor.lastrowid

	cursor.execute("INSERT INTO bus_models (name, seats) VALUES (?, ?)", ("A", 30))
	model_a_id = cursor.lastrowid
	cursor.execute("INSERT INTO bus_models (name, seats) VALUES (?, ?)", ("B", 50))
	model_b_id = cursor.lastrowid

	buses_by_service = {}
	for service_name, service_id in service_ids.items():
		cursor.execute(
			"""
			INSERT INTO physical_buses (bus_model_id, service_id, schedule_type)
			VALUES (?, ?, ?)
			""",
			(model_a_id, service_id, "weekend"),
		)
		weekend_bus_id = cursor.lastrowid

		cursor.execute(
			"""
			INSERT INTO physical_buses (bus_model_id, service_id, schedule_type)
			VALUES (?, ?, ?)
			""",
			(model_b_id, service_id, "workday"),
		)
		workday_bus_id = cursor.lastrowid

		buses_by_service[service_name] = {
			"weekend": weekend_bus_id,
			"workday": workday_bus_id,
		}

	today = date.today()
	tomorrow = today + timedelta(days=1)
	letterkenny_run_for_tomorrow = None

	for day_offset in range(7):
		run_day = today + timedelta(days=day_offset)
		run_date = run_day.strftime("%Y-%m-%d")
		schedule_key = "weekend" if run_day.weekday() >= 5 else "workday"

		for service_name, service_id in service_ids.items():
			assigned_bus_id = buses_by_service[service_name][schedule_key]
			cursor.execute(
				"""
				INSERT INTO runs (service_id, physical_bus_id, date)
				VALUES (?, ?, ?)
				""",
				(service_id, assigned_bus_id, run_date),
			)

			if (
				service_name == "Dublin to Letterkenny, 8am"
				and run_day == tomorrow
			):
				letterkenny_run_for_tomorrow = cursor.lastrowid

	if letterkenny_run_for_tomorrow is None:
		raise RuntimeError("Could not find tomorrow's Letterkenny run for ticket creation.")

	cursor.execute(
		"INSERT INTO tickets (user_id, run_id, number) VALUES (?, ?, ?)",
		(user_id, letterkenny_run_for_tomorrow, 1),
	)


def create_database() -> None:
	"""Create a fresh flyonwheels.db database in the current folder."""
	with sqlite3.connect(DB_PATH) as connection:
		cursor = connection.cursor()
		drop_existing_schema(cursor)
		create_schema(cursor)
		seed_data(cursor)
		create_compatibility_views(cursor)
		connection.commit()

	print(f"Created database at: {DB_PATH}")


def main() -> None:
	"""Create a fresh flyonwheels.db database in the current folder."""
	create_database()


if __name__ == "__main__":
	main()