from flask import Flask, request, render_template, session, g, url_for, redirect
from database import db_connect, db_init
from random import randint
import rexpr
import hashlib


app = Flask(__name__)
app.config.from_object('config')
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')


def get_db():
    db = getattr(g, '_db_instance', None)
    if db is None:
        db = g._db_instance = db_connect(app.config)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_db_instance', None)
    if db is not None:
        db.close()


# INDEX
@app.route("/")
def index():
    # configura a dificuldade inicial
    session['difi'] = 1
    # condigura o contador de acertos
    session['count'] = 0
    # verificador para evitar o salto de questoes
    session['valid'] = 1
    # verificador para prova
    session['istest'] = 0
    return render_template("pages/index.jade")


# GERACAO DOS NUMEROS PARA A QUESTAO
@app.route("/solve")
def question():
    # verifica se a questao anterior foi respondida, se sim gera outra
    if session['valid']:
        banco = get_db().cursor()
        # verifiva se e uma prova
        if session['istest']:
            # verifica se ja respondeu todas as questoes
            if session['respondidas'] == session['qtd_quest']:
                # grava a resolucao no banco
                banco.execute("INSERT INTO RESOLUCOES(QTD_ACERTOS, NOME_ALUNO, PROVA) VALUES(?, ?, ?);",
                              (session['count'], session['alunoNome'], session['alunoProva']))
                get_db().commit()
                banco.close()
                # exibe os acertos
                return render_template("pages/mensagem.jade", mensagem="Acertos: ", variavel=session['count'])
            # se nao terminou gera uma nova questao a partir dos padroes da prova
            else:
                banco.execute("SELECT * FROM PROVA WHERE ID=?;", [session['alunoProva']])
                thisprova = banco.fetchone()
                session['difi'] = thisprova[3]
                tipoq = thisprova[2]
                banco.execute("SELECT ID FROM QUESTAO WHERE DIFICULDADE=? AND TIPO=?;", (session['difi'], tipoq))
                questao = banco.fetchall()
                quest = randint(0, len(questao)-1)
                banco.execute("SELECT * FROM QUESTAO WHERE ID=?;", [questao[quest][0]])
                questao = banco.fetchone()
                mod = questao[2]
        # se nao for prova busca questoes no banco baseado na dificuldade
        else:
            banco.execute("SELECT ID FROM QUESTAO WHERE DIFICULDADE=%s;" % (session['difi']))
            questao = banco.fetchall()
            quest = randint(0, len(questao)-1)
            banco.execute("SELECT * FROM QUESTAO WHERE ID=%s;" % (questao[quest][0]))
            questao = banco.fetchone()
            mod = questao[2]
        # compila a expressao
        expr, text, count = rexpr.compile(mod)
        args = []
        # gera 'count' argumentos randomicos
        for i in xrange(count):
            args.append(randint(questao[4], questao[5]))
        # resolve a expressao com os valores gerados
        result, args = rexpr.eval(expr, args)
        # armazena os valores para o caso de nao responder a questao
        session['respo'] = int(result)
        resp = hashlib.md5(str(int(result)) + "paodebatata")
        expressao = text.format(*tuple(args))
        session['quest'] = expressao
        banco.close()
    # pro caso da questao anterior nao ter sido resolvida
    else:
        result = session['respo']
        resp = hashlib.md5(str(int(result)) + "paodebatata")
        expressao = session['quest']
    # MUDA O PARAMETRO VERIFICADOR DA RESPOSTA
    session['valid'] = 0
    if session['istest']:
        return render_template("pages/question.jade", vari="Quantidade de questoes: ", acertos=session['qtd_quest'],
                               expressao=expressao, secret=resp.hexdigest())
    return render_template("pages/question.jade", vari="Acertos", expressao=expressao, acertos=session['count'],
                           secret=resp.hexdigest())


