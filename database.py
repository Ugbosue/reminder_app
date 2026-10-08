import sqlite3


def init_db():
	"""Initialize the SQLite database and create the contacts table."""
	conn = sqlite3.connect("contacts.db")
	try:
		cursor = conn.cursor()
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS contacts (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT NOT NULL,
				relation TEXT NOT NULL,
				special_day TEXT NOT NULL,
				occasion TEXT NOT NULL,
				phone TEXT NOT NULL,
				delivery_pref TEXT NOT NULL
			)
		""")

		cursor.execute("SELECT COUNT(*) FROM contacts")
		if cursor.fetchone()[0] == 0:
			sample_contacts = [
				("Martha", "wife", "10-06", "Birthday", "+447359230965", "WhatsApp"),
				("Isaac", "Best Friend", "10-06", "Marriage Anniversary", "+447359230962", "SMS"),
			]
			cursor.executemany("""
				INSERT INTO contacts (name, relation, special_day, occasion, phone, delivery_pref)
				VALUES (?, ?, ?, ?, ?, ?)
			""", sample_contacts)
			conn.commit()
			print("✅ Database initialized and sample contacts inserted!")
		else:
			print("ℹ️ Database already exists and contains records.")
	finally:
		conn.close()


if __name__ == "__main__":
	init_db()
