
import sqlite3

# Create database connection
def create_connection():
    connection = sqlite3.connect("tickets.db")
    connection.row_factory = sqlite3.Row
    return connection


# Create tickets table and migrate existing database
def create_table():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT,
            severity TEXT,
            priority TEXT,
            confidence REAL,
            status TEXT DEFAULT 'Open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Add department column to existing databases if missing
    cursor.execute("PRAGMA table_info(tickets)")
    columns = [column["name"] for column in cursor.fetchall()]

    if "department" not in columns:
        cursor.execute(
            "ALTER TABLE tickets ADD COLUMN department TEXT"
        )
        print("Department column added successfully!")

    connection.commit()
    connection.close()

    print("Tickets table created successfully!")


# Save a new ticket
def save_ticket(employee_name, email, title, description,
                category, severity, priority,
                confidence=0.0, department=""):

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO tickets (
            employee_name, email, department, title,
            description, category, severity, priority, confidence
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        employee_name, email, department, title,
        description, category, severity, priority, confidence
    ))

    connection.commit()
    ticket_id = cursor.lastrowid
    connection.close()

    print("Ticket saved successfully! Ticket ID:", ticket_id)

    return ticket_id


# Retrieve all tickets
def get_all_tickets():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM tickets
        ORDER BY created_at DESC, ticket_id DESC
    """)

    tickets = [dict(row) for row in cursor.fetchall()]

    connection.close()
    return tickets


# Retrieve one ticket using its ID
def get_ticket_by_id(ticket_id):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM tickets
        WHERE ticket_id = ?
    """, (ticket_id,))

    ticket = cursor.fetchone()

    connection.close()

    return dict(ticket) if ticket else None


# Initialize database when executed directly
if __name__ == "__main__":
    create_table()

    tickets = get_all_tickets()

    print("\nTOTAL TICKETS:", len(tickets))
    print("Database retrieval is working!")
