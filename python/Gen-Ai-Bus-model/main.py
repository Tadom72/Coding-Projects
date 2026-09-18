"""Command-line menu for logging in or creating users in flyonwheels.db."""

import sqlite3
from pathlib import Path

from user import User, create_user, login, view_user_tickets
from bus_service import view_existing_services, create_new_service
from bus_run import view_future_bus_runs
from ticket import buy_tickets


def admin_menu(connection: sqlite3.Connection, admin_user: User) -> None:
	"""Show the admin menu until logout."""
	while True:
		print(f"\nAdmin Menu - {admin_user.username}")
		print("1. View existing services")
		print("2. Create new service")
		print("3. Log out")

		choice = input("Select an option (1-3): ").strip()
		if choice == "1":
			view_existing_services(connection)
		elif choice == "2":
			create_new_service(connection)
		elif choice == "3":
			print("Logged out.")
			break
		else:
			print("Invalid option. Please choose 1, 2, or 3.")


def user_menu(connection: sqlite3.Connection, current_user: User) -> None:
	"""Show the user menu until logout."""
	while True:
		print(f"\nUser Menu - {current_user.username}")
		print("1. View future bus runs")
		print("2. Buy tickets")
		print("3. View your tickets")
		print("4. Log out")

		choice = input("Select an option (1-4): ").strip()
		if choice == "1":
			view_future_bus_runs(connection)
		elif choice == "2":
			buy_tickets(connection, current_user)
		elif choice == "3":
			view_user_tickets(connection, current_user)
		elif choice == "4":
			print("Logged out.")
			break
		else:
			print("Invalid option. Please choose 1, 2, 3, or 4.")


def main() -> None:
	"""Open flyonwheels.db and launch the user menu."""
	database_path = Path(__file__).with_name("flyonwheels.db")
	if not database_path.exists():
		raise FileNotFoundError(
			"Database file not found. Run create_database.py first."
		)

	with sqlite3.connect(database_path) as connection:
		connection.row_factory = sqlite3.Row
		print("=== Transport Booking System ===")
		while True:
			print("\nMain Menu")
			print("1. Log in")
			print("2. Create user")
			print("3. Exit")

			choice = input("Select an option (1-3): ").strip()

			if choice == "1":
				current_user = login(connection)
				if current_user is not None:
					if current_user.admin:
						admin_menu(connection, current_user)
					else:
						user_menu(connection, current_user)
			elif choice == "2":
				create_user(connection)
			elif choice == "3":
				print("Goodbye.")
				break
			else:
				print("Invalid option. Please choose 1, 2, or 3.")


if __name__ == "__main__":
	main()
