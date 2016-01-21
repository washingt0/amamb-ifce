from flask import Flask, request, render_template, session, url_for, redirect
from random import randint

app = Flask(__name__)

app.secret_key = 'ailovebeico'

#INDEX
@app.route("/")
def index():
	session['first'] = 0
	session['seccond']= 10
	session['count'] = 0
	return render_template("index.html")

#GERACAO DOS NUMEROS PARA A QUESTAO
@app.route("/solve")
def question():
	a = randint(session['first'], session['seccond']) #
	b = randint(session['first'], session['seccond']) #
	c = randint(session['first'], session['seccond']) #   GERA OS NUMEROS ALEATORIOS DENTRO DO NIVEL DO ALUNO
	d = randint(session['first'], session['seccond']) #
	#GERA A RESPOSTA PARA SER CONFERIDA
	session['resp']=a*b+c-d
	#MUDA O PARAMETRO VERIFICADOR DA RESPOSTA
	session['valid']=0
	return render_template("question.html", num1=a, num2=b, num3=c, num4=d, acertos=session['count'])

#PAGINA QUE FAZ A VERIFICACAO DA RESPOSTA E PONTUA NO CONTADOR DE ACERTOS 'count'
@app.route("/solve/teste", methods=['POST', 'GET'])
def teste():
	#RECEBE O VALOR QUE O USUARIO DIGITOU E ARMAZENA EM 'aluno'
	aluno = int(request.form['resposta'])
	#VERIFICA SE ELE JA RESPONDEU PELO MENOS 5 QUESTOES NO LEVEL ATUAL ANTES DE AUMENTAR O TAMANHO DOS NUMEROS
	if (session['count']%5==0) and (session['count']>1):
		session['first']+=10
		session['seccond']+=30

	#VERIFICA SE A RESPOSTA ESTA CERTA
	if aluno == session['resp']:
		if session['valid']==0:
			session['count']+=1 #SE SIM INCREMENTA O CONTADOR SE
			session['valid']=1
		return 'ok<br /> <a href="/solve">Continuar</a>'
	else:
		session['count']=0
		return 'errou <br /> <a href="/"> Reiniciar</a>'

#USAR O DEBUG APENAS ENQUANTO ESTIVER MEXENDO NO CODIGO
app.run(debug=False, use_reloader=True, host='0.0.0.0')
