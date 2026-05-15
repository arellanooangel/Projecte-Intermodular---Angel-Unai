## MODEL RELACIONAL
**ESPECIALITAT** ((PK)*id_especialitat*, descripcio)

**MEDICAMENT** ((PK)*id_medicament*, nom)

**APARELL** ((PK)*id_aparell*, descripcio)

**PLANTA** ((PK)*id_planta*, descripcio)

**PACIENT** ((PK)*targeta_sanitaria*, nom, cognom1, cognom2, data_naixement)

**PERSONAL** ((PK)*id_personal*, dni, nom, cognom1, cognom2, email)

**USUARI** ((PK)*usuari*, contrasenya, estat, id_personal)

ON (id_personal) REFERENCIA PERSONAL (id_personal)

**VARI** ((PK)*id_personal*, feina)

ON (id_personal) REFERENCIA PERSONAL (id_personal)

**METGE** ((PK)*id_personal*, estudis, experiencia, id_especialitat)

ON (id_personal) REFERENCIA PERSONAL (id_personal)

ON (id_especialitat) REFERENCIA ESPECIALITAT (id_especialitat)

**INFERMER** ((PK)*id_personal*, curs, experiencia)

ON (id_personal) REFERENCIA PERSONAL (id_personal)

**INFERM_PLANTA** ((PK)*id_personal*, id_planta)

ON (id_personal) REFERENCIA INFERMER (id_personal)

ON (id_planta) REFERENCIA PLANTA (id_planta)

**INFERM_METGE** ((PK)*id_personal*, id_metge)

ON (id_personal) REFERENCIA INFERMER (id_personal)

ON (id_metge) REFERENCIA METGE (id_personal)

**HABITACIO** ((PK)*id_habitacio*, descripcio, id_planta)

ON (id_planta) REFERENCIA PLANTA (id_planta)

**QUIROFAN**((PK)*id_quirofan, id_planta)

ON (id_planta) REFERENCIA PLANTA (id_planta)

**VISITA** ((PK)*id_visita*, data_hora, diagnostic, id_metge, targeta_sanitaria)

ON (id_metge) REFERENCIA METGE (id_personal)

ON (tarjeta_sanitaria) REFERENCIA PACIENT (tarjeta_sanitaria)

**INGRES** ((PK)*id_ingres*, data_ingres, data_alta, targeta_sanitaria, id_habitacio)

ON (tarjeta_sanitaria) REFERENCIA PACIENT (tarjeta_sanitaria)

ON (id_habitacio) REFERENCIA HABITACIO (id_habitacio)

**OPERACIO** ((PK)*id_operacio*, descripcio, data_hora, targeta_sanitaria, id_metge, id_planta, id_quirofan)

ON (tarjeta_sanitaria) REFERENCIA PACIENT (tarjeta_sanitaria)

ON (id_metge) REFERENCIA METGE (id_personal)

ON (id_planta, id_quirofan) REFERENCIA QUIROFAN (id_planta, id_quirofan)

**QUIROFAN_APARELL** ((PK)*id_planta, id_quirofan, id_aparell*, quantitat)

ON (id_planta, id_quirofan) REFERENCIA QUIROFAN (id_planta, id_quirofan)

ON (id_aparell) REFERENCIA APARELL (id_aparell)

**VISITA_MEDICAMENT** ((PK)*id_visita, id_medicament*)

ON (id_visita) REFERENCIA VISITA (id_visita)

ON (id_medicament) REFERENCIA MEDICAMENT (id_medicament)

**OPERACIO_INFERMER** ((PK)*id_operacio, id_infermer*)

ON (id_operacio) REFERENCIA OPERACIO (id_operacio)

ON (id_infermer) REFERENCIA INFERMER (id_personal)