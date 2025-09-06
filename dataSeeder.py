import json
import pyodbc

# Database connection string
CONNECTION_STRING = (
    "Driver={SQL Server};"
    "Server=DESKTOP-7J4O389\\SQLEXPRESS;"
    "Database=CocoAttendance;"
    "Trusted_Connection=yes;"
)

def load_json(file_path):
    """Load the JSON data from the file."""
    with open(file_path, "r") as file:
        return json.load(file)

def seed_people_and_roles(data):
    """Insert people into the database and link their roles."""
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()

        # Combine participants and people into one list
        combined_people = data["participants"]

        for person in combined_people:
            # Common fields
            person_id = person["id"]
            name = person.get("name", "Unknown")
            email = person.get("email", f"{name.replace(' ', '').lower()}@example.com")
            role = person.get("role", "participant")
            school = person.get("school", "Unknown")

            # Check if the person exists
            cursor.execute("SELECT COUNT(*) FROM People WHERE ID = ?", person_id)
            if cursor.fetchone()[0] == 0:
                # Insert the person
                cursor.execute(
                    """
                    INSERT INTO People (ID, Name, Email, School, Role)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    person_id, name, email, school, role
                )
                print(f"Inserted: {name} - {role}")

                # Insert roles if present
                if role in ["organizing", "support", "photographer"]:
                    cursor.execute(
                        "INSERT INTO Roles (PersonID, RoleName) VALUES (?, ?)",
                        person_id, role
                    )
                    print(f"  Assigned role: {role}")

                # Insert schedule (workshops/classes)
                schedule = person.get("schedule", [])
                for class_name in schedule:
                    if class_name:
                        # Get the class ID from the database
                        cursor.execute("SELECT ID FROM Classes WHERE Name = ?", class_name)
                        class_row = cursor.fetchone()
                        if class_row:
                            class_id = class_row[0]
                            # Insert into ClassList
                            cursor.execute(
                                "INSERT INTO ClassList (PersonID, ClassID) VALUES (?, ?)",
                                person_id, class_id
                            )
                            print(f"  Linked {name} to class: {class_name}")
            else:
                print(f"Skipped (already exists): {name} - {role}")

        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    json_file_path = "participants.json"
    data = load_json(json_file_path)
    seed_people_and_roles(data)
