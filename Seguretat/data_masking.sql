CREATE EXTENSION IF NOT EXISTS anon CASCADE;
SELECT anon.init();


-- =========================
-- DECLARAR ROLS MASKED
-- =========================
SECURITY LABEL FOR anon ON ROLE rol_vari IS 'MASKED';
SECURITY LABEL FOR anon ON ROLE rol_consulta IS 'MASKED';

-- =========================
-- MASKING A LES TAULES
-- =========================
SECURITY LABEL FOR anon ON COLUMN pacient.targeta_sanitaria
IS 'MASKED WITH FUNCTION anon.partial(targeta_sanitaria, 0, 
$$
XXXX-XXXX-
$$
, 4)';

SECURITY LABEL FOR anon ON COLUMN pacient.nom
IS 'MASKED WITH FUNCTION anon.partial(nom, 1, 
$$
*****
$$
, 0)';

SECURITY LABEL FOR anon ON COLUMN pacient.cognom1
IS 'MASKED WITH FUNCTION anon.partial(cognom1, 1, 
$$
*****
$$
, 0)';

SECURITY LABEL FOR anon ON COLUMN pacient.cognom2
IS 'MASKED WITH FUNCTION anon.partial(cognom2, 1, 
$$
*****
$$
, 0)';

SECURITY LABEL FOR anon ON COLUMN pacient.data_naixement
IS 'MASKED WITH VALUE 
$$
1900-01-01
$$
::date';



SECURITY LABEL FOR anon ON COLUMN personal.dni
IS 'MASKED WITH FUNCTION anon.partial(dni, 0, 
$$
********
$$
, 1)';

SECURITY LABEL FOR anon ON COLUMN personal.nom
IS 'MASKED WITH FUNCTION anon.partial(nom, 1, 
$$
*****
$$
, 0)';

SECURITY LABEL FOR anon ON COLUMN personal.cognom1
IS 'MASKED WITH FUNCTION anon.partial(cognom1, 1, 
$$
*****
$$
, 0)';

SECURITY LABEL FOR anon ON COLUMN personal.cognom2
IS 'MASKED WITH FUNCTION anon.partial(cognom2, 1, 
$$
*****
$$
, 0)';

SECURITY LABEL FOR anon ON COLUMN personal.email
IS 'MASKED WITH FUNCTION anon.partial_email(email)';




SECURITY LABEL FOR anon ON COLUMN visita.diagnostic
IS 'MASKED WITH VALUE 
$$
[CONFIDENCIAL]
$$
';




SECURITY LABEL FOR anon ON COLUMN operacio.descripcio
IS 'MASKED WITH VALUE 
$$
[CONFIDENCIAL]
$$
';



SECURITY LABEL FOR anon ON COLUMN usuaris.password
IS 'MASKED WITH VALUE 
$$
[HASH OCULT]
$$
';

-- =========================
-- ACTIVAR MASKING DINÀMIC
-- =========================
SELECT anon.start_dynamic_masking();
