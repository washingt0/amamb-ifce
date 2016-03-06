"""
Configura a aplicacao para modo de debugging.
Recomendado desativar em ambiente de producao.
"""
DEBUG = False

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
Nome do banco SQL a ser utilizado pela aplicacao.
"""
DB_NAME = 'amamb'

"""
Host do banco de dados MySQL.
"""
MYSQL_DB_HOST = 'localhost'

"""
Nome de usuario do banco de dados.
"""
MYSQL_DB_USER = 'amamb'

"""
Senha do banco de dados.
"""
MYSQL_DB_PASSWORD = 'amamb123'
