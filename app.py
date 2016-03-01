from flask import Flask, request, render_template, session, g
from database import db_connect, db_init
from login_prof import trylogin, adduser
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
def db_close():
    db = getattr(g, '_db_instance', None)
    if db is not None:
        db.close()


# INDEX
@app.route("/")
def index():
    session['first'] = 0
    session['seccond'] = 10
    session['count'] = 0
    # verificador para evitar o salto de questoes
    session['valid'] = 1
    # verificador para prova
    session['istest'] = 0
    return render_template("pages/index.jade")


# GERACAO DOS NUMEROS PARA A QUESTAO
@app.route("/solve")
def question():
    # escolhe um modelo de expressao
    # FIXME: mover para banco de dados!
    mod = app.config['EXPR_TEST_DB'][randint(0, len(app.config['EXPR_TEST_DB']) - 1)]
    # compila a expressao
    expr, text, count = rexpr.compile(mod)
    args = []
    # gera 'count' argumentos randomicos
    for i in xrange(count):
        args.append(randint(session['first'], session['seccond']))
    # verifica se a questao foi respondida
    if session['valid'] == 1:
        # resolve a expressao com os valores gerados
        result, args = rexpr.eval(expr, args)
        session['respo'] = int(result)
    else:
        result = session['respo']
    resp = hashlib.md5(str(int(result)) + "paodebatata")
    # verifica se a questao foi respondida
    if session['valid'] == 1:
        # monta string legivel da expressao
        expressao = text.format(*tuple(args))
        session['quest'] = expressao
    else:
        expressao = session['quest']
    # MUDA O PARAMETRO VERIFICADOR DA RESPOSTA
    session['valid'] = 0
    # se nao for uma prova, inicia normalmente
    if session['istest'] == 0:
        return render_template("pages/question.jade", expressao=expressao, acertos=session['count'],
                               secret=resp.hexdigest())
    # se for prova manda a questao para o layout de prova
    else:
        return render_template("pages/question_p.jade", expressao=expressao, secret=resp.hexdigest())


# PAGINA QUE FAZ A VERIFICACAO DA RESPOSTA E PONTUA NO CONTADOR DE ACERTOS 'count'
@app.route("/solve/teste", methods=['POST', 'GET'])
def teste():
    # RECEBE O VALOR QUE O USUARIO DIGITOU E ARMAZENA EM 'aluno'
    try:
        correcao = hashlib.md5(request.form['resposta'] + "paodebatata")
        aluno = correcao.hexdigest()
        gabarito = request.form['resp']
    except ValueError:
        session['count'] = 0
        return render_template("pages/wrong.jade")

    # VERIFICA SE ELE JA RESPONDEU PELO MENOS 5 QUESTOES NO LEVEL ATUAL ANTES DE AUMENTAR O TAMANHO DOS NUMEROS
    if (session['count'] % 5 == 0) and (session['count'] > 1):
        session['first'] += 10
        session['seccond'] += 30

    # VERIFICA SE A RESPOSTA ESTA CERTA
    if aluno == gabarito:
        if session['valid'] == 0:
            session['count'] += 1  # SE SIM INCREMENTA O CONTADOR SE
            session['valid'] = 1
        return render_template("pages/okay.jade")
    else:
        session['count'] = 0
        return render_template("pages/wrong.jade")


# prepara a variavel para a prova
@app.route("/pre")
def pre():
    session['istest'] = 1
    return render_template("pages/login_aluno.jade")


# confirma os dados da prova
@app.route("/prova", methods=['POST', 'GET'])
def prova():
    session['alunoNome'] = "Nao deu"
    session['alunoEmail'] = "Nao deu"
    session['alunoProva'] = "Nao deu"
    try:
        session['alunoNome'] = request.form['nome']
        session['alunoEmail'] = request.form['email']
        session['alunoProva'] = request.form['prova']
    except ValueError:
        session['alunoNome'] = "Nao deu"
        session['alunoEmail'] = "Nao deu"
        session['alunoProva'] = "Nao deu"
    return render_template("pages/prova.jade", nome=session['alunoNome'],
                           email=session['alunoEmail'], prova=session['alunoProva'])


@app.route("/logar")
def logar():
    return render_template("pages/login_prof.jade")


# tenta fazer o login
@app.route("/login", methods=['POST', 'GET'])
def login():
    try:
        usuario = request.form.get('user')
        keypass = request.form.get('key')
    except ValueError:
        return render_template("pages/error.jade")
    testes = trylogin(usuario, keypass)
    if testes == 1:
        return render_template("pages/success.jade")
    elif testes == 0:
        return render_template("pages/notsuccess.jade", error="Senha Incorreta")
    elif testes == -1:
        return render_template("pages/notsuccess.jade", error="Usuario Inexistente")
    else:
        return render_template("pages/error.jade")


@app.route("/cad_prof")
def cad_prof():
    return render_template("pages/cad_prof.jade")


@app.route("/newprof", methods=['POST', 'GET'])
def newprof():
    receive = 0
    try:
        usuario = request.form.get('user')
        senha1 = request.form.get('key')
        senha2 = request.form.get('keyConfirm')
    except ValueError:
        return render_template("pages/notsuccess.jade", error="Os dados nao passaram na validacao")
    if senha1 == senha2:
        adduser(usuario, senha1)
        return render_template("pages/success.jade")
    if receive == 0:
        return render_template("pages/notsuccess.jade", error="Os dados nao passaram na validacao")

        
if __name__ == '__main__':
    if app.config['DEBUG'] == True or app.config['TESTING'] == True:
        import os.path
        if not os.path.isfile(app.config['DB_NAME'] + '.db'):
            db = db_connect(app.config)
            db_init(db)
            db.close()
    app.run(host='0.0.0.0')
