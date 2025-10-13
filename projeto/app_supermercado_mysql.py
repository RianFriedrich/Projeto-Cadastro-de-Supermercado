import sys
import mysql.connector # Ainda necessário para o tratamento de erros específicos
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QComboBox
)
from PySide6.QtCore import Qt

# --- 1. Importar as funções do nosso novo arquivo ---
from database import inicializar_banco_de_dados, get_db_connection

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        # ... (toda a configuração da janela, como setWindowTitle, setGeometry, etc., continua a mesma) ...
        self.setWindowTitle("Sistema de Cadastro de Produtos - Supermercado (MySQL)")
        self.setGeometry(100, 100, 900, 600)

        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)

        self.layout_principal = QVBoxLayout(self.widget_central)
        self.layout_formulario = QGridLayout()
        
        self.aplicar_estilo()
        self.criar_formulario()
        self.criar_tabela()

        self.layout_principal.addLayout(self.layout_formulario)
        self.layout_principal.addWidget(self.tabela_produtos)
        
        self.carregar_produtos()


    def aplicar_estilo(self):
        # O estilo (QSS) permanece o mesmo, sem alterações
        self.setStyleSheet("""
            QWidget { background-color: #f0f0f0; font-family: Arial, sans-serif; }
            QLabel { font-size: 14px; font-weight: bold; }
            QLineEdit, QComboBox { font-size: 14px; padding: 8px; border: 1px solid #ccc; border-radius: 4px; background-color: #fff; }
            QPushButton { font-size: 16px; font-weight: bold; padding: 10px; border-radius: 5px; background-color: #007bff; color: white; }
            QPushButton:hover { background-color: #0056b3; }
            QTableWidget { background-color: white; border: 1px solid #ccc; font-size: 13px; gridline-color: #e0e0e0; }
            QHeaderView::section { background-color: #f2f2f2; padding: 5px; border: 1px solid #ccc; font-size: 14px; font-weight: bold; }
        """)
        
    def criar_formulario(self):
        # A criação do formulário permanece a mesma, sem alterações
        self.label_nome = QLabel("Nome do Produto:")
        self.label_codigo = QLabel("Código de Barras:")
        self.label_preco = QLabel("Preço (R$):")
        self.label_estoque = QLabel("Estoque (Unid.):")
        self.label_categoria = QLabel("Categoria:")
        self.input_nome = QLineEdit()
        self.input_codigo = QLineEdit()
        self.input_preco = QLineEdit()
        self.input_estoque = QLineEdit()
        self.input_categoria = QComboBox()
        self.input_categoria.addItems(["Mercearia", "Hortifruti", "Açougue", "Padaria", "Bebidas", "Limpeza", "Higiene"])
        self.botao_cadastrar = QPushButton("Cadastrar Produto")
        self.botao_cadastrar.clicked.connect(self.cadastrar_produto)
        self.layout_formulario.addWidget(self.label_nome, 0, 0); self.layout_formulario.addWidget(self.input_nome, 1, 0)
        self.layout_formulario.addWidget(self.label_codigo, 0, 1); self.layout_formulario.addWidget(self.input_codigo, 1, 1)
        self.layout_formulario.addWidget(self.label_preco, 2, 0); self.layout_formulario.addWidget(self.input_preco, 3, 0)
        self.layout_formulario.addWidget(self.label_estoque, 2, 1); self.layout_formulario.addWidget(self.input_estoque, 3, 1)
        self.layout_formulario.addWidget(self.label_categoria, 4, 0); self.layout_formulario.addWidget(self.input_categoria, 5, 0)
        self.layout_formulario.addWidget(self.botao_cadastrar, 5, 1, 1, 1, Qt.AlignmentFlag.AlignRight)

    def criar_tabela(self):
        # A criação da tabela permanece a mesma, sem alterações
        self.tabela_produtos = QTableWidget()
        self.tabela_produtos.setColumnCount(6)
        self.tabela_produtos.setHorizontalHeaderLabels(["ID", "Nome", "Cód. Barras", "Preço (R$)", "Estoque", "Categoria"])
        header = self.tabela_produtos.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.tabela_produtos.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    def cadastrar_produto(self):
        # Lógica de validação dos campos permanece a mesma
        nome = self.input_nome.text()
        codigo = self.input_codigo.text()
        preco_texto = self.input_preco.text().replace(',', '.')
        estoque_texto = self.input_estoque.text()
        categoria = self.input_categoria.currentText()
        if not all([nome, codigo, preco_texto, estoque_texto]):
            QMessageBox.warning(self, "Atenção", "Todos os campos devem ser preenchidos!")
            return
        try:
            preco = float(preco_texto)
            estoque = int(estoque_texto)
        except ValueError:
            QMessageBox.warning(self, "Erro de Formato", "Preço e Estoque devem ser números válidos!")
            return
        
        conexao = None
        try:
            # --- 2. Usar a nova função para obter a conexão ---
            conexao = get_db_connection()
            if conexao is None:
                QMessageBox.critical(self, "Erro de Conexão", "Não foi possível conectar ao banco de dados para cadastrar.")
                return

            cursor = conexao.cursor()
            query = "INSERT INTO produtos (nome, codigo_barras, preco, estoque, categoria) VALUES (%s, %s, %s, %s, %s)"
            valores = (nome, codigo, preco, estoque, categoria)
            cursor.execute(query, valores)
            conexao.commit()
            
            QMessageBox.information(self, "Sucesso", "Produto cadastrado com sucesso!")
            self.limpar_campos()
            self.carregar_produtos()
            
        except mysql.connector.IntegrityError:
            QMessageBox.warning(self, "Erro", f"O código de barras '{codigo}' já existe no banco de dados!")
        except Exception as e:
            QMessageBox.critical(self, "Erro Crítico", f"Ocorreu um erro inesperado: {e}")
        finally:
            if conexao and conexao.is_connected():
                cursor.close()
                conexao.close()

    def carregar_produtos(self):
        conexao = None
        try:
            # --- 3. Usar a nova função aqui também ---
            conexao = get_db_connection()
            if conexao is None:
                QMessageBox.critical(self, "Erro de Conexão", "Não foi possível conectar ao banco para carregar os produtos.")
                return

            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, codigo_barras, preco, estoque, categoria FROM produtos ORDER BY nome")
            produtos = cursor.fetchall()

            # Lógica para popular a tabela continua a mesma
            self.tabela_produtos.setRowCount(len(produtos))
            for linha, produto in enumerate(produtos):
                for coluna, valor in enumerate(produto):
                    if coluna == 3:
                       valor_item = QTableWidgetItem(f"{valor:.2f}")
                    else:
                       valor_item = QTableWidgetItem(str(valor))
                    self.tabela_produtos.setItem(linha, coluna, valor_item)

        except Exception as e:
            QMessageBox.critical(self, "Erro ao Carregar", f"Não foi possível carregar os produtos: {e}")
        finally:
            if conexao and conexao.is_connected():
                cursor.close()
                conexao.close()

    def limpar_campos(self):
        self.input_nome.clear()
        self.input_codigo.clear()
        self.input_preco.clear()
        self.input_estoque.clear()

# --- 4. Bloco Principal de Execução (A MUDANÇA MAIS IMPORTANTE) ---
if __name__ == "__main__":
    # Primeiro, tenta inicializar o banco de dados
    if inicializar_banco_de_dados():
        # Se a inicialização for bem-sucedida, inicia a aplicação gráfica
        app = QApplication(sys.argv)
        janela = JanelaPrincipal()
        janela.show()
        sys.exit(app.exec())
    else:
        # Se a inicialização falhar, exibe uma mensagem no console (já exibida pela função)
        # e encerra o programa sem abrir a janela.
        QMessageBox.critical(None, "Falha na Inicialização", 
                             "Não foi possível configurar o banco de dados. "
                             "Verifique as credenciais em 'database.py' e se o servidor MySQL está em execução. "
                             "O programa será encerrado.")
        sys.exit(1) # Encerra com um código de erro