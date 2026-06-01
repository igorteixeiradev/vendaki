import sqlite3

class Database:
    def __init__(self):
        self.conn = None

    def conectar(self):
        try:
            self.conn = sqlite3.connect("./db/HinginoRafael.db")
            return self.conn
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None

    def criar_tabelas(self):
        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS utilizadores (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Usuario TEXT NOT NULL UNIQUE,
                Senha TEXT NOT NULL,
                NomeCompleto TEXT,
                Cargo TEXT DEFAULT 'Vendedor'
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categoria_carros (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome TEXT NOT NULL UNIQUE,
                Descricao TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS carros (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Marca TEXT NOT NULL,
                Modelo TEXT NOT NULL,
                Ano INTEGER NOT NULL,
                Cor TEXT,
                Combustivel TEXT,
                Transmissao TEXT,
                Quilometragem INTEGER DEFAULT 0,
                NumChassi TEXT UNIQUE,
                NumMotor TEXT,
                PrecoVenda REAL NOT NULL,
                IDCategoria INTEGER,
                Estado TEXT DEFAULT 'Disponivel',
                DataEntrada TEXT DEFAULT (date('now','localtime')),
                Observacoes TEXT,
                FOREIGN KEY (IDCategoria) REFERENCES categoria_carros(ID)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome TEXT NOT NULL,
                Telefone TEXT,
                Email TEXT,
                Endereco TEXT,
                BI TEXT UNIQUE,
                DataCadastro TEXT DEFAULT (date('now','localtime'))
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                IDCarro INTEGER NOT NULL,
                IDCliente INTEGER NOT NULL,
                PrecoVenda REAL NOT NULL,
                Desconto REAL DEFAULT 0,
                PrecoFinal REAL NOT NULL,
                FormaPagamento TEXT DEFAULT 'Dinheiro',
                DataVenda TEXT DEFAULT (datetime('now','localtime')),
                IDVendedor INTEGER,
                Observacoes TEXT,
                FOREIGN KEY (IDCarro) REFERENCES carros(ID),
                FOREIGN KEY (IDCliente) REFERENCES clientes(ID),
                FOREIGN KEY (IDVendedor) REFERENCES utilizadores(ID)
            )
        """)

        self.conn.commit()

    def inserir_dados_iniciais(self):
        cursor = self.conn.cursor()

        # Utilizador admin padrão
        cursor.execute("SELECT COUNT(*) FROM utilizadores")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO utilizadores (Usuario, Senha, NomeCompleto, Cargo) VALUES (?, ?, ?, ?)",
                ("admin", "admin123", "Administrador", "Administrador")
            )
            cursor.execute(
                "INSERT INTO utilizadores (Usuario, Senha, NomeCompleto, Cargo) VALUES (?, ?, ?, ?)",
                ("vendedor", "venda123", "João Vendedor", "Vendedor")
            )

        # Categorias de carros
        cursor.execute("SELECT COUNT(*) FROM categoria_carros")
        if cursor.fetchone()[0] == 0:
            categorias = [
                ("Sedan", "Carros de 4 portas com porta-malas separado"),
                ("SUV", "Sport Utility Vehicle - veículos utilitários"),
                ("Pickup", "Camionetes de carga e uso misto"),
                ("Hatchback", "Carros compactos com porta traseira integrada"),
                ("Minivan", "Veículos de grande capacidade para famílias"),
                ("Coupe", "Carros esportivos de 2 portas"),
                ("Cabrio", "Carros descapotáveis"),
                ("Furgão / Comercial", "Veículos para uso comercial e de carga"),
            ]
            for nome, desc in categorias:
                cursor.execute("INSERT OR IGNORE INTO categoria_carros (Nome, Descricao) VALUES (?, ?)", (nome, desc))

        # Clientes iniciais
        cursor.execute("SELECT COUNT(*) FROM clientes")
        if cursor.fetchone()[0] == 0:
            clientes = [
                ("Carlos Mbemba", "923 456 789", "carlos@gmail.com", "Rua do Carmo, 45, Luanda", "004523789LA"),
                ("Ana Loureiro", "912 345 678", "ana.loureiro@hotmail.com", "Av. Lenin, 102, Luanda", "005123456LA"),
                ("Manuel Simões", "935 678 901", "", "Bairro Rangel, Luanda", "006789012LA"),
                ("Fátima Neto", "924 567 890", "fatima.neto@gmail.com", "Luanda Sul, Talatona", "007890123LA"),
                ("Paulo Gonçalves", "945 012 345", "", "Município de Viana", "008901234LA"),
            ]
            for c in clientes:
                cursor.execute(
                    "INSERT OR IGNORE INTO clientes (Nome, Telefone, Email, Endereco, BI) VALUES (?,?,?,?,?)", c
                )

        # Carros iniciais
        cursor.execute("SELECT COUNT(*) FROM carros")
        if cursor.fetchone()[0] == 0:
            carros = [
                ("Toyota", "Corolla", 2020, "Branco", "Gasolina", "Automático", 45000, "CH100001", "MT10001", 12500000.0, 1, "Disponivel", ""),
                ("Toyota", "Hilux", 2021, "Preto", "Diesel", "Manual", 32000, "CH100002", "MT10002", 18000000.0, 3, "Disponivel", ""),
                ("Honda", "Civic", 2019, "Cinzento", "Gasolina", "Automático", 67000, "CH100003", "MT10003", 10800000.0, 1, "Disponivel", ""),
                ("Mitsubishi", "Outlander", 2022, "Azul", "Gasolina", "Automático", 18000, "CH100004", "MT10004", 22000000.0, 2, "Disponivel", ""),
                ("Ford", "Ranger", 2021, "Vermelho", "Diesel", "Manual", 28000, "CH100005", "MT10005", 19500000.0, 3, "Disponivel", ""),
                ("Volkswagen", "Golf", 2018, "Branco", "Gasolina", "Manual", 80000, "CH100006", "MT10006", 9200000.0, 4, "Disponivel", ""),
                ("Hyundai", "Tucson", 2023, "Prata", "Gasolina", "Automático", 5000, "CH100007", "MT10007", 25000000.0, 2, "Disponivel", ""),
                ("Nissan", "Frontier", 2020, "Preto", "Diesel", "Automático", 52000, "CH100008", "MT10008", 17000000.0, 3, "Disponivel", ""),
                ("BMW", "Série 3", 2019, "Preto", "Gasolina", "Automático", 61000, "CH100009", "MT10009", 28000000.0, 6, "Disponivel", ""),
                ("Mercedes-Benz", "C200", 2021, "Branco", "Gasolina", "Automático", 22000, "CH100010", "MT10010", 35000000.0, 1, "Disponivel", ""),
            ]
            for c in carros:
                cursor.execute(
                    "INSERT OR IGNORE INTO carros (Marca, Modelo, Ano, Cor, Combustivel, Transmissao, Quilometragem, NumChassi, NumMotor, PrecoVenda, IDCategoria, Estado, Observacoes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", c
                )

        self.conn.commit()

    def fechar(self):
        if self.conn:
            self.conn.close()
