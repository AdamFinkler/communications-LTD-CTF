from database.connection import connection, cursor


def create_customer_service(package_id: int, customer_name: str):
    try:
        cursor.execute(
            f"""
            SELECT id FROM packages WHERE id = {package_id}
            """
        )
        package = cursor.fetchone()

        if package is None:
            raise Exception("Package ID does not exist")

        # Vulnerable: executescript allows stacked SQL (multiple INSERTs from SQLi payload)
        connection.executescript(
            f"""
            INSERT INTO customers (package_id, customer_name)
            VALUES ({package_id}, '{customer_name}');
            """
        )
        connection.commit()

        cursor.execute(
            """
            SELECT id, package_id, customer_name FROM customers
            ORDER BY id
            """
        )
        all_customers = cursor.fetchall()

        return {
            "message": "Customer created successfully",
            "package_id": package_id,
            "customer_name": customer_name,
            "customers": all_customers,
        }
    except Exception as e:
        return {
            "message": str(e),
        }
