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

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categoria (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome TEXT NOT NULL UNIQUE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome TEXT NOT NULL,
                Preco REAL NOT NULL,
                IDCategoria INTEGER,
                Stock INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (IDCategoria) REFERENCES categoria(ID)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Preco REAL NOT NULL,
                IDCliente INTEGER,
                IDProduto INTEGER,
                Qt INTEGER NOT NULL,
                DataHora TEXT NOT NULL DEFAULT (datetime('now','localtime')),
                FOREIGN KEY (IDCliente) REFERENCES clientes(ID),
                FOREIGN KEY (IDProduto) REFERENCES produtos(ID)
            )
        """)

        try:
            cursor.execute("ALTER TABLE produtos ADD COLUMN Stock INTEGER NOT NULL DEFAULT 0")
        except sqlite3.OperationalError:
            pass
        try:
            cursor.execute("ALTER TABLE vendas ADD COLUMN DataHora TEXT NOT NULL DEFAULT (datetime('now','localtime'))")
        except sqlite3.OperationalError:
            pass

        self.conn.commit()

    def inserir_dados_iniciais(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM categoria")
        if cursor.fetchone()[0] > 0:
            return

        categorias = ["Limpeza", "Alimentação", "Electronicos", "Bebidas", "Higiene Pessoal", "Lacticinios", "Cereais e Graos"]
        for cat in categorias:
            cursor.execute("INSERT OR IGNORE INTO categoria (Nome) VALUES (?)", (cat,))

        clientes = ["Carlos Teixeira", "Ana Rodrigues", "Manuel da Silva", "Fatima Neto", "Paulo Goncalves"]
        for cli in clientes:
            cursor.execute("INSERT OR IGNORE INTO clientes (Nome) VALUES (?)", (cli,))

        produtos = [
            ("Detergente Ariel 3kg",        2500.00, 1, 40),
            ("Lixivia Brimax 2L",            800.00,  1, 60),
            ("Desinfetante Dettol 1L",       1200.00, 1, 35),
            ("Esponja Scotch-Brite pack 3",  450.00,  1, 80),
            ("Sabão em Po Omo 2kg",          1800.00, 1, 45),
            ("Arroz Angoriano 5kg",          1500.00, 2, 100),
            ("Feijao Frade 1kg",             600.00,  2, 90),
            ("Oléo de Palma 5L",             2200.00, 2, 50),
            ("Massa Esparguete 500g",        350.00,  2, 120),
            ("Farinha de Trigo 1kg",         400.00,  2, 80),
            ("Açucar Refinado 1kg",          500.00,  2, 100),
            ("Sal Grosso 1kg",               200.00,  2, 150),
            ("Tomate em Lata 400g",          350.00,  2, 70),
            ("Sardinha em Lata Tricana",     450.00,  2, 60),
            ("Frango Inteiro 1.5kg",         3500.00, 2, 30),
            ("Televisão Samsung 43pol",   250000.00, 3, 5),
            ("Frigorifico Hisense 150L",  180000.00, 3, 4),
            ("Ventoinha de Mesa",          8500.00,  3, 20),
            ("Ferro de Engomar Philips",   12000.00, 3, 15),
            ("Carregador USB Tipo-C",       2500.00, 3, 40),
            ("Água Caxito 6x1.5L",          900.00,  4, 80),
            ("Sumo Sumol Laranja 330ml",    400.00,  4, 100),
            ("Coca-Cola 2L",                900.00,  4, 60),
            ("Cerveja Cuca 6x330ml",       2200.00,  4, 50),
            ("Leite Mimosa 1L",             850.00,  4, 70),
            ("Sabonete Palmolive pack 3",   600.00,  5, 90),
            ("Shampoo Head Shoulders 400ml",1800.00, 5, 40),
            ("Pasta Dentifria Colgate 75ml", 700.00, 5, 60),
            ("Desodorizante Rexona 150ml",  1200.00, 5, 45),
            ("Papel Higienico Renova 12un", 1500.00, 5, 55),
            ("Queijo Fresco 250g",          1200.00, 6, 30),
            ("Iogurte Natural Mimosa 4un",   950.00, 6, 40),
            ("Manteiga Planta 250g",        1100.00, 6, 35),
            ("Fuba de Milho 2kg",            700.00, 7, 80),
            ("Aveia Quaker 500g",           1300.00, 7, 45),
            ("Lentilhas 500g",               550.00, 7, 60),
        ]
        for prod in produtos:
            cursor.execute(
                "INSERT OR IGNORE INTO produtos (Nome, Preco, IDCategoria, Stock) VALUES (?, ?, ?, ?)",
                prod,
            )

        self.conn.commit()

    def fechar(self):
        if self.conn:
            self.conn.close()
