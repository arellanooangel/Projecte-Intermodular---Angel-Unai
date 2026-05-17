================================================================================
GUIA DE CONFIGURACIÓ SSL: POSTGRESQL (UA - HOSPITAL Blanes)
================================================================================

Aquest document detalla la implementació de seguretat per al servidor amb 
IP i PostgreSQL.

--------------------------------------------------------------------------------
1. GENERACIÓ DEL CERTIFICAT (REQUISIT 2 - PART A)
--------------------------------------------------------------------------------
Com que el servidor opera en una xarxa local amb una IP privada, no és possible 
utilitzar entitats certificadores públiques com Let's Encrypt. Per aquest motiu, 
s'ha generat un certificat AUTOFIRMAT mitjançant l'eina OpenSSL.

Comandaments executats al servidor:

# 1. Generació de la clau privada i el certificat (vàlid per 365 dies)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout server.key \
  -out server.crt \
  -subj "/C=ES/ST=Catalunya/L=Blanes/O=Hospital/CN=192.168.2.5"

# 2. Trasllat de fitxers a la ruta de dades de PostgreSQL
sudo cp server.crt /var/lib/postgresql/16/main/
sudo cp server.key /var/lib/postgresql/16/main/

# 3. Configuració de permisos (Restricció estricta per seguretat)
sudo chown postgres:postgres /var/lib/postgresql/16/main/server.crt /var/lib/postgresql/16/main/server.key
sudo chmod 600 /var/lib/postgresql/16/main/server.key

--------------------------------------------------------------------------------
2. RENOVACIÓ AUTOMÀTICA (REQUISIT 2 - PART B)
--------------------------------------------------------------------------------
Atès que els certificats autofirmats no disposen d'un servei de renovació 
extern, s'ha implementat un sistema d'automatització local mitjançant un 
Script de Bash i una tasca programada (Cron Job).

A) Script de renovació (/usr/local/bin/renova_ssl_postgres.sh):
--------------------------------------------------------------
#!/bin/bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /var/lib/postgresql/16/main/server.key \
  -out /var/lib/postgresql/16/main/server.crt \
  -subj "/C=ES/ST=Catalunya/L=Blanes/O=Hospital/CN=192.168.2.5"

chown postgres:postgres /var/lib/postgresql/16/main/server.crt /var/lib/postgresql/16/main/server.key
chmod 600 /var/lib/postgresql/16/main/server.key
systemctl restart postgresql

B) Programació del Cron:
------------------------
S'ha configurat el sistema perquè l'script s'executi automàticament cada any:
(sudo crontab -l ; echo "0 0 1 1 * /bin/bash /usr/local/bin/renova_ssl_postgres.sh") | sudo crontab -

--------------------------------------------------------------------------------
3. CONFIGURACIÓ DEL SERVIDOR POSTGRESQL
--------------------------------------------------------------------------------

A) Fitxer postgresql.conf:
S'han identificat i activat els següents paràmetres de xifrat:
- ssl = on
- ssl_cert_file = '/var/lib/postgresql/16/main/server.crt'
- ssl_key_file = '/var/lib/postgresql/16/main/server.key'

B) Fitxer pg_hba.conf:
S'han establert regles per obligar a l'ús de SSL i rebutjar connexions insegures:
- hostssl all all 0.0.0.0/0 scram-sha-256
- hostnossl all all 0.0.0.0/0 reject

--------------------------------------------------------------------------------
4. IMPLEMENTACIÓ DEL CLIENT (PYTHON)
--------------------------------------------------------------------------------
La connexió des de l'aplicació s'ha configurat per forçar el mode segur mitjançant
la llibreria psycopg2.

Codi del fitxer db_connexion.py (amb IP, usuari i contrasenya de prova):

import psycopg2

def get_connection():
    try:
        connection = psycopg2.connect(
            host="192.168.2.5",
            database="hospital",
            user="postgres",
            password="1234",
            sslmode="require"  # Força el xifrat SSL amb el certificat autofirmat
        )
        return connection
    except Exception as e:
        print(f"Error: {e}")
        return None
