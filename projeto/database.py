import mysql.connector
from mysql.connector import errorcode

# --- ÚNICO LUGAR PARA CONFIGURAR O BANCO DE DADOS ---
# Altere estes valores para corresponder à sua configuração do MySQL.
# O usuário 'root' é usado aqui para a configuração inicial.
# Lembre-se de trocar 'sua_senha_do_root' pela senha real do seu usuário root do MySQL.
DB_SERVER_CONFIG = {
    'user': 'root',
    'password': 'senha', # IMPORTANTE: Troque esta senha!
    'host': 'localhost'
}

DB_NAME = 'supermercado_db'

# Configuração para a aplicação usar depois que o banco for criado
DB_APP_CONFIG = {
    'user': 'root', # Ou o 'app_user' que você pode criar
    'password': 'senha', # IMPORTANTE: Troque esta senha!
    'host': 'localhost',
    'database': DB_NAME
}


def inicializar_banco_de_dados():
    """
    Verifica e cria o banco de dados e a tabela 'produtos' se não existirem.
    Retorna True se tudo estiver OK, False se ocorrer um erro crítico.
    """
    try:
        # 1. Conecta-se ao SERVIDOR MySQL (sem especificar um banco de dados)
        print("Conectando ao servidor MySQL...")
        conexao_servidor = mysql.connector.connect(**DB_SERVER_CONFIG)
        cursor = conexao_servidor.cursor()
        print("Conexão bem-sucedida.")

        # 2. Cria o banco de dados se ele não existir
        print(f"Verificando/criando banco de dados '{DB_NAME}'...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4")
        print("Banco de dados garantido.")
        
        # 3. Usa o banco de dados recém-criado/existente
        cursor.execute(f"USE {DB_NAME}")

        # 4. Cria a tabela de produtos se ela não existir
        print("Verificando/criando tabela 'produtos'...")
        tabela_produtos_sql = """
        CREATE TABLE IF NOT EXISTS produtos (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nome VARCHAR(255) NOT NULL,
            codigo_barras VARCHAR(100) UNIQUE NOT NULL,
            preco DECIMAL(10, 2) NOT NULL,
            estoque INT NOT NULL,
            categoria VARCHAR(100)
        )
        """
        cursor.execute(tabela_produtos_sql)
        print("Tabela 'produtos' garantida.")

        cursor.close()
        conexao_servidor.close()
        print("Configuração do banco de dados concluída com sucesso!")
        return True

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro Crítico: Acesso negado. Verifique seu nome de usuário e senha em 'database.py'.")
        else:
            print(f"Erro Crítico ao inicializar o banco de dados: {err}")
        return False
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return False

def get_db_connection():
    """
    Cria e retorna uma conexão com o banco de dados da aplicação.
    """
    try:
        conexao = mysql.connector.connect(**DB_APP_CONFIG)
        return conexao
    except mysql.connector.Error as err:
        # A inicialização já deve ter falhado, mas é bom ter um fallback.
        print(f"Não foi possível conectar ao banco de dados '{DB_NAME}': {err}")
        return None