from sqlite3 import connect as sqlite3_connect
from pymysql import connect as pymysql_connect

def db_init(db):
	schema = open('database/AMAMB_SQLite.sql')
	db.cursor().executescript(schema.read())
	schema.close()
	db.commit()

def db_connect(config):
	db = None
	if config['TESTING'] == True:
		db = sqlite3_connect(':memory:')
	elif config['DEBUG'] == True:
		db = sqlite3_connect(config['DB_NAME'] + '.db')
	else:
		db = pymysql_connect(host=config['MYSQL_DB_HOST'],user=config['MYSQL_DB_USER'],password=config['MYSQL_DB_PASSWORD'],database=config['DB_NAME'])
	return db
