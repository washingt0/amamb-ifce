from flask import Flask, request, render_template, session, url_for, redirect
from random import randint

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

#GERACAO DOS NUMEROS PARA A QUESTAO
@app.route("/solve")
def question():
	a = randint(session['first'], session['seccond']) #
	b = randint(session['first'], session['seccond']) #
	c = randint(session['first'], session['seccond']) #   GERA OS NUMEROS ALEATORIOS DENTRO DO NIVEL DO ALUNO
	d = randint(session['first'], session['seccond']) #
	v1 = chr(randint(42,45))
	v2 = chr(randint(42,45))
	v3 = chr(randint(42,45))
	if(v1==','):
		v1='-'
	if(v2==','):
		v2='+'
	if(v3==','):
		v3='*'
	#GERA A RESPOSTA PARA SER CONFERIDA
	if(v1=='+'):
		if(v2=='+'):
			if(v3=='+'):
				session['resp']=a+b+c+d
			elif(v3=='-'):
				session['resp']=a+b+c-d
			elif(v3=='*'):
				session['resp']=a+b+c*d
		elif(v2=='-'):
			if(v3=='+'):
				session['resp']=a+b-c+d
			elif(v3=='-'):
				session['resp']=a+b-c-d
			elif(v3=='*'):
				session['resp']=a+b-c*d
		elif(v2=='*'):
			if(v3=='+'):
				session['resp']=a+b*c+d
			elif(v3=='-'):
				session['resp']=a+b*c-d
			elif(v3=='*'):
				session['resp']=a+b*c*d
	elif(v1=='-'):
		if(v2=='+'):
			if(v3=='+'):
				session['resp']=a-b+c+d
			elif(v3=='-'):
				session['resp']=a-b+c-d
			elif(v3=='*'):
				session['resp']=a-b+c*d
		elif(v2=='-'):
			if(v3=='+'):
				session['resp']=a-b-c+d
			elif(v3=='-'):
				session['resp']=a-b-c-d
			elif(v3=='*'):
				session['resp']=a-b-c*d
		elif(v2=='*'):
			if(v3=='+'):
				session['resp']=a-b*c+d
			elif(v3=='-'):
				session['resp']=a-b*c-d
			elif(v3=='*'):
				session['resp']=a-b*c*d
	elif(v1=='*'):
		if(v2=='+'):
			if(v3=='+'):
				session['resp']=a*b+c+d
			elif(v3=='-'):
				session['resp']=a*b+c-d
			elif(v3=='*'):
				session['resp']=a*b+c*d
		elif(v2=='-'):
			if(v3=='+'):
				session['resp']=a*b-c+d
			elif(v3=='-'):
				session['resp']=a*b-c-d
			elif(v3=='*'):
				session['resp']=a*b-c*d
		elif(v2=='*'):
			if(v3=='+'):
				session['resp']=a*b*c+d
			elif(v3=='-'):
				session['resp']=a*b*c-d
			elif(v3=='*'):
				session['resp']=a*b*c*d
	#MUDA O PARAMETRO VERIFICADOR DA RESPOSTA
	session['valid']=0
	return render_template("pages/question.jade", num1=a, num2=b, num3=c, num4=d, acertos=session['count'], q1=v1, q2=v2, q3=v3 )

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
		return render_template("pages/okay.jade")
	else:
		session['count']=0
		return render_template("pages/wrong.jade")

#USAR O DEBUG APENAS ENQUANTO ESTIVER MEXENDO NO CODIGO
app.run(debug=True, use_reloader=True, host='0.0.0.0')
