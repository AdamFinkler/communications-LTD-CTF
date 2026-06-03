from database.connection import connection, cursor


def delete_customer_service(customer_id: int):
    try:
        customer_id = int(customer_id)
        cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
        connection.commit()

        if cursor.rowcount == 0:
            return {"message": "Customer not found"}

        cursor.execute(
            """
            SELECT id, package_id, customer_name FROM customers
            ORDER BY id
            """
        )

        return {
            "message": "Customer deleted successfully",
            "customers": cursor.fetchall(),
        }
    except Exception as e:
        return {"message": str(e)}
