from faker import Faker
import random
from db_connexio
import get_connection 

# Inicialitzem Faker per a Català/Castellà i per a Rus (caràcters cirílics)
fake_local = Faker('ca_ES')
fake_rus = Faker('ru_RU')


def generar_pacients(conn, quantitat=50000):
    cursor = conn.cursor()
    pacients_data = []
    
    print(f"Generant {quantitat} pacients en memòria...")
    
    for _ in range(quantitat):
        # Fem que un 5% dels pacients tinguin dades en cirílic
        if random.random() < 0.05:
            f = fake_rus
        else:
            f = fake_local
            
        # Generem les dades falses
        # Faker.bothify ens permet generar un patró. Ex: 4 lletres i 8 números
        targeta_sanitaria = f.unique.bothify(text='????########').upper()
        nom = f.first_name()
        cognom1 = f.last_name()
        cognom2 = f.last_name()
        # Data de naixement per a gent entre 1 i 99 anys
        data_naixement = f.date_of_birth(minimum_age=1, maximum_age=99)
        
        # Afegim la tupla a la nostra llista
        pacients_data.append((targeta_sanitaria, nom, cognom1, cognom2, data_naixement))

    print("Inserint pacients a la Base de Dades...")
    
    # Utilitzem executemany per inserir tot el bloc de cop
    sql = """
        INSERT INTO hospital.pacient (targeta_sanitaria, nom, cognom1, cognom2, data_naixement) 
        VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cursor.executemany(sql, pacients_data)
        conn.commit()
        print("Pacients inserits correctament!")
    except Exception as e:
        conn.rollback()
        print(f"Error inserint pacients: {e}")
    finally:
        cursor.close()



def generar_personal_i_rols(conn):
    cursor = conn.cursor()

    try:
        # 1. INSERIR ESPECIALITATS BÀSIQUES (Metges ho necessiten)
        especialitats = ['Traumatologia', 'Cardiologia', 'Pediatria', 'Neurologia', 'Cirurgia General', 'Oncologia', 'Dermatologia', 'Psiquiatria']
        print("1. Preparant Especialitats Mèdiques...")
        ids_especialitats = []
        for esp in especialitats:
            # Usem un insert normal (suposant que no existeixen).
            # Si ja teniu dades, podeu canviar-ho per un simple SELECT
            cursor.execute("INSERT INTO hospital.especialitat (descripcio) VALUES (%s) RETURNING id_especialitat", (esp,))
            ids_especialitats.append(cursor.fetchone()[0])
            
        # 2. GENERAR 450 REGISTRES DE PERSONAL
        total_personal = 450 # 100 metges + 200 inf + 100 neteja + 50 admin
        nous_ids_personal = []
        personal_data = []
        
        print(f"2. Generant i inserint {total_personal} empleats base...")
        # Generem la llista base
        for _ in range(total_personal):
            dni = fake_local.unique.bothify(text='########?').upper()
            nom = fake_local.first_name()
            cognom1 = fake_local.last_name()
            cognom2 = fake_local.last_name()
            # Generem un email "corporatiu"
            email = f"{nom.lower()[:3]}{cognom1.lower()[:3]}{dni[-3:]}@hospitalblanes.cat"
            personal_data.append((dni, nom, cognom1, cognom2, email))

        # Inserim d'un en un per obtenir el RETURNING ID fàcilment 
        # (450 inserts són fraccions de segon)
        sql_pers = """
            INSERT INTO hospital.personal (dni, nom, cognom1, cognom2, email) 
            VALUES (%s, %s, %s, %s, %s) RETURNING id_personal
        """
        for p in personal_data:
            cursor.execute(sql_pers, p)
            nous_ids_personal.append(cursor.fetchone()[0])
            
        print("3. Repartint els rols i creant Usuaris de login...")
        
        # Llistes per a cada subtaula i per usuaris
        metges_data = []
        infermeres_data = []
        vari_data = []
        usuaris_data = []

        # Recorrem els ID acabats de crear i els separem per quotes
        for idx, id_pers in enumerate(nous_ids_personal):
            # L'username serà el DNI
            username = personal_data[idx][0]
            # Passem la contrasenya en text pla, el SQL farà el hash a la base de dades
            usuaris_data.append((username, 'pwd_hospital123', id_pers))

            if idx < 100:
                # 100 Metges
                estudis = "Llicenciatura en Medicina"
                experiencia = f"{random.randint(1, 30)} anys"
                id_esp = random.choice(ids_especialitats)
                metges_data.append((id_pers, estudis, experiencia, id_esp))
                
            elif idx < 300:
                # 200 Infermeres
                curs = "Grau en Infermeria"
                experiencia = f"{random.randint(1, 25)} anys"
                infermeres_data.append((id_pers, curs, experiencia))
                
            elif idx < 400:
                # 100 Neteja (A la taula vari)
                vari_data.append((id_pers, 'Neteja'))
                
            else:
                # 50 Administració (A la taula vari)
                vari_data.append((id_pers, 'Administració'))

        # Inserim en bloc a les subtaules (Ara que ja sabem l'estructura)
        cursor.executemany("INSERT INTO hospital.metge (id_personal, estudis, experiencia, id_especialitat) VALUES (%s, %s, %s, %s)", metges_data)
        cursor.executemany("INSERT INTO hospital.infermer (id_personal, curs, experiencia) VALUES (%s, %s, %s)", infermeres_data)
        cursor.executemany("INSERT INTO hospital.vari (id_personal, feina) VALUES (%s, %s)", vari_data)

        # Inserim els usuaris usant pgcrypto directament a la crida SQL (Com teniu a creacio_taules)
        sql_usuaris = """
            INSERT INTO hospital.usuaris (username, password, estat, id_personal)
            VALUES (%s, encode(digest(%s, 'sha256'), 'hex'), 'actiu', %s)
        """
        cursor.executemany(sql_usuaris, usuaris_data)

        conn.commit()
        print("Personal i rols vinculats amb èxit! La teva estructura relacional ja funciona.")

    except Exception as e:
        conn.rollback()
        print(f"Error generant personal i rols: {e}")
    finally:
        cursor.close()


def generar_infraestructura(conn):
    cursor = conn.cursor()

    try:
        # --- PAS 1: Catàleg d'Aparells ---
        print("1. Creant catàleg d'aparells mèdics...")
        noms_aparells = ['Respirador', 'Màquina d\'oxigen', 'Desfibril·lador', 'Monitor de constants', 'Bisturí elèctric']
        ids_aparells = []
        
        for nom in noms_aparells:
            cursor.execute("INSERT INTO hospital.aparell (descripcio) VALUES (%s) RETURNING id_aparell", (nom,))
            ids_aparells.append(cursor.fetchone()[0])

        # --- PAS 2: Creem les 4 Plantes de l'enunciat ---
        print("2. Construint l'hospital: Plantes, Habitacions i Quiròfans...")
        noms_plantes = ['Primera', 'Segona', 'Tercera', 'Quarta']
        
        # Usem enumerate per tenir un número de l'1 al 4 (idx_planta) i el nom
        for idx_planta, nom_planta in enumerate(noms_plantes, start=1):
            
            # Creem la Planta
            cursor.execute("INSERT INTO hospital.planta (descripcio) VALUES (%s) RETURNING id_planta", (nom_planta,))
            id_planta_db = cursor.fetchone()[0]

            # --- PAS 3: Creem 20 habitacions per a aquesta planta ---
            for num_hab in range(1, 21):
                # Format visual bonic: Ex. Planta 1, hab 5 -> "Habitació 105"
                nom_hab = f"Habitació {idx_planta}{num_hab:02d}" 
                cursor.execute("""
                    INSERT INTO hospital.habitacio (descripcio, id_planta) 
                    VALUES (%s, %s)
                """, (nom_hab, id_planta_db))

            # --- PAS 4: Creem 2 quiròfans per a aquesta planta ---
            for id_quirofan in range(1, 3):
                # Aquí l'id_quirofan l'inserim manualment (1 i 2) perquè no és SERIAL
                cursor.execute("""
                    INSERT INTO hospital.quirofan (id_quirofan, id_planta) 
                    VALUES (%s, %s)
                """, (id_quirofan, id_planta_db))

                # --- PAS 5: Assignem aparells al quiròfan ---
                # Escollim entre 2 i 4 aparells a l'atzar d'aquells que vam crear al PAS 1
                quants_aparells_diferents = random.randint(2, 4)
                aparells_escollits = random.sample(ids_aparells, quants_aparells_diferents)
                
                for id_ap in aparells_escollits:
                    quantitat_unitats = random.randint(1, 3) # Ex: 2 respiradors
                    cursor.execute("""
                        INSERT INTO hospital.quirofan_aparell (id_planta, id_quirofan, id_aparell, quantitat) 
                        VALUES (%s, %s, %s, %s)
                    """, (id_planta_db, id_quirofan, id_ap, quantitat_unitats))

        # Ho guardem tot a la base de dades
        conn.commit()
        print("Tota la infraestructura s'ha muntat correctament!")

    except Exception as e:
        conn.rollback()
        print(f"Error a l'hora de crear la infraestructura: {e}")
    finally:
        cursor.close()


def generar_visites_massives(conn):
    cursor = conn.cursor()

    try:
        # --- PAS 1: Recollir els IDs existents a la BD ---
        print("1. Recollint pacients i metges de la base de dades...")
        
        # Agafem totes les targetes sanitàries
        cursor.execute("SELECT targeta_sanitaria FROM hospital.pacient")
        # 'fetchall' retorna una llista de tuples: [('123A',), ('456B',), ...]
        # Ho convertim a una llista normal amb una mica de màgia de Python:
        llista_pacients = [fila[0] for fila in cursor.fetchall()]

        # Agafem els IDs només dels metges (no volem infermeres ni neteja fent visites!)
        cursor.execute("SELECT id_personal FROM hospital.metge")
        llista_metges = [fila[0] for fila in cursor.fetchall()]

        # Comprovació de seguretat
        if not llista_pacients or not llista_metges:
            print("Error: Primer has de generar pacients i metges!")
            return

        # --- PAS 2: Generar les dades en memòria ---
        print("2. Generant 100.000 visites en memòria")
        
        diagnostics_comuns = [
            'Grip comuna', 'Esquinç de turmell', 'Migranya', 'Otitis', 
            'Revisió rutinària', 'Gastroenteritis', 'Lumbàlgia', 'Ansietat'
        ]
        
        visites_data = [] # Aquí guardarem totes les visites abans d'enviar-les

        # Bucle de 100.000 (Comença posant 1000 per provar, després canvia-ho a 100000)
        for i in range(100000): 
            # Faker ens permet generar dates entre "avui" i fa 2 anys enrere
            data_hora = fake_local.date_time_between(start_date='-2y', end_date='now')
            
            diagnostic = random.choice(diagnostics_comuns)
            
            # Escolliu un metge i un pacient a l'atzar de les llistes que hem descarregat
            id_metge = random.choice(llista_metges)
            pacient = random.choice(llista_pacients)

            # Afegim la tupla a la nostra gran llista
            visites_data.append((data_hora, diagnostic, id_metge, pacient))

        # --- PAS 3: Inserció massiva (executemany) ---
        print("3. Inserint a la Base de Dades de cop...")
        
        sql = """
            INSERT INTO hospital.visita (data_hora, diagnostic, id_metge, targeta_sanitaria) 
            VALUES (%s, %s, %s, %s)
        """
        # executemany s'encarrega d'agafar la nostra llista de 100.000 tuples 
        # i fer els INSERTS de la manera més ràpida possible
        cursor.executemany(sql, visites_data)
        
        conn.commit()
        print("Èxit! S'han inserit 100.000 visites espectacularment ràpid.")

    except Exception as e:
        conn.rollback()
        print(f"Error inserint visites: {e}")
    finally:
        cursor.close()


# --- BLOC DE PROVA ---
if __name__ == "__main__":
    
    print("Iniciant el procés de generació de Dummy Data...")
    conn = connectar_bd() # Obrim connexió
    
    if conn:
        try:
            # 1. Generem pacients
            print("PAS 1: PACIENTS")
            generar_pacients(conn, quantitat=50000) # Deixa'ho en 500 per la prova inicial
            
            # 2. Generem personal i rols
            print("PAS 2: PERSONAL")
            generar_personal_i_rols(conn)
            
            # 3. Generem infraestructura (Plantes, hab, etc)
            print("PAS 3: INFRAESTRUCTURA")
            generar_infraestructura(conn)
            
            # 4. Generem visites massives
            print("PAS 4: VISITES")
            generar_visites_massives(conn) # Recorda posar el bucle a 1000 o 2000 per provar

        except Exception as e:
            print(f"Hi ha hagut un error crític durant l'execució: {e}")
            
        finally:
            # TANQUEM LA CONNEXIÓ AL FINAL DE TOT
            conn.close()
            print("Connexió a la base de dades tancada.")
            print("Procés finalitzat!")
    else:
        print("No s'ha pogut connectar a la base de dades.")