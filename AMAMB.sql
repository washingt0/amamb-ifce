CREATE DATABASE AMAMB;

USE AMAMB;

CREATE TABLE PROFESSOR(
	ID INT NOT NULL,
	NOME VARCHAR(10),
	USUARIO VARCHAR(10),
	SENHA VARCHAR(50),
	PRIMARY KEY(ID),
	UNIQUE KEY(USUARIO)
);

CREATE TABLE QUESTAO(
	ID INT NOT NULL,
	TIPO INT,
	MODELO VARCHAR(30),
	DIFICULDADE INT,
	PRIMARY KEY(ID),
	UNIQUE KEY(MODELO)
);

CREATE TABLE PROVA(
	ID INT NOT NULL,
	PROFESSOR INT,
	TIPO INT,
	DIFICULDADE INT,
	QTD_QUESTOES INT,
	PRIMARY KEY(ID),
	FOREIGN KEY(PROFESSOR) REFERENCES PROFESSOR(ID)
);

CREATE TABLE RESOLUCOES(
	ID INT NOT NULL,
	QTD_ACERTOS INT,
	EMAIL VARCHAR(80),
	NOME_ALUNO VARCHAR(20),
	PROVA INT,
	PRIMARY KEY(ID,EMAIL,PROVA), 
	FOREIGN KEY(PROVA) REFERENCES PROVA(ID)
);