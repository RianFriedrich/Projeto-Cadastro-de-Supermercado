CREATE DATABASE IF NOT EXISTS supermercado_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'app_user'@'localhost' IDENTIFIED BY 'sua_senha_aqui';

GRANT ALL PRIVILEGES ON supermercado_db.* TO 'app_user'@'localhost';

FLUSH PRIVILEGES;

USE supermercado_db;

CREATE TABLE IF NOT EXISTS produtos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    codigo_barras VARCHAR(100) UNIQUE NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    estoque INT NOT NULL,
    categoria VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS categorias (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) UNIQUE NOT NULL
);

INSERT IGNORE INTO categorias (nome) VALUES
('Mercearia'),
('Hortifruti'),
('Açougue'),
('Padaria'),
('Bebidas'),
('Limpeza'),
('Higiene'),
('Frios'),
('Congelados'),
('Doces'),
('Conveniência'),
('Pet Shop'),
('Infantil');