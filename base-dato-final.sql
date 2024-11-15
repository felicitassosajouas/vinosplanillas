CREATE DATABASE finalprogramacion;
USE finalprogramacion;
 DROP TABLE if EXISTS usuario;
 DROP TABLE IF EXISTS solicitudMuestra;
create table usuario (
	id int auto_increment primary key,
   nombre varchar(100),
   email varchar(100),
   contraseña VARCHAR(255)
);


CREATE TABLE solicitudMuestra (
	id INT AUTO_INCREMENT PRIMARY KEY,
    rcqln INT,
    vigencia VARCHAR(100),
    revision INT(200),
    fecha VARCHAR(100),
    laboratorio VARCHAR(100),
    vinoMosto VARCHAR(50),
    codigo INT(200),
    densidad VARCHAR(150),
    extDens VARCHAR(150),
    bx VARCHAR(150),
    alcAlcolyzer VARCHAR(150),
    alcDest VARCHAR(150),
    azQco VARCHAR(150),
    foss VARCHAR(150),
    so2lt VARCHAR(150),
    so2Real VARCHAR(150),
    so2Rankine VARCHAR(150),
    atTitulable VARCHAR(150),
    avDestilacion VARCHAR(150),
    colorEspectro VARCHAR(150),
    oxigeno VARCHAR(150),
    co2 VARCHAR(150),
    rcih VARCHAR(150),
    rProtCalor VARCHAR(150),
    hierro VARCHAR(150),
    cobre VARCHAR(150),
    potasio VARCHAR(150),
    sorbato VARCHAR(150),
    purezaVarietal VARCHAR(150),
    matColArt VARCHAR(150),
    calcio VARCHAR(150),
    cloruros VARCHAR(150),
    sulfatos VARCHAR(150),
    ferro VARCHAR(150),
    checkStab VARCHAR(150),
    filtrabilidad VARCHAR(150),
    pruebaFrio VARCHAR(150),
    npa VARCHAR(150),
    polifTotales VARCHAR(150),
    rtoViabilidad VARCHAR(150),
    ntu VARCHAR(150)
);

ALTER TABLE solicitudMuestra
ADD COLUMN tipovino VARCHAR(50) FIRST;

ALTER TABLE solicitudMuestra
ADD COLUMN sectorproveniente VARCHAR(50) AFTER tipovino;

CREATE TABLE vinosproceso(
id INT AUTO_INCREMENT PRIMARY KEY,
tipodevino 	VARCHAR(50),
variedaddeuva VARCHAR(50),
numerovasija VARCHAR(50),
metodosvinificacion VARCHAR(50)
);

CREATE TABLE vinosterminados(
id INT AUTO_INCREMENT PRIMARY KEY,
tipodevino 	VARCHAR(50),
numerovasija VARCHAR(50),
destinofinal VARCHAR(50)
);



CREATE TABLE ordentrabajo (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sector VARCHAR(100) NOT NULL,
    operario VARCHAR(100) NOT NULL,
    fecha DATE NOT NULL,
    detalles_tarea TEXT,
    encargado_a_cargo VARCHAR(100) NOT NULL
);

DESCRIBE solicitudMuestra;

SELECT * FROM ordentrabajo;
SELECT * FROM vinosproceso;
select * from solicitudmuestra;
SELECT * FROM usuario;
ALTER TABLE solicitudMuestra MODIFY COLUMN rcqln INT AUTO_INCREMENT;