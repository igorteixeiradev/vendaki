import sqlite3

class Cliente:
    def __init__(self, ID=None, Nome=None, Telefone=None, Email=None, Endereco=None, BI=None):
        self.ID = ID
        self.Nome = Nome
        self.Telefone = Telefone
        self.Email = Email
        self.Endereco = Endereco
        self.BI = BI

    def cadastrar(self, conn):
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO clientes (Nome, Telefone, Email, Endereco, BI) VALUES (?, ?, ?, ?, ?)",
                (self.Nome, self.Telefone, self.Email, self.Endereco, self.BI)
            )
            conn.commit()
            return True
        except sqlite3.Error:
            return False

    def atualizar(self, conn):
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE clientes SET Nome=?, Telefone=?, Email=?, Endereco=?, BI=? WHERE ID=?",
                (self.Nome, self.Telefone, self.Email, self.Endereco, self.BI, self.ID)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    def apagar(self, conn):
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM vendas WHERE IDCliente = ?", (self.ID,))
            if cursor.fetchone()[0] > 0:
                return False
            cursor.execute("DELETE FROM clientes WHERE ID = ?", (self.ID,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    @staticmethod
    def listar_todos(conn):
        cursor = conn.cursor()
        cursor.execute("SELECT ID, Nome, Telefone, Email, BI FROM clientes ORDER BY Nome")
        return cursor.fetchall()
