import sqlite3
import json


def update_metal(url, metal):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
        UPDATE Metals SET metal = ?, price = ?
        WHERE id = ?
            """,
            (
                metal["metal"],
                metal["price"],
                url["pk"],
            ),
        )
        count_rows_updated = db_cursor.rowcount

    return True if count_rows_updated > 0 else False
