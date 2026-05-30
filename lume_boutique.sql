CREATE DATABASE lume_boutique;
USE lume_boutique;

CREATE TABLE usuarios (
id INT AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR(200) NOT NULL,
email VARCHAR(100) UNIQUE NOT NULL,
senha VARCHAR(100) NOT NULL,
tipo ENUM('admin', 'cliente') DEFAULT 'cliente'

);

CREATE TABLE categorias (
id INT AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO categorias(nome) VALUES
('Roupas'),
('Acessórios'),
('Cosméticos'),
('Íntimos'),
('Calçados');

CREATE TABLE produtos (
id INT AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR(100) NOT NULL,
categoria_id INT,
descricao TEXT,
preco DECIMAL(10,2),
estoque INT,
FOREIGN KEY (categoria_id)
REFERENCES categorias(id)
);

CREATE TABLE pedidos (
id INT AUTO_INCREMENT PRIMARY KEY,
usuario_id INT,
total DECIMAL(10,2),
data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
rua VARCHAR (150),
cep CHAR(8),
complemento VARCHAR (100), 
FOREIGN KEY (usuario_id)
REFERENCES usuarios(id)
);

CREATE TABLE itens_pedido (
id INT AUTO_INCREMENT PRIMARY KEY,
pedido_id INT,
produto_id INT,
quantidade INT,
subtotal DECIMAL(10,2),
FOREIGN KEY (pedido_id)
REFERENCES pedidos(id),
FOREIGN KEY (produto_id)
REFERENCES produtos(id)
);


INSERT INTO usuarios(nome, email, senha, tipo) VALUES 
('administrador', 'admin@lume.com', 'admin123', 'admin');
