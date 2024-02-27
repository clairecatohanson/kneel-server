import sqlite3
import json


def get_all_orders(url):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        orders = []

        if "_expand" in url["query_params"]:
            db_cursor.execute(
                """
            SELECT o.id, o.metal_id, o.size_id, o.style_id, o.timestamp, m.id AS metalId, m.metal, m.price AS metalPrice, si.id AS sizeId, si.carats, si.price AS sizePrice, st.id AS styleId, st.style, st.price AS stylePrice FROM Orders o
            JOIN Metals m ON o.metal_id = m.id
            JOIN Sizes si ON o.size_id = si.id
            JOIN Styles st ON o.style_id = st.id
                """
            )

            sql_results = db_cursor.fetchall()
            for row in sql_results:
                metal = {"metal": row["metal"], "price": row["metalPrice"]}
                size = {"carats": row["carats"], "price": row["sizePrice"]}
                style = {"style": row["style"], "price": row["stylePrice"]}
                order = {
                    "id": row["id"],
                    "metal_id": row["metal_id"],
                    "metal": metal,
                    "size_id": row["size_id"],
                    "size": size,
                    "style_id": row["style_id"],
                    "style": style,
                    "timestamp": row["timestamp"],
                }
                orders.append(order)
        else:
            db_cursor.execute(
                """
            SELECT id, metal_id, size_id, style_id, timestamp FROM Orders
                """
            )

            sql_results = db_cursor.fetchall()
            for row in sql_results:
                orders.append(dict(row))

        serialized_results = json.dumps(orders)

    return serialized_results


def get_single_order(url):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        if "_expand" in url["query_params"]:
            db_cursor.execute(
                """
            SELECT o.id, o.metal_id, o.size_id, o.style_id, o.timestamp, m.id AS metalId, m.metal, m.price AS metalPrice, si.id AS sizeId, si.carats, si.price AS sizePrice, st.id AS styleId, st.style, st.price AS stylePrice FROM Orders o
            JOIN Metals m ON o.metal_id = m.id
            JOIN Sizes si ON o.size_id = si.id
            JOIN Styles st ON o.style_id = st.id
            WHERE o.id = ?
                """,
                (url["pk"],),
            )
            sql_result = dict(db_cursor.fetchone())
            metal = {"metal": sql_result["metal"], "price": sql_result["metalPrice"]}
            size = {"carats": sql_result["carats"], "price": sql_result["sizePrice"]}
            style = {"style": sql_result["style"], "price": sql_result["stylePrice"]}
            order = {
                "id": sql_result["id"],
                "metal_id": sql_result["metal_id"],
                "metal": metal,
                "size_id": sql_result["size_id"],
                "size": size,
                "style_id": sql_result["style_id"],
                "style": style,
                "timestamp": sql_result["timestamp"],
            }

        else:
            db_cursor.execute(
                """
            SELECT * FROM Orders WHERE id = ?
                """,
                (url["pk"],),
            )
            sql_result = db_cursor.fetchone()
            order = dict(sql_result)

        serialized_order = json.dumps(order)

    return serialized_order


def create_order(order):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
        INSERT INTO Orders (metal_id, size_id, style_id, timestamp) VALUES (?, ?, ?, datetime())
            """,
            (
                order["metal_id"],
                order["size_id"],
                order["style_id"],
            ),
        )

    return True if db_cursor.rowcount > 0 else False


def delete_order(url):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
        DELETE FROM Orders WHERE id = ?
            """,
            (url["pk"],),
        )
        count_rows_deleted = db_cursor.rowcount

    return True if count_rows_deleted > 0 else False
