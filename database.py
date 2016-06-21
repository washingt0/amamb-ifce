from sqlite3 import connect as sqlite3_connect
from pymysql import connect as pymysql_connect
from sqlite3 import Connection as sqlite3Connection

GLOBAL_QUERY = {
    # insere prova
    'INSERE_PROVA': [
        'INSERT INTO PROVA(PROFESSOR, DIFICULDADE, TIPO, QTD_QUESTOES) VALUES(?, ?, ?, ?);',
        'INSERT INTO PROVA(PROFESSOR, DIFICULDADE, TIPO, QTD_QUESTOES) VALUES(%s, %s, %s, %s);'
    ],
    'SELECT_PROVA':[
        'SELECT * FROM PROVA WHERE ID=?;',
        'SELECT * FROM PROVA WHERE ID=%s;'
    ],
    # pega a id da prova inserida
    'SELECT_ID_PROVA': [
        'SELECT ID FROM PROVA WHERE QTD_QUESTOES=? AND PROFESSOR=? AND TIPO=? AND DIFICULDADE=?;',
        'SELECT ID FROM PROVA WHERE QTD_QUESTOES=%s AND PROFESSOR=%s AND TIPO=%s AND DIFICULDADE=%s;'
    ],
    'SELECT_PROVA_PROF': [
        'SELECT * FROM PROVA WHERE PROFESSOR=?;',
        'SELECT * FROM PROVA WHERE PROFESSOR=%s;'
    ],
    'INSERT_RESOLUCAO': [
        'INSERT INTO RESOLUCOES(QTD_ACERTOS, NOME_ALUNO, PROVA, EMAIL_ALUNO) VALUES(?, ?, ?, ?);',
        'INSERT INTO RESOLUCOES(QTD_ACERTOS, NOME_ALUNO, PROVA, EMAIL_ALUNO) VALUES(%s, %s, %s, %s);'
    ],
    'SELECT_RESOLUCAO': [
        'SELECT RESOLUCOES.NOME_ALUNO, RESOLUCOES.QTD_ACERTOS, RESOLUCOES.PROVA, PROVA.QTD_QUESTOES, '
        'RESOLUCOES.EMAIL_ALUNO FROM RESOLUCOES, PROVA WHERE PROVA.ID=RESOLUCOES.PROVA AND PROVA.PROFESSOR=?;',
        'SELECT RESOLUCOES.NOME_ALUNO, RESOLUCOES.QTD_ACERTOS, RESOLUCOES.PROVA, PROVA.QTD_QUESTOES,'
        ' RESOLUCOES.EMAIL_ALUNO FROM RESOLUCOES, PROVA WHERE PROVA.ID=RESOLUCOES.PROVA AND PROVA.PROFESSOR=%s;'
    ],
    'SELECT_LOGIN': [
        'SELECT ID, SENHA, NOME, ATIVO FROM PROFESSOR WHERE USUARIO=?;',
        'SELECT ID, SENHA, NOME, ATIVO FROM PROFESSOR WHERE USUARIO=%s;'
    ],
    'INSERT_PROF': [
        'INSERT INTO PROFESSOR(NOME, EMAIL, USUARIO, SENHA, ATIVO) VALUES(?, ?, ?, ?, 0);',
        'INSERT INTO PROFESSOR(NOME, EMAIL, USUARIO, SENHA, ATIVO) VALUES(%s, %s, %s, %s, 0);'
    ],
    'SELECT_QUESTAO_ID': [
        'SELECT * FROM QUESTAO WHERE ID=?;',
        'SELECT * FROM QUESTAO WHERE ID=%s;'
    ],
    'SELECT_ID_QUESTAO_DIF': [
        'SELECT ID FROM QUESTAO WHERE DIFICULDADE=?;',
        'SELECT ID FROM QUESTAO WHERE DIFICULDADE=%s;'
    ],
    'SELECT_ID_QUESTAO_TIP_DIF': [
        'SELECT ID FROM QUESTAO WHERE DIFICULDADE=? AND TIPO=?;',
        'SELECT ID FROM QUESTAO WHERE DIFICULDADE=%s AND TIPO=%s;'
    ],
    'INSERT_EMAIL_TEMP': [
        'INSERT INTO ACTIVATE(EMAIL, MD5) VALUES(?, ?);',
        'INSERT INTO ACTIVATE(EMAIL, MD5) VALUES(%s, %s);'
    ],
    'SELECT_EMAIL_TEMP':[
        'SELECT EMAIL FROM ACTIVATE WHERE MD5=?;',
        'SELECT EMAIL FROM ACTIVATE WHERE MD5=%s;'
    ],
    'REMOVE_EMAIL_TEMP':[
        'DELETE FROM ACTIVATE WHERE MD5=?;',
        'DELETE FROM ACTIVATE WHERE MD5=%s;'
    ],
    'CONFIRMA_EMAIL':[
        'UPDATE PROFESSOR SET ATIVO=1 WHERE EMAIL=?;',
        'UPDATE PROFESSOR SET ATIVO=1 WHERE EMAIL=%s;'
    ]

}


def db_query(db, query):
    if isinstance(db, sqlite3Connection):
        return GLOBAL_QUERY[query][0]
    else:
        return GLOBAL_QUERY[query][1]


def db_init(db):
    schema = open('database/AMAMB_SQLite.sql')
    db.cursor().executescript(schema.read())
    schema.close()
    db.commit()


def db_connect(config):
    db = None
    if config['TESTING']:
        db = sqlite3_connect(':memory:')
    elif config['DEBUG']:
        db = sqlite3_connect(config['DB_NAME'] + '.db')
    else:
        db = pymysql_connect(host=config['MYSQL_DB_HOST'], user=config['MYSQL_DB_USER'],
                             password=config['MYSQL_DB_PASSWORD'], database=config['DB_NAME'])
    return db
