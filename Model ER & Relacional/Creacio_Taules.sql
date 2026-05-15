-- =========================
-- BASE DE DADES
-- =========================
CREATE DATABASE hospital;

-- =========================
-- EXTENSIÓ PER HASH
-- =========================
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- =========================
-- ELIMINACIÓ PER FER PROVES
-- =========================
DROP TABLE IF EXISTS operacio_infermer CASCADE;
DROP TABLE IF EXISTS visita_medicament CASCADE;
DROP TABLE IF EXISTS quirofan_aparell CASCADE;
DROP TABLE IF EXISTS operacio CASCADE;
DROP TABLE IF EXISTS ingres CASCADE;
DROP TABLE IF EXISTS visita CASCADE;
DROP TABLE IF EXISTS inferm_metge CASCADE;
DROP TABLE IF EXISTS inferm_planta CASCADE;
DROP TABLE IF EXISTS habitacio CASCADE;
DROP TABLE IF EXISTS quirofan CASCADE;
DROP TABLE IF EXISTS infermer CASCADE;
DROP TABLE IF EXISTS metge CASCADE;
DROP TABLE IF EXISTS vari CASCADE;
DROP TABLE IF EXISTS usuaris CASCADE;
DROP TABLE IF EXISTS personal CASCADE;
DROP TABLE IF EXISTS pacient CASCADE;
DROP TABLE IF EXISTS planta CASCADE;
DROP TABLE IF EXISTS aparell CASCADE;
DROP TABLE IF EXISTS medicament CASCADE;
DROP TABLE IF EXISTS especialitat CASCADE;

-- =========================
-- TAULES BÀSIQUES
-- =========================

CREATE TABLE especialitat (
    id_especialitat SERIAL PRIMARY KEY,
    descripcio VARCHAR(100) NOT NULL
);

CREATE TABLE medicament (
    id_medicament SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL
);

CREATE TABLE aparell (
    id_aparell SERIAL PRIMARY KEY,
    descripcio VARCHAR(100) NOT NULL
);

CREATE TABLE planta (
    id_planta SERIAL PRIMARY KEY,
    descripcio VARCHAR(100) NOT NULL
);

CREATE TABLE pacient (
    targeta_sanitaria VARCHAR(20) PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    cognom1 VARCHAR(100) NOT NULL,
    cognom2 VARCHAR(100),
    data_naixement DATE NOT NULL
);

CREATE TABLE personal (
    id_personal SERIAL PRIMARY KEY,
    dni VARCHAR(9) NOT NULL UNIQUE,
    nom VARCHAR(100) NOT NULL,
    cognom1 VARCHAR(100) NOT NULL,
    cognom2 VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

-- =========================
-- USUARIS (INTEGRAT AMB pgcrypto)
-- =========================
CREATE TABLE usuaris (
    username VARCHAR(50) PRIMARY KEY,
    password TEXT NOT NULL,
    estat VARCHAR(7) NOT NULL default 'actiu',
    id_personal INTEGER,

    CONSTRAINT fk_usuaris_personal
        FOREIGN KEY (id_personal)
        REFERENCES personal(id_personal)
);

-- Admin per defecte (hash SHA-256)
INSERT INTO personal (dni, nom, cognom1, cognom2, email)
VALUES (
    '48197077W',
    'Angel',
    'Arellano',
    'Diaz',
    'a.arellano@ua.es'
);
INSERT INTO usuaris (username, password, estat, id_personal)
VALUES (
    'ua-admin',
    encode(digest('admin123', 'sha256'), 'hex'),
    'actiu',
    1
)
ON CONFLICT (username) DO NOTHING;

-- =========================
-- ROLES PERSONAL
-- =========================
CREATE TABLE vari (
    id_personal INTEGER PRIMARY KEY,
    feina VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_personal) REFERENCES personal(id_personal)
);

CREATE TABLE metge (
    id_personal INTEGER PRIMARY KEY,
    estudis TEXT NOT NULL,
    experiencia TEXT NOT NULL,
    id_especialitat INTEGER NOT NULL,

    FOREIGN KEY (id_personal) REFERENCES personal(id_personal),
    FOREIGN KEY (id_especialitat) REFERENCES especialitat(id_especialitat)
);

