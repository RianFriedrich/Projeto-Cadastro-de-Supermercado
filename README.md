# Projeto Cadastro de Supermercado

Aplicação PySide6 + MySQL para gerenciar produtos de supermercado (CRUD) e categorias.

Pré-requisitos
- Python 3.8+
- MySQL server

# Projeto: Cadastro de Supermercado

Aplicação desktop em Python (PySide6) com MySQL para gerenciar um catálogo de produtos de supermercado.

Visão geral
- Interface gráfica para criar, ler, atualizar e excluir produtos (CRUD).
- Suporte a categorias persistentes (tabela `categorias`) com gerenciador para listar, renomear e excluir.
- O script de inicialização cria o banco, usuário de aplicação e tabelas necessárias na primeira execução.

Funcionalidades principais
- Cadastrar produtos com: nome, código de barras (único), preço, estoque e categoria.
- Editar e excluir produtos a partir da tabela.
- Criar, remover e renomear categorias; remoção verifica e trata produtos que usam a categoria.
- Categorias padrão pré-carregadas: Mercearia, Hortifruti, Açougue, Padaria, Bebidas, Limpeza, Higiene, Frios, Congelados, Doces, Conveniência, Pet Shop, Infantil.

Requisitos
- Python 3.8 ou superior
- MySQL Server (local ou remoto)
- (recomendado) ambiente virtual para Python

Dependências
- As dependências estão no arquivo `requirements.txt`. As principais são:
	- `PySide6` (GUI)
	- `mysql-connector-python` (conexão com MySQL)

Instalação e execução (Windows / PowerShell)
1. Abra PowerShell e vá para a pasta do projeto:

```powershell
cd C:\Users\user\Desktop\Projeto-Cadastro-de-Supermercado-main\projeto
```

2. (Opcional, recomendado) criar e ativar um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instalar dependências:

```powershell
pip install -r requirements.txt
```

4. Ajustar credenciais (se necessário):
- As configurações de conexão ficam em `database.py`. Você pode configurar via variáveis de ambiente:
	- `DB_SERVER_USER` (padrão: `root`)
	- `DB_SERVER_PASSWORD` (padrão: `senha`)
	- `DB_HOST` (padrão: `localhost`)
	- `DB_NAME` (padrão: `supermercado_db`)
	- `DB_APP_USER` (padrão: `app_user`)
	- `DB_APP_PASSWORD` (padrão: `sua_senha_aqui`)

5. Executar o aplicativo:

```powershell
python .\app_supermercado_mysql.py
```

Observações sobre a inicialização do banco
- Ao iniciar, `database.py` tenta conectar com o usuário do servidor (por padrão `root`) para criar o banco e o usuário de aplicação. Se preferir criar manualmente, execute `setup.sql` no seu servidor MySQL.
- Se o banco estiver vazio, o aplicativo tentará criar e inserir as categorias padrão automaticamente.

Como usar a aplicação
- Preencha os campos do formulário de produto e clique em `Cadastrar Produto`.
- Selecione uma linha da tabela para carregar os dados no formulário e usar `Atualizar Produto` ou `Excluir Produto`.
- Para categorias: use o campo `Nova Categoria` + `Adicionar Categoria`. Para remover, use `Remover Categoria` (há confirmação se houver produtos usando a categoria).
- Abra `Gerenciar Categorias` para renomear ou excluir categorias em lote.

Resolução de problemas comuns
- Erro de conexão com MySQL: verifique se o servidor está rodando e as credenciais em `database.py` ou nas variáveis de ambiente.
- ImportError relacionado a `PySide6`: instale as dependências no ambiente ativo (`pip install -r requirements.txt`).
- Permissões ao criar usuário DB: use um usuário MySQL com permissões suficientes (ex.: `root`) ou crie manualmente as permissões com `setup.sql`.

Executando o script SQL manualmente (opcional)
- Para aplicar `setup.sql` manualmente no MySQL CLI:

```sql
SOURCE C:/Users/user/Desktop/Projeto-Cadastro-de-Supermercado-main/projeto/setup.sql;
```
