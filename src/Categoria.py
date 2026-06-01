import sqlite3

class Categoria:
    def __init__(self, ID=None, Nome=None, Descricao=None):
        self.ID = ID
        self.Nome = Nome
        self.Descricao = Descricao

    def cadastrar(self, conn):
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO categoria_carros (Nome, Descricao) VALUES (?, ?)", (self.Nome, self.Descricao))
            conn.commit()
            return True
        except sqlite3.Error:
            return False

    def atualizar(self, conn):
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE categoria_carros SET Nome = ?, Descricao = ? WHERE ID = ?", (self.Nome, self.Descricao, self.ID))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    def apagar(self, conn):
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM carros WHERE IDCategoria = ?", (self.ID,))
            if cursor.fetchone()[0] > 0:
                return False
            cursor.execute("DELETE FROM categoria_carros WHERE ID = ?", (self.ID,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    @staticmethod
    def listar_todos(conn):
        cursor = conn.cursor()
        cursor.execute("SELECT ID, Nome, Descricao FROM categoria_carros ORDER BY Nome")
        return cursor.fetchall()