# PAGINA QUE FAZ A VERIFICACAO DA RESPOSTA E PONTUA NO CONTADOR DE ACERTOS 'count'
@app.route("/solve/teste", methods=['POST', 'GET'])
def teste():
    # RECEBE O VALOR QUE O USUARIO DIGITOU E ARMAZENA EM 'aluno'
    try:
        correcao = hashlib.md5(request.form['resposta'] + "paodebatata")
        aluno = correcao.hexdigest()
        gabarito = request.form['resp']
    except ValueError:
        if session['istest']:
            return redirect(url_for('question'))
        else:
            session['count'] = 0
            return render_template("pages/wrong.jade")

    # VERIFICA SE ELE JA RESPONDEU PELO MENOS 8 QUESTOES NO LEVEL ATUAL ANTES DE AUMENTAR O TAMANHO DOS NUMEROS
    if session['istest'] == 0:
        if (session['count'] % 8 == 0) and (session['count'] > 1):
            if session['difi'] < 3:
                session['difi'] += 1

    # verifica se e prova
    if session['istest']:
        # VERIFICA SE A RESPOSTA ESTA CERTA
        if aluno == gabarito:
            if session['valid'] == 0:
                session['respondidas'] += 1
                session['count'] += 1
                session['valid'] = 1
            return redirect(url_for('question'))
        else:
            session['respondidas'] += 1
            session['valid'] = 1
            return redirect(url_for('question'))
    else:
        # VERIFICA SE A RESPOSTA ESTA CERTA
        if aluno == gabarito:
            if session['valid'] == 0:
                session['count'] += 1  # SE SIM INCREMENTA O CONTADOR SE
                session['valid'] = 1
            return render_template("pages/okay.jade")
        else:
            session['count'] = 0
            return render_template("pages/wrong.jade")


# login para a prova
@app.route("/pre")
def pre():
    return render_template("pages/login_aluno.jade")


# confirma os dados da prova e prepara as variaveis
@app.route("/prova", methods=['POST', 'GET'])
def prova():
    try:
        session['alunoNome'] = request.form['nome']
        session['alunoEmail'] = request.form['email']
        session['alunoProva'] = request.form['prova']

    except ValueError:
        session['alunoNome'] = "Nao deu"
        session['alunoEmail'] = "Nao deu"
        session['alunoProva'] = "Nao deu"
    try:
        session['alunoProva'] = int(session['alunoProva'])
    except ValueError:
        return render_template("pages/mensagem.jade", mensagem="Prova Inexistente")
    banco = get_db().cursor()
    banco.execute("SELECT * FROM PROVA WHERE ID=?;", [session['alunoProva']])
    provas = banco.fetchone()
    banco.close()
    session['istest'] = 1
    session['qtd_quest'] = provas[4]
    session['respondidas'] = 0
    if provas:
        return render_template("pages/prova.jade", nome=session['alunoNome'],
                               email=session['alunoEmail'], prova=provas[0])
    else:
        return render_template("pages/mensagem.jade", mensagem="Prova Inexistente")


# funcao para adicionar novo usuario ao banco
def adduser(name, user, key):
    banco = get_db().cursor()
    passw = hashlib.md5(str(key) + "lolzinho")
    key = passw.hexdigest()
    banco.execute("INSERT INTO PROFESSOR(NOME, USUARIO, SENHA) VALUES(?, ?, ?);", (name, user, key))
    get_db().commit()
    banco.close()
    return 1


# funcao que tenta efetuar o login
def trylogin(user, key):
    password = hashlib.md5(str(key) + "lolzinho")
    key = password.hexdigest()
    banco = get_db().cursor()
    banco.execute("SELECT ID,SENHA FROM PROFESSOR WHERE USUARIO=?;", [user])
    senha = banco.fetchone()
    banco.close()
    if senha:
        if key == senha[1]:
            session['prof_logged'] = senha[0]
            return 1
        else:
            return 0
    return -1


# rota da pagina de logon
@app.route("/logar")
def logar():
    if 'logged' in session:
        if session['logged']:
            return render_template("pages/index_p.jade")
    return render_template("pages/login_prof.jade")


# rota da pagina inicial do professor
@app.route("/professor")
def professor():
    if session['logged']:
        return render_template("pages/index_p.jade")
    else:
        return redirect(url_for('logar'))


# rota para efetuar o logoff
@app.route("/logout")
def logout():
    session['logged'] = 0
    session['prof_logged'] = -1
    return redirect(url_for('index'))


# recebe os dados do formulario e tenta fazer o logon
@app.route("/login", methods=['POST', 'GET'])
def login():
    try:
        usuario = request.form.get('user')
        keypass = request.form.get('key')
    except ValueError:
        return render_template("pages/mensagem.jade", mensagem="Houve um erro")
    testes = trylogin(usuario, keypass)
    if testes == 1:
        session['logged'] = 1
        return render_template("pages/index_p.jade")
    elif testes == 0:
        return render_template("pages/mensagem.jade", mensagem="Senha Incorreta")
    elif testes == -1:
        return render_template("pages/mensagem.jade", mensagem="Usuario Inexistente")
    else:
        return render_template("pages/mensagem.jade", mensagem="Houve um erro")


