"""
Configura a aplicacao para modo de debugging.
Recomendado desativar em ambiente de producao.
"""
DEBUG = True

"""
Chave secreta usada para encriptacao.
Usar valor padrao apenas em ambiente de desenvolvimento.
"""
SECRET_KEY = 'ailovebeico'

"""
Define o diretorio raiz sob o qual a aplicacao esta rodando.
Ex.:
	Para uma aplicacao rodando em `mysite.com` ou `myapp.mysite.com`
	o valor padrao `None` pode ser utilizado, caso a aplicacao
	esteja em `mysite.com/myapp/` alterar valor para `/myapp`
"""
APPLICATION_ROOT = None

"""
Configura a aplicacao para modo de testing.
Ativar apenas para execucao de testes.
"""
TESTING = False

"""
Configuracao temporaria para testes de expressoes.
"""
# FIXME: mover para banco de dados!
EXPR_TEST_DB = [
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