CREATE TABLE infermer (
    id_personal INTEGER PRIMARY KEY,
    curs TEXT,
    experiencia TEXT,

    FOREIGN KEY (id_personal) REFERENCES personal(id_personal)
);

-- =========================
-- RESTA DEL SISTEMA HOSPITALARI
-- =========================

CREATE TABLE habitacio (
    id_habitacio SERIAL PRIMARY KEY,
    descripcio VARCHAR(100) NOT NULL,
    id_planta INTEGER NOT NULL,
    FOREIGN KEY (id_planta) REFERENCES planta(id_planta)
);

CREATE TABLE quirofan (
    id_quirofan INTEGER NOT NULL,
    id_planta INTEGER NOT NULL,

    PRIMARY KEY (id_planta, id_quirofan),
    FOREIGN KEY (id_planta) REFERENCES planta(id_planta)
);

CREATE TABLE inferm_planta (
    id_personal INTEGER PRIMARY KEY,
    id_planta INTEGER NOT NULL,

    FOREIGN KEY (id_personal) REFERENCES infermer(id_personal),
    FOREIGN KEY (id_planta) REFERENCES planta(id_planta)
);

CREATE TABLE inferm_metge (
    id_personal INTEGER PRIMARY KEY,
    id_metge INTEGER NOT NULL,

    FOREIGN KEY (id_personal) REFERENCES infermer(id_personal),
    FOREIGN KEY (id_metge) REFERENCES metge(id_personal)
);

CREATE TABLE visita (
    id_visita SERIAL PRIMARY KEY,
    data_hora TIMESTAMP NOT NULL,
    diagnostic TEXT,
    id_metge INTEGER NOT NULL,
    targeta_sanitaria VARCHAR(20) NOT NULL,

    FOREIGN KEY (id_metge) REFERENCES metge(id_personal),
    FOREIGN KEY (targeta_sanitaria) REFERENCES pacient(targeta_sanitaria)
);

CREATE TABLE ingres (
    id_ingres SERIAL PRIMARY KEY,
    data_ingres TIMESTAMP NOT NULL,
    data_alta TIMESTAMP,
    targeta_sanitaria VARCHAR(20) NOT NULL,
    id_habitacio INTEGER NOT NULL,

    FOREIGN KEY (targeta_sanitaria) REFERENCES pacient(targeta_sanitaria),
    FOREIGN KEY (id_habitacio) REFERENCES habitacio(id_habitacio)
);

CREATE TABLE operacio (
    id_operacio SERIAL PRIMARY KEY,
    descripcio TEXT NOT NULL,
    data_hora TIMESTAMP NOT NULL,
    targeta_sanitaria VARCHAR(20) NOT NULL,
    id_metge INTEGER NOT NULL,
    id_planta INTEGER NOT NULL,
    id_quirofan INTEGER NOT NULL,

    FOREIGN KEY (targeta_sanitaria) REFERENCES pacient(targeta_sanitaria),
    FOREIGN KEY (id_metge) REFERENCES metge(id_personal),
    FOREIGN KEY (id_planta, id_quirofan)
        REFERENCES quirofan(id_planta, id_quirofan)
);

CREATE TABLE quirofan_aparell (
    id_planta INTEGER NOT NULL,
    id_quirofan INTEGER NOT NULL,
    id_aparell INTEGER NOT NULL,
    quantitat INTEGER NOT NULL DEFAULT 1,

    PRIMARY KEY (id_planta, id_quirofan, id_aparell),

    FOREIGN KEY (id_planta, id_quirofan)
        REFERENCES quirofan(id_planta, id_quirofan),
    FOREIGN KEY (id_aparell)
        REFERENCES aparell(id_aparell)
);

CREATE TABLE visita_medicament (
    id_visita INTEGER NOT NULL,
    id_medicament INTEGER NOT NULL,

    PRIMARY KEY (id_visita, id_medicament),

    FOREIGN KEY (id_visita) REFERENCES visita(id_visita),
    FOREIGN KEY (id_medicament) REFERENCES medicament(id_medicament)
);

CREATE TABLE operacio_infermer (
    id_operacio INTEGER NOT NULL,
    id_infermer INTEGER NOT NULL,

    PRIMARY KEY (id_operacio, id_infermer),

    FOREIGN KEY (id_operacio) REFERENCES operacio(id_operacio),
    FOREIGN KEY (id_infermer) REFERENCES infermer(id_personal)
);