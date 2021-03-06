CREATE DATABASE amamb DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;

USE amamb;

CREATE TABLE PROFESSOR(
	ID INT NOT NULL AUTO_INCREMENT,
	NOME VARCHAR(50),
	EMAIL VARCHAR(50),
	USUARIO VARCHAR(30),
	SENHA VARCHAR(50),
	ATIVO SMALLINT(1),
	PRIMARY KEY(ID),
	UNIQUE(USUARIO),
	UNIQUE(EMAIL)
)DEFAULT CHARACTER SET=utf8  COLLATE=utf8_general_ci;

CREATE TABLE QUESTAO(
	ID INT NOT NULL AUTO_INCREMENT,
	TIPO INT,
	MODELO VARCHAR(50),
	DIFICULDADE INT,
  RANGE_MIN INT,
	RANGE_MAX INT,
	PRIMARY KEY(ID),
	UNIQUE(MODELO)
)DEFAULT CHARACTER SET=utf8  COLLATE=utf8_general_ci;

CREATE TABLE PROVA(
	ID INT NOT NULL AUTO_INCREMENT,
	PROFESSOR INT,
	TIPO INT,
	DIFICULDADE INT,
	QTD_QUESTOES INT,
	PRIMARY KEY(ID),
	FOREIGN KEY(PROFESSOR) REFERENCES PROFESSOR(ID)
)DEFAULT CHARACTER SET=utf8  COLLATE=utf8_general_ci;
ALTER TABLE PROVA AUTO_INCREMENT=100100;

CREATE TABLE RESOLUCOES(
	ID INT NOT NULL AUTO_INCREMENT,
	QTD_ACERTOS INT,
	NOME_ALUNO VARCHAR(30),
	EMAIL_ALUNO VARCHAR(100),
	PROVA INT,
	PRIMARY KEY(ID), 
	FOREIGN KEY(PROVA) REFERENCES PROVA(ID)
)DEFAULT CHARACTER SET=utf8  COLLATE=utf8_general_ci;

CREATE TABLE ACTIVATE(
  EMAIL VARCHAR(50),
  MD5 VARCHAR(50),
  UNIQUE(MD5)
)DEFAULT CHARACTER SET=utf8  COLLATE=utf8_general_ci;

INSERT INTO QUESTAO(TIPO, MODELO, DIFICULDADE, RANGE_MIN, RANGE_MAX) VALUES
  ('1','1+2','1','0','10'),
  ('1','1+1+3','1','0','10'),
  ('1','1-2','1','0','10'),
  ('1','1-2-3','1','0','10'),
  ('1','1-2-2','1','0','10'),
  ('1','1+2-3','1','0','10'),
  ('2','1*2','1','0','5'),
  ('2','1*2*3','1','0','5'),
  ('2','1*2*2','1','0','5'),
  ('3','1/2','1','0','5'),
  ('3','1/2-1','1','0','5'),
  ('3','1/2+1','1','0','5'),
  ('3','1/2+2*1/3','1','0','5'),
  ('3','1/2-2*1/3','1','0','5'),
  ('1','1+2+3+4','2','0','20'),
  ('1','1-2+3-4','2','0','20'),
  ('1','1+2-3-4','2','0','20'),
  ('2','1+(2+[3*1]+4)','2','0','10'),
  ('2','1+(2-[3*1]-4)','2','0','10'),
  ('2','1+(2+[3*{1*2}]-1-[4*{3*1}])','2','0','10'),
  ('2','1-(2-[3*{1*2}]+1+[4*{3*1}])','2','0','10'),
  ('3','1-4/2+3-3/1','2','0','10'),
  ('3','1+4/2+3+3/1','2','0','10'),
  ('3','1-(2*[4/2+{3/1}-1])','2','0','10'),
  ('3','1+(2*[4/2-{3/1}-1])','2','0','10'),
  ('3','1-(2*[4/2-{3/1}+1])','2','0','10'),
  ('1','(1+2)-(3+4)+(3+1)-(5+2)','3','0','50'),
  ('1','(1+2)-[{3+4}+{3+2}]-(4+2)','3','0','50'),
  ('1','(1+2)-[{3+4}+{{5+4}-{3+2}}-{3+1}]-(4+2)','3','0','50'),
  ('1','(1+2)+[{3+4}+{{1+2}+{3+2}}+{3+1}]+(4+2)','3','0','50'),
  ('2','1-(1*2*3)+(1*2*4)-4','3','0','15'),
  ('2','1+(1*2*[3-4-2*{2-1}]-2*4)','3','0','15'),
  ('2','1-(1*2*[3+4+1*{2-1}]-2*4)','3','0','15'),
  ('2','1+(1*2*[3-4-5*{2+1}]+2*4)','3','0','15'),
  ('3','2-4/2+3-3/1','3','0','15'),
  ('3','2+4/2+3+3/1','3','1','15'),
  ('3','2-(2*[4/2+{3/1}-1])','3','1','15'),
  ('3','2+(2*[4/2-{3/1}-1])','3','1','15'),
  ('3','2-(2*[4/2-{3/1}+1])','3','1','15'),
  ('4','1^2','3','0','10'),
  ('5','q(1)','3','10','100')