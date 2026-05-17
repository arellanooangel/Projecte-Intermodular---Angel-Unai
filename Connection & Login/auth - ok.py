import psycopg2
import hashlib

def get_connection():
    """Estableix la connexió amb la base de dades PostgreSQL."""
    try:
        return psycopg2.connect(
            host="192.168.10.10",
            database="hospital",
            user="ua-admin",
            password="admin123"
        )
    except Exception as e:
        print(f"❌ Error de connexió: {e}")
        return None

def xifrar_password(password):
    """Genera un hash SHA-256 de la contrasenya."""
    return hashlib.sha256(password.encode()).hexdigest()

def login_user_db(u, p):
    conn = get_connection()
    if not conn: return None
    try:
        cur = conn.cursor()
        cur.execute("SET search_path TO hospital;")
        pw_hash = xifrar_password(p)
        query = """
            SELECT u.id_personal, p.nom, p.cognom1 
            FROM usuaris u 
            JOIN personal p ON u.id_personal = p.id_personal 
            WHERE u.username = %s AND u.password = %s
        """
        cur.execute(query, (u, pw_hash))
        return cur.fetchone()
    finally:
        conn.close()

def register_personal_db(dni, nom, c1, c2, email, user, pw, rol):
    conn = get_connection()
    if not conn: return False
    try:
        cur = conn.cursor()
        cur.execute("SET search_path TO hospital;")
        cur.execute("""
            INSERT INTO personal (dni, nom, cognom1, cognom2, email) 
            VALUES (%s, %s, %s, %s, %s) RETURNING id_personal
        """, (dni, nom, c1, c2, email))
        id_p = cur.fetchone()[0]
        pw_hash = xifrar_password(pw)
        cur.execute("INSERT INTO usuaris (username, password, id_personal) VALUES (%s, %s, %s)", (user, pw_hash, id_p))
        if rol == "metge": cur.execute("INSERT INTO metge (id_personal) VALUES (%s)", (id_p,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error: {e}"); conn.rollback(); return False
    finally:
        conn.close()

def insertar_pacient_db(ts, nom, cognom1, cognom2, data_naix):
    conn = get_connection()
    if not conn: return False
    try:
        cur = conn.cursor()
        cur.execute("SET search_path TO hospital, public;")
        
        # Fem servir la sintaxi INSERT INTO taula VALUES (...) 
        # ATENCIÓ: L'ordre ha de coincidir amb com vas crear la taula.
        # Normalment: (targeta, nom, cognom1, cognom2, data_naixement)
        query = """
            INSERT INTO pacient 
            VALUES (%s, %s, %s, %s, %s);
        """
        cur.execute(query, (ts, nom, cognom1, cognom2, data_naix))
        conn.commit()
        return True
    except Exception as e:
        print("------------------------------------------")
        print(f"❌ ERROR REAL: {e}")
        print("------------------------------------------")
        conn.rollback()
        return False
    finally:
        conn.close()

def get_recursos_planta_db(p_id):
    conn = get_connection()
    res = {"h": 0, "q": 0, "i": 0}
    if not conn: return res
    try:
        cur = conn.cursor(); cur.execute("SET search_path TO hospital;")
        cur.execute("SELECT COUNT(*) FROM habitacio WHERE id_planta = %s", (p_id,)); res["h"] = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM quirofan WHERE id_planta = %s", (p_id,)); res["q"] = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM inferm_planta WHERE id_planta = %s", (p_id,)); res["i"] = cur.fetchone()[0]
    finally: conn.close()
    return res

def get_informe_personal_db():
    conn = get_connection()
    if not conn: return []
    try:
        cur = conn.cursor(); cur.execute("SET search_path TO hospital;")
        cur.execute("SELECT dni, nom, cognom1, email FROM personal ORDER BY cognom1 ASC;")
        return cur.fetchall()
    finally: conn.close()

def get_visites_per_dia_db():
    conn = get_connection()
    if not conn: return []
    try:
        cur = conn.cursor(); cur.execute("SET search_path TO hospital;")
        cur.execute("SELECT data_hora::date, COUNT(*) FROM visita GROUP BY 1 ORDER BY 1 DESC;")
        return cur.fetchall()
    finally: conn.close()

def get_ranking_metges_db():
    conn = get_connection()
    if not conn: return []
    try:
        cur = conn.cursor(); cur.execute("SET search_path TO hospital;")
        cur.execute("""
            SELECT p.nom, p.cognom1, COUNT(v.id_visita) as total
            FROM metge m JOIN personal p ON m.id_personal = p.id_personal
            JOIN visita v ON m.id_personal = v.id_metge GROUP BY 1, 2 ORDER BY 3 DESC;
        """)
        return cur.fetchall()
    finally: conn.close()
