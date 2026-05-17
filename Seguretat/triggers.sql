SET search_path TO hospital;

-- ======================================
-- TRIGGER VALIDACIO DEL FORMAT DEL DNI
-- ======================================

CREATE OR REPLACE FUNCTION validar_format_dni()
RETURNS TRIGGER AS $$
BEGIN
    -- Comprova DNI tingui exactament 8 numeros i 1 lletra majuscula 
    IF NEW.dni !~ '^[0-9]{8}[A-Z]$' THEN
        RAISE EXCEPTION 'Format de DNI no valid: %. Ha de ser 8 numeros i 1 lletra.', NEW.dni;
    END IF;
    
    RETURN NEW; -- Si es correcte, deixa passar
END;
$$ LANGUAGE plpgsql;

-- Creem trigger per la taula personal
DROP TRIGGER IF EXISTS trg_validar_dni ON personal;
CREATE TRIGGER trg_validar_dni
BEFORE INSERT OR UPDATE ON personal
FOR EACH ROW EXECUTE FUNCTION validar_format_dni();



-- =====================================
-- TRIGGER VALIDACIO SOLAPAMENT VISITES
-- =====================================

CREATE OR REPLACE FUNCTION evitar_solapament_visites()
RETURNS TRIGGER AS $$
BEGIN
    -- Busquem si el metge ja te visita a aquella data i hora
    IF EXISTS (
        SELECT 1 FROM hospital.visita 
        WHERE id_metge = NEW.id_metge 
        AND data_hora = NEW.data_hora
    ) THEN
        RAISE EXCEPTION 'El metge ja te una visita programada per al dia i hora: %', NEW.data_hora;
    END IF;
    
    RETURN NEW; -- Si l'agenda esta lliure, permet la visita
END;
$$ LANGUAGE plpgsql;

-- Creem trigger per la taula visita
DROP TRIGGER IF EXISTS trg_solapament_visites ON visita;
CREATE TRIGGER trg_solapament_visites
BEFORE INSERT OR UPDATE ON visita
FOR EACH ROW EXECUTE FUNCTION evitar_solapament_visites();
