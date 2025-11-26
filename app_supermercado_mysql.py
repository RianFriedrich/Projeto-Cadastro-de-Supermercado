import sys
import mysql.connector
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QComboBox,
    QHBoxLayout,
    QDialog,
    QListWidget,
    QInputDialog,
)
from PySide6.QtCore import Qt

from database import inicializar_banco_de_dados, get_db_connection


class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(
            "Sistema de Cadastro de Produtos - Supermercado (MySQL)")
        self.setGeometry(100, 100, 900, 600)

        self.editing_id = None

        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)

        self.layout_principal = QVBoxLayout(self.widget_central)
        self.layout_formulario = QGridLayout()

        self.aplicar_estilo()
        self.criar_formulario()
        self.criar_tabela()

        self.layout_principal.addLayout(self.layout_formulario)
        self.layout_principal.addWidget(self.tabela_produtos)

        try:
            self.carregar_categorias()
        except Exception:
            pass
        self.carregar_produtos()

    def aplicar_estilo(self):
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
        
        self.botao_cadastrar = QPushButton("Cadastrar Produto")
        self.botao_cadastrar.clicked.connect(self.cadastrar_produto)

        
        self.label_nova_categoria = QLabel("Nova Categoria:")
        self.input_nova_categoria = QLineEdit()
        self.botao_adicionar_categoria = QPushButton("Adicionar Categoria")
        self.botao_adicionar_categoria.clicked.connect(self.adicionar_categoria)
        self.botao_remover_categoria = QPushButton("Remover Categoria")
        self.botao_remover_categoria.clicked.connect(self.remover_categoria)

        
        self.botao_atualizar = QPushButton("Atualizar Produto")
        self.botao_excluir = QPushButton("Excluir Produto")
        self.botao_cancelar = QPushButton("Cancelar")
        self.botao_atualizar.clicked.connect(self.atualizar_produto)
        self.botao_excluir.clicked.connect(self.excluir_produto)
        self.botao_cancelar.clicked.connect(self.cancelar_edicao)

        self.botao_atualizar.setVisible(False)
        self.botao_excluir.setVisible(False)
        self.botao_cancelar.setVisible(False)

        self.layout_formulario.addWidget(self.label_nome, 0, 0)
        self.layout_formulario.addWidget(self.input_nome, 1, 0)
        self.layout_formulario.addWidget(self.label_codigo, 0, 1)
        self.layout_formulario.addWidget(self.input_codigo, 1, 1)
        self.layout_formulario.addWidget(self.label_preco, 2, 0)
        self.layout_formulario.addWidget(self.input_preco, 3, 0)
        self.layout_formulario.addWidget(self.label_estoque, 2, 1)
        self.layout_formulario.addWidget(self.input_estoque, 3, 1)
        self.layout_formulario.addWidget(self.label_categoria, 4, 0)
        self.layout_formulario.addWidget(self.input_categoria, 5, 0)

        
        self.layout_formulario.addWidget(self.label_nova_categoria, 6, 0)
        self.layout_formulario.addWidget(self.input_nova_categoria, 7, 0)
        botoes_cat_container = QWidget()
        botoes_cat_layout = QHBoxLayout(botoes_cat_container)
        botoes_cat_layout.setContentsMargins(0, 0, 0, 0)
        botoes_cat_layout.addWidget(self.botao_adicionar_categoria)
        botoes_cat_layout.addWidget(self.botao_remover_categoria)
        
        self.botao_gerenciar_categorias = QPushButton("Gerenciar Categorias")
        self.botao_gerenciar_categorias.clicked.connect(self.abrir_gerenciador_categorias)
        botoes_cat_layout.addWidget(self.botao_gerenciar_categorias)
        self.layout_formulario.addWidget(botoes_cat_container, 7, 1)

        
        botoes_container = QWidget()
        botoes_layout = QHBoxLayout(botoes_container)
        botoes_layout.setContentsMargins(0, 0, 0, 0)
        botoes_layout.addWidget(self.botao_cadastrar)
        botoes_layout.addWidget(self.botao_atualizar)
        botoes_layout.addWidget(self.botao_excluir)
        botoes_layout.addWidget(self.botao_cancelar)
        self.layout_formulario.addWidget(
            botoes_container, 5, 1, 1, 1, Qt.AlignmentFlag.AlignRight
        )

    def criar_tabela(self):
        self.tabela_produtos = QTableWidget()
        self.tabela_produtos.setColumnCount(6)
        self.tabela_produtos.setHorizontalHeaderLabels(
            ["ID", "Nome", "Cód. Barras", "Preço (R$)", "Estoque", "Categoria"])
        header = self.tabela_produtos.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.tabela_produtos.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers)
        self.tabela_produtos.cellClicked.connect(self.selecionar_produto)

    def cadastrar_produto(self):
        nome = self.input_nome.text()
        codigo = self.input_codigo.text()
        preco_texto = self.input_preco.text().replace(',', '.')
        estoque_texto = self.input_estoque.text()
        categoria = self.input_categoria.currentText()
        if not all([nome, codigo, preco_texto, estoque_texto]):
            QMessageBox.warning(
                self, "Atenção", "Todos os campos devem ser preenchidos!")
            return
        try:
            preco = float(preco_texto)
            estoque = int(estoque_texto)
        except ValueError:
            QMessageBox.warning(self, "Erro de Formato",
                                "Preço e Estoque devem ser números válidos!")
            return
        conexao = None
        try:
            conexao = get_db_connection()
            if conexao is None:
                QMessageBox.critical(
                    self, "Erro de Conexão", "Não foi possível conectar ao banco de dados para cadastrar.")
                return
            cursor = conexao.cursor()
            query = (
                "INSERT INTO produtos (nome, codigo_barras, preco, estoque, categoria)"
                " VALUES (%s, %s, %s, %s, %s)"
            )
            valores = (nome, codigo, preco, estoque, categoria)
            cursor.execute(query, valores)
            conexao.commit()

            QMessageBox.information(
                self, "Sucesso", "Produto cadastrado com sucesso!")
            self.limpar_campos()
            self.carregar_produtos()

        except mysql.connector.IntegrityError:
            QMessageBox.warning(
                self, "Erro", f"O código de barras '{codigo}' já existe no banco de dados!")
        except Exception as e:
            QMessageBox.critical(self, "Erro Crítico",
                                 f"Ocorreu um erro inesperado: {e}")
        finally:
            try:
                if cursor is not None:
                    cursor.close()
            except Exception:
                pass
            if conexao and hasattr(conexao, "is_connected") and conexao.is_connected():
                conexao.close()

    def carregar_categorias(self):
        """Carrega as categorias da tabela `categorias` e popula o QComboBox."""
        conexao = None
        try:
            conexao = get_db_connection()
            if conexao is None:
                    QMessageBox.warning(self, "Aviso", "Não foi possível conectar ao banco para carregar categorias. Usando categorias padrão locais.")
                    fallback = [
                        'Mercearia', 'Hortifruti', 'Açougue', 'Padaria',
                        'Bebidas', 'Limpeza', 'Higiene', 'Frios', 'Congelados',
                        'Doces', 'Conveniência', 'Pet Shop', 'Infantil'
                    ]
                    self.input_categoria.clear()
                    self.input_categoria.addItems(fallback)
                    return
            cursor = conexao.cursor()
            cursor.execute("SELECT nome FROM categorias ORDER BY nome")
            linhas = cursor.fetchall()
            nomes = [r[0] for r in linhas]
            
            if not nomes:
                nomes = [
                    'Mercearia', 'Hortifruti', 'Açougue', 'Padaria',
                    'Bebidas', 'Limpeza', 'Higiene', 'Frios', 'Congelados',
                    'Doces', 'Conveniência', 'Pet Shop', 'Infantil'
                ]
                try:
                    for cat in nomes:
                        cursor.execute("INSERT IGNORE INTO categorias (nome) VALUES (%s)", (cat,))
                    conexao.commit()
                except Exception:
                    pass

            self.input_categoria.clear()
            self.input_categoria.addItems(nomes)
        except Exception:
            pass
        finally:
            try:
                if cursor is not None:
                    cursor.close()
            except Exception:
                pass
            if conexao and hasattr(conexao, "is_connected") and conexao.is_connected():
                conexao.close()

    def carregar_produtos(self):
        conexao = None
        try:
            conexao = get_db_connection()
            if conexao is None:
                QMessageBox.critical(
                    self, "Erro de Conexão", "Não foi possível conectar ao banco para carregar os produtos.")
                return
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT id, nome, codigo_barras, preco, estoque, categoria FROM produtos ORDER BY nome"
            )
            produtos = cursor.fetchall()

            self.tabela_produtos.setRowCount(len(produtos))
            for linha, produto in enumerate(produtos):
                for coluna, valor in enumerate(produto):
                    if coluna == 3:
                        valor_item = QTableWidgetItem(f"{valor:.2f}")
                    else:
                        valor_item = QTableWidgetItem(str(valor))
                    self.tabela_produtos.setItem(linha, coluna, valor_item)

        except Exception as e:
            QMessageBox.critical(self, "Erro ao Carregar",
                                 f"Não foi possível carregar os produtos: {e}")
        finally:
            try:
                if cursor is not None:
                    cursor.close()
            except Exception:
                pass
            if conexao and hasattr(conexao, "is_connected") and conexao.is_connected():
                conexao.close()

    def selecionar_produto(self, row, column):
        try:
            id_item = self.tabela_produtos.item(row, 0)
            if id_item is None:
                return
            produto_id = int(id_item.text())
            nome_item = self.tabela_produtos.item(row, 1)
            codigo_item = self.tabela_produtos.item(row, 2)
            preco_item = self.tabela_produtos.item(row, 3)
            estoque_item = self.tabela_produtos.item(row, 4)
            categoria_item = self.tabela_produtos.item(row, 5)

            self.input_nome.setText(nome_item.text() if nome_item else "")
            self.input_codigo.setText(codigo_item.text() if codigo_item else "")
            self.input_preco.setText(preco_item.text() if preco_item else "")
            self.input_estoque.setText(estoque_item.text() if estoque_item else "")
            if categoria_item:
                idx = self.input_categoria.findText(categoria_item.text())
                if idx >= 0:
                    self.input_categoria.setCurrentIndex(idx)

            self.editing_id = produto_id
            self.botao_cadastrar.setVisible(False)
            self.botao_atualizar.setVisible(True)
            self.botao_excluir.setVisible(True)
            self.botao_cancelar.setVisible(True)
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Falha ao selecionar produto: {e}")

    def atualizar_produto(self):
        if self.editing_id is None:
            QMessageBox.warning(self, "Atenção", "Nenhum produto selecionado para atualizar.")
            return
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
            QMessageBox.warning(self, "Erro de Formato",
                                "Preço e Estoque devem ser números válidos!")
            return
        conexao = None
        try:
            conexao = get_db_connection()
            if conexao is None:
                QMessageBox.critical(self, "Erro de Conexão", "Não foi possível conectar ao banco para atualizar.")
                return
            cursor = conexao.cursor()
            query = (
                "UPDATE produtos SET nome=%s, codigo_barras=%s, preco=%s, estoque=%s, categoria=%s WHERE id=%s"
            )
            valores = (nome, codigo, preco, estoque, categoria, self.editing_id)
            cursor.execute(query, valores)
            conexao.commit()
            QMessageBox.information(self, "Sucesso", "Produto atualizado com sucesso!")
            self.limpar_campos()
            self.carregar_produtos()
        except mysql.connector.IntegrityError:
            QMessageBox.warning(self, "Erro", f"O código de barras '{codigo}' já existe no banco de dados!")
        except Exception as e:
            QMessageBox.critical(self, "Erro Crítico",
                                 f"Ocorreu um erro inesperado ao atualizar: {e}")
        finally:
            try:
                if cursor is not None:
                    cursor.close()
            except Exception:
                pass
            if conexao and hasattr(conexao, "is_connected") and conexao.is_connected():
                conexao.close()

    def excluir_produto(self):
        if self.editing_id is None:
            QMessageBox.warning(self, "Atenção", "Nenhum produto selecionado para exclusão.")
            return
        resp = QMessageBox.question(self, "Confirmar Exclusão",
                                    "Deseja realmente excluir o produto selecionado?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if resp != QMessageBox.StandardButton.Yes:
            return
        conexao = None
        try:
            conexao = get_db_connection()
            if conexao is None:
                QMessageBox.critical(self, "Erro de Conexão", "Não foi possível conectar ao banco para excluir.")
                return
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM produtos WHERE id=%s", (self.editing_id,))
            conexao.commit()
            QMessageBox.information(self, "Sucesso", "Produto excluído com sucesso.")
            self.limpar_campos()
            self.carregar_produtos()
        except Exception as e:
            QMessageBox.critical(self, "Erro ao Excluir", f"Não foi possível excluir o produto: {e}")
        finally:
            try:
                if cursor is not None:
                    cursor.close()
            except Exception:
                pass
            if conexao and hasattr(conexao, "is_connected") and conexao.is_connected():
                conexao.close()

    def cancelar_edicao(self):
        self.limpar_campos()

    def limpar_campos(self):
        self.input_nome.clear()
        self.input_codigo.clear()
        self.input_preco.clear()
        self.input_estoque.clear()
        self.input_nova_categoria.clear()
        
        self.editing_id = None
        self.botao_cadastrar.setVisible(True)
        self.botao_atualizar.setVisible(False)
        self.botao_excluir.setVisible(False)
        self.botao_cancelar.setVisible(False)

    def adicionar_categoria(self):
        nova = self.input_nova_categoria.text().strip()
        if not nova:
            QMessageBox.warning(self, "Atenção", "Digite o nome da categoria para adicionar.")
            return
        conexao = None
        try:
            conexao = get_db_connection()
            if conexao is None:
                QMessageBox.critical(self, "Erro de Conexão", "Não foi possível conectar ao banco para adicionar categoria.")
                return
            cursor = conexao.cursor()
            cursor.execute("INSERT IGNORE INTO categorias (nome) VALUES (%s)", (nova,))
            conexao.commit()
            QMessageBox.information(self, "Sucesso", f"Categoria '{nova}' adicionada.")
            self.carregar_categorias()
            idx = self.input_categoria.findText(nova)
            if idx >= 0:
                self.input_categoria.setCurrentIndex(idx)
            self.input_nova_categoria.clear()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível adicionar a categoria: {e}")
        finally:
            try:
                if cursor is not None:
                    cursor.close()
            except Exception:
                pass
            if conexao and hasattr(conexao, "is_connected") and conexao.is_connected():
                conexao.close()

    def remover_categoria(self):
        nome = self.input_nova_categoria.text().strip()
        if not nome:
            # If no name in input, try current selection
            nome = self.input_categoria.currentText()
        if not nome:
            QMessageBox.warning(self, "Atenção", "Selecione ou digite o nome da categoria para remover.")
            return

        # Check if any products use this category
        conexao = None
        try:
            conexao = get_db_connection()
            if conexao is None:
                QMessageBox.critical(self, "Erro de Conexão", "Não foi possível conectar ao banco para remover categoria.")
                return
            cursor = conexao.cursor()
            cursor.execute("SELECT COUNT(*) FROM produtos WHERE categoria=%s", (nome,))
            count = cursor.fetchone()[0]
            if count > 0:
                resp = QMessageBox.question(
                    self,
                    "Categoria em Uso",
                    f"Existem {count} produto(s) com a categoria '{nome}'.\nDeseja remover a categoria e definir a categoria desses produtos como NULL?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                )
                if resp != QMessageBox.StandardButton.Yes:
                    return
                # Set products' category to NULL
                cursor.execute("UPDATE produtos SET categoria=NULL WHERE categoria=%s", (nome,))

            # Delete category
            cursor.execute("DELETE FROM categorias WHERE nome=%s", (nome,))
            conexao.commit()
            QMessageBox.information(self, "Sucesso", f"Categoria '{nome}' removida.")
            self.input_nova_categoria.clear()
            self.carregar_categorias()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível remover a categoria: {e}")
        finally:
            try:
                if cursor is not None:
                    cursor.close()
            except Exception:
                pass
            if conexao and hasattr(conexao, "is_connected") and conexao.is_connected():
                conexao.close()

    def abrir_gerenciador_categorias(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Gerenciar Categorias")
        dlg.setModal(True)
        layout = QVBoxLayout(dlg)

        list_widget = QListWidget()

        # carregar categorias
        conexao = None
        try:
            conexao = get_db_connection()
            if conexao is not None:
                cursor = conexao.cursor()
                cursor.execute("SELECT nome FROM categorias ORDER BY nome")
                for (nome,) in cursor.fetchall():
                    list_widget.addItem(nome)
                try:
                    cursor.close()
                except Exception:
                    pass
        except Exception:
            pass
        finally:
            if conexao and hasattr(conexao, "is_connected") and conexao.is_connected():
                conexao.close()

        layout.addWidget(list_widget)

        btns = QWidget()
        btns_layout = QHBoxLayout(btns)
        btns_layout.setContentsMargins(0, 0, 0, 0)
        btn_renomear = QPushButton("Renomear")
        btn_excluir = QPushButton("Excluir")
        btn_fechar = QPushButton("Fechar")
        btns_layout.addWidget(btn_renomear)
        btns_layout.addWidget(btn_excluir)
        btns_layout.addWidget(btn_fechar)
        layout.addWidget(btns)

        def refresh_list():
            list_widget.clear()
            conex = get_db_connection()
            if conex is None:
                return
            try:
                cur = conex.cursor()
                cur.execute("SELECT nome FROM categorias ORDER BY nome")
                for (n,) in cur.fetchall():
                    list_widget.addItem(n)
            finally:
                try:
                    cur.close()
                except Exception:
                    pass
                if conex and hasattr(conex, "is_connected") and conex.is_connected():
                    conex.close()

        def renomear():
            item = list_widget.currentItem()
            if item is None:
                QMessageBox.warning(dlg, "Atenção", "Selecione uma categoria para renomear.")
                return
            antigo = item.text()
            novo, ok = QInputDialog.getText(dlg, "Renomear Categoria", "Novo nome:", text=antigo)
            if not ok:
                return
            novo = novo.strip()
            if not novo:
                QMessageBox.warning(dlg, "Atenção", "Nome inválido.")
                return
            conex = None
            try:
                conex = get_db_connection()
                if conex is None:
                    QMessageBox.critical(dlg, "Erro", "Não foi possível conectar ao banco para renomear.")
                    return
                cur = conex.cursor()
                try:
                    cur.execute("UPDATE categorias SET nome=%s WHERE nome=%s", (novo, antigo))
                    conex.commit()
                except mysql.connector.IntegrityError:
                    QMessageBox.warning(dlg, "Erro", f"Já existe uma categoria com o nome '{novo}'.")
                    return
            except Exception as e:
                QMessageBox.critical(dlg, "Erro", f"Falha ao renomear: {e}")
            finally:
                try:
                    cur.close()
                except Exception:
                    pass
                if conex and hasattr(conex, "is_connected") and conex.is_connected():
                    conex.close()
            refresh_list()
            self.carregar_categorias()

        def excluir():
            item = list_widget.currentItem()
            if item is None:
                QMessageBox.warning(dlg, "Atenção", "Selecione uma categoria para excluir.")
                return
            nome = item.text()
            conex = None
            try:
                conex = get_db_connection()
                if conex is None:
                    QMessageBox.critical(dlg, "Erro", "Não foi possível conectar ao banco para excluir.")
                    return
                cur = conex.cursor()
                cur.execute("SELECT COUNT(*) FROM produtos WHERE categoria=%s", (nome,))
                count = cur.fetchone()[0]
                if count > 0:
                    resp = QMessageBox.question(
                        dlg,
                        "Categoria em Uso",
                        f"Existem {count} produto(s) com a categoria '{nome}'.\nDeseja remover a categoria e definir a categoria desses produtos como NULL?",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    )
                    if resp != QMessageBox.StandardButton.Yes:
                        return
                    cur.execute("UPDATE produtos SET categoria=NULL WHERE categoria=%s", (nome,))
                cur.execute("DELETE FROM categorias WHERE nome=%s", (nome,))
                conex.commit()
            except Exception as e:
                QMessageBox.critical(dlg, "Erro", f"Falha ao excluir: {e}")
            finally:
                try:
                    cur.close()
                except Exception:
                    pass
                if conex and hasattr(conex, "is_connected") and conex.is_connected():
                    conex.close()
            refresh_list()
            self.carregar_categorias()

        btn_renomear.clicked.connect(renomear)
        btn_excluir.clicked.connect(excluir)
        btn_fechar.clicked.connect(dlg.close)

        dlg.exec()


if __name__ == "__main__":
    if inicializar_banco_de_dados():
        app = QApplication(sys.argv)
        janela = JanelaPrincipal()
        janela.show()
        sys.exit(app.exec())
    else:
        QMessageBox.critical(
            None,
            "Falha na Inicialização",
            (
                "Não foi possível configurar o banco de dados. "
                "Verifique as credenciais em 'database.py' e se o servidor MySQL está em execução. "
                "O programa será encerrado."
            ),
        )
        sys.exit(1)