# rota que mostra as resolucoes das provas de um professor
@app.route("/prof/res_prov", methods=['POST', 'GET'])
def res_prov():
    if session['logged']:
        banco = get_db().cursor()
        banco.execute("SELECT RESOLUCOES.NOME_ALUNO, RESOLUCOES.QTD_ACERTOS, RESOLUCOES.PROVA, PROVA.QTD_QUESTOES,"
                      " RESOLUCOES.EMAIL_ALUNO FROM RESOLUCOES, PROVA WHERE PROVA.ID=RESOLUCOES.PROVA AND "
                      "PROVA.PROFESSOR=?;", [session['prof_logged']])
        resultados = banco.fetchall()
        banco.close()
        if resultados:
            return render_template("pages/result.jade", mensagem="Resultados", resultado=resultados)
        else:
            return render_template("pages/mensagem.jade", mensagem="Nao ha dados")
    else:
        return redirect(url_for('logar'))


# rota para cadastro do professor
@app.route("/cad_prof")
def cad_prof():
    return render_template("pages/cad_prof.jade")


# rota para validar os dados e adicionaro professor ao banco
@app.route("/newprof", methods=['POST', 'GET'])
def newprof():
    receive = 0
    try:
        nome = request.form.get('nome')
        usuario = request.form.get('user')
        senha1 = request.form.get('key')
        senha2 = request.form.get('keyConfirm')
    except ValueError:
        return render_template("pages/mensagem.jade", mensagem="Os dados nao passaram na validacao")
    if senha1 == senha2:
        adduser(nome, usuario, senha1)
        return redirect(url_for(professor))
    if receive == 0:
        return render_template("pages/mensagem.jade", mensagem="Os dados nao passaram na validacao")


# rota para visualizar as provas de um professor
@app.route("/view_prov")
def view_prov():
    if session['logged']:
        banco = get_db().cursor()
        banco.execute("SELECT * FROM PROVA WHERE PROFESSOR=?;", [session['prof_logged']])
        resultados = banco.fetchall()
        banco.close()
        if resultados:
            return render_template("pages/view_prov.jade", mensagem="Provas", resultado=resultados)
        else:
            return render_template("pages/mensagem.jade", mensagem="Nao ha dados")
    else:
        return redirect(url_for('logar'))


# rota para cadastrar nova prova
@app.route("/cad_prov")
def cad_prov():
    if session['logged']:
        return render_template("pages/cad_prova.jade")
    else:
        return render_template("pages/login_prof.jade")


# rota que verifica os dados e insere a prova no banco
@app.route("/newprov", methods=['POST', 'GET'])
def newprov():
    if session['logged']:
        test = 1
        dific = tipo = qtd = 0
        try:
            dific = request.form.get('dificuldade')
            tipo = request.form.get('tipo')
            qtd = request.form.get('qtd')
        except ValueError:
            test = 0
        try:
            qtd = int(qtd)
        except ValueError:
            test = 0
        if test:
            banco = get_db().cursor()
            banco.execute("INSERT INTO PROVA(PROFESSOR, DIFICULDADE, TIPO, QTD_QUESTOES) VALUES(?, ?, ?, ?);",
                          (session['prof_logged'], dific, tipo, qtd))
            banco.execute("SELECT ID FROM PROVA WHERE QTD_QUESTOES=? AND PROFESSOR=? AND TIPO=? AND DIFICULDADE=?;"
                          "", (qtd, session['prof_logged'], tipo, dific))
            get_db().commit()
            idprova = banco.fetchone()
            banco.close()
            return render_template("pages/mensagem.jade", mensagem="Codigo da prova: ", variavel=idprova[0])
        else:
            return render_template("pages/mensagem.jade", mensagem="Os dados nao passaram na validacao")
    else:
        return redirect(url_for('logar'))


if __name__ == '__main__':
    def debug():
        import os.path
        if not os.path.isfile(app.config['DB_NAME'] + '.db'):
            db = db_connect(app.config)
            db_init(db)
            db.close()

    if app.config['DEBUG'] == True or app.config['TESTING'] == True:
        debug()
    app.run(host='0.0.0.0')
