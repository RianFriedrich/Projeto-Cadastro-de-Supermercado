import os
import mysql.connector
from mysql.connector import errorcode

DB_SERVER_USER = os.getenv('DB_SERVER_USER', 'root')
DB_SERVER_PASSWORD = os.getenv('DB_SERVER_PASSWORD', 'senha')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'supermercado_db')

DB_APP_USER = os.getenv('DB_APP_USER', 'app_user')
DB_APP_PASSWORD = os.getenv('DB_APP_PASSWORD', 'sua_senha_aqui')

DB_SERVER_CONFIG = {
    'user': DB_SERVER_USER,
    'password': DB_SERVER_PASSWORD,
    'host': DB_HOST,
}

DB_APP_CONFIG = {
    'user': DB_APP_USER,
    'password': DB_APP_PASSWORD,
    'host': DB_HOST,
    'database': DB_NAME,
}


def inicializar_banco_de_dados():
    try:
        print("Conectando ao servidor MySQL...")
        conexao_servidor = mysql.connector.connect(**DB_SERVER_CONFIG)
        cursor = conexao_servidor.cursor()
        print("Conexão bem-sucedida.")

        print(f"Verificando/criando banco de dados '{DB_NAME}'...")
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4")
        print("Banco de dados garantido.")

        cursor.execute(f"USE {DB_NAME}")

        try:
            cursor.execute(
                f"CREATE USER IF NOT EXISTS '{DB_APP_USER}'@'{DB_HOST}' IDENTIFIED BY '{DB_APP_PASSWORD}'"
            )
            cursor.execute(
                f"GRANT ALL PRIVILEGES ON {DB_NAME}.* TO '{DB_APP_USER}'@'{DB_HOST}'"
            )
            cursor.execute("FLUSH PRIVILEGES")
        except Exception:
            pass

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

        print("Verificando/criando tabela 'categorias'...")
        tabela_categorias_sql = """
        CREATE TABLE IF NOT EXISTS categorias (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nome VARCHAR(100) UNIQUE NOT NULL
        )
        """
        cursor.execute(tabela_categorias_sql)
        categorias_padrao = [
            'Mercearia', 'Hortifruti', 'Açougue', 'Padaria',
            'Bebidas', 'Limpeza', 'Higiene', 'Frios', 'Congelados',
            'Doces', 'Conveniência', 'Pet Shop', 'Infantil'
        ]
        for cat in categorias_padrao:
            try:
                cursor.execute(
                    "INSERT IGNORE INTO categorias (nome) VALUES (%s)",
                    (cat,)
                )
            except Exception:
                pass
        print("Tabela 'categorias' garantida.")

        cursor.close()
        conexao_servidor.close()
        print("Configuração do banco de dados concluída com sucesso!")
        return True

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print(
                "Erro Crítico: Acesso negado. Verifique seu nome de usuário e senha em 'database.py'.")
        else:
            print(f"Erro Crítico ao inicializar o banco de dados: {err}")
        return False
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return False


def get_db_connection():
    try:
        conexao = mysql.connector.connect(**DB_APP_CONFIG)
        return conexao
    except mysql.connector.Error as err:
        print(
            f"Não foi possível conectar ao banco de dados '{DB_NAME}': {err}")
        return None
