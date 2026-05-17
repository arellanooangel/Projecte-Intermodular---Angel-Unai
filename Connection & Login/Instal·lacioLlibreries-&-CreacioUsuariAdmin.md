# Per instal·lar les llibreries haurem de fer aquets passos:

    Cerca “Edita les variables d'entorn del sistema” al Windows.
    A Variables d'entorn, seleccioneu Path a les variables del sistema.
    Afegeix les rutes següents (ajusta-les segons la teva versió de Python):
        C:\Users\Usuari\AppData\Local\Programs\Python\Python312\
        C:\Users\Usuari\AppData\Local\Programs\Python\Python312\Scripts\
    Accepteu els canvis i reinicieu PowerShell.

    Executar la seguent comanda a la terminal
        py -m pip install -r ".\Connection and Login\requeriments.txt"

# Crear la BD i l'usuari admin per poder accedir a afegir personal
    Executar el document "creacio_taules.sql" amb el servidor connectat editant el codi del fitxer "db_connexio.py" amb les dades del servidor
        1. Primer executem solament la línia que conté "CREATE DATABASE hospital;"
        2. Després executarem la resta del codi
