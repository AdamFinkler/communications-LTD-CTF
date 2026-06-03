from database.connection import cursor


def list_customers_service():
    cursor.execute(
        """
        SELECT id, package_id, customer_name FROM customers
        ORDER BY id
        """
    )
    return {"customers": cursor.fetchall()}
