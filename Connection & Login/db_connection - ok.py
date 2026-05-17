import psycopg2
from psycopg2 import OperationalError

def get_connection():
    """Estableix la connexió amb Alta Disponibilitat."""
    
    # Intentem servidor principal
    try:
        print("Intentant connectar a node1...")
        connection = psycopg2.connect(
            host="192.168.56.10",
            database="hospital",
            user="ua-admin", 
            password="admin123",
            sslmode="require"
        )
        print("Connectat al node1 amb èxit.")
        return connection
        
    except OperationalError:
        print("node1 caigut. Activant protocol d'emergència cap a node2...")
        
        # Si el principal falla
        try:
            connection = psycopg2.connect(
                host="192.168.56.20", 
                database="hospital",
                user="ua-admin", 
                password="admin123",
                sslmode="require"
            )
            print("Connectat al node2 amb èxit.")
            return connection
            
        except Exception as e:
            print(f"Error crític: Els dos servidors estan caiguts. Detalls: {e}")
            return None
        
if __name__ == "__main__":
    conn = get_connection()
    if conn:
        print("Connexió establerta. Procedint amb operacions a la base de dades...")
        # Aquí podríem afegir codi per interactuar amb la base de dades
        conn.close()
    else:
        print("No s'ha pogut establir connexió amb cap servidor.")
