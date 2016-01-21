from flask import Flask, request, render_template, session
from random import randint

app = Flask(__name__)

app.secret_key = 'ailovebeico'
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

@app.route("/")
def index():
	session['first'] = 0
	session['seccond']= 10
	session['count'] = 0
	return render_template("index.jade")

@app.route("/solve")
def question():
	a = randint(session['first'], session['seccond'])
	b = randint(session['first'], session['seccond'])
	c = randint(session['first'], session['seccond'])
	d = randint(session['first'], session['seccond'])
	session['resp']=a*b+c-d
	return render_template("question.html", num1=a, num2=b, num3=c, num4=d, acertos=session['count'])

@app.route("/solve/teste", methods=['POST', 'GET'])
def teste():
	aluno = int(request.form['resposta'])
	if session['count'] > 3:
		session['first']+=10
		session['seccond']+=30

	if aluno == session['resp']:
		session['count']+=1
		return 'ok<br /> <a href="/solve">Continuar</a>'
	else:
		session['count']=0
		return 'errou <br /> <a href="/"> Reiniciar</a>'

app.run(use_reloader=True, host='0.0.0.0')
