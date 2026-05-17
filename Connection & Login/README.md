**LOGIN**

El sistema està dissenyat seguint una estructura de capes on la interfície (GUI) recull dades, el mòdul d'autenticació les processa i la base de dades PostgreSQL les emmagatzema de forma segura.

1. _Interfície d'Usuari (GUI amb Tkinter)_

La interfície actua com el primer filtre de dades i gestor d'accessos:
- Pestanyes Diferenciades: separa el flux d'entrada (Login) del de creació (Registre).
- Seguretat en el Registre: s'implementa una barrera d'entrada. La pestanya de registre no es pot veure sense passar primer per verify_admin_credentials(), una pestanya que exigeix permisos d'administrador.
- Recollida de Dades: el formulari està vinculat directament a l'estructura del model ER, recollint dades personals i el rol específic (metge, infermer, vari) que determinarà el camí de la dada en el servidor.

2. _La Seguretat i Rols (auth.py)_

Aquest mòdul és el que connecta Python amb PostgreSQL, assegurant que la informació es tracti amb criteri:

A. Seguretat i Xifrat (Hash)

Per complir amb els estàndards de seguretat, el sistema no guarda contrasenyes reals. Utilitza SHA-256:
- En fer login o registre, la contrasenya es transforma en un hash.
- A la base de dades només es guarda el resultat hexadecimal, protegint la privacitat del personal en cas de filtració.

B. Gestió de la Jerarquia

La funció register_personal_db executa la lògica que vam definir al model ER. Per cada nou empleat, el sistema realitza una operació en cascada:
-  Taula personal: crea el perfil humà (DNI, nom, email).
-  Taula usuaris: crea les credencials d'accés vinculades a la persona.
-  Taula de Rol: segons el desplegable triat, insereix la informació específica a metge, infermer o vari.

3. _Integritat i Control d'Errors_

El backend està protegit per evitar dades corruptes o inconsistents:
- Transaccions de Dades Vigilada i Automatitzada: S'utilitza conn.commit() i conn.rollback(). Si el registre falla en qualsevol dels tres passos (per exemple, si el DNI ja existeix), la transacció de les dades es cancel·la sencera per evitar deixar un "usuari sense persona" o una "persona sense rol".
- Validació de l'Estat: El login comprova que el camp estat sigui 'actiu', permetent una baixa lògica del personal sense haver d'esborrar el seu historial d'operacions o consultes.


**Connector a la BD**

Aquest mòdul fa que en lloc de repetir la configuració del servidor en cada part del programa, centralitzes les credencials aquí per motius d'eficiència i seguretat.

1. _Paràmetres de Xarxa i Accés_

El codi especifica exactament on s'ha d'anar a buscar la informació:
- Host (192.168.2.5): indica que la base de dades no està en el teu propi ordinador, sinó en un servidor de la xarxa local. Això és propi d'un entorn real d'hospital on les dades resideixen en un servidor centralitzat.
- Port (5432): Utilitza el port estàndard de PostgreSQL.
- Credencials: defineix l'usuari (postgres) i la base de dades (hospital) on es crearan les taules de personal, quiròfans i usuaris.

2. _OperationalError_

El codi està preparat per a imprevistos mitjançant un bloc try-except:
- Si el servidor de la BD està apagat, el cable de xarxa desconnectat o la contrasenya és incorrecta, el programa no "petarà" (no es tancarà bruscament).
- En lloc d'això, captura l'error (OperationalError), imprimeix un missatge informatiu i retorna None, permetent que la resta de l'aplicació gestioni el problema de forma controlada (mostrant un avís a l'usuari).
