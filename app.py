from flask import Flask, request, render_template, session, url_for, redirect
from random import randint
import rexpr

app = Flask(__name__)

app.secret_key = 'FQNHumNvRCy9fRbVTiiXewjDcsdeLV8scVjqUF7oV73xA6Z7hfiv9NWfUmnuLMcP'

app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

#INDEX
@app.route("/")
def index():
	session['first'] = 0
	session['seccond']= 10
	session['count'] = 0
	return render_template("pages/index.jade")

# expressoes apenas para testes
TEST_DB = [
	'1+1',
	'1+2',
	'1-2',
	'1+2-3',
	'1+2+3-1+4',
	'2*1',
	'1*2+1',
	'1+3-2',
	'1-3+4*2',
	'3*4+2+1*5',
]

#GERACAO DOS NUMEROS PARA A QUESTAO
@app.route("/solve")
def question():
	# escolhe um modelo de expressao
	mod = TEST_DB[ randint( 0, len(TEST_DB)-1 ) ]
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

#USAR O DEBUG APENAS ENQUANTO ESTIVER MEXENDO NO CODIGO
app.run(debug=True, use_reloader=True, host='0.0.0.0')
