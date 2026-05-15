import psycopg2

def get_connection():
    """Estableix la connexió amb la base de dades PostgreSQL."""
    try:
        connection = psycopg2.connect(
            host="192.168.1.10",
            database="hospital",
            user="ua-admin", 
            password="admin123",
            sslmode="require"  # Força el xifrat SSL amb el certificat autofirmat
        )
        return connection
    except Exception as e:
        print(f"Error de connexió: {e}")
        return None