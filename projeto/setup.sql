-- 1. Cria o banco de dados se ele ainda não existir.
-- Usamos um nome diferente para não confundir com o arquivo do SQLite.
CREATE DATABASE IF NOT EXISTS supermercado_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 2. Cria um usuário específico para a aplicação se ele não existir.
-- Troque 'sua_senha_aqui' por uma senha forte e segura.
CREATE USER IF NOT EXISTS 'app_user'@'localhost' IDENTIFIED BY 'sua_senha_aqui';

-- 3. Concede ao novo usuário todas as permissões no banco de dados 'supermercado_db'.
GRANT ALL PRIVILEGES ON supermercado_db.* TO 'app_user'@'localhost';

-- 4. Atualiza os privilégios para que as mudanças tenham efeito.
FLUSH PRIVILEGES;

-- 5. Usa o banco de dados recém-criado para os próximos comandos.
USE supermercado_db;

-- 6. Cria a tabela de produtos com tipos de dados otimizados para MySQL.
CREATE TABLE IF NOT EXISTS produtos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    codigo_barras VARCHAR(100) UNIQUE NOT NULL,
    -- Usar DECIMAL para valores monetários é a melhor prática para evitar erros de arredondamento.
    preco DECIMAL(10, 2) NOT NULL,
    estoque INT NOT NULL,
    categoria VARCHAR(100)
);

-- Mensagem opcional para o usuário que executa o script
-- SELECT 'Banco de dados e tabela criados com sucesso!' AS status;