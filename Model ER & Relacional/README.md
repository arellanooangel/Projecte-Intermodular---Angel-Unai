**MODEL ER** 

En la creació d'aquest model ER ens hem topat amb reptes i hem tingut algunes consideracions.  
Considerem que el personal pot tenir més d'un usuari, per evitar-nos problemes a futur.  
Pensem que és més correcte tenir generalitzacions a l'hora de guardar el personal, per saber quin és el seu treball.  
Considerem que els quiròfans es troben a les plantes, però el nom de quiròfan no és únic. A la planta 1 trobem el Q1 i Q2 i a la planta 2 també trobem el Q1 i Q2, fent aquesta una entitat feble.  
Considerem que a una operació hi pot haver més d'un infermer.  
Pel que fa als atributs, quan especifiquem data_hora, veuríem un TIMESTAMP en passar-ho a SQL. En canvi, quan fiquem qualsevol altra data (com ara data_alta o data_naixement), aquest serà un camp DATE, ja que l'hora no és necessària en aquests casos.  
Creiem que camps com estudis, experiència, i similars, no han de ser limitats com a VARCHAR, perquè guardarem una quantitat de dades que actualment no sabem que tan gran són.  
Ens hem reservat l'opció d'afegir més atributs si fossin necessaris en un futur.