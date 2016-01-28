from flask import Flask, request, render_template, session
from random import randint
import rexpr

app = Flask(__name__)
app.config.from_object('config')
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

#INDEX
@app.route("/")
def index():
	session['first'] = 0
	session['seccond']= 10
	session['count'] = 0
	return render_template("pages/index.jade")

#GERACAO DOS NUMEROS PARA A QUESTAO
@app.route("/solve")
def question():
	# escolhe um modelo de expressao
	# FIXME: mover para banco de dados!
	mod = app.config['EXPR_TEST_DB'][ randint( 0, len(app.config['EXPR_TEST_DB'])-1 ) ]
	# compila a expressao
	expr, text, count = rexpr.compile(mod)
	args = []
	# gera 'count' argumentos randomicos
	for i in xrange(count) :
		args.append( randint( session['first'], session['seccond'] ) )
	# resolve a expressao com os valores gerados
	session['resp'] = rexpr.eval(expr,args)
	# monta string legivel da expressao
	expressao = text.format(*tuple(args))
	#MUDA O PARAMETRO VERIFICADOR DA RESPOSTA
	session['valid']=0
	return render_template("pages/question.jade", expressao=expressao, acertos=session['count'])

#PAGINA QUE FAZ A VERIFICACAO DA RESPOSTA E PONTUA NO CONTADOR DE ACERTOS 'count'
@app.route("/solve/teste", methods=['POST', 'GET'])
def teste():
	#RECEBE O VALOR QUE O USUARIO DIGITOU E ARMAZENA EM 'aluno'
	try:
		aluno = int(request.form['resposta'])
	except ValueError:
		session['count']=0
		return render_template("pages/wrong.jade")

	#VERIFICA SE ELE JA RESPONDEU PELO MENOS 5 QUESTOES NO LEVEL ATUAL ANTES DE AUMENTAR O TAMANHO DOS NUMEROS
	if (session['count']%5==0) and (session['count']>1):
		session['first']+=10
		session['seccond']+=30

	#VERIFICA SE A RESPOSTA ESTA CERTA
	if aluno == session['resp']:
		if session['valid']==0:
			session['count']+=1 #SE SIM INCREMENTA O CONTADOR SE
			session['valid']=1
		return render_template("pages/okay.jade")
	else:
		session['count']=0
		return render_template("pages/wrong.jade")

if __name__ == '__main__' :
	app.run(host='0.0.0.0')
