from auth_ok import get_connection

def llistar_columnes():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'hospital.pacient'
    """)
    columnes = cur.fetchall()
    print("Les teves columnes reals són:")
    for col in columnes:
        print(f"- {col[0]}")
    conn.close()

llistar_columnes()
