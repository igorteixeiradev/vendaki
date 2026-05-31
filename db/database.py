import sqlite3


class Database:
    def __init__(self):
        self.conn = None

    def conectar(self):
        try:
            self.conn = sqlite3.connect("./db/VendaProdutos.db")
            return self.conn
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None

    def criar_tabelas(self):
        cursor = self.conn.cursor()

        # Tabela categoria (ID, Nome)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categoria (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome TEXT NOT NULL UNIQUE
            )
        """)

        # Tabela produtos (ID, Nome, Preco, IDCategoria)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome TEXT NOT NULL,
                Preco REAL NOT NULL,
                IDCategoria INTEGER,
                FOREIGN KEY (IDCategoria) REFERENCES categoria(ID)
            )
        """)

        # Tabela clientes (ID, Nome)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome TEXT NOT NULL
            )
        """)

        # Tabela vendas (ID, Preco, IDCliente, IDProduto, Qt)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Preco REAL NOT NULL,
                IDCliente INTEGER,
                IDProduto INTEGER,
                Qt INTEGER NOT NULL,
                FOREIGN KEY (IDCliente) REFERENCES clientes(ID),
                FOREIGN KEY (IDProduto) REFERENCES produtos(ID)
            )
        """)

        self.conn.commit()

    def inserir_dados_iniciais(self):
        cursor = self.conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM categoria")
        if cursor.fetchone()[0] > 0:
            return

        # Inserir categorias padrão
        categorias = ["Eletrônicos", "Roupas", "Alimentos", "Livros", "Esportes"]
        for cat in categorias:
            cursor.execute("INSERT OR IGNORE INTO categoria (Nome) VALUES (?)", (cat,))

        # Inserir clientes padrão
        clientes = ["João Silva", "Maria Santos", "Pedro Oliveira", "Ana Costa"]
        for cli in clientes:
            cursor.execute("INSERT OR IGNORE INTO clientes (Nome) VALUES (?)", (cli,))

        # Inserir produtos padrão
        produtos = [
            ("Smartphone", 1500.00, 1),
            ("Camiseta", 49.90, 2),
            ("Arroz", 25.90, 3),
            ("Livro Python", 89.90, 4),
            ("Bola de Futebol", 59.90, 5),
        ]
        for prod in produtos:
            cursor.execute(
                "INSERT OR IGNORE INTO produtos (Nome, Preco, IDCategoria) VALUES (?, ?, ?)",
                prod,
            )

        self.conn.commit()

    def fechar(self):
        if self.conn:
            self.conn.close()
