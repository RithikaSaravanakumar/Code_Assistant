"""
Apply schema updates for the coding assessment module.
Safe to run multiple times on existing databases.

    python migrate_schema.py
"""

from sqlalchemy import inspect, text
from app import app
from models import db


def column_exists(table, column):
    insp = inspect(db.engine)
    if table not in insp.get_table_names():
        return False
    return column in [c["name"] for c in insp.get_columns(table)]


def migrate():
    with app.app_context():
        db.create_all()

        # Legacy coding_submissions may reference old questions table
        if column_exists("coding_submissions", "code") and not column_exists("coding_submissions", "submitted_code"):
            with db.engine.begin() as conn:
                conn.execute(text(
                    "ALTER TABLE coding_submissions CHANGE COLUMN code submitted_code TEXT NOT NULL"
                ))
                print("Renamed coding_submissions.code -> submitted_code")

        new_cols = [
            ("programming_language", "VARCHAR(20) NOT NULL DEFAULT 'python'"),
            ("status", "VARCHAR(50) NOT NULL DEFAULT 'Pending'"),
            ("test_cases_passed", "INT NOT NULL DEFAULT 0"),
            ("test_cases_total", "INT NOT NULL DEFAULT 0"),
            ("score", "FLOAT NOT NULL DEFAULT 0"),
            ("execution_status", "VARCHAR(100) NOT NULL DEFAULT 'Not Executed'"),
            ("is_run", "BOOLEAN NOT NULL DEFAULT 0"),
        ]
        for col, typedef in new_cols:
            if not column_exists("coding_submissions", col):
                with db.engine.begin() as conn:
                    conn.execute(text(f"ALTER TABLE coding_submissions ADD COLUMN {col} {typedef}"))
                    print(f"Added coding_submissions.{col}")

        print("Schema migration complete.")


if __name__ == "__main__":
    migrate()
