import app as amamb
import unittest
import tempfile
import os

class MainTestCase(unittest.TestCase):
    """
    Encapsula testes principais.
    """

    """
    Prepara execucao dos testes.
    """
    def setUp(self):
        print 'Configurando testes...'
        amamb.app.config['TESTING'] = True

        print 'Configurando banco de dados.'
        db_file = tempfile.mkstemp()
        self.db_fd = db_file[0]
        amamb.app.config['DB_NAME'] = db_file[1]

        print 'Iniciando aplicacao.'
        amamb.init_debug()

        self.client = amamb.app.test_client()

    """
    Solicita paginas principais da aplicacao.
    """
    def test_default_pages(self):
        print 'Executando testes de paginas principais...'
        # Paginas padrao
        # Pagina inicial
        assert self.client.get('/').status_code == 200
        # Creditos
        assert self.client.get('/creditos').status_code == 200
        # Pratica
        assert self.client.get('/solve').status_code == 200

        # Formularios
        # Fazer prova
        assert self.client.get('/pre').status_code == 200
        # Login
        assert self.client.get('/logar').status_code == 200
        # Cadastro de professor
        assert self.client.get('/cad_prof').status_code == 200
        # Recuperar senha
        assert self.client.get('/forgot').status_code == 200
        # Alterar senha
        assert self.client.get('/change').status_code == 200
    
    def tearDown(self):
        print 'Finalizando testes.'
        os.close(self.db_fd)
        os.unlink(amamb.app.config['DB_NAME'])

if __name__ == '__main__':
    unittest.main()
